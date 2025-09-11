#!/usr/bin/env python3
"""
rdf_diff_graph.py

Create RDF *diff graphs* between two versions:
- additions = NEW minus OLD
- removals  = OLD minus NEW
- unchanged = intersection (optional)

Blank nodes are handled via isomorphism-aware comparison.

Usage examples:
  python rdf_diff_graph.py old.ttl new.ttl
  python rdf_diff_graph.py old.ttl new.ttl --out-prefix health-ri-ontology-v0.10.1_vs_v0.9.2
  python rdf_diff_graph.py old.ttl new.ttl --format ttl --no-unchanged

Exit codes:
  0 = ran successfully (diffs may be empty)
  2 = error
"""

import argparse
import sys
from pathlib import Path

from rdflib import Graph
from rdflib.compare import to_isomorphic, graph_diff

def load_graph(path: Path) -> Graph:
    g = Graph()
    # rdflib guesses the format from extension/content; override with --old-format / --new-format if needed
    g.parse(path.as_posix())
    return g

def serialize_sorted_nt(g: Graph) -> list[str]:
    """Helper for deterministic debug or tests (not used for output files)."""
    data = g.serialize(format="nt")
    text = data.decode("utf-8") if isinstance(data, (bytes, bytearray)) else str(data)
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    lines.sort()
    return lines

def write_graph(g: Graph, out_path: Path, fmt: str) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    data = g.serialize(format=fmt)
    if isinstance(data, (bytes, bytearray)):
        out_path.write_bytes(data)
    else:
        out_path.write_text(data, encoding="utf-8")

def main() -> int:
    p = argparse.ArgumentParser(description="Create diff graphs (additions/removals) between two RDF files.")
    p.add_argument("old", type=Path, help="OLD file (e.g., .ttl)")
    p.add_argument("new", type=Path, help="NEW file (e.g., .ttl)")
    p.add_argument("--out-prefix", default="diff", help="Prefix for output files (default: diff)")
    p.add_argument("--format", default="turtle", choices=["turtle", "nt", "xml", "json-ld", "trig", "n3"],
                   help="Serialization format for outputs (default: turtle)")
    p.add_argument("--no-unchanged", action="store_true", help="Do not write unchanged.ttl")
    # Optional explicit parse formats (rarely needed)
    p.add_argument("--old-format", default=None, help="Force parser format for OLD (e.g., 'turtle', 'xml')")
    p.add_argument("--new-format", default=None, help="Force parser format for NEW")
    args = p.parse_args()

    if not args.old.exists():
        print(f"ERROR: File not found: {args.old}", file=sys.stderr)
        return 2
    if not args.new.exists():
        print(f"ERROR: File not found: {args.new}", file=sys.stderr)
        return 2

    try:
        g_old = Graph()
        g_new = Graph()
        g_old.parse(args.old.as_posix(), format=args.old_format)
        g_new.parse(args.new.as_posix(), format=args.new_format)

        # Isomorphism-aware compare (handles blank nodes robustly)
        iso_old = to_isomorphic(g_old)
        iso_new = to_isomorphic(g_new)
        in_both, in_old_only, in_new_only = graph_diff(iso_old, iso_new)

        out_base = Path(args.out_prefix)
        additions_path = out_base.with_suffix("")  # just to get stem cleanly
        # Build filenames with explicit suffixes for clarity
        out_additions = Path(f"{args.out_prefix}.additions.ttl" if args.format == "turtle" else f"{args.out_prefix}.additions.{ext_for(args.format)}")
        out_removals  = Path(f"{args.out_prefix}.removals.ttl"  if args.format == "turtle" else f"{args.out_prefix}.removals.{ext_for(args.format)}")
        out_unchanged = Path(f"{args.out_prefix}.unchanged.ttl" if args.format == "turtle" else f"{args.out_prefix}.unchanged.{ext_for(args.format)}")

        write_graph(in_new_only, out_additions, args.format)
        write_graph(in_old_only, out_removals, args.format)
        if not args.no_unchanged:
            write_graph(in_both, out_unchanged, args.format)

        # Summary
        print(f"OLD: {args.old.name}  NEW: {args.new.name}")
        print(f"Triples in OLD: {len(g_old)}   in NEW: {len(g_new)}")
        print(f"Δ additions (NEW−OLD): {len(in_new_only)}  -> {out_additions}")
        print(f"Δ removals  (OLD−NEW): {len(in_old_only)}  -> {out_removals}")
        if not args.no_unchanged:
            print(f"Unchanged (∩): {len(in_both)}          -> {out_unchanged}")

        return 0

    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 2

def ext_for(fmt: str) -> str:
    return {
        "turtle": "ttl",
        "nt": "nt",
        "xml": "rdf",
        "json-ld": "jsonld",
        "trig": "trig",
        "n3": "n3",
    }.get(fmt, fmt)

if __name__ == "__main__":
    sys.exit(main())
