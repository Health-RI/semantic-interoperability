"""
Post-process the latest versioned Health-RI ontology Turtle file.

This script enriches the ontology TTL using its paired OntoUML JSON export.

Adds / maintains:
1) SKOS labels
   - Keep existing rdfs:label triples.
   - For every rdfs:label, add a mirror skos:prefLabel (same literal, incl. language tag).
   - For JSON elements with tagged value "synonyms" (or "synonym"):
     - Split the string on commas to produce multiple skos:altLabel literals.
     - Attach altLabel(s) to the RDF subject whose rdfs:label matches the element's "name".
     - Do NOT add an altLabel identical to the resource's prefLabel for the same language (SKOS disjointness).

2) Ontology ownership
   - Add rdfs:isDefinedBy <https://w3id.org/health-ri/ontology> to every resource in the hrio: namespace.

3) Packages (from JSON)
   - Create/ensure a package resource for every JSON Package:
       <https://w3id.org/health-ri/ontology#package/{PackagePath}>
     where PackagePath is normalized to UpperCamelCase per segment and joined with "/".
   - For each package resource, ensure:
       a skos:Collection ;
       rdfs:label "..."@en ;
       skos:prefLabel "..."@en .   (mirrored from rdfs:label)

4) Package membership (from JSON)
   - For each JSON Class element nested in a JSON Package, add:
       dcterms:isPartOf <...#package/{PackagePath}>
     to the matching RDF resource (matched by rdfs:label == JSON "name").

5) Package maturity (from JSON, with inheritance)
   - For each JSON Package resource, add:
       vs:term_status "int|irv|erv|pub"
     Stage values are inherited from the closest ancestor package that has "stage".
     (If no ancestor has "stage", no vs:term_status is added for that package.)

6) Literal cleanup
   - Normalize rdfs:comment line endings to LF only (remove stray "\\r" / CRLF).

Behavior / workflow:
- Automatically finds and edits the latest matching TTL+JSON version in ontologies/versioned/.
- No CLI arguments required.

Safety / correctness:
- File size guardrails (MAX_*_BYTES).
- Idempotent additions (won't duplicate triples).
- Avoids creating multiple prefLabels for the same subject+language if one already exists.
- Optional reconciliation/migration for package-related triples (see flags below).
- Atomic write to avoid partially-written TTL files on failure.

NOTES:
- rdflib serialization does NOT preserve Turtle comments (# ...) or prefix ordering.
"""

from __future__ import annotations

import json
import logging
import re
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterator, List, Optional, Tuple

from packaging import version as semver
from rdflib import Graph, Literal, Namespace, URIRef
from rdflib.namespace import DCTERMS, OWL, RDF, RDFS, SKOS

# ----------------------------
# Configuration
# ----------------------------

ONTOLOGY_STEM = "health-ri-ontology"
VERSIONED_REL = Path("ontologies") / "versioned"

# Accepts filenames like: health-ri-ontology-v1.6.0.ttl / .json
VERSION_RE = re.compile(rf"^{re.escape(ONTOLOGY_STEM)}-v(\d+\.\d+\.\d+)\.(ttl|json)$")

# Guardrails against accidental huge inputs
MAX_TTL_BYTES = 50_000_000
MAX_JSON_BYTES = 50_000_000

# If True, treat mapping issues (unmapped/ambiguous labels) as errors
STRICT_MODE = False

# If True, synchronize package memberships derived from JSON by removing *other*
# dcterms:isPartOf values in the hrio:#package/ namespace for each class.
RECONCILE_PACKAGE_MEMBERSHIP = True

# If True, synchronize package vs:term_status derived from JSON by removing any existing
# vs:term_status values for each computed package IRI before writing the new one.
RECONCILE_PACKAGE_STATUS = True

# If True, remove legacy percent-encoded package IRIs (e.g., ...#package/Health%20Condition)
# and their related triples (membership, status, and package-node triples).
MIGRATE_PERCENT_ENCODED_PACKAGE_IRIS = True

# Canonical namespace/IRIs
HRIO_NS_STR = "https://w3id.org/health-ri/ontology#"
ONTOLOGY_IRI = URIRef("https://w3id.org/health-ri/ontology")

