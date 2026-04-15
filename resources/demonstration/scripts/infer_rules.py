#!/usr/bin/env python3
"""Infer knowledge for the latest Health-RI demo model.

This version follows the latest uploaded metamodel and rule notes.
Compared with the previous script, the current model:
- uses generic RepresentationConcept -> OntologyConcept exact-meaning relations;
- represents exact-meaning qualifiers on a generic Mapping relation instance
  with attributes ``polarity`` and ``provenance``;
- uses horizontal relations directly between RepresentationConcept instances:
  ``aligns``, ``cannotAlign``, ``mayAlign``, and ``partiallyAligns``;
- uses an Alignment owned element only for ``aligns`` provenance;
- derives inconsistency on RepresentationConcept via ``isConsistent``.

Implemented rule notes from the latest XML:
- R1   ``aligns``, ``cannotAlign``, ``mayAlign``, and ``partiallyAligns`` are
       symmetric and irreflexive.
- R1a  ``aligns`` is transitively closed over distinct endpoints.
- R2   ``aligns`` from shared positive exact meanings.
- R3   ``cannotAlign`` from opposite-polarity exact meanings.
- R4a  ``mayAlignCandidate`` from shared negative exact meanings.
- R4b  ``mayAlign`` from ``mayAlignCandidate`` when not blocked.
- R5a  ``partiallyAlignsCandidate`` from positive exact meanings to related
       ontology concepts.
- R5b  ``partiallyAligns`` from ``partiallyAlignsCandidate`` when not blocked.
- R6   Exact-meaning propagation across an alignment, preserving polarity.
- R7   Inconsistency from multiple positive exact meanings to distinct ontology
       concepts.
- R8   Inconsistency from opposite-polarity exact meanings to the same
       ontology concept.

Implementation choices grounded in the current model notes:
- The reasoner targets only the latest instance pattern produced by the current
  instance generator. Exact meanings are read from reified ``demo:Mapping``
  instances only. Asserted alignments are read primarily from reified
  ``demo:Alignment`` instances, with optional seeding from bare ``demo:aligns``
  only when ``--trust-bare-aligns`` is explicitly enabled.
- Mapping and Alignment instances are read/written using the current schema
  predicates ``demo:hasMappingSource``, ``demo:hasTargetOntologyConcept``,
  ``demo:hasAlignmentSource``, ``demo:hasAlignmentTarget``,
  ``demo:hasPolarity``, and ``demo:hasProvenance``. The generic predicates
  ``demo:source`` and ``demo:target`` are also materialized for convenience,
  matching the current generator output.
- ``R5a`` requires ontology hierarchy triples. These can be supplied with one or
  more ``--ontology-input`` files and are used for reasoning only; they are not
  copied into the output file.
- Because ``R4b`` and ``R5b`` are stratified, final horizontal classifications
  are recomputed from the current exact-meaning closure before materialization.
- ``mayAlignCandidate`` and ``partiallyAlignsCandidate`` are auxiliary and are
  not materialized to the output graph.
- ``rdfs:subClassOf`` is evaluated transitively when checking ontology relatedness.
- The XML notes state that final horizontal classifications are de facto
  disjoint. This script therefore fails by default when more than one final
  horizontal relation holds for the same pair. Use
  ``--allow-horizontal-conflicts`` only when you intentionally want to inspect
  an invalid input state.
- ``isConsistent`` is fully normalized on every run for all discovered
  RepresentationConcept instances.
- To keep the script safely rerunnable, existing direct ``cannotAlign``,
  ``mayAlign``, and ``partiallyAligns`` triples are treated as materialized
  output by default and are recomputed from the current exact-meaning closure.
  Use ``--trust-horizontal-input`` only if you intentionally want to seed the
  reasoner with those direct horizontal facts.

The script rewrites direct horizontal relation triples so that stale
materialization from older runs is removed. Asserted Mapping and Alignment owned
elements are preserved; inferred owned elements are regenerated.
"""

from __future__ import annotations

import argparse
import hashlib
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from rdflib import Graph, Literal, Namespace, URIRef
from rdflib.namespace import OWL, RDF, RDFS, XSD

DEMO = Namespace("https://w3id.org/health-ri/semantic-interoperability/schema/")
DEMOI = Namespace("https://example.org/health-ri/demo-instance/")

HORIZONTAL_PREDS = {
    "aligns": DEMO.aligns,
    "cannotAlign": DEMO.cannotAlign,
    "mayAlign": DEMO.mayAlign,
    "partiallyAligns": DEMO.partiallyAligns,
}

