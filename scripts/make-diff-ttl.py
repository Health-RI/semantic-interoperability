"""
rdf_diff_graph.py (logging + pruning + diff modes)

Creates RDF *diff graphs* between two RDF/OWL files:
- additions = NEW minus OLD
- removals  = OLD minus NEW
- unchanged = intersection (optional)

Normalizations (fast + deterministic):
  1) Canonicalize RDF list order for OWL list-bearing props
     (unionOf, intersectionOf, oneOf, members, disjointUnionOf, propertyChainAxiom, hasKey).
  2) Determinize list-head bnodes by hashing the (sorted) member set and rewire all pointers to a single canonical head.
  3) (NEW) Optionally prune *orphaned* list chains left behind after rewiring (on by default).
  4) Force `owl:equivalentClass` orientation to <URI> eq _:bnode (never the reverse). Fallback to lexicographic when both sides same kind.
  5) (Optional) Canonicalize other symmetric edges (sameAs, equivalentProperty, disjointWith) to (min, max) N3 order.

Diff modes:
  - isomorphic (default): rdflib.compare.graph_diff on isomorphic-wrapped graphs (semantically robust).
  - simple: canonicalize bnodes with `to_isomorphic()` and compute an N-Triples set-diff (fast; typically equivalent after the normalizations).

CLI examples:
  python rdf_diff_graph.py old.ttl new.ttl --out-prefix diff --log-level INFO
  python rdf_diff_graph.py old.ttl new.ttl --diff-mode simple --log-level INFO
  python rdf_diff_graph.py old.ttl new.ttl --no-list-canon --log-level DEBUG

Exit codes: 0 ok, 2 error.
"""

import argparse
import sys
import hashlib
import logging
import time
from pathlib import Path
from typing import Set

from rdflib import Graph, RDF, OWL, BNode, URIRef
from rdflib.compare import to_isomorphic, graph_diff
from rdflib.collection import Collection
from rdflib.term import Node

# ---- Config ----

LIST_PROPS = {
    OWL.unionOf,
    OWL.intersectionOf,
    OWL.members,
    OWL.disjointUnionOf,
    OWL.propertyChainAxiom,
    OWL.hasKey,
    OWL.oneOf,
}

# IMPORTANT: exclude OWL.equivalentClass (handled by a dedicated rule)
SYMM_PROPS = {
    OWL.equivalentProperty,
    OWL.sameAs,
    OWL.disjointWith,
}

log = logging.getLogger("rdf-diff")

# ---- Utils ----


def ext_for(fmt: str) -> str:
    return {
        "turtle": "ttl",
        "nt": "nt",
        "xml": "rdf",
        "json-ld": "jsonld",
        "trig": "trig",
        "n3": "n3",
    }.get(fmt, fmt)


def write_graph(g: Graph, out_path: Path, fmt: str) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    data = g.serialize(format=fmt)
    if isinstance(data, (bytes, bytearray)):
        out_path.write_bytes(data)
    else:
        out_path.write_text(data, encoding="utf-8")


def _n3_key(g: Graph, term: Node) -> str:
    try:
        return term.n3(g.namespace_manager)
    except Exception:
        return repr(term)


def _tsec(start: float) -> str:
    return f"{(time.perf_counter() - start):.3f}s"


def _as_text(data) -> str:
    """Return a UTF-8 str regardless of whether rdflib gave us bytes or str."""
    return data.decode("utf-8") if isinstance(data, (bytes, bytearray)) else str(data)


# ---- List canonicalization ----


def _sorted_list_items(g: Graph, head: Node):
    """Return list items (as Nodes) sorted by N3; [] on malformed/empty list."""
    try:
        items = list(Collection(g, head))
    except Exception:
        return []
    if not items:
        return []
    return sorted(items, key=lambda t: _n3_key(g, t))


def canonicalize_rdf_list(g: Graph, head: Node) -> int:
    """
    Rebuild an RDF list at 'head' with items sorted; returns rewritten count.
    """
    items_sorted = _sorted_list_items(g, head)
    if not items_sorted:
        return 0
    try:
        current = list(Collection(g, head))
    except Exception:
        return 0
    if current == items_sorted:
        return 0
    Collection(g, head).clear()
    col = Collection(g, head)
    for it in items_sorted:
        col.append(it)
    return len(items_sorted)