# W3C SW Vocabulary Status (vs:)
VS = Namespace("http://www.w3.org/2003/06/sw-vocab-status/ns#")
ALLOWED_STAGES = {"int", "irv", "erv", "pub"}

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
        raise ValueError(
            f"Refusing to read {path} ({size} bytes) > limit {max_bytes} bytes"
        )


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


_TOKEN_RE = re.compile(r"[0-9A-Za-z]+")


def _to_upper_camel(segment: str) -> str:
    """
    Normalize a package path segment to UpperCamelCase.

    Examples:
      "Health Condition" -> "HealthCondition"
      "Sex-Gender Outcome" -> "SexGenderOutcome"
      "Sex and Gender" -> "SexAndGender"
      "FHIR" -> "FHIR"
    """
    tokens = _TOKEN_RE.findall(segment.strip())
    if not tokens:
        return "Package"

    out = []
    for t in tokens:
        if t.isupper():
            out.append(t)
        else:
            out.append(t[0].upper() + t[1:])
    return "".join(out)


def _normalize_package_path(package_path: str) -> str:
    """
    Normalize a full package path "A/B C/D" into "A/BC/D" (UpperCamelCase per segment).
    """
    segments = [seg for seg in package_path.split("/") if seg]
    return "/".join(_to_upper_camel(seg) for seg in segments)


def _package_iri(package_path: str) -> URIRef:
    """
    Build <...#package/{NormalizedPackagePath}>.
    """
    norm_path = _normalize_package_path(package_path)
    return URIRef(f"{HRIO_NS_STR}package/{norm_path}")


def _is_legacy_percent_encoded_package_iri(iri: URIRef) -> bool:
    s = str(iri)
    return s.startswith(f"{HRIO_NS_STR}package/") and "%" in s


def _extract_packages_and_classes(
    model_json: Dict[str, Any],
) -> Tuple[List[Tuple[str, str]], Dict[str, Optional[str]]]:
    """
    Traverse JSON Packages and collect:
    - class_records: [(class_name, package_path)]
    - package_stage: {package_path: effective_stage_or_None}

    Stage inheritance:
    - effective_stage is the closest ancestor's (or this package's) propertyAssignments.stage.
    - If no ancestor has stage, effective_stage is None.
    """
    class_records: List[Tuple[str, str]] = []
    package_stage: Dict[str, Optional[str]] = {}

    top_contents = model_json.get("model", {}).get("contents", [])
    if not isinstance(top_contents, list):
        return class_records, package_stage

    def walk_package(
        pkg: Dict[str, Any],
        ancestors: List[str],
        inherited_stage: Optional[str],
    ) -> None:
        name = pkg.get("name")
        if not isinstance(name, str) or not name.strip():
            return
        name = name.strip()

        path = "/".join([*ancestors, name]) if ancestors else name

        pa = pkg.get("propertyAssignments")
        stage_here: Optional[str] = None
        if (
            isinstance(pa, dict)
            and isinstance(pa.get("stage"), str)
            and pa["stage"].strip()
        ):
            stage_here = pa["stage"].strip()

        stage_effective = stage_here or inherited_stage
        package_stage[path] = stage_effective

        if stage_effective is not None and stage_effective not in ALLOWED_STAGES:
            logging.warning(
                f"Unknown stage '{stage_effective}' on package '{path}' "
                f"(expected one of {sorted(ALLOWED_STAGES)}). Will still write it."
            )

        contents = pkg.get("contents", [])
        if not isinstance(contents, list):
            return

        for child in contents:
            if not isinstance(child, dict):
                continue

            ctype = child.get("type")
            if ctype == "Package":
                walk_package(child, [*ancestors, name], stage_effective)
            elif ctype == "Class":
                cname = child.get("name")
                if isinstance(cname, str) and cname.strip():
                    class_records.append((cname.strip(), path))

    for item in top_contents:
        if isinstance(item, dict) and item.get("type") == "Package":
            walk_package(item, [], None)

    return class_records, package_stage


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


def _add_is_defined_by(g: Graph) -> int:
    """
    Add rdfs:isDefinedBy ONTOLOGY_IRI to every URI in the hrio: namespace that appears
    anywhere in the graph (subject, predicate, or object).
    """
    added = 0
    nodes = set(g.subjects()) | set(g.predicates()) | set(g.objects())
    for term in nodes:
        if isinstance(term, URIRef) and str(term).startswith(HRIO_NS_STR):
            if (term, RDFS.isDefinedBy, ONTOLOGY_IRI) not in g:
                g.add((term, RDFS.isDefinedBy, ONTOLOGY_IRI))
                added += 1
    return added


