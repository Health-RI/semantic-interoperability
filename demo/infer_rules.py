#!/usr/bin/env python3
"""Infer additional knowledge over instances.ttl for the demo schema.

This script reads an instance graph, applies the latest rule notes found in the
most recent project.xml, and writes the updated graph back.

Rules implemented from the latest XML:
- R1  Symmetry of Alignment
- R2  Propagation of a positive ModelConcept mapping to its implemented StandardConcept
- R3a Propagation of a positive StandardConcept mapping to its implementing ModelConcept
- R3b Alignment inferred from a shared implementing ModelConcept
- R4  Propagation of a positive StandardConcept mapping across an Alignment
- R5  Alignment inferred from shared positive exact-meaning mappings
- R6  Propagation of a negative StandardConcept mapping across an Alignment
- R7  Detection of incompatibility between aligned concepts with opposite polarity
      to the same OntologyConcept

Important note:
The latest XML contains eight rule notes because two distinct rules are both
labeled "R3". This script implements both.

Conservative interpretation choices:
- Replaced mappings are ignored during inference.
- General propagation rules (R2, R3a, R4, R5) operate on positive mappings.
- The explicit negative propagation rule (R6) handles negative mappings.
- R7 is a validation rule: it reports violations but does not remove triples.

By default, the script writes to a sibling file named <input>_extended.ttl.
"""

from __future__ import annotations

import argparse
import hashlib
import sys
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

from rdflib import Graph, Literal, Namespace, URIRef
from rdflib.namespace import OWL, RDF, RDFS, XSD

DEMO = Namespace("https://w3id.org/health-ri/semantic-interoperability/schema/")
HRIV = Namespace("https://w3id.org/health-ri/mapping-vocabulary/")
HRIM = Namespace("https://w3id.org/health-ri/semantic-interoperability/mappings#")


@dataclass(frozen=True)
class MappingAssertion:
    mapping: URIRef
    kind: str  # standard | model
    source: URIRef
    target: URIRef
    polarity: URIRef
    provenance: URIRef | None
    status: URIRef | None

    @property
    def active(self) -> bool:
        return self.status != DEMO.replaced

    @property
    def positive(self) -> bool:
        return self.polarity == DEMO.positive

    @property
    def negative(self) -> bool:
        return self.polarity == DEMO.negative


@dataclass(frozen=True)
class Violation:
    concept_a: URIRef
    concept_b: URIRef
    ontology_concept: URIRef

    def render(self) -> str:
        return (
            "R7 violation: aligned concepts have conflicting positive and negative mappings to the same ontology concept: "
            f"aligned({self.concept_a.n3()}, {self.concept_b.n3()}), "
            f"ontology={self.ontology_concept.n3()}"
        )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Infer rule-based knowledge into instances.ttl"
    )
    parser.add_argument(
        "--input",
        default="instances.ttl",
        help="Input Turtle file (default: instances.ttl)",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Output Turtle file (default: <input>_extended.ttl)",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit with status 2 when R7 violations are found",
    )
    return parser.parse_args()


def digest_token(*parts: str, length: int = 16) -> str:
    h = hashlib.sha256()
    for part in parts:
        h.update(part.encode("utf-8"))
        h.update(b"\x1f")
    return h.hexdigest()[:length]


def ordered_pair(a: URIRef, b: URIRef) -> tuple[URIRef, URIRef]:
    return (a, b) if str(a) <= str(b) else (b, a)


def alignment_uri(a: URIRef, b: URIRef) -> URIRef:
    x, y = ordered_pair(a, b)
    return HRIM[f"inf-align-{digest_token(str(x), str(y))}"]


def mapping_uri(kind: str, source: URIRef, target: URIRef, polarity: URIRef) -> URIRef:
    prefix = "inf-sm" if kind == "standard" else "inf-mm"
    pol = "neg" if polarity == DEMO.negative else "pos"
    return HRIM[f"{prefix}-{digest_token(kind, str(source), str(target), pol)}"]


