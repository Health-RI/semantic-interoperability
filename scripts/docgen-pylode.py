#!/usr/bin/env python3
"""
docgen-pylode.py

Orchestrator for generating and post-processing PyLODE HTML specifications.

What this script does
- Detects the latest versioned TTL for:
  - Ontology: ontologies/versioned/health-ri-ontology-vX.Y.Z.ttl
  - Vocabulary: vocabulary/versioned/health-ri-vocabulary-vX.Y.Z.ttl
- Preserves historical artifacts:
  - If the versioned HTML already exists, it is NOT rewritten.
  - docs/ and latest/ outputs are (re)built from the versioned HTML and post-processed.
- If the versioned HTML does not exist:
  - Generate raw HTML via pylode-html-generate.py
  - Post-process via pylode-html-postprocess.py
  - Write docs/ output, then copy it to versioned/ and latest/

Design
- All HTML transforms live in pylode-html-postprocess.py.
- This script only handles versioning decisions, calling scripts, and copying outputs.

Exit codes
- 0: success
- 1: one or more specs failed
- 2: invalid inputs / missing scripts
"""

from __future__ import annotations

import logging
import os
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, List, Optional, Tuple

from packaging import version


# ---------------------------
# Version discovery
# ---------------------------


def _find_latest_versioned_ttl(
    directory: Path,
    *,
    filename_regex: str,
    glob_pattern: str,
) -> Tuple[Optional[Path], Optional[version.Version]]:
    latest_file: Optional[Path] = None
    latest_version: Optional[version.Version] = None

    rx = re.compile(filename_regex)

    for file in directory.glob(glob_pattern):
        m = rx.fullmatch(file.name)
        if not m:
            continue
        file_version = version.parse(m.group(1))
        if latest_version is None or file_version > latest_version:
            latest_version = file_version
            latest_file = file

    return latest_file, latest_version


def get_latest_ontology_ttl_file(
    directory: Path,
) -> Tuple[Optional[Path], Optional[version.Version]]:
    return _find_latest_versioned_ttl(
        directory,
        filename_regex=r"health-ri-ontology-v(\d+\.\d+\.\d+)\.ttl",
        glob_pattern="health-ri-ontology-v*.ttl",
    )


def get_latest_vocabulary_ttl_file(
    directory: Path,
) -> Tuple[Optional[Path], Optional[version.Version]]:
    return _find_latest_versioned_ttl(
        directory,
        filename_regex=r"health-ri-vocabulary-v(\d+\.\d+\.\d+)\.ttl",
        glob_pattern="health-ri-vocabulary-v*.ttl",
    )


# ---------------------------
# Orchestration
# ---------------------------


@dataclass(frozen=True)
class SpecConfig:
    name: str  # for logs
    ttl_dir: Path
    ttl_finder: Callable[[Path], Tuple[Optional[Path], Optional[version.Version]]]

    docs_output: Path
    latest_output: Path
    versioned_output_dir: Path

    raw_output_dir: Path

    # Extra postprocess flags, e.g. ["--no-classes-restructure"]
    postprocess_extra_args: List[str] = field(default_factory=list)


def _run(cmd: List[str]) -> None:
    logging.info("Running: %s", " ".join(cmd))
    subprocess.run(cmd, check=True)