def _mirror_rdfs_label_to_skos_preflabel(g: Graph) -> Tuple[int, int]:
    """
    Mirror all rdfs:label -> skos:prefLabel, avoiding multiple prefLabels per subject+language.
    Returns: (added_pref, pref_conflicts)
    """
    added_pref = 0
    pref_conflicts = 0

    for s, _, o in list(g.triples((None, RDFS.label, None))):
        if not isinstance(o, Literal):
            continue

        lang = o.language
        existing_same_lang = [
            x
            for x in g.objects(s, SKOS.prefLabel)
            if isinstance(x, Literal) and x.language == lang
        ]

        if any(x == o for x in existing_same_lang):
            continue
        if existing_same_lang:
            pref_conflicts += 1
            continue

        g.add((s, SKOS.prefLabel, o))
        added_pref += 1

    return added_pref, pref_conflicts


def _normalize_comment_line_endings(g: Graph) -> int:
    """
    Replace CRLF/CR line endings with LF for rdfs:comment literals.
    """
    changed = 0
    for s, o in list(g.subject_objects(RDFS.comment)):
        if not isinstance(o, Literal) or not isinstance(o.value, str):
            continue
        if "\r" not in str(o):
            continue

        new_text = str(o).replace("\r\n", "\n").replace("\r", "\n")
        new_lit = Literal(new_text, lang=o.language, datatype=o.datatype)

        if new_lit == o:
            continue

        g.remove((s, RDFS.comment, o))
        g.add((s, RDFS.comment, new_lit))
        changed += 1

    return changed


def _validate_ontology_metadata_present(g: Graph) -> None:
    """
    Basic sanity check to help catch 'wrong file' issues or accidental graph loss.
    """
    if (ONTOLOGY_IRI, RDF.type, OWL.Ontology) not in g:
        msg = (
            f"Expected to find ontology node '{ONTOLOGY_IRI}' typed as owl:Ontology, but it was not found. "
            f"This may indicate the script is operating on an unexpected TTL file."
        )
        if STRICT_MODE:
            raise RuntimeError(msg)
        logging.warning(msg)


def _atomic_write_text(path: Path, text: str, encoding: str = "utf-8") -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    with tmp.open("w", encoding=encoding, newline="\n") as f:
        f.write(text)
    tmp.replace(path)


def _ensure_package_resources(
    g: Graph,
    package_paths: List[str],
    lang: str = "en",
) -> Dict[str, int]:
    """
    Ensure each JSON package has a corresponding package resource:
      - rdf:type skos:Collection
      - rdfs:label (default @en, unless already present)
    skos:prefLabel is mirrored from rdfs:label by the mirror step.

    Returns counts: created_type, created_rdfs_label, created_from_existing_prefLabel
    """
    created_type = 0
    created_rdfs_label = 0
    created_from_existing_pref = 0

    for pkg_path in package_paths:
        pkg_iri = _package_iri(pkg_path)

        # type skos:Collection
        if (pkg_iri, RDF.type, SKOS.Collection) not in g:
            g.add((pkg_iri, RDF.type, SKOS.Collection))
            created_type += 1

        # Ensure rdfs:label exists (prefer last segment's original name)
        has_any_label = any(True for _ in g.objects(pkg_iri, RDFS.label))
        if not has_any_label:
            # If a prefLabel exists, mirror it to rdfs:label first (then later we mirror back)
            existing_pref = next(
                (
                    x
                    for x in g.objects(pkg_iri, SKOS.prefLabel)
                    if isinstance(x, Literal)
                ),
                None,
            )
            if isinstance(existing_pref, Literal) and isinstance(
                existing_pref.value, str
            ):
                g.add((pkg_iri, RDFS.label, existing_pref))
                created_from_existing_pref += 1
                continue

            # Otherwise, use the raw (human) package name = last segment of the JSON path
            raw_last_segment = pkg_path.split("/")[-1].strip()
            if not raw_last_segment:
                raw_last_segment = "Package"
            g.add((pkg_iri, RDFS.label, Literal(raw_last_segment, lang=lang)))
            created_rdfs_label += 1

    return {
        "created_pkg_type_skos_collection": created_type,
        "created_pkg_rdfs_label": created_rdfs_label,
        "created_pkg_rdfs_label_from_existing_pref": created_from_existing_pref,
    }


