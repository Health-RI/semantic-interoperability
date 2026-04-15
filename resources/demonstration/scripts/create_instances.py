#!/usr/bin/env python3
"""Create instance data for the semantic interoperability demo schema.

This version supports three CSV inputs:
- prefix.csv
- input-standard.csv
- input-model.csv
- input-horizontal.csv

Vertical input files
--------------------
``input-standard.csv`` and ``input-model.csv`` must have exactly these columns,
in this order:
- subject_id
- subject_label
- predicate_id
- predicate_modifier
- object_id
- object_label

Only ``hriv:hasExactMeaning`` rows are materialized as vertical mappings.
Other predicates are ignored for transformation purposes, but their subjects are
still registered as known representation concepts so they can be referenced from
``input-horizontal.csv``.

Horizontal input file
---------------------
``input-horizontal.csv`` must have exactly these columns, in this order:
- subject_type
- subject_id
- subject_label
- object_type
- object_id
- object_label

Each row asserts an ``aligns(subject, object)`` relation. This script only
materializes asserted alignments; inferred horizontal relations are handled by
a different script. The script validates that both referenced concepts exist in
the appropriate vertical input file according to the declared type.

Implementation notes
--------------------
- Standard/model concepts are typed as ``demo:RepresentationConcept`` plus their
  respective subtype and linked from a generated artifact instance per CURIE
  prefix.
- Exact meanings are represented only with reified ``demo:Mapping`` instances.
- Asserted horizontal alignments are represented both as direct symmetric
  ``demo:aligns`` triples and as reified ``demo:Alignment`` instances with
  asserted provenance.
- Reified Mapping and Alignment instances use both the generic ``demo:source`` /
  ``demo:target`` predicates and the more specific predicates defined in the
  current schema.
- Conflicting labels for the same representation concept are treated as a data
  error and cause the script to fail.

Why direct hriv:hasExactMeaning triples are NOT created
-------------------------------------------------------
Conceptually, every exact-meaning mapping is of type ``hriv:hasExactMeaning``.
However, in the RDF implementation, each such mapping can also have a polarity
(``demo:positive`` or ``demo:negative``). A plain RDF triple like
``s hriv:hasExactMeaning o`` cannot itself carry that polarity.

That creates a modeling problem:
- a positive mapping and a negative mapping between the same endpoints would
  collapse to the same bare RDF triple;
- a negative mapping would therefore be misrepresented if exported as a direct
  ``hriv:hasExactMeaning`` assertion.

Decision taken for this generator:
- the authoritative RDF representation of exact meaning is the reified
  ``demo:Mapping`` instance;
- polarity is always attached via ``demo:hasPolarity`` on that mapping node;
- therefore this generator intentionally does NOT emit direct
  ``hriv:hasExactMeaning`` triples at all.

Any consumer that needs exact-meaning information should read the reified
``demo:Mapping`` instances rather than expect direct ``hriv:hasExactMeaning``
triples in the generated instance file.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import re
import sys
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Literal as TypingLiteral

from rdflib import Graph, Literal, Namespace, URIRef
from rdflib.namespace import OWL, RDF, RDFS, XSD

SCHEMA = Namespace("https://w3id.org/health-ri/semantic-interoperability/schema/")
HRIV = Namespace("https://w3id.org/health-ri/mapping-vocabulary/")
DEMOI = Namespace("https://example.org/health-ri/demo-instance/")
SCHEMA_ONTOLOGY_IRI = URIRef(
    "https://w3id.org/health-ri/semantic-interoperability/schema"
)
INSTANCES_ONTOLOGY_IRI = URIRef("urn:instances:semantic-interoperability-demo")

EXPECTED_PREFIX_COLUMNS = ["prefix", "url"]
EXPECTED_VERTICAL_COLUMNS = [
    "subject_id",
    "subject_label",
    "predicate_id",
    "predicate_modifier",
    "object_id",
    "object_label",
]
EXPECTED_HORIZONTAL_COLUMNS = [
    "subject_type",
    "subject_id",
    "subject_label",
    "object_type",
    "object_id",
    "object_label",
]

ALLOWED_HORIZONTAL_TYPES = {"standard", "model"}

CURIE_RE = re.compile(r"^(?P<prefix>[A-Za-z][A-Za-z0-9._-]*):(?P<local>.+)$")
QUOTED_LANGSTRING_RE = re.compile(
    r'^"(?P<text>(?:[^"\\]|\\.)*)"@(?P<lang>[A-Za-z]{2,8}(?:-[A-Za-z0-9]{1,8})*)$'
)
BARE_LANGSTRING_RE = re.compile(
    r"^(?P<text>.+)@(?P<lang>[A-Za-z]{2,8}(?:-[A-Za-z0-9]{1,8})*)$"
)


class ScriptError(Exception):
    """Raised when the input cannot be transformed safely."""


@dataclass(frozen=True)
class VerticalRow:
    row_number: int
    source_path: str
    source_kind: TypingLiteral["standard", "model"]
    subject_id: str
    subject_label: str
    predicate_id: str
    predicate_modifier: str
    object_id: str
    object_label: str


@dataclass(frozen=True)
class HorizontalRow:
    row_number: int
    source_path: str
    subject_type: TypingLiteral["standard", "model"]
    subject_id: str
    subject_label: str
    object_type: TypingLiteral["standard", "model"]
    object_id: str
    object_label: str


class PrefixMap:
    def __init__(self, mapping: dict[str, str]) -> None:
        self.mapping = mapping

    def expand(self, curie: str) -> URIRef:
        match = CURIE_RE.fullmatch(curie)
        if not match:
            raise ScriptError(f"Invalid CURIE: {curie}")
        prefix = match.group("prefix")
        local = match.group("local")
        if prefix not in self.mapping:
            raise ScriptError(f"Unknown CURIE prefix '{prefix}' in value '{curie}'")
        return URIRef(self.mapping[prefix] + local)

    def prefix_of(self, curie: str) -> str:
        match = CURIE_RE.fullmatch(curie)
        if not match:
            raise ScriptError(f"Invalid CURIE: {curie}")
        prefix = match.group("prefix")
        if prefix not in self.mapping:
            raise ScriptError(f"Unknown CURIE prefix '{prefix}' in value '{curie}'")
        return prefix


class ConceptRegistry:
    def __init__(self, prefixes: PrefixMap) -> None:
        self.prefixes = prefixes
        self.known_ids: dict[tuple[str, str], Literal] = {}

    def register(
        self,
        kind: TypingLiteral["standard", "model"],
        curie: str,
        label_value: str,
        context: str,
    ) -> None:
        self.prefixes.expand(curie)
        label = parse_label_literal(label_value)
        key = (kind, curie)
        existing = self.known_ids.get(key)
        if existing is not None and existing != label:
            raise ScriptError(
                f"Conflicting labels for {kind} concept '{curie}' in {context}: "
                f"existing {existing.n3()} vs new {label.n3()}"
            )
        self.known_ids[key] = label

        other_kind = "model" if kind == "standard" else "standard"
        if (other_kind, curie) in self.known_ids:
            raise ScriptError(
                f"Concept '{curie}' is declared as both standard and model."
            )

    def require(
        self,
        kind: TypingLiteral["standard", "model"],
        curie: str,
        label_value: str,
        context: str,
    ) -> Literal:
        key = (kind, curie)
        if key not in self.known_ids:
            raise ScriptError(
                f"{context}: referenced {kind} concept '{curie}' was not found in the corresponding vertical input file."
            )
        given = parse_label_literal(label_value)
        known = self.known_ids[key]
        if known != given:
            raise ScriptError(
                f"{context}: label mismatch for {kind} concept '{curie}': "
                f"expected {known.n3()} but found {given.n3()}"
            )
        return known


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Create instances.ttl from prefix.csv, input-standard.csv, input-model.csv, "
            "and input-horizontal.csv for the semantic interoperability demo schema."
        )
    )
    parser.add_argument(
        "--standard-input",
        default=None,
        help="Path to input-standard.csv. Default: ../inputs/input-standard.csv relative to this script.",
    )
    parser.add_argument(
        "--model-input",
        default=None,
        help="Path to input-model.csv. Default: ../inputs/input-model.csv relative to this script.",
    )
    parser.add_argument(
        "--horizontal-input",
        default=None,
        help="Path to input-horizontal.csv. Default: ../inputs/input-horizontal.csv relative to this script.",
    )
    parser.add_argument(
        "--prefix",
        default=None,
        help="Path to prefix.csv. Default: ../inputs/prefix.csv relative to this script.",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Path to the output Turtle file. Default: ../inputs/instances.ttl relative to this script.",
    )
    parser.add_argument(
        "--delimiter",
        default=";",
        help="CSV delimiter used by the input files (default: ';')",
    )
    parser.add_argument(
        "--import-schema",
        action="store_true",
        help="Add owl:imports to the schema ontology IRI.",
    )
    return parser.parse_args()


def digest_token(*parts: str, length: int = 16) -> str:
    h = hashlib.sha256()
    for part in parts:
        h.update(part.encode("utf-8"))
        h.update(b"\x1f")
    return h.hexdigest()[:length]


def ordered_pair(
    a: tuple[str, str], b: tuple[str, str]
) -> tuple[tuple[str, str], tuple[str, str]]:
    return (a, b) if a <= b else (b, a)


def mapping_uri(source: URIRef, target: URIRef, polarity: URIRef) -> URIRef:
    pol = "neg" if polarity == SCHEMA.negative else "pos"
    return DEMOI[f"asserted-map-{digest_token(str(source), str(target), pol)}"]


def alignment_uri(left: URIRef, right: URIRef) -> URIRef:
    a, b = (
        (str(left), str(right)) if str(left) <= str(right) else (str(right), str(left))
    )
    return DEMOI[f"asserted-align-{digest_token(a, b)}"]


def read_csv_rows(path: Path, delimiter: str) -> tuple[list[str], list[dict[str, str]]]:
    try:
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle, delimiter=delimiter)
            if reader.fieldnames is None:
                raise ScriptError(f"CSV file '{path}' is missing a header row.")
            rows: list[dict[str, str]] = []
            for row in reader:
                normalized: dict[str, str] = {}
                for key, value in row.items():
                    if key is None:
                        continue
                    normalized[key.strip()] = (value or "").strip()
                rows.append(normalized)
            return [name.strip() for name in reader.fieldnames], rows
    except FileNotFoundError as exc:
        raise ScriptError(f"File not found: {path}") from exc


def load_prefixes(path: Path, delimiter: str) -> PrefixMap:
    fieldnames, rows = read_csv_rows(path, delimiter)
    if fieldnames != EXPECTED_PREFIX_COLUMNS:
        raise ScriptError(
            "prefix.csv must have exactly these columns in this order: "
            f"{EXPECTED_PREFIX_COLUMNS}. Found: {fieldnames}"
        )

    mapping: dict[str, str] = {}
    for row in rows:
        prefix = row.get("prefix", "")
        url = row.get("url", "")
        if not prefix or not url:
            raise ScriptError(
                "Every prefix.csv row must provide both 'prefix' and 'url'."
            )
        if prefix in mapping:
            raise ScriptError(f"Duplicate prefix in prefix.csv: {prefix}")
        mapping[prefix] = url

    return PrefixMap(mapping)


def load_vertical_rows(
    path: Path,
    delimiter: str,
    source_kind: TypingLiteral["standard", "model"],
) -> list[VerticalRow]:
    fieldnames, raw_rows = read_csv_rows(path, delimiter)
    if fieldnames != EXPECTED_VERTICAL_COLUMNS:
        raise ScriptError(
            f"{path.name} must have exactly these columns in this order: "
            f"{EXPECTED_VERTICAL_COLUMNS}. Found: {fieldnames}"
        )

    rows: list[VerticalRow] = []
    for row_number, raw in enumerate(raw_rows, start=2):
        row = VerticalRow(
            row_number=row_number,
            source_path=path.name,
            source_kind=source_kind,
            subject_id=raw.get("subject_id", ""),
            subject_label=raw.get("subject_label", ""),
            predicate_id=raw.get("predicate_id", ""),
            predicate_modifier=raw.get("predicate_modifier", ""),
            object_id=raw.get("object_id", ""),
            object_label=raw.get("object_label", ""),
        )
        if not row.subject_id:
            raise ScriptError(
                f"{path.name}, row {row_number}: 'subject_id' is required."
            )
        if not row.subject_label:
            raise ScriptError(
                f"{path.name}, row {row_number}: 'subject_label' is required."
            )
        if not row.predicate_id:
            raise ScriptError(
                f"{path.name}, row {row_number}: 'predicate_id' is required."
            )
        if not row.object_id:
            raise ScriptError(
                f"{path.name}, row {row_number}: 'object_id' is required."
            )
        if not row.object_label:
            raise ScriptError(
                f"{path.name}, row {row_number}: 'object_label' is required."
            )
        if (
            row.predicate_id == "hriv:hasExactMeaning"
            and row.predicate_modifier not in {"", "Not"}
        ):
            raise ScriptError(
                f"{path.name}, row {row_number}: unsupported predicate_modifier '{row.predicate_modifier}'. "
                "Allowed values for hriv:hasExactMeaning are empty and 'Not'."
            )
        rows.append(row)
    return rows


def load_horizontal_rows(path: Path, delimiter: str) -> list[HorizontalRow]:
    fieldnames, raw_rows = read_csv_rows(path, delimiter)
    if fieldnames != EXPECTED_HORIZONTAL_COLUMNS:
        raise ScriptError(
            f"{path.name} must have exactly these columns in this order: "
            f"{EXPECTED_HORIZONTAL_COLUMNS}. Found: {fieldnames}"
        )

    rows: list[HorizontalRow] = []
    seen_pairs: set[tuple[tuple[str, str], tuple[str, str]]] = set()
    for row_number, raw in enumerate(raw_rows, start=2):
        subject_type = raw.get("subject_type", "")
        object_type = raw.get("object_type", "")
        if subject_type not in ALLOWED_HORIZONTAL_TYPES:
            raise ScriptError(
                f"{path.name}, row {row_number}: 'subject_type' must be exactly 'standard' or 'model'."
            )
        if object_type not in ALLOWED_HORIZONTAL_TYPES:
            raise ScriptError(
                f"{path.name}, row {row_number}: 'object_type' must be exactly 'standard' or 'model'."
            )

        row = HorizontalRow(
            row_number=row_number,
            source_path=path.name,
            subject_type=subject_type,  # type: ignore[arg-type]
            subject_id=raw.get("subject_id", ""),
            subject_label=raw.get("subject_label", ""),
            object_type=object_type,  # type: ignore[arg-type]
            object_id=raw.get("object_id", ""),
            object_label=raw.get("object_label", ""),
        )
        if not row.subject_id:
            raise ScriptError(
                f"{path.name}, row {row_number}: 'subject_id' is required."
            )
        if not row.subject_label:
            raise ScriptError(
                f"{path.name}, row {row_number}: 'subject_label' is required."
            )
        if not row.object_id:
            raise ScriptError(
                f"{path.name}, row {row_number}: 'object_id' is required."
            )
        if not row.object_label:
            raise ScriptError(
                f"{path.name}, row {row_number}: 'object_label' is required."
            )
        if row.subject_id == row.object_id and row.subject_type == row.object_type:
            raise ScriptError(
                f"{path.name}, row {row_number}: aligns is irreflexive, so subject and object must differ."
            )

        pair = ordered_pair(
            (row.subject_type, row.subject_id), (row.object_type, row.object_id)
        )
        if pair in seen_pairs:
            raise ScriptError(
                f"{path.name}, row {row_number}: duplicate horizontal aligns pair detected "
                f"for {pair[0]} and {pair[1]}."
            )
        seen_pairs.add(pair)
        rows.append(row)
    return rows


def parse_label_literal(value: str) -> Literal:
    value = value.strip()
    if not value:
        raise ScriptError("Empty label literal is not allowed.")

    quoted_match = QUOTED_LANGSTRING_RE.fullmatch(value)
    if quoted_match:
        text = bytes(quoted_match.group("text"), "utf-8").decode("unicode_escape")
        return Literal(text, lang=quoted_match.group("lang"))

    bare_match = BARE_LANGSTRING_RE.fullmatch(value)
    if bare_match:
        return Literal(bare_match.group("text"), lang=bare_match.group("lang"))

    return Literal(value)


def slugify(value: str) -> str:
    slug = re.sub(r"[^A-Za-z0-9_-]+", "-", value).strip("-")
    return slug or "item"


def artifact_uri(kind: TypingLiteral["standard", "model"], prefix: str) -> URIRef:
    stem = "standard" if kind == "standard" else "model"
    return DEMOI[f"{stem}-{slugify(prefix)}"]


def add_label(graph: Graph, subject: URIRef, label_value: str) -> None:
    graph.add((subject, RDFS.label, parse_label_literal(label_value)))


def ensure_artifact(
    graph: Graph, kind: TypingLiteral["standard", "model"], prefix: str
) -> URIRef:
    artifact = artifact_uri(kind, prefix)
    if kind == "standard":
        graph.add((artifact, RDF.type, SCHEMA.Standard))
        graph.add((artifact, RDFS.label, Literal(prefix, lang="en")))
    else:
        graph.add((artifact, RDF.type, SCHEMA.Model))
        graph.add((artifact, RDFS.label, Literal(prefix, lang="en")))
    return artifact


def ensure_representation_concept(
    graph: Graph,
    prefixes: PrefixMap,
    kind: TypingLiteral["standard", "model"],
    curie: str,
    label_value: str | None,
) -> URIRef:
    concept = prefixes.expand(curie)
    artifact = ensure_artifact(graph, kind, prefixes.prefix_of(curie))
    graph.add((concept, RDF.type, SCHEMA.RepresentationConcept))
    graph.set((concept, SCHEMA.isConsistent, Literal(True, datatype=XSD.boolean)))

    if kind == "standard":
        graph.add((concept, RDF.type, SCHEMA.StandardConcept))
        graph.add((artifact, SCHEMA.hasStandardConcept, concept))
    else:
        graph.add((concept, RDF.type, SCHEMA.ModelConcept))
        graph.add((artifact, SCHEMA.hasModelConcept, concept))

    if label_value:
        add_label(graph, concept, label_value)
    return concept


def ensure_ontology_concept(
    graph: Graph,
    prefixes: PrefixMap,
    curie: str,
    label_value: str | None,
) -> URIRef:
    concept = prefixes.expand(curie)
    graph.add((concept, RDF.type, SCHEMA.OntologyConcept))
    if label_value:
        add_label(graph, concept, label_value)
    return concept


def validate_vertical_duplicates(rows: Iterable[VerticalRow]) -> None:
    seen: set[tuple[str, str, str, str, str, str, str]] = set()
    for row in rows:
        key = (
            row.source_kind,
            row.subject_id,
            row.subject_label,
            row.predicate_id,
            row.predicate_modifier,
            row.object_id,
            row.object_label,
        )
        if key in seen:
            raise ScriptError(
                f"Duplicate semantic row detected: {row.source_path}, row {row.row_number}."
            )
        seen.add(key)


def register_known_concepts(
    registry: ConceptRegistry, rows: Iterable[VerticalRow]
) -> None:
    for row in rows:
        registry.register(
            kind=row.source_kind,
            curie=row.subject_id,
            label_value=row.subject_label,
            context=f"{row.source_path}, row {row.row_number}",
        )


def add_exact_meaning_row(graph: Graph, row: VerticalRow, prefixes: PrefixMap) -> None:
    source = ensure_representation_concept(
        graph, prefixes, row.source_kind, row.subject_id, row.subject_label
    )
    target = ensure_ontology_concept(graph, prefixes, row.object_id, row.object_label)
    polarity = SCHEMA.negative if row.predicate_modifier == "Not" else SCHEMA.positive
    mapping = mapping_uri(source, target, polarity)

    # IMPORTANT MODELING DECISION
    # ---------------------------
    # We intentionally do NOT emit a direct triple:
    #     source hriv:hasExactMeaning target
    #
    # Reason:
    # - both positive and negative exact-meaning mappings use the same conceptual
    #   relation type (hriv:hasExactMeaning);
    # - in RDF, a plain binary triple cannot carry the polarity qualifier;
    # - therefore emitting the bare triple would collapse positive and negative
    #   mappings between the same endpoints into the same assertion.
    #
    # Authoritative representation in this generator:
    # - exact meaning is represented only through a reified demo:Mapping node;
    # - polarity is stored explicitly with demo:hasPolarity;
    # - consumers must use the Mapping instance, not expect direct
    #   hriv:hasExactMeaning triples in the output.
    graph.add((mapping, RDF.type, SCHEMA.Mapping))
    graph.add((mapping, SCHEMA.source, source))
    graph.add((mapping, SCHEMA.target, target))
    graph.add((mapping, SCHEMA.hasMappingSource, source))
    graph.add((mapping, SCHEMA.hasTargetOntologyConcept, target))
    graph.add((mapping, SCHEMA.hasPolarity, polarity))
    graph.add((mapping, SCHEMA.hasProvenance, SCHEMA.asserted))


def add_asserted_alignment(
    graph: Graph,
    prefixes: PrefixMap,
    subject_type: TypingLiteral["standard", "model"],
    subject_id: str,
    subject_label: str,
    object_type: TypingLiteral["standard", "model"],
    object_id: str,
    object_label: str,
) -> None:
    left = ensure_representation_concept(
        graph, prefixes, subject_type, subject_id, subject_label
    )
    right = ensure_representation_concept(
        graph, prefixes, object_type, object_id, object_label
    )
    if left == right:
        raise ScriptError("aligns is irreflexive, so subject and object must differ.")

    node = alignment_uri(left, right)
    graph.add((node, RDF.type, SCHEMA.Alignment))
    graph.add((node, SCHEMA.source, left))
    graph.add((node, SCHEMA.target, right))
    graph.add((node, SCHEMA.hasAlignmentSource, left))
    graph.add((node, SCHEMA.hasAlignmentTarget, right))
    graph.add((node, SCHEMA.hasProvenance, SCHEMA.asserted))

    graph.add((left, SCHEMA.aligns, right))
    graph.add((right, SCHEMA.aligns, left))


def build_graph(
    vertical_rows: list[VerticalRow],
    horizontal_rows: list[HorizontalRow],
    prefixes: PrefixMap,
    import_schema: bool = False,
) -> tuple[Graph, Counter[str]]:
    graph = Graph()
    graph.bind("demo", SCHEMA)
    graph.bind("hriv", HRIV)
    graph.bind("demoi", DEMOI)
    graph.bind("owl", OWL)
    graph.bind("rdf", RDF)
    graph.bind("rdfs", RDFS)
    graph.bind("xsd", XSD)
    for prefix, url in prefixes.mapping.items():
        graph.bind(prefix, Namespace(url))

    graph.add((INSTANCES_ONTOLOGY_IRI, RDF.type, OWL.Ontology))
    if import_schema:
        graph.add((INSTANCES_ONTOLOGY_IRI, OWL.imports, SCHEMA_ONTOLOGY_IRI))

    validate_vertical_duplicates(vertical_rows)
    registry = ConceptRegistry(prefixes)
    register_known_concepts(registry, vertical_rows)

    skipped_predicates: Counter[str] = Counter()
    for row in vertical_rows:
        if row.predicate_id == "hriv:hasExactMeaning":
            add_exact_meaning_row(graph, row, prefixes)
        else:
            ensure_representation_concept(
                graph, prefixes, row.source_kind, row.subject_id, row.subject_label
            )
            skipped_predicates[row.predicate_id] += 1

    for row in horizontal_rows:
        registry.require(
            row.subject_type,
            row.subject_id,
            row.subject_label,
            f"{row.source_path}, row {row.row_number}",
        )
        registry.require(
            row.object_type,
            row.object_id,
            row.object_label,
            f"{row.source_path}, row {row.row_number}",
        )
        add_asserted_alignment(
            graph,
            prefixes,
            row.subject_type,
            row.subject_id,
            row.subject_label,
            row.object_type,
            row.object_id,
            row.object_label,
        )

    return graph, skipped_predicates


def main() -> int:
    args = parse_args()

    script_dir = Path(__file__).resolve().parent
    input_dir = script_dir.parent / "inputs"

    prefix_path = (
        Path(args.prefix).expanduser().resolve()
        if args.prefix
        else (input_dir / "prefix.csv").resolve()
    )
    standard_input_path = (
        Path(args.standard_input).expanduser().resolve()
        if args.standard_input
        else (input_dir / "input-standard.csv").resolve()
    )
    model_input_path = (
        Path(args.model_input).expanduser().resolve()
        if args.model_input
        else (input_dir / "input-model.csv").resolve()
    )
    horizontal_input_path = (
        Path(args.horizontal_input).expanduser().resolve()
        if args.horizontal_input
        else (input_dir / "input-horizontal.csv").resolve()
    )
    output_path = (
        Path(args.output).expanduser().resolve()
        if args.output
        else (input_dir / "instances.ttl").resolve()
    )

    prefixes = load_prefixes(prefix_path, args.delimiter)
    standard_rows = load_vertical_rows(standard_input_path, args.delimiter, "standard")
    model_rows = load_vertical_rows(model_input_path, args.delimiter, "model")
    horizontal_rows = load_horizontal_rows(horizontal_input_path, args.delimiter)

    graph, skipped_predicates = build_graph(
        vertical_rows=[*standard_rows, *model_rows],
        horizontal_rows=horizontal_rows,
        prefixes=prefixes,
        import_schema=args.import_schema,
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    graph.serialize(destination=output_path, format="turtle")

    exact_rows = sum(
        1
        for row in [*standard_rows, *model_rows]
        if row.predicate_id == "hriv:hasExactMeaning"
    )
    print(f"Wrote {output_path}")
    print(f"Standard rows: {len(standard_rows)}")
    print(f"Model rows: {len(model_rows)}")
    print(f"Horizontal rows: {len(horizontal_rows)}")
    print(f"Exact-meaning rows materialized: {exact_rows}")
    print(f"Vertical non-exact rows skipped: {sum(skipped_predicates.values())}")
    if skipped_predicates:
        details = ", ".join(
            f"{predicate}={count}"
            for predicate, count in sorted(skipped_predicates.items())
        )
        print(f"Skipped predicates: {details}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ScriptError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        raise SystemExit(1)