def _ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def _orchestrate_one_spec(
    cfg: SpecConfig,
    *,
    generate_script: Path,
    postprocess_script: Path,
    pylode_cmd: str,
) -> bool:
    cfg.ttl_dir.mkdir(parents=True, exist_ok=True)
    cfg.versioned_output_dir.mkdir(parents=True, exist_ok=True)
    cfg.raw_output_dir.mkdir(parents=True, exist_ok=True)
    _ensure_parent(cfg.docs_output)
    _ensure_parent(cfg.latest_output)

    latest_ttl, latest_ver = cfg.ttl_finder(cfg.ttl_dir)
    if not latest_ttl or latest_ver is None:
        logging.warning(
            "No valid TTL files found for %s in: %s (skipping).", cfg.name, cfg.ttl_dir
        )
        return True

    ver_str = str(latest_ver)
    versioned_output = cfg.versioned_output_dir / f"specification-v{ver_str}.html"

    # ---------------------------
    # Case A: versioned HTML exists -> preserve it, rebuild docs/latest and post-process those copies only
    # ---------------------------
    if versioned_output.exists():
        shutil.copyfile(versioned_output, cfg.docs_output)

        _run(
            [
                sys.executable,
                str(postprocess_script),
                "--html-in",
                str(cfg.docs_output),
                "--ttl",
                str(latest_ttl),
                *cfg.postprocess_extra_args,
            ]
        )

        shutil.copyfile(cfg.docs_output, cfg.latest_output)

        logging.info(
            "%s specification for v%s already exists (%s). Synced docs/latest from versioned and post-processed docs/latest only.",
            cfg.name,
            ver_str,
            versioned_output,
        )
        return True

    # ---------------------------
    # Case B: versioned HTML missing -> generate raw + postprocess into docs, then copy docs -> versioned + latest
    # ---------------------------
    raw_html = cfg.raw_output_dir / f"{cfg.name.casefold()}-v{ver_str}-raw.html"

    _run(
        [
            sys.executable,
            str(generate_script),
            "--ttl",
            str(latest_ttl),
            "--out",
            str(raw_html),
            "--overwrite",
            "--pylode-cmd",
            pylode_cmd,
        ]
    )

    _run(
        [
            sys.executable,
            str(postprocess_script),
            "--html-in",
            str(raw_html),
            "--ttl",
            str(latest_ttl),
            "--html-out",
            str(cfg.docs_output),
            *cfg.postprocess_extra_args,
        ]
    )

    _ensure_parent(versioned_output)
    shutil.copyfile(cfg.docs_output, versioned_output)
    shutil.copyfile(cfg.docs_output, cfg.latest_output)

    logging.info(
        "%s specification generated and written to docs/latest/versioned for v%s.",
        cfg.name,
        ver_str,
    )
    return True


def main() -> int:
    logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")

    base_dir = Path(__file__).resolve().parent.parent
    script_dir = Path(__file__).resolve().parent

    generate_script = script_dir / "pylode-html-generate.py"
    postprocess_script = script_dir / "pylode-html-postprocess.py"

    if not generate_script.exists():
        logging.error("Missing generator script: %s", generate_script)
        return 2
    if not postprocess_script.exists():
        logging.error("Missing post-processor script: %s", postprocess_script)
        return 2

    # Allow override in CI if needed
    pylode_cmd = os.environ.get("PYLODE_CMD", "pylode")

    ok = True

    ok = (
        _orchestrate_one_spec(
            SpecConfig(
                name="Ontology",
                ttl_dir=base_dir / "ontologies" / "versioned",
                ttl_finder=get_latest_ontology_ttl_file,
                docs_output=base_dir
                / "docs"
                / "ontology"
                / "specification-ontology.html",
                latest_output=base_dir
                / "ontologies"
                / "latest"
                / "documentations"
                / "specification.html",
                versioned_output_dir=base_dir
                / "ontologies"
                / "versioned"
                / "documentations",
                raw_output_dir=base_dir / "build" / "pylode" / "ontology",
                postprocess_extra_args=[],
            ),
            generate_script=generate_script,
            postprocess_script=postprocess_script,
            pylode_cmd=pylode_cmd,
        )
        and ok
    )

    # For the vocabulary spec, we keep legacy HTML tweaks but disable package-based Classes restructuring by default.
    # This avoids failures in cases where the vocabulary HTML has no #classes section.
    ok = (
        _orchestrate_one_spec(
            SpecConfig(
                name="Vocabulary",
                ttl_dir=base_dir / "vocabulary" / "versioned",
                ttl_finder=get_latest_vocabulary_ttl_file,
                docs_output=base_dir
                / "docs"
                / "method"
                / "specification-vocabulary.html",
                latest_output=base_dir
                / "vocabulary"
                / "latest"
                / "documentations"
                / "specification.html",
                versioned_output_dir=base_dir
                / "vocabulary"
                / "versioned"
                / "documentations",
                raw_output_dir=base_dir / "build" / "pylode" / "vocabulary",
                postprocess_extra_args=["--no-classes-restructure"],
            ),
            generate_script=generate_script,
            postprocess_script=postprocess_script,
            pylode_cmd=pylode_cmd,
        )
        and ok
    )

    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