def postprocess_ontology(
    ttl_path: Path,
    json_path: Path,
) -> Dict[str, int]:
    """
    Post-process TTL in-place, returning a stats dict.
    """
    _guard_file_size(ttl_path, MAX_TTL_BYTES)
    _guard_file_size(json_path, MAX_JSON_BYTES)

    g = Graph()
    g.parse(str(ttl_path), format="turtle")
    g.bind("skos", SKOS)
    g.bind("dct", DCTERMS)
    g.bind("vs", VS)

    _validate_ontology_metadata_present(g)

    # Index rdfs:label -> [(subject, literal)]  (do NOT restrict to URIRef; preserves older behavior)
    label_index: Dict[str, List[Tuple[Any, Literal]]] = defaultdict(list)
    for s, _, o in g.triples((None, RDFS.label, None)):
        # NEW: exclude package nodes so their labels don't create ambiguous matches on reruns
        if isinstance(s, URIRef) and str(s).startswith(f"{HRIO_NS_STR}package/"):
            continue

        if isinstance(o, Literal) and isinstance(o.value, str):
            label_index[str(o).strip()].append((s, o))

    # 1) Mirror rdfs:label -> skos:prefLabel (initial pass; needed for synonym disjointness check)
    added_pref_1, pref_conflicts_1 = _mirror_rdfs_label_to_skos_preflabel(g)

    # Load JSON
    model_json = json.loads(_decode_json_bytes(json_path.read_bytes()))

    # 1b) Synonyms -> skos:altLabel
    syn_records = _extract_synonym_records(model_json)
    added_alt = 0
    unmapped_synonyms = 0

    unmapped_label_rows: List[List[str]] = []

    def _tsv_escape(x: Any) -> str:
        if x is None:
            return ""
        return str(x).replace("\t", "\\t").replace("\r", "\\r").replace("\n", "\\n")

    def _fmt_lit(lit: Literal) -> str:
        base = str(lit)
        if lit.language:
            return f"{base}@{lit.language}"
        if lit.datatype:
            return f"{base}^^<{str(lit.datatype)}>"
        return base

    for json_idx, (elem_name, syn_str) in enumerate(syn_records, start=1):
        hits = label_index.get(elem_name.strip(), [])
        if len(hits) != 1:
            unmapped_synonyms += 1

            conflict_type = (
                "missing_label_match" if not hits else "ambiguous_label_match"
            )
            cand_subjects = ";".join(str(s) for s, _ in hits)
            cand_labels = ";".join(_fmt_lit(label_lit) for _, label_lit in hits)

            unmapped_label_rows.append(
                [
                    "synonym",  # kind
                    conflict_type,  # conflict_type
                    str(json_idx),  # json_index (1-based within syn_records)
                    _tsv_escape(elem_name),  # json_name
                    _tsv_escape(elem_name.strip()),  # label_key used for lookup
                    str(len(hits)),  # hit_count
                    _tsv_escape(syn_str),  # synonyms
                    "",  # package_path (n/a)
                    _tsv_escape(cand_subjects),  # candidate_subjects
                    _tsv_escape(cand_labels),  # candidate_labels
                ]
            )
            continue

        subj, label_lit = hits[0]
        lang = label_lit.language

        pref_lex = {
            str(x)
            for x in g.objects(subj, SKOS.prefLabel)
            if isinstance(x, Literal) and x.language == lang
        }

        for alt in _split_synonyms(syn_str):
            if alt in pref_lex:
                continue

            lit = Literal(alt, lang=lang) if lang else Literal(alt)
            if (subj, SKOS.altLabel, lit) not in g:
                g.add((subj, SKOS.altLabel, lit))
                added_alt += 1

    # 2) Packages/classes from JSON
    class_records, package_stage = _extract_packages_and_classes(model_json)
    package_paths = list(package_stage.keys())

    # 2.0) Optional migration cleanup: remove triples about legacy percent-encoded package IRIs
    removed_legacy_pkg_subject_triples = 0
    if MIGRATE_PERCENT_ENCODED_PACKAGE_IRIS:
        legacy_subjects = {
            s
            for s in set(g.subjects())
            if isinstance(s, URIRef) and _is_legacy_percent_encoded_package_iri(s)
        }
        for s in legacy_subjects:
            triples = list(g.triples((s, None, None)))
            for t in triples:
                g.remove(t)
            removed_legacy_pkg_subject_triples += len(triples)

    # 2.1) Ensure package resources exist as skos:Collection with rdfs:label (prefLabel mirrored later)
    pkg_resource_stats = _ensure_package_resources(g, package_paths, lang="en")

    # 2.2) Add dcterms:isPartOf to classes
    added_partof = 0
    unmapped_classes = 0
    removed_stale_partof = 0
    removed_legacy_partof = 0

    for json_idx, (class_name, pkg_path) in enumerate(class_records, start=1):
        hits = label_index.get(class_name.strip(), [])
        if len(hits) != 1:
            unmapped_classes += 1

            conflict_type = (
                "missing_label_match" if not hits else "ambiguous_label_match"
            )
            cand_subjects = ";".join(str(s) for s, _ in hits)
            cand_labels = ";".join(_fmt_lit(label_lit) for _, label_lit in hits)

            unmapped_label_rows.append(
                [
                    "class",  # kind
                    conflict_type,  # conflict_type
                    str(json_idx),  # json_index (1-based within class_records)
                    _tsv_escape(class_name),  # json_name
                    _tsv_escape(class_name.strip()),  # label_key used for lookup
                    str(len(hits)),  # hit_count
                    "",  # synonyms (n/a)
                    _tsv_escape(pkg_path),  # package_path
                    _tsv_escape(cand_subjects),  # candidate_subjects
                    _tsv_escape(cand_labels),  # candidate_labels
                ]
            )
            continue

        subj, _ = hits[0]
        pkg_iri = _package_iri(pkg_path)

        if MIGRATE_PERCENT_ENCODED_PACKAGE_IRIS:
            legacy = [
                (subj, DCTERMS.isPartOf, obj)
                for obj in g.objects(subj, DCTERMS.isPartOf)
                if isinstance(obj, URIRef)
                and _is_legacy_percent_encoded_package_iri(obj)
            ]
            for t in legacy:
                g.remove(t)
            removed_legacy_partof += len(legacy)

        if RECONCILE_PACKAGE_MEMBERSHIP:
            stale = [
                (subj, DCTERMS.isPartOf, obj)
                for obj in g.objects(subj, DCTERMS.isPartOf)
                if isinstance(obj, URIRef)
                and str(obj).startswith(f"{HRIO_NS_STR}package/")
                and obj != pkg_iri
            ]
            for t in stale:
                g.remove(t)
            removed_stale_partof += len(stale)

        if (subj, DCTERMS.isPartOf, pkg_iri) not in g:
            g.add((subj, DCTERMS.isPartOf, pkg_iri))
            added_partof += 1

    # 2.3) Add vs:term_status on each package IRI
    added_term_status = 0
    removed_term_status = 0
    packages_without_stage = 0

    for pkg_path, stage in package_stage.items():
        pkg_iri = _package_iri(pkg_path)
        existing = list(g.objects(pkg_iri, VS.term_status))

        if stage is None:
            packages_without_stage += 1
            # Optional: if you want "no stage" => ensure no vs:term_status remains
            if RECONCILE_PACKAGE_STATUS and existing:
                for o in existing:
                    g.remove((pkg_iri, VS.term_status, o))
                removed_term_status += len(existing)
            continue

        desired = Literal(stage)

        if RECONCILE_PACKAGE_STATUS:
            stale = [o for o in existing if o != desired]
            for o in stale:
                g.remove((pkg_iri, VS.term_status, o))
            removed_term_status += len(stale)

        if (pkg_iri, VS.term_status, desired) not in g:
            g.add((pkg_iri, VS.term_status, desired))
            added_term_status += 1

    # 3) Add rdfs:isDefinedBy to all hrio:* resources (includes package nodes)
    added_is_defined_by = _add_is_defined_by(g)

    # 4) Normalize rdfs:comment line endings
    normalized_comments = _normalize_comment_line_endings(g)

    # 5) Mirror again so package rdfs:label also produces skos:prefLabel
    added_pref_2, pref_conflicts_2 = _mirror_rdfs_label_to_skos_preflabel(g)

    _validate_ontology_metadata_present(g)

    total_changes = (
        added_pref_1
        + added_alt
        + pkg_resource_stats["created_pkg_type_skos_collection"]
        + pkg_resource_stats["created_pkg_rdfs_label"]
        + pkg_resource_stats["created_pkg_rdfs_label_from_existing_pref"]
        + removed_legacy_pkg_subject_triples
        + added_partof
        + removed_stale_partof
        + removed_legacy_partof
        + added_term_status
        + removed_term_status
        + added_is_defined_by
        + normalized_comments
        + added_pref_2
    )

    if unmapped_label_rows:
        report_path = ttl_path.with_suffix(".unmapped-label-matches.tsv")
        header = [
            "kind",
            "conflict_type",
            "json_index",
            "json_name",
            "label_key",
            "hit_count",
            "synonyms",
            "package_path",
            "candidate_subjects",
            "candidate_labels",
        ]
        lines = ["\t".join(header)]
        lines.extend("\t".join(row) for row in unmapped_label_rows)
        _atomic_write_text(report_path, "\n".join(lines) + "\n", encoding="utf-8")
        logging.info(f"Wrote unmapped-label report: {report_path}")

    if total_changes:
        logging.info(f"Applied {total_changes} change(s); writing updated TTL.")
        _atomic_write_text(ttl_path, g.serialize(format="turtle"), encoding="utf-8")
    else:
        logging.info("Ontology TTL already up to date; no changes applied.")

    return {
        # prefLabel mirrors (two passes; second is mainly for newly added package labels)
        "added_skos_prefLabel_pass1": added_pref_1,
        "skos_prefLabel_conflicts_pass1": pref_conflicts_1,
        "added_skos_prefLabel_pass2": added_pref_2,
        "skos_prefLabel_conflicts_pass2": pref_conflicts_2,
        # synonyms
        "added_skos_altLabel": added_alt,
        "unmapped_synonym_elements": unmapped_synonyms,
        # packages created/ensured
        **pkg_resource_stats,
        "removed_legacy_pkg_subject_triples": removed_legacy_pkg_subject_triples,
        # membership
        "added_dct_isPartOf": added_partof,
        "unmapped_class_elements": unmapped_classes,
        "removed_stale_dct_isPartOf": removed_stale_partof,
        "removed_legacy_dct_isPartOf": removed_legacy_partof,
        # status
        "added_vs_term_status": added_term_status,
        "removed_vs_term_status": removed_term_status,
        "packages_without_stage": packages_without_stage,
        # ownership + cleanup
        "added_rdfs_isDefinedBy": added_is_defined_by,
        "normalized_rdfs_comment": normalized_comments,
    }