def canonicalize_all_lists(g: Graph, log_every: int = 0) -> (int, Set[Node]):
    """
    Canonicalize ALL RDF lists referenced by LIST_PROPS; touches each head once.
    Returns (rewritten_count, set_of_heads).
    """
    heads = set()
    for p in LIST_PROPS:
        for _, _, lst in g.triples((None, p, None)):
            heads.add(lst)
    heads = list(heads)
    log.info(f"[lists] Found {len(heads)} list heads across {len(LIST_PROPS)} properties")
    rewritten = 0
    for i, head in enumerate(heads, 1):
        rewritten += canonicalize_rdf_list(g, head)
        if log_every and (i % log_every == 0):
            log.debug(f"[lists] processed {i}/{len(heads)} heads (rewrites so far: {rewritten})")
    log.info(f"[lists] Canonicalized {rewritten} list items across {len(heads)} heads")
    return rewritten, set(heads)


# ---- Deterministic list-head IDs & pruning ----


def _list_hash(g: Graph, head: Node) -> str:
    """
    Stable sha1 over sorted N3 of members; '' if not a proper non-empty list.
    """
    items = _sorted_list_items(g, head)
    if not items:
        return ""
    return hashlib.sha1("|".join(_n3_key(g, t) for t in items).encode("utf-8")).hexdigest()


def determinize_list_heads(g: Graph, heads: Set[Node], log_every: int = 0):
    """
    Assign a stable BNode id to every OWL list-head based on member-set hash.
    Rewire (s,p) pointers to a single canonical head per unique member set.
    Returns (rewired_count, mapping_original_head_to_canonical).
    """
    # Collect (s,p,head) for *provided* heads only
    prop_heads = []
    for p in LIST_PROPS:
        for s, _, head in g.triples((None, p, None)):
            if head in heads:
                prop_heads.append((s, p, head))

    unique_heads = set(heads)
    log.info(f"[heads] {len(unique_heads)} unique list heads; {len(prop_heads)} property references")

    canonical_by_hash = {}  # hash -> canonical BNode
    head2canon = {}  # original head -> canonical BNode

    # Build canonical heads once per unique hash
    for head in unique_heads:
        h = _list_hash(g, head)
        if not h:
            continue
        if h not in canonical_by_hash:
            canon = BNode(f"L_{h}")
            canonical_by_hash[h] = canon
            # Materialize canonical list if missing
            if (canon, RDF.first, None) not in g and (canon, RDF.rest, None) not in g:
                col = Collection(g, canon)
                for it in _sorted_list_items(g, head):
                    col.append(it)
        head2canon[head] = canonical_by_hash.get(h)

    rewired = 0
    for i, (s, p, head) in enumerate(prop_heads, 1):
        canon = head2canon.get(head)
        if not canon or head == canon:
            continue
        if (s, p, canon) not in g:
            g.add((s, p, canon))
        g.remove((s, p, head))
        rewired += 1
        if log_every and (i % log_every == 0):
            log.debug(f"[heads] rewired {i}/{len(prop_heads)} refs (rewired so far: {rewired})")

    log.info(f"[heads] Rewired {rewired} refs to canonical heads; {len(canonical_by_hash)} unique member sets")
    return rewired, head2canon


def _collect_list_chain_nodes(g: Graph, head: Node) -> Set[Node]:
    """Traverse rdf:first/rest from head and collect chain nodes (guard against cycles)."""
    visited = set()
    stack = [head]
    while stack:
        node = stack.pop()
        if node in visited:
            continue
        visited.add(node)
        # Follow rest
        for _, _, nxt in g.triples((node, RDF.rest, None)):
            if isinstance(nxt, (BNode, URIRef)):  # list cells are usually bnodes
                stack.append(nxt)
    return visited


