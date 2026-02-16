#!/usr/bin/env python3
"""
pylode-html-generate.py

Minimal PyLODE HTML generator. This script is intentionally limited:
- It runs PyLODE on a TTL input and writes raw HTML output.
- It can optionally skip overwriting an existing output file.

Intended to be called by an orchestrator that handles versioning/copying.
"""

from __future__ import annotations

import argparse
import logging
import subprocess
from pathlib import Path


def run_pylode(ttl_path: Path, html_out: Path, pylode_cmd: str = "pylode") -> None:
    html_out.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run([pylode_cmd, str(ttl_path), "-o", str(html_out)], check=True)


def main() -> int:
    logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")

    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--ttl", required=True, type=Path, help="Input TTL file to feed PyLODE."
    )
    ap.add_argument("--out", required=True, type=Path, help="Output HTML path.")
    ap.add_argument(
        "--pylode-cmd", default="pylode", help="PyLODE command (default: pylode)."
    )
    ap.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite output if it already exists (default: skip).",
    )
    args = ap.parse_args()

    if not args.ttl.exists():
        logging.error(f"TTL not found: {args.ttl}")
        return 2

    if args.out.exists() and not args.overwrite:
        logging.info(f"Output exists; skipping generation: {args.out}")
        return 0

    try:
        logging.info(f"Running PyLODE: {args.ttl} -> {args.out}")
        run_pylode(args.ttl, args.out, pylode_cmd=args.pylode_cmd)
        logging.info(f"Generated: {args.out}")
        return 0
    except subprocess.CalledProcessError as e:
        logging.error(f"PyLODE failed: {e}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