MAPPING_SOURCE_PREDS = (
    DEMO.hasMappingSource,
    DEMO.source,
)
MAPPING_TARGET_PREDS = (
    DEMO.hasTargetOntologyConcept,
    DEMO.target,
)
ALIGNMENT_SOURCE_PREDS = (
    DEMO.hasAlignmentSource,
    DEMO.source,
)
ALIGNMENT_TARGET_PREDS = (
    DEMO.hasAlignmentTarget,
    DEMO.target,
)
POLARITY_PREDS = (DEMO.hasPolarity,)
PROVENANCE_PREDS = (DEMO.hasProvenance,)


@dataclass(frozen=True)
class MappingAssertion:
    source: URIRef
    target: URIRef
    polarity: URIRef
    provenance: URIRef
    origin: str  # node
    node: URIRef | None = None

    @property
    def key(self) -> tuple[URIRef, URIRef, URIRef]:
        return (self.source, self.target, self.polarity)

    @property
    def positive(self) -> bool:
        return self.polarity == DEMO.positive

    @property
    def negative(self) -> bool:
        return self.polarity == DEMO.negative

    @property
    def asserted(self) -> bool:
        return self.provenance != DEMO.inferred


@dataclass(frozen=True)
class AlignmentAssertion:
    pair: tuple[URIRef, URIRef]
    provenance: URIRef
    node: URIRef | None = None

    @property
    def asserted(self) -> bool:
        return self.provenance != DEMO.inferred


@dataclass(frozen=True)
class HorizontalConflict:
    pair: tuple[URIRef, URIRef]
    relations: tuple[str, ...]

    def render(self) -> str:
        left, right = self.pair
        rels = ", ".join(self.relations)
        return f"{left.n3()} / {right.n3()}: {rels}"


@dataclass(frozen=True)
class InferenceResult:
    mapping_keys: set[tuple[URIRef, URIRef, URIRef]]
    inferred_mapping_keys: set[tuple[URIRef, URIRef, URIRef]]
    aligns: set[tuple[URIRef, URIRef]]
    cannot_align: set[tuple[URIRef, URIRef]]
    may_align: set[tuple[URIRef, URIRef]]
    partially_aligns: set[tuple[URIRef, URIRef]]
    inferred_aligns_r2: set[tuple[URIRef, URIRef]]
    inferred_aligns_r1a: set[tuple[URIRef, URIRef]]
    inferred_cannot_align: set[tuple[URIRef, URIRef]]
    may_candidates: set[tuple[URIRef, URIRef]]
    inferred_may_align: set[tuple[URIRef, URIRef]]
    partial_candidates: set[tuple[URIRef, URIRef]]
    inferred_partially_aligns: set[tuple[URIRef, URIRef]]
    inconsistent_r7: set[URIRef]
    inconsistent_r8: set[URIRef]
    conflicts: list[HorizontalConflict]