def curie_or_uri(graph: Graph, term: URIRef) -> str:
    try:
        return graph.namespace_manager.normalizeUri(term)
    except Exception:
        return str(term)


def collect_mappings(graph: Graph) -> list[MappingAssertion]:
    out: list[MappingAssertion] = []
    for mapping in set(graph.subjects(RDF.type, DEMO.StandardMapping)) | set(
        graph.subjects(RDF.type, DEMO.ModelMapping)
    ):
        kind = (
            "standard"
            if (mapping, RDF.type, DEMO.StandardMapping) in graph
            else "model"
        )
        source_pred = (
            DEMO.hasSourceStandardConcept
            if kind == "standard"
            else DEMO.hasSourceModelConcept
        )
        source = next(graph.objects(mapping, source_pred), None)
        target = next(graph.objects(mapping, DEMO.hasTargetOntologyConcept), None)
        polarity = next(graph.objects(mapping, DEMO.hasPolarity), DEMO.positive)
        provenance = next(graph.objects(mapping, DEMO.hasProvenance), None)
        status = next(graph.objects(mapping, DEMO.hasStatus), None)
        if (
            isinstance(source, URIRef)
            and isinstance(target, URIRef)
            and isinstance(polarity, URIRef)
        ):
            out.append(
                MappingAssertion(
                    mapping,
                    kind,
                    source,
                    target,
                    polarity,
                    provenance if isinstance(provenance, URIRef) else None,
                    status if isinstance(status, URIRef) else None,
                )
            )
    return out


def collect_implements(graph: Graph) -> set[tuple[URIRef, URIRef]]:
    return {
        (m, s)
        for m, s in graph.subject_objects(DEMO.implements)
        if isinstance(m, URIRef) and isinstance(s, URIRef)
    }


def collect_alignment_pairs(graph: Graph) -> set[tuple[URIRef, URIRef]]:
    pairs: set[tuple[URIRef, URIRef]] = set()
    for s, o in graph.subject_objects(DEMO.aligns):
        if isinstance(s, URIRef) and isinstance(o, URIRef) and s != o:
            pairs.add(ordered_pair(s, o))
    for alignment in graph.subjects(RDF.type, DEMO.Alignment):
        src = next(graph.objects(alignment, DEMO.hasAlignmentSource), None)
        tgt = next(graph.objects(alignment, DEMO.hasAlignmentTarget), None)
        if isinstance(src, URIRef) and isinstance(tgt, URIRef) and src != tgt:
            pairs.add(ordered_pair(src, tgt))
    return pairs


def ensure_positive_exact_meaning(graph: Graph, source: URIRef, target: URIRef) -> bool:
    if (source, HRIV.hasExactMeaning, target) in graph:
        return False
    graph.add((source, HRIV.hasExactMeaning, target))
    return True


def ensure_alignment(graph: Graph, a: URIRef, b: URIRef) -> bool:
    if a == b:
        return False
    x, y = ordered_pair(a, b)
    changed = False
    if (a, DEMO.aligns, b) not in graph:
        graph.add((a, DEMO.aligns, b))
        changed = True
    if (b, DEMO.aligns, a) not in graph:
        graph.add((b, DEMO.aligns, a))
        changed = True

    uri = alignment_uri(x, y)
    if (uri, RDF.type, DEMO.Alignment) not in graph:
        graph.add((uri, RDF.type, DEMO.Alignment))
        graph.add((uri, DEMO.hasAlignmentSource, x))
        graph.add((uri, DEMO.hasAlignmentTarget, y))
        graph.add((uri, DEMO.hasPolarity, DEMO.positive))
        graph.add((uri, DEMO.hasProvenance, DEMO.inferred))
        graph.add(
            (uri, DEMO.id, Literal(f"hrim:{uri.split('#')[-1]}", datatype=XSD.string))
        )
        changed = True
    else:
        if (uri, DEMO.hasAlignmentSource, x) not in graph:
            graph.add((uri, DEMO.hasAlignmentSource, x))
            changed = True
        if (uri, DEMO.hasAlignmentTarget, y) not in graph:
            graph.add((uri, DEMO.hasAlignmentTarget, y))
            changed = True
        if (uri, DEMO.hasPolarity, DEMO.positive) not in graph:
            graph.add((uri, DEMO.hasPolarity, DEMO.positive))
            changed = True
        if (uri, DEMO.hasProvenance, DEMO.inferred) not in graph:
            graph.add((uri, DEMO.hasProvenance, DEMO.inferred))
            changed = True
    return changed