def prune_orphan_lists(g: Graph, original_heads: Set[Node], head2canon: dict, log_every: int = 0) -> int:
    """
    Remove rdf:first/rest triples that belong to original list chains whose heads
    were rewired to canonical heads (and are no longer referenced as a list head).
    We only remove the list-structure triples; if a node has other uses it stays.
    Returns number of triples removed.
    """
    removed = 0
    # Heads that were replaced (orig != canon)
    replaced_heads = [h for h, c in head2canon.items() if c and h != c and h in original_heads]
    if not replaced_heads:
        log.info("[prune] Nothing to prune (no replaced list heads)")
        return 0

    # Identify list heads still referenced by some (s, LIST_PROP, head)
    still_refd = set()
    for p in LIST_PROPS:
        for _, _, head in g.triples((None, p, None)):
            still_refd.add(head)

    # For each replaced head no longer referenced, remove its chain triples
    todo = [h for h in replaced_heads if h not in still_refd]
    log.info(
        f"[prune] Candidate orphan list heads: {len(todo)} (replaced={len(replaced_heads)}, still_refd={len(still_refd)})"
    )

    for i, head in enumerate(todo, 1):
        chain_nodes = _collect_list_chain_nodes(g, head)
        for n in chain_nodes:
            # Remove only list-structure triples; keep other facts intact
            for t in list(g.triples((n, RDF.first, None))):
                g.remove(t)
                removed += 1
            for t in list(g.triples((n, RDF.rest, None))):
                g.remove(t)
                removed += 1
        if log_every and (i % log_every == 0):
            log.debug(f"[prune] processed {i}/{len(todo)} orphan heads (removed so far: {removed})")

    log.info(f"[prune] Removed {removed} rdf:first/rest triples from orphan list chains")
    return removed


# ---- Equivalence & symmetric edges ----


def canonicalize_equivalentClass_orientation(g: Graph, log_every: int = 0) -> int:
    """
    Enforce <URI> owl:equivalentClass _:bnode when one side is URI and other is BNode.
    When both sides are same kind (both URIs or both BNodes), use N3 order.
    """
    p = OWL.equivalentClass
    pairs = list(g.subject_objects(p))
    log.info(f"[eqClass] Found {len(pairs)} owl:equivalentClass pairs")
    rewritten = 0
    for i, (s, o) in enumerate(pairs, 1):
        if isinstance(s, BNode) and isinstance(o, URIRef):
            if (o, p, s) not in g:
                g.add((o, p, s))
            g.remove((s, p, o))
            rewritten += 1
        elif isinstance(s, URIRef) and isinstance(o, BNode):
            pass  # already canonical
        else:
            left, right = _n3_key(g, s), _n3_key(g, o)
            if left > right:
                if (o, p, s) not in g:
                    g.add((o, p, s))
                g.remove((s, p, o))
                rewritten += 1
        if log_every and (i % log_every == 0):
            log.debug(f"[eqClass] processed {i}/{len(pairs)} (rewrites so far: {rewritten})")
    log.info(f"[eqClass] Rewrote {rewritten} triples")
    return rewritten


def canonicalize_symmetric_edges(g: Graph, log_every: int = 0) -> int:
    """
    Canonicalize symmetric properties (excluding equivalentClass) to (min, max) N3 order.
    """
    rewritten_total = 0
    for p in SYMM_PROPS:
        pairs = list(g.subject_objects(p))
        log.info(f"[symmetric] {p.n3()} pairs: {len(pairs)}")
        rewritten = 0
        for i, (s, o) in enumerate(pairs, 1):
            left, right = _n3_key(g, s), _n3_key(g, o)
            if left > right:
                if (o, p, s) not in g:
                    g.add((o, p, s))
                g.remove((s, p, o))
                rewritten += 1
            if log_every and (i % log_every == 0):
                log.debug(f"[symmetric] {p.n3()} processed {i}/{len(pairs)} (rewrites so far: {rewritten})")
        log.info(f"[symmetric] {p.n3()} rewrote {rewritten}")
        rewritten_total += rewritten
    return rewritten_total


# ---- Orchestration ----