@dataclass(frozen=True)
class CleanupSummary:
    removed_duplicate_mapping_nodes: int = 0
    removed_duplicate_alignment_nodes: int = 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Infer rule-based knowledge into instances.ttl"
    )
    parser.add_argument(
        "--input",
        default=None,
        help="Input Turtle file. Default: ../inputs/instances.ttl relative to this script.",
    )
    parser.add_argument(
        "--ontology-input",
        action="append",
        default=[],
        help=(
            "Additional ontology file used only for reasoning support "
            "(for example the HRIO ontology with rdfs:subClassOf triples). "
            "May be repeated. If omitted, the script will automatically use "
            "'health-ri-ontology.ttl' from the same folder as this script when available."
        ),
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Output Turtle file (default: <input>_extended.ttl)",
    )
    parser.add_argument(
        "--fail-on-horizontal-conflicts",
        action="store_true",
        help="Abort without writing output when more than one final horizontal classification holds for the same pair",
    )
    parser.add_argument(
        "--trust-horizontal-input",
        action="store_true",
        help=(
            "Treat existing direct cannotAlign/mayAlign/partiallyAligns triples as seed facts. "
            "Disabled by default to keep repeated runs safely rerunnable."
        ),
    )
    parser.add_argument(
        "--trust-bare-aligns",
        action="store_true",
        help=(
            "Treat direct aligns triples without an Alignment node as asserted seed facts. "
            "Disabled by default because the latest instance pattern uses Alignment nodes to carry provenance."
        ),
    )
    parser.add_argument(
        "--print-inconsistencies",
        action="store_true",
        help=(
            "Print detailed inconsistency information "
            "(R7 concepts, R8 concepts, and horizontal conflict pairs)."
        ),
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


def mapping_uri(source: URIRef, target: URIRef, polarity: URIRef) -> URIRef:
    pol = "neg" if polarity == DEMO.negative else "pos"
    return DEMOI[f"inf-map-{digest_token(str(source), str(target), pol)}"]


def alignment_uri(a: URIRef, b: URIRef) -> URIRef:
    left, right = ordered_pair(a, b)
    return DEMOI[f"inf-align-{digest_token(str(left), str(right))}"]


def first_uri(
    graph: Graph, subject: URIRef, predicates: Iterable[URIRef]
) -> URIRef | None:
    for predicate in predicates:
        value = next(graph.objects(subject, predicate), None)
        if isinstance(value, URIRef):
            return value
    return None


def remove_subject(graph: Graph, subject: URIRef) -> None:
    for triple in list(graph.triples((subject, None, None))):
        graph.remove(triple)
    for triple in list(graph.triples((None, None, subject))):
        graph.remove(triple)


def direct_pairs(graph: Graph, predicate: URIRef) -> set[tuple[URIRef, URIRef]]:
    pairs: set[tuple[URIRef, URIRef]] = set()
    for s, o in graph.subject_objects(predicate):
        if isinstance(s, URIRef) and isinstance(o, URIRef) and s != o:
            pairs.add(ordered_pair(s, o))
    return pairs


def preferred_mapping_assertion(assertions: list[MappingAssertion]) -> MappingAssertion:
    return max(
        assertions,
        key=lambda item: (
            1 if item.origin == "node" else 0,
            1 if item.asserted else 0,
            -len(str(item.node)) if item.node is not None else 0,
        ),
    )


def preferred_alignment_assertion(
    assertions: list[AlignmentAssertion],
) -> AlignmentAssertion:
    return max(
        assertions,
        key=lambda item: (
            1 if item.node is not None else 0,
            1 if item.asserted else 0,
            -len(str(item.node)) if item.node is not None else 0,
        ),
    )


def collect_mapping_assertions(
    graph: Graph,
) -> tuple[list[MappingAssertion], list[URIRef]]:
    assertions: list[MappingAssertion] = []

    for node in graph.subjects(RDF.type, DEMO.Mapping):
        if not isinstance(node, URIRef):
            continue
        source = first_uri(graph, node, MAPPING_SOURCE_PREDS)
        target = first_uri(graph, node, MAPPING_TARGET_PREDS)
        if not isinstance(source, URIRef) or not isinstance(target, URIRef):
            continue
        polarity = first_uri(graph, node, POLARITY_PREDS) or DEMO.positive
        provenance = first_uri(graph, node, PROVENANCE_PREDS) or DEMO.asserted
        assertion = MappingAssertion(
            source=source,
            target=target,
            polarity=polarity,
            provenance=provenance,
            origin="node",
            node=node,
        )
        assertions.append(assertion)

    grouped: dict[tuple[URIRef, URIRef, URIRef], list[MappingAssertion]] = defaultdict(
        list
    )
    for assertion in assertions:
        grouped[assertion.key].append(assertion)

    kept: list[MappingAssertion] = []
    duplicates_to_remove: list[URIRef] = []
    for group in grouped.values():
        winner = preferred_mapping_assertion(group)
        kept.append(winner)
        for assertion in group:
            if assertion.node is not None and assertion is not winner:
                duplicates_to_remove.append(assertion.node)
    return kept, duplicates_to_remove


def collect_alignment_assertions(
    graph: Graph, trust_bare_aligns: bool
) -> tuple[list[AlignmentAssertion], list[URIRef]]:
    assertions: list[AlignmentAssertion] = []

    for node in graph.subjects(RDF.type, DEMO.Alignment):
        if not isinstance(node, URIRef):
            continue
        source = first_uri(graph, node, ALIGNMENT_SOURCE_PREDS)
        target = first_uri(graph, node, ALIGNMENT_TARGET_PREDS)
        if (
            not isinstance(source, URIRef)
            or not isinstance(target, URIRef)
            or source == target
        ):
            continue
        provenance = first_uri(graph, node, PROVENANCE_PREDS) or DEMO.asserted
        assertions.append(
            AlignmentAssertion(ordered_pair(source, target), provenance, node)
        )

    if trust_bare_aligns:
        seen = {assertion.pair for assertion in assertions}
        for pair in direct_pairs(graph, DEMO.aligns):
            if pair in seen:
                continue
            assertions.append(AlignmentAssertion(pair, DEMO.asserted, None))

    grouped: dict[tuple[URIRef, URIRef], list[AlignmentAssertion]] = defaultdict(list)
    for assertion in assertions:
        grouped[assertion.pair].append(assertion)

    kept: list[AlignmentAssertion] = []
    duplicates_to_remove: list[URIRef] = []
    for group in grouped.values():
        winner = preferred_alignment_assertion(group)
        kept.append(winner)
        for assertion in group:
            if assertion.node is not None and assertion is not winner:
                duplicates_to_remove.append(assertion.node)
    return kept, duplicates_to_remove


def load_hierarchy_graph(instance_graph: Graph, ontology_inputs: list[str]) -> Graph:
    """Build a support graph used only for hierarchy lookups during reasoning."""
    hierarchy_graph = Graph()
    for triple in instance_graph:
        hierarchy_graph.add(triple)

    for path_str in ontology_inputs:
        ontology_path = Path(path_str)
        hierarchy_graph.parse(ontology_path)

    return hierarchy_graph


def transitive_superclasses(graph: Graph, concept: URIRef) -> set[URIRef]:
    out: set[URIRef] = set()
    agenda = [concept]
    seen = {concept}
    while agenda:
        current = agenda.pop()
        for parent in graph.objects(current, RDFS.subClassOf):
            if isinstance(parent, URIRef) and parent not in seen:
                seen.add(parent)
                out.add(parent)
                agenda.append(parent)
    return out


def ontology_related(graph: Graph, left: URIRef, right: URIRef) -> bool:
    if left == right:
        return False
    return right in transitive_superclasses(
        graph, left
    ) or left in transitive_superclasses(graph, right)


def clique_closure(edges: set[tuple[URIRef, URIRef]]) -> set[tuple[URIRef, URIRef]]:
    adjacency: dict[URIRef, set[URIRef]] = defaultdict(set)
    nodes: set[URIRef] = set()
    for left, right in edges:
        nodes.add(left)
        nodes.add(right)
        adjacency[left].add(right)
        adjacency[right].add(left)

    visited: set[URIRef] = set()
    closure: set[tuple[URIRef, URIRef]] = set()
    for node in sorted(nodes, key=str):
        if node in visited:
            continue
        component: list[URIRef] = []
        stack = [node]
        visited.add(node)
        while stack:
            current = stack.pop()
            component.append(current)
            for neighbor in adjacency[current]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    stack.append(neighbor)
        items = sorted(component, key=str)
        for i in range(len(items)):
            for j in range(i + 1, len(items)):
                closure.add((items[i], items[j]))
    return closure


def detect_horizontal_conflicts(
    aligns_total: set[tuple[URIRef, URIRef]],
    cannot_total: set[tuple[URIRef, URIRef]],
    may_total: set[tuple[URIRef, URIRef]],
    partial_total: set[tuple[URIRef, URIRef]],
) -> list[HorizontalConflict]:
    by_pair: dict[tuple[URIRef, URIRef], set[str]] = defaultdict(set)
    for pair in aligns_total:
        by_pair[pair].add("aligns")
    for pair in cannot_total:
        by_pair[pair].add("cannotAlign")
    for pair in may_total:
        by_pair[pair].add("mayAlign")
    for pair in partial_total:
        by_pair[pair].add("partiallyAligns")

    conflicts: list[HorizontalConflict] = []
    for pair, relations in by_pair.items():
        if len(relations) > 1:
            conflicts.append(HorizontalConflict(pair, tuple(sorted(relations))))
    return sorted(
        conflicts,
        key=lambda item: (str(item.pair[0]), str(item.pair[1]), item.relations),
    )


def derive_relations(
    hierarchy_graph: Graph,
    mapping_keys: set[tuple[URIRef, URIRef, URIRef]],
    asserted_aligns: set[tuple[URIRef, URIRef]],
    seed_cannot: set[tuple[URIRef, URIRef]],
    seed_may: set[tuple[URIRef, URIRef]],
    seed_partial: set[tuple[URIRef, URIRef]],
) -> dict[str, object]:
    positives = {
        (source, target)
        for source, target, polarity in mapping_keys
        if polarity == DEMO.positive
    }
    negatives = {
        (source, target)
        for source, target, polarity in mapping_keys
        if polarity == DEMO.negative
    }

    positive_by_target: dict[URIRef, set[URIRef]] = defaultdict(set)
    negative_by_target: dict[URIRef, set[URIRef]] = defaultdict(set)
    for source, target in positives:
        positive_by_target[target].add(source)
    for source, target in negatives:
        negative_by_target[target].add(source)

    r2_edges: set[tuple[URIRef, URIRef]] = set()
    for concepts in positive_by_target.values():
        items = sorted(concepts, key=str)
        for i in range(len(items)):
            for j in range(i + 1, len(items)):
                r2_edges.add((items[i], items[j]))

    base_align_edges = asserted_aligns | r2_edges
    aligns_total = clique_closure(base_align_edges)
    r1a_edges = aligns_total - base_align_edges

    r3_edges: set[tuple[URIRef, URIRef]] = set()
    all_targets = set(positive_by_target) | set(negative_by_target)
    for target in all_targets:
        pos_items = positive_by_target.get(target, set())
        neg_items = negative_by_target.get(target, set())
        for left in pos_items:
            for right in neg_items:
                if left != right:
                    r3_edges.add(ordered_pair(left, right))
    cannot_total = seed_cannot | r3_edges

    r5a_candidates: set[tuple[URIRef, URIRef]] = set()
    positive_items = sorted(positives, key=lambda item: (str(item[0]), str(item[1])))
    for i in range(len(positive_items)):
        c1, o1 = positive_items[i]
        for j in range(i + 1, len(positive_items)):
            c2, o2 = positive_items[j]
            if c1 == c2 or o1 == o2:
                continue
            if ontology_related(hierarchy_graph, o1, o2):
                r5a_candidates.add(ordered_pair(c1, c2))

    inferred_partial = {
        pair
        for pair in r5a_candidates
        if pair not in aligns_total
        and pair not in cannot_total
        and pair not in seed_partial
    }
    partial_total = seed_partial | inferred_partial

    r4a_candidates: set[tuple[URIRef, URIRef]] = set()
    for concepts in negative_by_target.values():
        items = sorted(concepts, key=str)
        for i in range(len(items)):
            for j in range(i + 1, len(items)):
                r4a_candidates.add((items[i], items[j]))

    inferred_may = {
        pair
        for pair in r4a_candidates
        if pair not in aligns_total
        and pair not in cannot_total
        and pair not in partial_total
        and pair not in seed_may
    }
    may_total = seed_may | inferred_may

    inconsistent_r7: set[URIRef] = set()
    positive_targets_by_concept: dict[URIRef, set[URIRef]] = defaultdict(set)
    negative_targets_by_concept: dict[URIRef, set[URIRef]] = defaultdict(set)
    for source, target in positives:
        positive_targets_by_concept[source].add(target)
    for source, target in negatives:
        negative_targets_by_concept[source].add(target)

    for concept, targets in positive_targets_by_concept.items():
        if len(targets) > 1:
            inconsistent_r7.add(concept)

    inconsistent_r8: set[URIRef] = set()
    for concept in set(positive_targets_by_concept) | set(negative_targets_by_concept):
        if positive_targets_by_concept.get(
            concept, set()
        ) & negative_targets_by_concept.get(concept, set()):
            inconsistent_r8.add(concept)

    conflicts = detect_horizontal_conflicts(
        aligns_total, cannot_total, may_total, partial_total
    )

    return {
        "r2_edges": r2_edges,
        "r1a_edges": r1a_edges,
        "aligns_total": aligns_total,
        "r3_edges": r3_edges,
        "cannot_total": cannot_total,
        "r5a_candidates": r5a_candidates,
        "inferred_partial": inferred_partial,
        "partial_total": partial_total,
        "r4a_candidates": r4a_candidates,
        "inferred_may": inferred_may,
        "may_total": may_total,
        "inconsistent_r7": inconsistent_r7,
        "inconsistent_r8": inconsistent_r8,
        "conflicts": conflicts,
    }


def infer(
    instance_graph: Graph,
    hierarchy_graph: Graph,
    trust_horizontal_input: bool,
    trust_bare_aligns: bool,
) -> tuple[
    InferenceResult,
    Counter,
    list[MappingAssertion],
    list[AlignmentAssertion],
    CleanupSummary,
]:
    mapping_assertions, duplicate_mapping_nodes = collect_mapping_assertions(
        instance_graph
    )
    alignment_assertions, duplicate_alignment_nodes = collect_alignment_assertions(
        instance_graph, trust_bare_aligns=trust_bare_aligns
    )

    cleanup = CleanupSummary(
        removed_duplicate_mapping_nodes=len(duplicate_mapping_nodes),
        removed_duplicate_alignment_nodes=len(duplicate_alignment_nodes),
    )

    asserted_mapping_keys = {item.key for item in mapping_assertions if item.asserted}
    asserted_alignment_pairs = {
        item.pair for item in alignment_assertions if item.asserted
    }
    if trust_horizontal_input:
        seed_cannot = direct_pairs(instance_graph, DEMO.cannotAlign)
        seed_may = direct_pairs(instance_graph, DEMO.mayAlign)
        seed_partial = direct_pairs(instance_graph, DEMO.partiallyAligns)
    else:
        seed_cannot = set()
        seed_may = set()
        seed_partial = set()

    mapping_keys = set(asserted_mapping_keys)
    while True:
        derived = derive_relations(
            hierarchy_graph,
            mapping_keys,
            asserted_alignment_pairs,
            seed_cannot,
            seed_may,
            seed_partial,
        )

        aligns_total = derived["aligns_total"]
        new_keys: set[tuple[URIRef, URIRef, URIRef]] = set()
        existing_by_source: dict[URIRef, list[tuple[URIRef, URIRef]]] = defaultdict(
            list
        )
        for source, target, polarity in mapping_keys:
            existing_by_source[source].append((target, polarity))

        for left, right in aligns_total:
            for target, polarity in existing_by_source.get(left, []):
                key = (right, target, polarity)
                if key not in mapping_keys:
                    new_keys.add(key)
            for target, polarity in existing_by_source.get(right, []):
                key = (left, target, polarity)
                if key not in mapping_keys:
                    new_keys.add(key)

        if not new_keys:
            break
        mapping_keys |= new_keys

    final = derive_relations(
        hierarchy_graph,
        mapping_keys,
        asserted_alignment_pairs,
        seed_cannot,
        seed_may,
        seed_partial,
    )

    inferred_mapping_keys = mapping_keys - asserted_mapping_keys
    result = InferenceResult(
        mapping_keys=mapping_keys,
        inferred_mapping_keys=inferred_mapping_keys,
        aligns=final["aligns_total"],
        cannot_align=final["cannot_total"],
        may_align=final["may_total"],
        partially_aligns=final["partial_total"],
        inferred_aligns_r2=final["r2_edges"] - asserted_alignment_pairs,
        inferred_aligns_r1a=final["r1a_edges"],
        inferred_cannot_align=final["r3_edges"] - seed_cannot,
        may_candidates=final["r4a_candidates"],
        inferred_may_align=final["inferred_may"],
        partial_candidates=final["r5a_candidates"],
        inferred_partially_aligns=final["inferred_partial"],
        inconsistent_r7=final["inconsistent_r7"],
        inconsistent_r8=final["inconsistent_r8"],
        conflicts=final["conflicts"],
    )

    counters = Counter()
    counters["R2"] = len(result.inferred_aligns_r2)
    counters["R1a"] = len(result.inferred_aligns_r1a)
    counters["R3"] = len(result.inferred_cannot_align)
    counters["R4a"] = len(result.may_candidates)
    counters["R4b"] = len(result.inferred_may_align)
    counters["R5a"] = len(result.partial_candidates)
    counters["R5b"] = len(result.inferred_partially_aligns)
    counters["R6"] = len(result.inferred_mapping_keys)
    counters["R7"] = len(result.inconsistent_r7)
    counters["R8"] = len(result.inconsistent_r8)
    counters["conflicts"] = len(result.conflicts)
    counters["removed_duplicate_mapping_nodes"] = (
        cleanup.removed_duplicate_mapping_nodes
    )
    counters["removed_duplicate_alignment_nodes"] = (
        cleanup.removed_duplicate_alignment_nodes
    )
    return result, counters, mapping_assertions, alignment_assertions, cleanup


def rewrite_direct_horizontal(
    graph: Graph, predicate: URIRef, pairs: set[tuple[URIRef, URIRef]]
) -> int:
    initial = {
        (s, o)
        for s, o in graph.subject_objects(predicate)
        if isinstance(s, URIRef) and isinstance(o, URIRef)
    }
    for triple in list(graph.triples((None, predicate, None))):
        graph.remove(triple)
    added = 0
    for left, right in pairs:
        if (left, predicate, right) not in initial:
            added += 1
        if (right, predicate, left) not in initial:
            added += 1
        graph.add((left, predicate, right))
        graph.add((right, predicate, left))
    return added


def remove_duplicate_nodes(graph: Graph, nodes: Iterable[URIRef]) -> int:
    count = 0
    for node in nodes:
        if (node, None, None) in graph or (None, None, node) in graph:
            remove_subject(graph, node)
            count += 1
    return count


def rewrite_inferred_mapping_nodes(
    graph: Graph,
    mapping_assertions: list[MappingAssertion],
    inferred_mapping_keys: set[tuple[URIRef, URIRef, URIRef]],
) -> None:
    for assertion in mapping_assertions:
        if assertion.node is not None and not assertion.asserted:
            remove_subject(graph, assertion.node)

    for source, target, polarity in sorted(
        inferred_mapping_keys,
        key=lambda item: (str(item[0]), str(item[1]), str(item[2])),
    ):
        node = mapping_uri(source, target, polarity)
        graph.add((node, RDF.type, DEMO.Mapping))
        graph.add((node, DEMO.source, source))
        graph.add((node, DEMO.hasMappingSource, source))
        graph.add((node, DEMO.target, target))
        graph.add((node, DEMO.hasTargetOntologyConcept, target))
        graph.add((node, DEMO.hasPolarity, polarity))
        graph.add((node, DEMO.hasProvenance, DEMO.inferred))


def rewrite_inferred_alignment_nodes(
    graph: Graph,
    alignment_assertions: list[AlignmentAssertion],
    aligns_total: set[tuple[URIRef, URIRef]],
) -> None:
    asserted_pairs = {item.pair for item in alignment_assertions if item.asserted}
    for assertion in alignment_assertions:
        if assertion.node is not None and not assertion.asserted:
            remove_subject(graph, assertion.node)

    inferred_pairs = aligns_total - asserted_pairs
    for left, right in sorted(
        inferred_pairs, key=lambda item: (str(item[0]), str(item[1]))
    ):
        node = alignment_uri(left, right)
        graph.add((node, RDF.type, DEMO.Alignment))
        graph.add((node, DEMO.source, left))
        graph.add((node, DEMO.hasAlignmentSource, left))
        graph.add((node, DEMO.target, right))
        graph.add((node, DEMO.hasAlignmentTarget, right))
        graph.add((node, DEMO.hasProvenance, DEMO.inferred))


def collect_representation_concepts(
    graph: Graph,
    mapping_assertions: list[MappingAssertion],
    alignment_assertions: list[AlignmentAssertion],
) -> set[URIRef]:
    concepts: set[URIRef] = set()
    for concept in graph.subjects(RDF.type, DEMO.RepresentationConcept):
        if isinstance(concept, URIRef):
            concepts.add(concept)
    for assertion in mapping_assertions:
        concepts.add(assertion.source)
    for assertion in alignment_assertions:
        concepts.add(assertion.pair[0])
        concepts.add(assertion.pair[1])
    for predicate in HORIZONTAL_PREDS.values():
        for left, right in direct_pairs(graph, predicate):
            concepts.add(left)
            concepts.add(right)
    for concept, _value in graph.subject_objects(DEMO.isConsistent):
        if isinstance(concept, URIRef):
            concepts.add(concept)
    return concepts


def normalize_consistency(
    graph: Graph, concepts: set[URIRef], inconsistent_concepts: set[URIRef]
) -> int:
    changed = 0
    final_values = {
        concept: Literal(concept not in inconsistent_concepts, datatype=XSD.boolean)
        for concept in concepts
    }
    for concept in concepts:
        existing = list(graph.objects(concept, DEMO.isConsistent))
        wanted = final_values[concept]
        if len(existing) != 1 or existing[0] != wanted:
            changed += 1
        for obj in existing:
            graph.remove((concept, DEMO.isConsistent, obj))
        graph.add((concept, DEMO.isConsistent, wanted))
    return changed


def serialize(graph: Graph, path: Path) -> None:
    graph.bind("demo", DEMO)
    graph.bind("demoi", DEMOI)
    graph.bind("owl", OWL)
    graph.bind("rdf", RDF)
    graph.bind("rdfs", RDFS)
    graph.bind("xsd", XSD)
    data = graph.serialize(format="turtle")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(data, encoding="utf-8")


def print_inconsistencies(result: InferenceResult) -> None:
    if result.inconsistent_r7:
        print(f"R7 inconsistent concepts: {len(result.inconsistent_r7)}")
        for concept in sorted(result.inconsistent_r7, key=str):
            print(f"- R7: {concept.n3()}")
    else:
        print("R7 inconsistent concepts: 0")

    if result.inconsistent_r8:
        print(f"R8 inconsistent concepts: {len(result.inconsistent_r8)}")
        for concept in sorted(result.inconsistent_r8, key=str):
            print(f"- R8: {concept.n3()}")
    else:
        print("R8 inconsistent concepts: 0")

    if result.conflicts:
        print(f"Horizontal classification conflicts: {len(result.conflicts)}")
        for conflict in result.conflicts:
            print(f"- {conflict.render()}")
    else:
        print("Horizontal classification conflicts: 0")


def main() -> int:
    args = parse_args()

    script_dir = Path(__file__).resolve().parent
    input_dir = script_dir.parent / "inputs"

    input_path = (
        Path(args.input).expanduser().resolve()
        if args.input
        else (input_dir / "instances.ttl").resolve()
    )
    default_output = input_path.with_name(f"{input_path.stem}_extended.ttl")
    output_path = (
        Path(args.output).expanduser().resolve() if args.output else default_output
    )

    ontology_inputs = [
        str(Path(path).expanduser().resolve()) for path in args.ontology_input
    ]
    if not ontology_inputs:
        default_ontology_path = (input_dir / "health-ri-ontology.ttl").resolve()
        if default_ontology_path.is_file():
            ontology_inputs.append(str(default_ontology_path))

    instance_graph = Graph()
    instance_graph.parse(input_path)

    hierarchy_graph = load_hierarchy_graph(instance_graph, ontology_inputs)

    result, counters, mapping_assertions, alignment_assertions, _cleanup = infer(
        instance_graph,
        hierarchy_graph,
        trust_horizontal_input=args.trust_horizontal_input,
        trust_bare_aligns=args.trust_bare_aligns,
    )

    if result.conflicts:
        if args.fail_on_horizontal_conflicts:
            print(
                f"Final classification conflicts detected: {len(result.conflicts)}",
                file=sys.stderr,
            )
            if args.print_inconsistencies:
                for conflict in result.conflicts:
                    print(f"- {conflict.render()}", file=sys.stderr)
            print(
                "Refusing to write an invalid final classification state.",
                file=sys.stderr,
            )
            return 2

    # Refresh collections after inference for cleanup/rematerialization.
    _mapping_assertions2, duplicate_mapping_nodes = collect_mapping_assertions(
        instance_graph
    )
    _alignment_assertions2, duplicate_alignment_nodes = collect_alignment_assertions(
        instance_graph,
        trust_bare_aligns=True,
    )
    counters["removed_duplicate_mapping_nodes"] = remove_duplicate_nodes(
        instance_graph, duplicate_mapping_nodes
    )
    counters["removed_duplicate_alignment_nodes"] = remove_duplicate_nodes(
        instance_graph, duplicate_alignment_nodes
    )

    counters["R1"] = 0
    counters["R1"] += rewrite_direct_horizontal(
        instance_graph, DEMO.aligns, result.aligns
    )
    counters["R1"] += rewrite_direct_horizontal(
        instance_graph, DEMO.cannotAlign, result.cannot_align
    )
    counters["R1"] += rewrite_direct_horizontal(
        instance_graph, DEMO.mayAlign, result.may_align
    )
    counters["R1"] += rewrite_direct_horizontal(
        instance_graph, DEMO.partiallyAligns, result.partially_aligns
    )
    rewrite_inferred_mapping_nodes(
        instance_graph, mapping_assertions, result.inferred_mapping_keys
    )
    rewrite_inferred_alignment_nodes(
        instance_graph, alignment_assertions, result.aligns
    )

    representation_concepts = collect_representation_concepts(
        instance_graph,
        mapping_assertions,
        alignment_assertions,
    )
    counters["consistency_updates"] = normalize_consistency(
        instance_graph,
        representation_concepts,
        result.inconsistent_r7 | result.inconsistent_r8,
    )

    serialize(instance_graph, output_path)

    print(f"Updated graph written to: {output_path}")
    if ontology_inputs:
        print(f"Ontology support files loaded: {len(ontology_inputs)}")
        for ontology_path in ontology_inputs:
            print(f"- {ontology_path}")
    else:
        print("Ontology support files loaded: 0")
    print("Inference summary:")
    for rule_id in [
        "R1",
        "R1a",
        "R2",
        "R3",
        "R4a",
        "R4b",
        "R5a",
        "R5b",
        "R6",
        "R7",
        "R8",
    ]:
        print(f"- {rule_id}: {counters.get(rule_id, 0)}")
    print(f"- consistency normalizations: {counters.get('consistency_updates', 0)}")
    print(
        f"- duplicate Mapping nodes removed: {counters.get('removed_duplicate_mapping_nodes', 0)}"
    )
    print(
        f"- duplicate Alignment nodes removed: {counters.get('removed_duplicate_alignment_nodes', 0)}"
    )

    print(f"Final classification conflicts detected: {len(result.conflicts)}")

    if args.print_inconsistencies:
        print_inconsistencies(result)

    return 0


if __name__ == "__main__":
    sys.exit(main())
