#!/usr/bin/env python3
"""Create instance data for the semantic interoperability schema ontology.

The script reads:
- input.csv   : mapping rows
- prefix.csv  : prefix declarations used by the input CURIEs

And writes:
- instances.ttl

Implemented assumptions based on the latest requirements:
- Only rows with predicate_id == hriv:hasExactMeaning are transformed.
- One artifact instance is derived per source CURIE prefix:
  - standard rows -> demo:Standard artifact
  - model rows    -> demo:Model artifact
- The optional aligns column is supported before implements.
  When present on a standard row, it creates:
  - demo:aligns from the source StandardConcept to the referenced StandardConcept
  - one asserted, positive demo:Alignment instance linking the two concepts
- The optional implements column is supported as the last column.
  When present on a model row, it creates demo:implements from the ModelConcept
  to the referenced StandardConcept.
- predicate_modifier controls polarity:
  - empty -> demo:positive
  - Not   -> demo:negative
- rows whose mapping is referenced by another retained row via replaces are
  marked demo:replaced; all other retained mappings are marked demo:valid.
- By default, the generated instances ontology does not import the schema.
  This avoids a circular import when you import instances.ttl into the schema
  ontology in Protégé. Use --import-schema if you want a standalone instances
  ontology that imports the schema directly.

Important modeling note:
The ontology uses instance IRIs as identifiers and therefore this script does
not generate demo:id literals. Positive exact mappings are asserted directly
with hriv:hasExactMeaning for convenience. Negative exact mappings are
represented structurally through mapping instances plus
demo:hasPolarity demo:negative, and therefore do not get a direct
hriv:hasExactMeaning assertion.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from rdflib import Graph, Literal, Namespace, URIRef
from rdflib.namespace import OWL, RDF, RDFS

SCHEMA = Namespace("https://w3id.org/health-ri/semantic-interoperability/schema/")
HRIV = Namespace("https://w3id.org/health-ri/mapping-vocabulary/")
HRIM = Namespace("https://w3id.org/health-ri/semantic-interoperability/mappings#")
ONTOLOGY_IRI = URIRef("https://w3id.org/health-ri/semantic-interoperability/schema")

BASE_COLUMNS = [
    "type",
    "mapping",
    "subject_id",
    "subject_label",
    "predicate_id",
    "predicate_modifier",
    "object_id",
    "object_label",
    "replaces",
]
COLUMNS_WITH_IMPLEMENTS = BASE_COLUMNS + ["implements"]
COLUMNS_WITH_ALIGNS = BASE_COLUMNS + ["aligns"]
COLUMNS_WITH_ALIGNS_AND_IMPLEMENTS = BASE_COLUMNS + ["aligns", "implements"]
ALLOWED_INPUT_COLUMNS = {
    tuple(BASE_COLUMNS),
    tuple(COLUMNS_WITH_IMPLEMENTS),
    tuple(COLUMNS_WITH_ALIGNS),
    tuple(COLUMNS_WITH_ALIGNS_AND_IMPLEMENTS),
}
EXPECTED_PREFIX_COLUMNS = ["prefix", "url"]
ALLOWED_TYPES = {"standard", "model"}
CURIE_RE = re.compile(r"^(?P<prefix>[A-Za-z][A-Za-z0-9._-]*):(?P<local>.+)$")
LANGSTRING_RE = re.compile(
    r'^"(?P<text>(?:[^"\\]|\\.)*)"@(?P<lang>[A-Za-z]{2,8}(?:-[A-Za-z0-9]{1,8})*)$'
)


@dataclass(frozen=True)
class Row:
    row_number: int
    type: str
    mapping: str
    subject_id: str
    subject_label: str
    predicate_id: str
    predicate_modifier: str
    object_id: str
    object_label: str
    replaces: str
    aligns: str = ""
    implements: str = ""


class ScriptError(Exception):
    """Raised when the input cannot be transformed safely."""


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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create instances.ttl from input.csv and prefix.csv for the semantic interoperability schema ontology."
    )
    parser.add_argument(
        "--input",
        default="input.csv",
        help="Path to the input CSV file (default: input.csv)",
    )
    parser.add_argument(
        "--prefix",
        default="prefix.csv",
        help="Path to the prefix CSV file (default: prefix.csv)",
    )
    parser.add_argument(
        "--output",
        default="instances.ttl",
        help="Path to the output Turtle file (default: instances.ttl)",
    )
    parser.add_argument(
        "--delimiter",
        default=";",
        help="CSV delimiter used by both files (default: ';')",
    )
    parser.add_argument(
        "--import-schema",
        action="store_true",
        help=(
            "Add owl:imports to the schema ontology IRI. Disabled by default so the output can be imported into the schema in Protégé without creating a circular import."
        ),
    )
    return parser.parse_args()


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
            f"prefix.csv must have exactly these columns in this order: {EXPECTED_PREFIX_COLUMNS}. Found: {fieldnames}"
        )

    prefixes: dict[str, str] = {}
    for row in rows:
        prefix = row.get("prefix", "")
        url = row.get("url", "")
        if not prefix or not url:
            raise ScriptError(
                "Every prefix.csv row must provide both 'prefix' and 'url'."
            )
        if prefix in prefixes:
            raise ScriptError(f"Duplicate prefix in prefix.csv: {prefix}")
        prefixes[prefix] = url

    return PrefixMap(prefixes)


def load_input_rows(path: Path, delimiter: str) -> list[Row]:
    fieldnames, raw_rows = read_csv_rows(path, delimiter)
    fieldnames_tuple = tuple(fieldnames)
    if fieldnames_tuple not in ALLOWED_INPUT_COLUMNS:
        raise ScriptError(
            "input.csv must have exactly these columns in this order: "
            f"{BASE_COLUMNS}, {COLUMNS_WITH_IMPLEMENTS}, {COLUMNS_WITH_ALIGNS}, "
            f"or {COLUMNS_WITH_ALIGNS_AND_IMPLEMENTS}. Found: {fieldnames}"
        )

    has_aligns = "aligns" in fieldnames
    has_implements = "implements" in fieldnames

    rows: list[Row] = []
    for row_number, raw in enumerate(raw_rows, start=2):
        row_type = raw.get("type", "")
        if row_type not in ALLOWED_TYPES:
            raise ScriptError(
                f"Row {row_number}: unsupported type '{row_type}'. Allowed values: {sorted(ALLOWED_TYPES)}"
            )
        rows.append(
            Row(
                row_number=row_number,
                type=row_type,
                mapping=raw.get("mapping", ""),
                subject_id=raw.get("subject_id", ""),
                subject_label=raw.get("subject_label", ""),
                predicate_id=raw.get("predicate_id", ""),
                predicate_modifier=raw.get("predicate_modifier", ""),
                object_id=raw.get("object_id", ""),
                object_label=raw.get("object_label", ""),
                replaces=raw.get("replaces", ""),
                aligns=raw.get("aligns", "") if has_aligns else "",
                implements=raw.get("implements", "") if has_implements else "",
            )
        )
    return rows


def parse_langstring(value: str) -> tuple[str, str]:
    match = LANGSTRING_RE.fullmatch(value)
    if not match:
        raise ScriptError(f"Invalid langString literal: {value}")
    text = bytes(match.group("text"), "utf-8").decode("unicode_escape")
    lang = match.group("lang")
    return text, lang


def slugify(value: str) -> str:
    slug = re.sub(r"[^A-Za-z0-9_-]+", "-", value).strip("-")
    return slug or "item"


def digest_token(*parts: str, length: int = 16) -> str:
    h = hashlib.sha256()
    for part in parts:
        h.update(part.encode("utf-8"))
        h.update(b"\x1f")
    return h.hexdigest()[:length]


def artifact_uri(kind: str, prefix: str) -> URIRef:
    return SCHEMA[f"artifact-{kind}-{slugify(prefix)}"]


def alignment_uri(source: URIRef, target: URIRef) -> URIRef:
    return HRIM[f"asserted-align-{digest_token(str(source), str(target))}"]


def add_label(graph: Graph, subject: URIRef, langstring: str) -> None:
    text, lang = parse_langstring(langstring)
    graph.add((subject, RDFS.label, Literal(text, lang=lang)))


def ensure_standard_artifact(graph: Graph, prefix: str) -> URIRef:
    uri = artifact_uri("standard", prefix)
    graph.add((uri, RDF.type, SCHEMA.Standard))
    graph.add((uri, RDFS.label, Literal(prefix, lang="en")))
    return uri


def ensure_model_artifact(graph: Graph, prefix: str) -> URIRef:
    uri = artifact_uri("model", prefix)
    graph.add((uri, RDF.type, SCHEMA.Model))
    graph.add((uri, RDFS.label, Literal(prefix, lang="en")))
    return uri


def ensure_standard_concept(
    graph: Graph, prefixes: PrefixMap, curie: str, label: str | None = None
) -> URIRef:
    uri = prefixes.expand(curie)
    prefix = prefixes.prefix_of(curie)
    standard = ensure_standard_artifact(graph, prefix)
    graph.add((uri, RDF.type, SCHEMA.StandardConcept))
    graph.add((uri, SCHEMA.isConceptOfStandard, standard))
    graph.add((standard, SCHEMA.hasStandardConcept, uri))
    if label:
        add_label(graph, uri, label)
    return uri


def ensure_model_concept(
    graph: Graph, prefixes: PrefixMap, curie: str, label: str | None = None
) -> URIRef:
    uri = prefixes.expand(curie)
    prefix = prefixes.prefix_of(curie)
    model = ensure_model_artifact(graph, prefix)
    graph.add((uri, RDF.type, SCHEMA.ModelConcept))
    graph.add((uri, SCHEMA.isConceptOfModel, model))
    graph.add((model, SCHEMA.hasModelConcept, uri))
    if label:
        add_label(graph, uri, label)
    return uri


def ensure_ontology_concept(
    graph: Graph, prefixes: PrefixMap, curie: str, label: str | None = None
) -> URIRef:
    uri = prefixes.expand(curie)
    graph.add((uri, RDF.type, SCHEMA.OntologyConcept))
    if label:
        add_label(graph, uri, label)
    return uri


def ensure_alignment(graph: Graph, source: URIRef, target: URIRef) -> URIRef:
    uri = alignment_uri(source, target)
    graph.add((source, SCHEMA.aligns, target))
    graph.add((uri, RDF.type, SCHEMA.Alignment))
    graph.add((uri, SCHEMA.hasAlignmentSource, source))
    graph.add((uri, SCHEMA.hasAlignmentTarget, target))
    graph.add((uri, SCHEMA.hasPolarity, SCHEMA.positive))
    graph.add((uri, SCHEMA.hasProvenance, SCHEMA.asserted))
    return uri


def retained_rows(rows: Iterable[Row]) -> list[Row]:
    return [row for row in rows if row.predicate_id == "hriv:hasExactMeaning"]


def replaced_mapping_ids(rows: Iterable[Row]) -> set[str]:
    return {row.replaces for row in rows if row.replaces}


def build_graph(
    rows: list[Row], prefixes: PrefixMap, import_schema: bool = False
) -> Graph:
    graph = Graph()
    graph.bind("demo", SCHEMA)
    graph.bind("hriv", HRIV)
    graph.bind("hrim", HRIM)
    graph.bind("owl", OWL)
    graph.bind("rdf", RDF)
    graph.bind("rdfs", RDFS)
    for prefix, url in prefixes.mapping.items():
        graph.bind(prefix, Namespace(url))

    instances_ontology = URIRef("urn:instances:semantic-interoperability-schema")
    graph.add((instances_ontology, RDF.type, OWL.Ontology))
    if import_schema:
        graph.add((instances_ontology, OWL.imports, ONTOLOGY_IRI))

    kept_rows = retained_rows(rows)
    kept_mapping_ids = {row.mapping for row in kept_rows}
    replaced_ids = replaced_mapping_ids(kept_rows)

    for row in kept_rows:
        mapping_uri = prefixes.expand(row.mapping)
        target_uri = ensure_ontology_concept(
            graph, prefixes, row.object_id, row.object_label
        )

        if row.type == "standard":
            source_uri = ensure_standard_concept(
                graph, prefixes, row.subject_id, row.subject_label
            )
            graph.add((mapping_uri, RDF.type, SCHEMA.StandardMapping))
            graph.add((mapping_uri, SCHEMA.hasSourceStandardConcept, source_uri))
            if row.predicate_modifier == "":
                graph.add((source_uri, HRIV.hasExactMeaning, target_uri))
            if row.aligns:
                aligned_uri = ensure_standard_concept(graph, prefixes, row.aligns)
                ensure_alignment(graph, source_uri, aligned_uri)

        elif row.type == "model":
            source_uri = ensure_model_concept(
                graph, prefixes, row.subject_id, row.subject_label
            )
            graph.add((mapping_uri, RDF.type, SCHEMA.ModelMapping))
            graph.add((mapping_uri, SCHEMA.hasSourceModelConcept, source_uri))
            if row.predicate_modifier == "":
                graph.add((source_uri, HRIV.hasExactMeaning, target_uri))
            if row.aligns:
                raise ScriptError(
                    f"Row {row.row_number}: 'aligns' is only supported for standard rows because demo:aligns relates StandardConcept instances."
                )
            if row.implements:
                implemented_uri = ensure_standard_concept(
                    graph, prefixes, row.implements
                )
                graph.add((source_uri, SCHEMA.implements, implemented_uri))
        else:  # pragma: no cover - defensive, should be prevented earlier
            raise ScriptError(f"Row {row.row_number}: unsupported type '{row.type}'")

        graph.add((mapping_uri, SCHEMA.hasTargetOntologyConcept, target_uri))
        graph.add((mapping_uri, SCHEMA.hasProvenance, SCHEMA.asserted))
        graph.add(
            (
                mapping_uri,
                SCHEMA.hasPolarity,
                SCHEMA.negative if row.predicate_modifier == "Not" else SCHEMA.positive,
            )
        )
        graph.add(
            (
                mapping_uri,
                SCHEMA.hasStatus,
                SCHEMA.replaced if row.mapping in replaced_ids else SCHEMA.valid,
            )
        )

        if row.replaces:
            if row.replaces in kept_mapping_ids:
                graph.add((mapping_uri, SCHEMA.replaces, prefixes.expand(row.replaces)))
            else:
                print(
                    f"Warning: row {row.row_number} replaces '{row.replaces}', but that mapping is not retained after filtering to hriv:hasExactMeaning.",
                    file=sys.stderr,
                )

    return graph


def main() -> int:
    args = parse_args()
    prefixes = load_prefixes(Path(args.prefix), args.delimiter)
    rows = load_input_rows(Path(args.input), args.delimiter)
    graph = build_graph(rows, prefixes, import_schema=args.import_schema)
    graph.serialize(destination=args.output, format="turtle")
    print(f"Wrote {args.output}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ScriptError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        raise SystemExit(1)
