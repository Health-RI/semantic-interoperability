#!/usr/bin/env python3
"""Run a SPARQL SELECT query over the demo graphs and export the result to CSV.

Default input graphs:
- demo-schema.ttl
- health-ri-ontology.ttl
- instances_extended.ttl

Example:
    python run_query.py --input query.rq

This will create:
    query-output.csv
"""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

from rdflib import BNode, Graph, Literal, URIRef


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run a SPARQL SELECT query over the demo TTL files and export the result to CSV."
    )
    parser.add_argument(
        "--input",
        required=True,
        help="Path to the file containing the SPARQL query to execute.",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Path to the output CSV file. Default: ../outputs/<input-stem>-output.csv relative to this script.",
    )
    parser.add_argument(
        "--schema",
        default=None,
        help="Path to demo-schema.ttl. Default: ../inputs/demo-schema.ttl relative to this script.",
    )
    parser.add_argument(
        "--ontology",
        default=None,
        help="Path to health-ri-ontology.ttl. Default: ../inputs/health-ri-ontology.ttl relative to this script.",
    )
    parser.add_argument(
        "--instances",
        default=None,
        help="Path to instances_extended.ttl. Default: ../inputs/instances_extended.ttl relative to this script.",
    )
    return parser.parse_args()


def resolve_existing_file(
    path_str: str | None, default_name: str | None = None, base_dir: Path | None = None
) -> Path:
    if path_str is not None:
        path = Path(path_str).expanduser().resolve()
    else:
        if default_name is None or base_dir is None:
            raise ValueError("Missing path and no default was provided.")
        path = (base_dir / default_name).resolve()

    if not path.is_file():
        raise FileNotFoundError(f"File not found: {path}")
    return path


def resolve_output_path(
    output_str: str | None, query_path: Path, output_dir: Path
) -> Path:
    if output_str:
        return Path(output_str).expanduser().resolve()
    return (output_dir / f"{query_path.stem}-output.csv").resolve()


def load_graph(paths: list[Path]) -> Graph:
    graph = Graph()
    for path in paths:
        graph.parse(path, format="turtle")
    return graph


def term_to_csv_value(term: object) -> str:
    if term is None:
        return ""
    if isinstance(term, URIRef):
        return str(term)
    if isinstance(term, BNode):
        return f"_:{term}"
    if isinstance(term, Literal):
        return str(term)
    return str(term)


def write_select_result_to_csv(result, output_path: Path) -> int:
    if getattr(result, "type", None) != "SELECT":
        raise ValueError("Only SPARQL SELECT queries can be exported to CSV.")

    variables = list(result.vars or [])
    if not variables:
        raise ValueError("The SELECT query returned no variables.")

    row_count = 0
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow([str(var) for var in variables])

        for row in result:
            writer.writerow([term_to_csv_value(row[i]) for i in range(len(variables))])
            row_count += 1

    return row_count


def main() -> int:
    args = parse_args()

    script_dir = Path(__file__).resolve().parent
    input_dir = script_dir.parent / "inputs"
    output_dir = script_dir.parent / "outputs"

    query_path = resolve_existing_file(args.input)
    output_path = resolve_output_path(args.output, query_path, output_dir)

    schema_path = resolve_existing_file(args.schema, "demo-schema.ttl", input_dir)
    ontology_path = resolve_existing_file(
        args.ontology, "health-ri-ontology.ttl", input_dir
    )
    instances_path = resolve_existing_file(
        args.instances, "instances_extended.ttl", input_dir
    )

    query_text = query_path.read_text(encoding="utf-8").strip()
    if not query_text:
        raise ValueError(f"Query file is empty: {query_path}")

    graph = load_graph([schema_path, ontology_path, instances_path])
    result = graph.query(query_text)
    row_count = write_select_result_to_csv(result, output_path)

    print("Loaded graph files:")
    print(f"- {schema_path}")
    print(f"- {ontology_path}")
    print(f"- {instances_path}")
    print(f"Query file: {query_path}")
    print(f"Output CSV: {output_path}")
    print(f"Rows written: {row_count}")

    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        raise SystemExit(1)