def normalize_for_diff(g: Graph, list_canon: bool, symm_canon: bool, prune_lists: bool, log_every: int = 0) -> None:
    """
    Apply normalizations in the right order (each list head touched once).
    """
    t0 = time.perf_counter()
    before = len(g)
    log.info(f"[normalize] starting; triples={before}")

    heads = set()
    if list_canon:
        t = time.perf_counter()
        _, heads = canonicalize_all_lists(g, log_every=log_every)  # 1
        log.info(f"[normalize] list-order canonicalization done in {_tsec(t)}")
        t = time.perf_counter()
        _, head2canon = determinize_list_heads(g, heads, log_every=log_every)  # 2
        log.info(f"[normalize] deterministic head ids done in {_tsec(t)}")
        if prune_lists:
            t = time.perf_counter()
            prune_orphan_lists(g, heads, head2canon, log_every=log_every)  # 3
            log.info(f"[normalize] orphan list pruning done in {_tsec(t)}")

    t = time.perf_counter()
    canonicalize_equivalentClass_orientation(g, log_every=log_every)  # 4
    log.info(f"[normalize] eqClass orientation done in {_tsec(t)}")

    if symm_canon:
        t = time.perf_counter()
        canonicalize_symmetric_edges(g, log_every=log_every)  # 5
        log.info(f"[normalize] symmetric canon done in {_tsec(t)}")

    after = len(g)
    log.info(f"[normalize] finished in {_tsec(t0)}; triples now {after} (Δ {after - before})")


# ---- Simple diff ----


def simple_set_diff(old_g: Graph, new_g: Graph):
    """
    Fast & correct: canonicalize bnodes with to_isomorphic(), then NT set-diff.
    Build output graphs by parsing each NT buffer once (no per-line parsing).
    """
    iso_old = to_isomorphic(old_g)
    iso_new = to_isomorphic(new_g)

    old_nt = _as_text(iso_old.serialize(format="nt"))
    new_nt = _as_text(iso_new.serialize(format="nt"))

    old_set = set(line for line in old_nt.splitlines() if line.strip())
    new_set = set(line for line in new_nt.splitlines() if line.strip())

    both = old_set & new_set
    old_only = old_set - new_set
    new_only = new_set - old_set

    in_both = Graph()
    in_old_only = Graph()
    in_new_only = Graph()
    if both:
        in_both.parse(data="\n".join(sorted(both)) + "\n", format="nt")
    if old_only:
        in_old_only.parse(data="\n".join(sorted(old_only)) + "\n", format="nt")
    if new_only:
        in_new_only.parse(data="\n".join(sorted(new_only)) + "\n", format="nt")
    return in_both, in_old_only, in_new_only


# ---- CLI ----


