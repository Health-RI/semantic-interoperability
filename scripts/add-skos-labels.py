"""
Add SKOS labels to the latest versioned Health-RI ontology Turtle file.

Behavior:
- Keep existing rdfs:label triples.
- For every rdfs:label, add a "mirror" skos:prefLabel (same literal, incl. language tag).
- For JSON elements with a tagged value "synonyms" (or "synonym"):
  - Split the string on commas to produce multiple skos:altLabel literals.
  - Attach altLabel(s) to the RDF subject whose rdfs:label matches the element's "name".
  - Do NOT add an altLabel identical to the resource's prefLabel for the same language (SKOS disjointness).
- Automatically finds and edits the latest matching TTL+JSON version in ontologies/versioned/.
- No CLI arguments required.

Safety / correctness:
- File size guardrails (MAX_*_BYTES).
- Idempotent additions (won't duplicate labels).
- Avoids creating multiple prefLabels for the same subject+language if one already exists.
"""

from __future__ import annotations

import json
import logging
import re
import sys
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, Iterator, List, Optional, Sequence, Tuple

from packaging import version as semver
from rdflib import Graph, Literal
from rdflib.namespace import RDFS, SKOS


# ----------------------------
# Configuration
# ----------------------------

ONTOLOGY_STEM = "health-ri-ontology"
VERSIONED_REL = Path("ontologies") / "versioned"

# Accepts filenames like: health-ri-ontology-v1.5.0.ttl / .json
VERSION_RE = re.compile(rf"^{re.escape(ONTOLOGY_STEM)}-v(\d+\.\d+\.\d+)\.(ttl|json)$")

# Guardrails against accidental huge inputs
MAX_TTL_BYTES = 50_000_000
MAX_JSON_BYTES = 50_000_000

# If True, treat mapping issues (unmapped/ambiguous labels) as errors
STRICT_MODE = False

logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")


# ----------------------------
# Helpers
# ----------------------------

@dataclass(frozen=True)
class VersionedPair:
    ver: semver.Version
    ttl: Path
    js: Path


def _find_base_dir(start: Path) -> Path:
    """
    Walk upwards from 'start' to find a directory containing ontologies/versioned/.
    This makes the script resilient to being placed in different subfolders.
    """
    for parent in [start, *start.parents]:
        candidate = parent / VERSIONED_REL
        if candidate.is_dir():
            return parent
    raise FileNotFoundError(
        f"Could not locate '{VERSIONED_REL.as_posix()}' by walking up from {start}"
    )


def _guard_file_size(path: Path, max_bytes: int) -> None:
    try:
        size = path.stat().st_size
    except OSError as e:
        raise OSError(f"Could not stat file: {path}") from e
    if size > max_bytes:
        raise ValueError(f"Refusing to read {path} ({size} bytes) > limit {max_bytes} bytes")


def _decode_json_bytes(raw: bytes) -> str:
    """
    Decode JSON bytes with safe fallbacks.
    OntoUML exports are often cp1252; utf-8 is tried first for portability.
    """
    for enc in ("utf-8", "cp1252", "latin-1"):
        try:
            return raw.decode(enc)
        except UnicodeDecodeError:
            continue
    # Extremely unlikely to reach here due to latin-1
    raise UnicodeDecodeError("utf-8", raw, 0, 1, "Unable to decode JSON bytes")