def ensure_mapping(
    graph: Graph,
    kind: str,
    source: URIRef,
    target: URIRef,
    polarity: URIRef,
) -> bool:
    assert kind in {"standard", "model"}
    assert polarity in {DEMO.positive, DEMO.negative}

    # Reuse an existing active mapping if present.
    for item in collect_mappings(graph):
        if (
            item.active
            and item.kind == kind
            and item.source == source
            and item.target == target
            and item.polarity == polarity
        ):
            changed = False
            if (
                item.provenance != DEMO.inferred
                and (item.mapping, DEMO.hasProvenance, DEMO.inferred) not in graph
            ):
                # Keep asserted provenance untouched.
                pass
            if polarity == DEMO.positive:
                changed = (
                    ensure_positive_exact_meaning(graph, source, target) or changed
                )
            return changed

    uri = mapping_uri(kind, source, target, polarity)
    mapping_class = DEMO.StandardMapping if kind == "standard" else DEMO.ModelMapping
    source_pred = (
        DEMO.hasSourceStandardConcept
        if kind == "standard"
        else DEMO.hasSourceModelConcept
    )

    graph.add((uri, RDF.type, mapping_class))
    graph.add((uri, source_pred, source))
    graph.add((uri, DEMO.hasTargetOntologyConcept, target))
    graph.add((uri, DEMO.hasPolarity, polarity))
    graph.add((uri, DEMO.hasProvenance, DEMO.inferred))
    graph.add((uri, DEMO.hasStatus, DEMO.valid))
    graph.add(
        (uri, DEMO.id, Literal(f"hrim:{uri.split('#')[-1]}", datatype=XSD.string))
    )
    if polarity == DEMO.positive:
        graph.add((source, HRIV.hasExactMeaning, target))
    return True


def detect_r7_violations(graph: Graph) -> list[Violation]:
    mappings = [m for m in collect_mappings(graph) if m.active and m.kind == "standard"]
    pos_pairs = {(m.source, m.target) for m in mappings if m.positive}
    neg_pairs = {(m.source, m.target) for m in mappings if m.negative}

    violations: dict[tuple[URIRef, URIRef, URIRef], Violation] = {}
    for a, b in collect_alignment_pairs(graph):
        targets = {t for s, t in pos_pairs if s in {a, b}} | {
            t for s, t in neg_pairs if s in {a, b}
        }
        for target in targets:
            conflict = ((a, target) in neg_pairs and (b, target) in pos_pairs) or (
                (b, target) in neg_pairs and (a, target) in pos_pairs
            )
            if conflict:
                key = (a, b, target)
                violations[key] = Violation(a, b, target)
    return sorted(
        violations.values(),
        key=lambda v: (str(v.concept_a), str(v.concept_b), str(v.ontology_concept)),
    )