def main() -> int:
    p = argparse.ArgumentParser(
        description="Create diff graphs (additions/removals) between two RDF files.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        epilog=(
            "Examples:\n"
            "  python rdf_diff_graph.py old.ttl new.ttl --out-prefix diff --log-level INFO\n"
            "  python rdf_diff_graph.py old.ttl new.ttl --diff-mode simple --log-level INFO\n"
            "  python rdf_diff_graph.py old.ttl new.ttl --no-list-canon --log-level DEBUG\n"
        ),
    )
    p.add_argument("old", type=Path, help="OLD file (e.g., .ttl)")
    p.add_argument("new", type=Path, help="NEW file (e.g., .ttl)")
    p.add_argument("--out-prefix", default="diff", help="Prefix for output files (default: diff)")
    p.add_argument(
        "--format",
        default="turtle",
        choices=["turtle", "nt", "xml", "json-ld", "trig", "n3"],
        help="Serialization format for outputs (default: turtle)",
    )
    p.add_argument("--no-unchanged", action="store_true", help="Do not write unchanged.ttl")
    p.add_argument(
        "--old-format", dest="old_format", default=None, help="Force parser format for OLD (e.g., 'turtle', 'xml')"
    )
    p.add_argument("--new-format", dest="new_format", default=None, help="Force parser format for NEW")
    p.add_argument(
        "--no-list-canon",
        dest="list_canon",
        action="store_false",
        help="Disable RDF list canonicalization + deterministic heads (default: on)",
    )
    p.add_argument(
        "--no-symmetric-canon",
        dest="symm_canon",
        action="store_false",
        help="Disable canonicalization of symmetric OWL edges (default: on)",
    )
    p.add_argument(
        "--no-prune-lists",
        dest="prune_lists",
        action="store_false",
        help="Do NOT prune orphaned list chains (default: prune)",
    )
    p.add_argument(
        "--diff-mode",
        choices=["isomorphic", "simple"],
        default="isomorphic",
        help="Diff algorithm: isomorphic (rdflib graph_diff) or simple (canonical NT set diff)",
    )
    p.add_argument(
        "--log-level",
        default="INFO",
        choices=["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG"],
        help="Logging level (default: INFO)",
    )
    p.add_argument(
        "--log-every", type=int, default=0, help="Heartbeat frequency for long loops (0 = off). Example: 500"
    )
    p.set_defaults(list_canon=True, symm_canon=True, prune_lists=True)

    args = p.parse_args()

    logging.basicConfig(
        level=getattr(logging, args.log_level),
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
        datefmt="%H:%M:%S",
    )

    if not args.old.exists():
        log.error(f"File not found: {args.old}")
        return 2
    if not args.new.exists():
        log.error(f"File not found: {args.new}")
        return 2

    try:
        t0 = time.perf_counter()

        # Parse
        t = time.perf_counter()
        g_old = Graph()
        g_new = Graph()
        g_old.parse(args.old.as_posix(), format=args.old_format)
        g_new.parse(args.new.as_posix(), format=args.new_format)
        log.info(
            f"[parse] old='{args.old.name}' triples={len(g_old)}; new='{args.new.name}' triples={len(g_new)} in {_tsec(t)}"
        )

        # Normalize once per graph
        normalize_for_diff(g_old, args.list_canon, args.symm_canon, args.prune_lists, log_every=args.log_every)
        normalize_for_diff(g_new, args.list_canon, args.symm_canon, args.prune_lists, log_every=args.log_every)

        # Diff
        if args.diff_mode == "simple":
            t = time.perf_counter()
            in_both, in_old_only, in_new_only = simple_set_diff(g_old, g_new)
            log.info(f"[diff/simple] finished in {_tsec(t)}")
        else:
            t = time.perf_counter()
            iso_old = to_isomorphic(g_old)
            iso_new = to_isomorphic(g_new)
            log.info(f"[diff] isomorphic wrapping done in {_tsec(t)}")
            t = time.perf_counter()
            in_both, in_old_only, in_new_only = graph_diff(iso_old, iso_new)
            log.info(f"[diff] graph_diff finished in {_tsec(t)}")

        out_additions = Path(f"{args.out_prefix}.additions.{ext_for(args.format)}")
        out_removals = Path(f"{args.out_prefix}.removals.{ext_for(args.format)}")
        out_unchanged = Path(f"{args.out_prefix}.unchanged.{ext_for(args.format)}")

        # Serialize
        t = time.perf_counter()
        write_graph(in_new_only, out_additions, args.format)
        write_graph(in_old_only, out_removals, args.format)
        if not args.no_unchanged:
            write_graph(in_both, out_unchanged, args.format)
        log.info(
            f"[write] wrote additions={len(in_new_only)}, removals={len(in_old_only)}, unchanged={len(in_both)} in {_tsec(t)}"
        )

        # Summary
        log.info(f"OLD: {args.old.name}  NEW: {args.new.name}")
        log.info(f"Triples in OLD: {len(g_old)}   in NEW: {len(g_new)}")
        log.info(f"Δ additions (NEW−OLD): {len(in_new_only)}  -> {out_additions}")
        log.info(f"Δ removals  (OLD−NEW): {len(in_old_only)}  -> {out_removals}")
        if not args.no_unchanged:
            log.info(f"Unchanged (∩): {len(in_both)}          -> {out_unchanged}")
        log.info(f"[total] completed in {_tsec(t0)}")
        return 0

    except Exception as e:
        log.exception(f"ERROR: {e}")
        return 2


if __name__ == "__main__":
    sys.exit(main())