def _iter_dicts(obj: Any) -> Iterator[Dict[str, Any]]:
    if isinstance(obj, dict):
        yield obj
        for v in obj.values():
            yield from _iter_dicts(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from _iter_dicts(v)


def _split_synonyms(value: str) -> List[str]:
    """
    Split a comma-separated string into clean, unique labels (preserving order).
    Example: "name1, name2" -> ["name1", "name2"].
    """
    seen = set()
    out: List[str] = []
    for part in (p.strip() for p in value.split(",")):
        if not part:
            continue
        if part not in seen:
            seen.add(part)
            out.append(part)
    return out


def _extract_synonym_records(model_json: Dict[str, Any]) -> List[Tuple[str, str]]:
    """
    Return list of (element_name, synonyms_string).
    Accepts both keys: 'synonyms' and 'synonym'.
    """
    records: List[Tuple[str, str]] = []

    for d in _iter_dicts(model_json):
        pa = d.get("propertyAssignments")
        if not isinstance(pa, dict):
            continue

        syn_val: Optional[str] = None
        if isinstance(pa.get("synonyms"), str) and pa["synonyms"].strip():
            syn_val = pa["synonyms"].strip()
        elif isinstance(pa.get("synonym"), str) and pa["synonym"].strip():
            syn_val = pa["synonym"].strip()

        if syn_val is None:
            continue

        name = d.get("name")
        if isinstance(name, str) and name.strip():
            records.append((name.strip(), syn_val))

    return records


def _find_latest_versioned_pair(versioned_dir: Path) -> VersionedPair:
    """
    Find the latest SemVer version for which BOTH a TTL and JSON exist.
    """
    ttl_by_ver: Dict[semver.Version, Path] = {}
    json_by_ver: Dict[semver.Version, Path] = {}

    for p in versioned_dir.iterdir():
        if not p.is_file():
            continue
        m = VERSION_RE.match(p.name)
        if not m:
            continue

        ver_str, ext = m.group(1), m.group(2)
        try:
            v = semver.parse(ver_str)
        except semver.InvalidVersion:
            logging.warning(f"Skipping invalid SemVer in filename: {p.name}")
            continue

        if ext == "ttl":
            ttl_by_ver[v] = p
        elif ext == "json":
            json_by_ver[v] = p

    common = sorted(set(ttl_by_ver.keys()) & set(json_by_ver.keys()))
    if not common:
        raise FileNotFoundError(
            f"No matching TTL+JSON versioned pairs found in {versioned_dir}"
        )

    latest = common[-1]
    return VersionedPair(ver=latest, ttl=ttl_by_ver[latest], js=json_by_ver[latest])


def add_skos_labels(
    ttl_path: Path,
    json_path: Path,
) -> Tuple[int, int, int, int]:
    """
    Returns: (added_pref, added_alt, unmapped_or_ambiguous, pref_conflicts)
    """
    _guard_file_size(ttl_path, MAX_TTL_BYTES)
    _guard_file_size(json_path, MAX_JSON_BYTES)

    # Load RDF
    g = Graph()
    g.parse(str(ttl_path), format="turtle")
    g.bind("skos", SKOS)

    # Index rdfs:label -> [(subject, literal)]
    label_index: Dict[str, List[Tuple[Any, Literal]]] = defaultdict(list)
    for s, _, o in g.triples((None, RDFS.label, None)):
        if isinstance(o, Literal) and isinstance(o.value, str):
            key = str(o).strip()
            label_index[key].append((s, o))

    # Mirror rdfs:label -> skos:prefLabel
    added_pref = 0
    pref_conflicts = 0
    for s, _, o in list(g.triples((None, RDFS.label, None))):
        if not isinstance(o, Literal):
            continue
        lang = o.language

        existing_same_lang = [
            x for x in g.objects(s, SKOS.prefLabel)
            if isinstance(x, Literal) and x.language == lang
        ]
        # Already mirrored
        if any(x == o for x in existing_same_lang):
            continue
        # Avoid multiple prefLabels for same subject+lang
        if existing_same_lang:
            pref_conflicts += 1
            continue

        g.add((s, SKOS.prefLabel, o))
        added_pref += 1

    # Load JSON
    raw = json_path.read_bytes()
    model_json = json.loads(_decode_json_bytes(raw))

    syn_records = _extract_synonym_records(model_json)

    added_alt = 0
    unmapped_or_ambiguous = 0

    for elem_name, syn_str in syn_records:
        hits = label_index.get(elem_name.strip(), [])
        if len(hits) != 1:
            unmapped_or_ambiguous += 1
            continue

        subj, label_lit = hits[0]
        lang = label_lit.language

        # Existing prefLabels in same language (lexical forms)
        pref_lex = {
            str(x) for x in g.objects(subj, SKOS.prefLabel)
            if isinstance(x, Literal) and x.language == lang
        }

        for alt in _split_synonyms(syn_str):
            # SKOS: altLabel and prefLabel are disjoint; avoid adding the same literal
            if alt in pref_lex:
                continue

            lit = Literal(alt, lang=lang) if lang else Literal(alt)

            if (subj, SKOS.altLabel, lit) not in g:
                g.add((subj, SKOS.altLabel, lit))
                added_alt += 1

    # Persist in place
    ttl_path.write_text(g.serialize(format="turtle"), encoding="utf-8")

    return added_pref, added_alt, unmapped_or_ambiguous, pref_conflicts


def main() -> int:
    try:
        base_dir = _find_base_dir(Path(__file__).resolve().parent)
        versioned_dir = base_dir / VERSIONED_REL

        pair = _find_latest_versioned_pair(versioned_dir)

        logging.info(f"Latest matching pair: v{pair.ver}")
        logging.info(f"TTL : {pair.ttl}")
        logging.info(f"JSON: {pair.js}")

        added_pref, added_alt, unmapped, pref_conflicts = add_skos_labels(pair.ttl, pair.js)

        logging.info(f"Added skos:prefLabel: {added_pref}")
        logging.info(f"Added skos:altLabel : {added_alt}")
        if pref_conflicts:
            logging.warning(
                f"Skipped {pref_conflicts} prefLabel mirrors due to existing prefLabel(s) in the same language."
            )
        if unmapped:
            msg = (
                f"{unmapped} synonym-bearing JSON element(s) could not be mapped uniquely to an rdfs:label "
                f"(missing or ambiguous label match)."
            )
            if STRICT_MODE:
                raise RuntimeError(msg)
            logging.warning(msg)

        return 0
    except Exception as e:
        logging.error(str(e))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