def main() -> int:
    try:
        base_dir = _find_base_dir(Path(__file__).resolve().parent)
        versioned_dir = base_dir / VERSIONED_REL

        pair = _find_latest_versioned_pair(versioned_dir)

        logging.info(f"Latest matching pair: v{pair.ver}")
        logging.info(f"TTL : {pair.ttl}")
        logging.info(f"JSON: {pair.js}")

        stats = postprocess_ontology(pair.ttl, pair.js)

        for k in sorted(stats.keys()):
            logging.info(f"{k}: {stats[k]}")

        # Warnings / strict checks
        if (
            stats["skos_prefLabel_conflicts_pass1"]
            or stats["skos_prefLabel_conflicts_pass2"]
        ):
            logging.warning(
                "Some rdfs:label -> skos:prefLabel mirrors were skipped due to existing "
                "prefLabel(s) in the same language."
            )

        if stats["unmapped_synonym_elements"]:
            msg = (
                f"{stats['unmapped_synonym_elements']} synonym-bearing JSON element(s) could not be mapped uniquely "
                f"to an rdfs:label (missing or ambiguous label match)."
            )
            if STRICT_MODE:
                raise RuntimeError(msg)
            logging.warning(msg)

        if stats["unmapped_class_elements"]:
            msg = (
                f"{stats['unmapped_class_elements']} JSON class element(s) could not be mapped uniquely "
                f"to an rdfs:label (missing or ambiguous label match)."
            )
            if STRICT_MODE:
                raise RuntimeError(msg)
            logging.warning(msg)

        if stats["packages_without_stage"]:
            logging.warning(
                f"{stats['packages_without_stage']} package(s) had no effective stage "
                f"(no stage on self or ancestors), so no vs:term_status was written."
            )

        return 0
    except Exception as e:
        logging.error(str(e))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
