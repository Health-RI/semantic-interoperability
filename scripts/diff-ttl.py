from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

from packaging import version


FILENAME_RE = re.compile(r"^health-ri-ontology-v(\d+\.\d+\.\d+)\.ttl$")


def pick_last_two_versioned_ttls(version_dir: Path) -> tuple[Path, Path]:
    candidates: list[tuple[version.Version, Path]] = []

    for f in version_dir.glob("health-ri-ontology-v*.ttl"):
        m = FILENAME_RE.match(f.name)
        if m:
            v = version.parse(m.group(1))
            candidates.append((v, f))

    if len(candidates) < 2:
        raise SystemExit(
            f"Need at least 2 versioned TTL files in {version_dir} matching "
            f"'health-ri-ontology-v<MAJOR>.<MINOR>.<PATCH>.ttl'. Found {len(candidates)}."
        )

    candidates.sort(key=lambda t: t[0])
    old_path = candidates[-2][1]
    new_path = candidates[-1][1]
    return old_path, new_path


def _section(title: str) -> None:
    bar = "=" * 80
    print(f"\n{bar}\n[diff-ttl] {title}\n{bar}", flush=True)


def main() -> int:
    script_dir = Path(__file__).resolve().parent
    repo_root = script_dir.parent

    p = argparse.ArgumentParser(
        description="Run owl-postprocess.py, then insert-metadata.py, then make-diff-ttl.py (auto-picks last two versions if args omitted)."
    )
    p.add_argument("old", nargs="?", help="Old TTL path (optional)")
    p.add_argument("new", nargs="?", help="New TTL path (optional)")
    p.add_argument(
        "--version-dir",
        default=str(repo_root / "ontologies" / "versioned"),
        help="Directory containing versioned TTLs (default: ontologies/versioned)",
    )
    p.add_argument("--dry-run", action="store_true", help="Print what would run and exit")

    args = p.parse_args()

    version_dir = Path(args.version_dir).resolve()

    # Resolve OLD/NEW
    if args.old and args.new:
        old_path = Path(args.old).resolve()
        new_path = Path(args.new).resolve()
    elif (args.old is None) and (args.new is None):
        old_path, new_path = pick_last_two_versioned_ttls(version_dir)
    else:
        raise SystemExit("Provide either BOTH OLD and NEW paths, or provide none (to auto-pick).")

    post_script = script_dir / "owl-postprocess.py"
    insert_script = script_dir / "insert-metadata.py"
    diff_script = script_dir / "make-diff-ttl.py"

    post_cmd = [sys.executable, str(post_script)]
    insert_cmd = [sys.executable, str(insert_script)]
    diff_cmd = [sys.executable, str(diff_script), str(old_path), str(new_path)]

    print(f"[diff-ttl] OLD: {old_path}")
    print(f"[diff-ttl] NEW: {new_path}")

    if args.dry_run:
        print("[diff-ttl] DRY RUN")
        print(" ".join(post_cmd))
        print(" ".join(insert_cmd))
        print(" ".join(diff_cmd))
        return 0

    _section("OWL postprocessor (owl-postprocess.py)")
    subprocess.run(post_cmd, check=True)

    _section("Metadata inserter (insert-metadata.py)")
    subprocess.run(insert_cmd, check=True)

    _section("Diff generator (make-diff-ttl.py)")
    subprocess.run(diff_cmd, check=True)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