def infer(graph: Graph) -> dict[str, int]:
    counters = defaultdict(int)

    while True:
        changed = False

        mappings = [m for m in collect_mappings(graph) if m.active]
        implements = collect_implements(graph)
        alignments = collect_alignment_pairs(graph)

        positive_standard = [
            (m.source, m.target)
            for m in mappings
            if m.kind == "standard" and m.positive
        ]
        negative_standard = [
            (m.source, m.target)
            for m in mappings
            if m.kind == "standard" and m.negative
        ]
        positive_model = [
            (m.source, m.target) for m in mappings if m.kind == "model" and m.positive
        ]

        # R1: symmetry of alignment and materialize Alignment instances for known pairs.
        for a, b in list(alignments):
            if ensure_alignment(graph, a, b):
                counters["R1"] += 1
                changed = True

        # R2: positive model mapping -> implemented standard concept.
        for model_concept, standard_concept in implements:
            for source, target in positive_model:
                if source == model_concept:
                    if ensure_mapping(
                        graph, "standard", standard_concept, target, DEMO.positive
                    ):
                        counters["R2"] += 1
                        changed = True

        # R3a: positive standard mapping -> implementing model concept.
        for model_concept, standard_concept in implements:
            for source, target in positive_standard:
                if source == standard_concept:
                    if ensure_mapping(
                        graph, "model", model_concept, target, DEMO.positive
                    ):
                        counters["R3a"] += 1
                        changed = True

        # R3b: same model concept implements two distinct standard concepts -> alignment.
        impl_by_model: dict[URIRef, set[URIRef]] = defaultdict(set)
        for model_concept, standard_concept in implements:
            impl_by_model[model_concept].add(standard_concept)
        for standards in impl_by_model.values():
            items = sorted(standards, key=str)
            for i in range(len(items)):
                for j in range(i + 1, len(items)):
                    if ensure_alignment(graph, items[i], items[j]):
                        counters["R3b"] += 1
                        changed = True

        # Refresh alignments after possible new ones.
        alignments = collect_alignment_pairs(graph)

        # R4: positive standard mapping across alignment.
        for a, b in alignments:
            for source, target in positive_standard:
                if source == a:
                    if ensure_mapping(graph, "standard", b, target, DEMO.positive):
                        counters["R4"] += 1
                        changed = True
                if source == b:
                    if ensure_mapping(graph, "standard", a, target, DEMO.positive):
                        counters["R4"] += 1
                        changed = True

        # R5: shared positive ontology mapping -> alignment.
        positive_by_target: dict[URIRef, set[URIRef]] = defaultdict(set)
        for source, target in positive_standard:
            positive_by_target[target].add(source)
        for concepts in positive_by_target.values():
            items = sorted(concepts, key=str)
            for i in range(len(items)):
                for j in range(i + 1, len(items)):
                    if ensure_alignment(graph, items[i], items[j]):
                        counters["R5"] += 1
                        changed = True

        # R6: negative standard mapping across alignment.
        alignments = collect_alignment_pairs(graph)
        for a, b in alignments:
            for source, target in negative_standard:
                if source == a:
                    if ensure_mapping(graph, "standard", b, target, DEMO.negative):
                        counters["R6"] += 1
                        changed = True
                if source == b:
                    if ensure_mapping(graph, "standard", a, target, DEMO.negative):
                        counters["R6"] += 1
                        changed = True

        if not changed:
            break

    return dict(counters)


def serialize(graph: Graph, path: Path) -> None:
    graph.bind("demo", DEMO)
    graph.bind("hriv", HRIV)
    graph.bind("hrim", HRIM)
    graph.bind("owl", OWL)
    graph.bind("rdf", RDF)
    graph.bind("rdfs", RDFS)
    graph.bind("xsd", XSD)
    data = graph.serialize(format="turtle")
    path.write_text(data, encoding="utf-8")


def main() -> int:
    args = parse_args()
    input_path = Path(args.input)
    default_output = input_path.with_name(f"{input_path.stem}_extended.ttl")
    output_path = Path(args.output) if args.output else default_output

    graph = Graph()
    graph.parse(input_path)

    counters = infer(graph)
    violations = detect_r7_violations(graph)

    serialize(graph, output_path)

    print(f"Updated graph written to: {output_path}")
    if counters:
        print("Inference summary:")
        for rule_id in ["R1", "R2", "R3a", "R3b", "R4", "R5", "R6"]:
            print(f"- {rule_id}: {counters.get(rule_id, 0)} new materialization(s)")
    else:
        print("Inference summary:\n- No new knowledge inferred.")

    if violations:
        print(f"R7 violations detected: {len(violations)}")
        for violation in violations:
            print(f"- {violation.render()}")
        if args.strict:
            return 2
    else:
        print("R7 violations detected: 0")

    return 0


if __name__ == "__main__":
    sys.exit(main())
