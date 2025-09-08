"""
Quick-and-dirty SSSOM TSV -> TTL converter
------------------------------------------

Scope:
- Tailored to the attached Health-RI SSSOM file.
- Emits *direct triples* (subject_id, predicate_id, object_id) only.
- Optionally adds rdfs:label from subject_label/object_label (supports '@lang').
- Tries to parse a simple prefix map from commented metadata ('# prefixes:' or '# curie_map:').
- Falls back to common prefixes if none found.

Out of scope:
- Full SSSOM OWL reification / mapping metadata graph.
- Complex multi-valued slot parsing, external metadata mode, etc.

Usage:
    python tsv2ttl.py -i /path/to/health-ri-mappings.tsv -o /path/to/health-ri-mappings.ttl

Requirements:
    pip install rdflib
"""

import logging
import re
from pathlib import Path
from typing import Dict, List, Tuple, Optional

from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import RDF, RDFS, OWL, XSD
from rdflib.namespace import DCAT

PAV = Namespace("http://purl.org/pav/")

logger = logging.getLogger("sssom-tsv2ttl")
logging.basicConfig(level=logging.INFO, format=" %(levelname)s: %(name)s: %(message)s")


def read_lines(p: Path) -> List[str]:
    """Read a UTF-8 text file and return its contents split into lines.

    Parameters
    ----------
    p : Path
        Path to the input file.

    Returns
    -------
    List[str]
        File contents as a list of lines (without trailing newlines).
    """
    return p.read_text(encoding="utf-8").splitlines()


def parse_metadata_from_comments(comment_lines: List[str]) -> Dict[str, List[str]]:
    """Parse selected metadata keys from the commented header block.

    This reads a minimal YAML-like structure from comment lines (already
    stripped of the leading '#'). It supports both inline `key: value` and
    simple lists:

        key:
          - value1
          - value2

    Only a fixed set of keys is collected (see the `wanted` set). Values are
    returned uniformly as lists of strings for downstream processing.

    Parameters
    ----------
    comment_lines : List[str]
        Lines from the top-of-file comments (without leading '#'), with
        indentation preserved.

    Returns
    -------
    Dict[str, List[str]]
        Mapping from key to list of string values.
    """
    wanted = {
        "creator_id",
        "comment",
        "see_also",
        "publication_date",
        "mapping_set_description",
        "mapping_set_title",
        "mapping_set_version",
        "sssom_version",
        "mapping_set_id",
        "issue_tracker",
        "license",
    }

    meta: Dict[str, List[str]] = {}
    i = 0
    n = len(comment_lines)

    # normalize helper

    def add_value(k: str, v: str):
        if not v:
            return
        meta.setdefault(k, []).append(v.strip())

    while i < n:
        raw = comment_lines[i]
        line = raw.rstrip()
        m = re.match(r"^\s*([A-Za-z0-9_]+)\s*:\s*(.*)$", line)
        if m:
            key = m.group(1)
            if key in wanted:
                inline = m.group(2).strip()
                # Case 1: inline value on the same line

                if inline:
                    # Allow comma-separated for quick-and-dirty multi-values

                    parts = [p.strip() for p in inline.split(",") if p.strip()]
                    for p in parts:
                        add_value(key, p)
                else:
                    # Case 2: possible simple YAML list in following indented '- ' lines

                    j = i + 1
                    while j < n:
                        nxt = comment_lines[j]
                        if re.match(r"^\s*-\s+(.*)$", nxt):
                            add_value(key, re.match(r"^\s*-\s+(.*)$", nxt).group(1))
                            j += 1
                            continue
                        # stop at first non-list or empty line with less/equal indent

                        if not nxt.startswith((" ", "\t")) or not nxt.strip():
                            break
                        j += 1
                    i = j - 1  # adjust outer loop
        i += 1
    return meta


def detect_header_and_rows(lines: List[str]) -> Tuple[List[str], List[str], List[str]]:
    """Split a TSV file into (commented header, column header, data rows).

    The function walks the file from top to bottom:
    - Lines starting with '#' (after optional leading whitespace) are collected
      as `comment_lines` with the '#' removed but indentation preserved.
    - The first non-empty, non-comment line is taken as the tab-separated
      header row and split into `header_cols`.
    - Subsequent non-empty lines are collected as raw `data_rows`.

    Parameters
    ----------
    lines : List[str]
        Full file as a list of raw lines.

    Returns
    -------
    Tuple[List[str], List[str], List[str]]
        (comment_lines, header_cols, data_rows)

    Raises
    ------
    RuntimeError
        If a header row cannot be found.
    """
    comment_lines: List[str] = []
    header_cols: Optional[List[str]] = None
    data_rows: List[str] = []

    for line in lines:
        if line.lstrip().startswith("#"):
            # Keep indentation *after* '#' so curie_map entries remain indented

            m = re.match(r"^\s*#\s?(.*)$", line.rstrip("\n"))
            if m:
                comment_lines.append(m.group(1))  # preserve leading spaces inside the block
            else:
                comment_lines.append("")  # fallback, shouldn't happen
            continue
        if not line.strip():
            continue
        if header_cols is None:
            header_cols = [c.strip() for c in line.rstrip("\n").split("\t")]
        else:
            data_rows.append(line.rstrip("\n"))
    if header_cols is None:
        raise RuntimeError("Could not find a header row in the TSV.")
    return comment_lines, header_cols, data_rows


def parse_prefix_map_from_comments(comment_lines: List[str]) -> Dict[str, str]:
    """Extract a CURIE prefix map from a `curie_map:` block in comments.

    The function searches for a line matching `curie_map:` (case-insensitive),
    then collects immediately following indented lines of the form:
        <indent><prefix>: <IRI>
    Collection stops at the first non-indented or empty line.

    Parameters
    ----------
    comment_lines : List[str]
        Commented header lines (without leading '#'), indentation preserved.

    Returns
    -------
    Dict[str, str]
        Mapping from prefix to base IRI. Empty if no `curie_map:` block found.
    """
    prefix_map: Dict[str, str] = {}

    # Find the line 'curie_map:' (case-insensitive) in the comment block

    start_idx = None
    for i, raw in enumerate(comment_lines):
        line = raw.strip()
        if re.match(r"^curie_?map\s*:\s*$", line, flags=re.IGNORECASE):
            start_idx = i + 1
            break
    if start_idx is None:
        return prefix_map  # no curie_map block found
    # Collect only the INDENTED lines immediately following the 'curie_map:' marker

    for raw in comment_lines[start_idx:]:
        # Stop at the first non-indented or empty line

        if not raw or not raw.startswith((" ", "\t")):
            break
        # Expect: <indent><prefix> : <IRI>

        m = re.match(r"^\s*([A-Za-z0-9_\-]+)\s*:\s*(\S+)\s*$", raw)
        if m:
            pfx, iri = m.groups()
            prefix_map[pfx] = iri
        # else: ignore anything that doesn't match <pfx>: <IRI> on an indented line
    return prefix_map


def expand_curie_or_iri(value: str, prefix_map: Dict[str, str]) -> URIRef:
    """Expand a CURIE or pass through an absolute IRI into an RDFLib URIRef.

    Behavior:
    - If `value` matches a real IRI scheme (e.g., `http://`), return as URIRef.
    - If `value` is of the form `pfx:local` and `pfx` is in `prefix_map`,
      concatenate base IRI + local and return as URIRef.
    - If `value` contains no colon, treat it as a bare IRI and return.
    - Otherwise, return the original string as a URIRef (best-effort).

    Parameters
    ----------
    value : str
        A CURIE (e.g., 'hrio:MaleBiologicalPerson') or absolute IRI.
    prefix_map : Dict[str, str]
        Known CURIE prefix base IRIs.

    Returns
    -------
    URIRef
        Expanded or passed-through URIRef.
    """
    v = value.strip()
    if ":" not in v:
        return URIRef(v)
    pfx, local = v.split(":", 1)

    # Treat only real IRIs (with scheme://) as absolute

    if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*://", v):
        return URIRef(v)
    base = prefix_map.get(pfx)
    if base:
        return URIRef(base + local)
    # Last-resort: keep as-is (opaque); crude but acceptable for quick-and-dirty

    return URIRef(value)


def parse_label_with_lang(value: Optional[str]) -> Tuple[Optional[str], Optional[str]]:
    """Parse a label string with optional language tag (e.g., 'Man@nl').

    This function also strips any surrounding quotes from the label text,
    so values like '"Zoogdier"@nl' become ('Zoogdier', 'nl').

    Parameters
    ----------
    value : Optional[str]
        Raw label value from the TSV (may be None, empty, or include quotes).

    Returns
    -------
    Tuple[Optional[str], Optional[str]]
        (text, lang) where `lang` is the language code (e.g., 'en', 'nl')
        or None if not present; `text` is None if input was None/blank.
    """
    if value is None:
        return None, None
    v = value.strip().strip('"')  # remove extra quotes
    if not v:
        return None, None
    m = re.match(r"^(.*)@([a-zA-Z-]+)$", v)
    if m:
        text = m.group(1).strip().strip('"')
        lang = m.group(2)
        return text, lang
    return v, None


def render_prefix_block(prefix_map: Dict[str, str]) -> str:
    """Render a Turtle @prefix header from a prefix map.

    Produces deterministic output by sorting prefixes alphabetically.

    Parameters
    ----------
    prefix_map : Dict[str, str]
        Mapping from prefix to base IRI.

    Returns
    -------
    str
        Lines of Turtle @prefix declarations ending with a blank line.
    """
    items = sorted(prefix_map.items(), key=lambda kv: kv[0])  # sort for stability
    return "\n".join([f"@prefix {pfx}: <{iri}> ." for pfx, iri in items]) + "\n\n"


ENTITY_TYPE_MAP = {
    # canonical SSSOM values (case-insensitive, collapse spaces)
    "owl class":"owl:Class",
    "owl object property":"owl:ObjectProperty",
    "owl data property":"owl:DataProperty",
    "owl annotation property":"owl:AnnotationProperty",
    "owl named individual":"owl:NamedIndividual",
    "skos concept":"skos:Concept",
    "rdfs resource":"rdfs:Resource",
    "rdfs class":"rdfs:Class",
    "rdfs literal":"rdfs:Literal",
    "rdfs datatype":"rdfs:Datatype",
    "rdf property":"rdf:Property",
    "composed entity expression":"sssom:ComposedEntityExpression",
}



def normalize_entity_type(value: Optional[str]) -> str:
    """
    Accepts either:
      - SSSOM EntityTypeEnum *value* (e.g., 'owl class') -> returns CURIE (e.g., 'owl:Class')
      - Already a CURIE/IRI (contains ':') -> returned as-is
      - Empty/unknown -> returns '' (caller skips adding)
    """
    if not value:
        return ""
    v = value.strip()
    if ":" in v:
        # looks like CURIE/IRI; keep
        return v
    # normalize spaces and lowercase for lookup
    key = re.sub(r"\s+", " ", v).lower()
    return ENTITY_TYPE_MAP.get(key, "")


def to_hrim_curie(rid: str) -> str:
    """Normalize a record identifier to an `hrim:` CURIE if needed.

    If `rid` already contains a colon (i.e., already a CURIE/IRI), it is
    returned unchanged; otherwise it is prefixed with 'hrim:'.

    Parameters
    ----------
    rid : str
        Raw record identifier value.

    Returns
    -------
    str
        A CURIE string suitable for expansion with `prefix_map`.
    """
    rid = rid.strip()
    return rid if ":" in rid else f"hrim:{rid}"


def convert_tsv_to_ttl(tsv_path: Path, out_path: Path) -> int:
    """Convert an SSSOM TSV file into a compact Turtle file.

    Workflow
    --------
    1) Read and split file into comments, header, and rows.
    2) Parse `curie_map` prefixes and free-text metadata from comments.
    3) Ensure core prefixes are present to avoid ns1/ns2 fallbacks.
    4) For each data row, mint an `sssom:Mapping` node and attach properties
       according to the quick-and-dirty transformation rules.
    5) Create one `sssom:MappingSet` node, attach metadata, and link all
       mapping nodes via `sssom:mappings`.
    6) Serialize as Turtle, replace RDFLib’s prefix header with our own
       complete `@prefix` block.

    Parameters
    ----------
    tsv_path : Path
        Path to the input SSSOM TSV file.
    out_path : Path
        Path to write the resulting Turtle file.

    Returns
    -------
    int
        Number of triples currently in the graph (as a convenience).
    """
    logger.info("Converting %s -> %s", tsv_path, out_path)

    lines = read_lines(tsv_path)
    comment_lines, header_cols, data_rows = detect_header_and_rows(lines)
    prefix_map = parse_prefix_map_from_comments(comment_lines)
    logger.debug("Parsed %d curie_map prefixes: %s", len(prefix_map), ", ".join(sorted(prefix_map.keys())))
    metadata = parse_metadata_from_comments(comment_lines)
    if metadata:
        logger.debug("Metadata keys detected: %s", ", ".join(sorted(metadata.keys())))
    else:
        logger.info("No metadata keys detected in commented header.")
    prefix_map.setdefault("hrim", "https://w3id.org/health-ri/semantic-interoperability/mappings#")

    # Ensure core prefixes used in output are available (prevents ns1/ns2 fallbacks)

    required_prefixes = {
        "owl": str(OWL),
        "rdfs": str(RDFS),
        "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
        "xsd": str(XSD),
        "pav": str(PAV),
        "dcat": str(DCAT),
        "skos": "http://www.w3.org/2004/02/skos/core#",
    }
    for k, iri in required_prefixes.items():
        prefix_map.setdefault(k, iri)
    g = Graph()
    g.bind("pav", PAV)
    g.bind("dcat", DCAT)
    # Bind prefixes (best-effort)

    for pfx, iri in prefix_map.items():
        try:
            g.bind(pfx, Namespace(iri))
        except Exception:
            pass
    col_idx = {c: i for i, c in enumerate(header_cols)}
    record_id_col = col_idx.get("record_id")
    record_ids = []
    # Minimal required columns for this quick conversion

    required = ["subject_id", "predicate_id", "object_id"]
    missing = [c for c in required if c not in col_idx]
    if missing:
        logger.error("Missing required SSSOM columns: %s", missing)
        raise RuntimeError(f"Missing required SSSOM columns: {missing}")

    for row in data_rows:
        if not row.strip():
            continue
        parts = row.split("\t")
        # Pad parts for safety

        if len(parts) < len(header_cols):
            parts += [""] * (len(header_cols) - len(parts))
        subj = parts[col_idx["subject_id"]].strip()
        pred = parts[col_idx["predicate_id"]].strip()
        obj = parts[col_idx["object_id"]].strip()
        if not subj or not pred or not obj:
            continue
        # Create Mapping node

        mapping_id = expand_curie_or_iri(to_hrim_curie(parts[col_idx["record_id"]].strip()), prefix_map)
        g.add((mapping_id, RDF.type, expand_curie_or_iri("sssom:Mapping", prefix_map)))

        def add_literal(prop, val, lang=None, datatype=None):
            if val is None:
                return
            v = val.strip()
            if v == "":
                return
            if datatype:
                g.add((mapping_id, expand_curie_or_iri(prop, prefix_map), Literal(v, datatype=datatype)))
            elif lang:
                g.add((mapping_id, expand_curie_or_iri(prop, prefix_map), Literal(v, lang=lang)))
            else:
                g.add((mapping_id, expand_curie_or_iri(prop, prefix_map), Literal(v)))

        def add_resource(prop, val):
            if val is None:
                return
            v = val.strip()
            if v == "":
                return
            g.add((mapping_id, expand_curie_or_iri(prop, prefix_map), expand_curie_or_iri(v, prefix_map)))

        # Apply transformation rules

        add_literal(
            "sssom:record_id",
            parts[col_idx["record_id"]].strip(),
            datatype=XSD.anyURI,
        )
        add_literal(
            "dcterms:identifier",
            parts[col_idx["record_id"]].strip(),
            datatype=XSD.anyURI,
        )
        add_resource("owl:annotatedSource", parts[col_idx["subject_id"]].strip())

        subj_label_val, subj_label_lang = (
            parse_label_with_lang(parts[col_idx.get("subject_label", -1)])
            if col_idx.get("subject_label")
            else (None, None)
        )
        if subj_label_val:
            add_literal("sssom:subject_label", subj_label_val, lang=subj_label_lang)
        add_resource("owl:annotatedProperty", parts[col_idx["predicate_id"]].strip())
        add_literal(
            "sssom:predicate_modifier",
            (parts[col_idx.get("predicate_modifier", -1)].strip() if col_idx.get("predicate_modifier") else ""),
        )

        add_resource("owl:annotatedTarget", parts[col_idx["object_id"]].strip())

        obj_label_val, obj_label_lang = (
            parse_label_with_lang(parts[col_idx.get("object_label", -1)])
            if col_idx.get("object_label")
            else (None, None)
        )
        if obj_label_val:
            add_literal("sssom:object_label", obj_label_val, lang=obj_label_lang)
        add_literal(
            "sssom:object_category",
            (parts[col_idx.get("object_category", -1)].strip() if col_idx.get("object_category") else ""),
        )
        add_resource(
            "sssom:mapping_justification",
            (parts[col_idx.get("mapping_justification", -1)].strip() if col_idx.get("mapping_justification") else ""),
        )

        add_resource(
            "pav:authoredBy",
            (parts[col_idx.get("author_id", -1)].strip() if col_idx.get("author_id") else ""),
        )
        add_literal(
            "sssom:author_label",
            (parts[col_idx.get("author_label", -1)].strip() if col_idx.get("author_label") else ""),
        )

        add_resource(
            "sssom:reviewer_id",
            (parts[col_idx.get("reviewer_id", -1)].strip() if col_idx.get("reviewer_id") else ""),
        )
        add_literal(
            "sssom:reviewer_label",
            (parts[col_idx.get("reviewer_label", -1)].strip() if col_idx.get("reviewer_label") else ""),
        )

        add_resource(
            "dcterms:creator",
            (parts[col_idx.get("creator_id", -1)].strip() if col_idx.get("creator_id") else ""),
        )
        add_literal(
            "sssom:creator_label",
            (parts[col_idx.get("creator_label", -1)].strip() if col_idx.get("creator_label") else ""),
        )

        add_resource(
            "dcterms:license",
            parts[col_idx.get("license", -1)].strip() if col_idx.get("license") else "",
        )

        raw_subj_type = parts[col_idx.get("subject_type", -1)].strip() if col_idx.get("subject_type") else ""
        norm_subj_type = normalize_entity_type(raw_subj_type)
        add_resource("sssom:subject_type", norm_subj_type)

        add_resource(
            "sssom:subject_source",
            (parts[col_idx.get("subject_source", -1)].strip() if col_idx.get("subject_source") else ""),
        )

        add_resource("sssom:object_source", "hrio:")

        add_literal(
            "sssom:subject_source_version",
            (parts[col_idx.get("subject_source_version", -1)].strip() if col_idx.get("subject_source_version") else ""),
        )
        add_literal(
            "sssom:object_source_version",
            (parts[col_idx.get("object_source_version", -1)].strip() if col_idx.get("object_source_version") else ""),
        )

        add_literal(
            "pav:authoredOn",
            (parts[col_idx.get("mapping_date", -1)].strip() if col_idx.get("mapping_date") else ""),
            datatype=XSD.date,
        )
        add_literal(
            "dcterms:issued",
            (parts[col_idx.get("publication_date", -1)].strip() if col_idx.get("publication_date") else ""),
            datatype=XSD.date,
        )

        add_literal(
            "rdfs:comment",
            parts[col_idx.get("comment", -1)].strip() if col_idx.get("comment") else "",
            lang="en",
        )
        add_literal(
            "dcat:replaces",
            (parts[col_idx.get("replaces", -1)].strip() if col_idx.get("replaces") else ""),
        )

        if record_id_col is not None:
            rid = parts[record_id_col].strip()
            if rid:
                record_ids.append(rid)
    # Deduplicate record_ids while preserving order

    record_ids = list(dict.fromkeys(record_ids))
    logger.info("Mappings to emit: %d", len(record_ids))    

    # Add the MappingSet declaration ONCE, after collecting all record_ids

    mapping_set_uri = URIRef("https://w3id.org/health-ri/semantic-interoperability/mappings#")
    g.add((mapping_set_uri, RDF.type, expand_curie_or_iri("sssom:MappingSet", prefix_map)))

    # Link to all mappings via their record_id

    for rid in record_ids:
        g.add(
            (
                mapping_set_uri,
                expand_curie_or_iri("sssom:mappings", prefix_map),
                expand_curie_or_iri(to_hrim_curie(rid), prefix_map),
            )
        )
    # license -> dcterms:license (typed anyURI); fallback if not provided in metadata

    licenses = metadata.get("license", []) or ["https://creativecommons.org/licenses/by/4.0/"]
    for v in licenses:
        g.add(
            (
                mapping_set_uri,
                expand_curie_or_iri("dcterms:license", prefix_map),
                Literal(v, datatype=XSD.anyURI),
            )
        )
    # ---- Add mapping-set metadata from commented header ----
    # creator_id -> dcterms:creator (CURIE/IRI if possible)

    for v in metadata.get("creator_id", []):
        g.add(
            (
                mapping_set_uri,
                expand_curie_or_iri("dcterms:creator", prefix_map),
                expand_curie_or_iri(v, prefix_map),
            )
        )
    # comment -> rdfs:comment (literal, always @en)

    for v in metadata.get("comment", []):
        g.add((mapping_set_uri, RDFS.comment, Literal(v, lang="en")))
    # see_also -> rdfs:seeAlso (treat as IRI/CURIE when possible, else literal)

    for v in metadata.get("see_also", []):
        obj = expand_curie_or_iri(v, prefix_map) if re.match(r"^\w+:", v) or v.startswith("http") else Literal(v)
        g.add((mapping_set_uri, RDFS.seeAlso, obj))
    # publication_date -> dcterms:issued (xsd:date if YYYY-MM-DD)

    for v in metadata.get("publication_date", []):
        if re.match(r"^\d{4}-\d{2}-\d{2}$", v):
            lit = Literal(v, datatype=XSD.date)
        else:
            lit = Literal(v)
        g.add((mapping_set_uri, expand_curie_or_iri("dcterms:issued", prefix_map), lit))
    # mapping_set_description -> dcterms:description (literal, always @en)

    for v in metadata.get("mapping_set_description", []):
        g.add(
            (
                mapping_set_uri,
                expand_curie_or_iri("dcterms:description", prefix_map),
                Literal(v, lang="en"),
            )
        )
    # mapping_set_title -> dcterms:title (literal, always @en)

    for v in metadata.get("mapping_set_title", []):
        g.add(
            (
                mapping_set_uri,
                expand_curie_or_iri("dcterms:title", prefix_map),
                Literal(v, lang="en"),
            )
        )
    # mapping_set_version -> owl:versionInfo (literal)

    for v in metadata.get("mapping_set_version", []):
        g.add((mapping_set_uri, OWL.versionInfo, Literal(v)))
    # sssom_version -> sssom:sssom_version (literal)

    for v in metadata.get("sssom_version", []):
        g.add(
            (
                mapping_set_uri,
                expand_curie_or_iri("sssom:sssom_version", prefix_map),
                Literal(v),
            )
        )
    # mapping_set_id -> dcterms:identifier and sssom:mapping_set_id (typed anyURI)

    for v in metadata.get("mapping_set_id", []):
        uri_lit = Literal(v, datatype=XSD.anyURI)
        g.add(
            (
                mapping_set_uri,
                expand_curie_or_iri("dcterms:identifier", prefix_map),
                uri_lit,
            )
        )
        g.add(
            (
                mapping_set_uri,
                expand_curie_or_iri("sssom:mapping_set_id", prefix_map),
                uri_lit,
            )
        )
    # issue_tracker -> sssom:issue_tracker (typed anyURI)

    for v in metadata.get("issue_tracker", []):
        uri_lit = Literal(v, datatype=XSD.anyURI)
        g.add(
            (
                mapping_set_uri,
                expand_curie_or_iri("sssom:issue_tracker", prefix_map),
                uri_lit,
            )
        )
    # Serialize graph to TTL

    ttl_graph = g.serialize(format="turtle")

    # Build a full @prefix header from the parsed curie_map (always emit all)

    prefix_header = render_prefix_block(prefix_map)

    # Strip ANY @prefix lines RDFLib may have emitted (handles leading spaces too)

    body_no_prefix = "\n".join(line for line in ttl_graph.splitlines() if not re.match(r"^\s*@prefix\s", line))

    # Write: only our curie_map prefixes + cleaned body (no duplicates)

    if not body_no_prefix.endswith("\n"):
        body_no_prefix += "\n"
    out_path.write_text(prefix_header + body_no_prefix, encoding="utf-8")
    logger.info("Wrote Turtle to %s", out_path)
    return len(g)


def main():
    """CLI entry-point.

    Always runs with the fixed input and output paths:
    ../mappings/health-ri-mappings.tsv → ../mappings/health-ri-mappings.ttl
    """
    try:
        tsv_path = Path("./mappings/health-ri-mappings.tsv")
        out_path = Path("./mappings/health-ri-mappings.ttl")

        if not tsv_path.exists():
            logger.error("Input not found: %s", tsv_path)
            raise SystemExit(2)

        n = convert_tsv_to_ttl(tsv_path, out_path)
        logger.info("Finished: %d triples", n)
    except Exception as e:
        logger.exception("Conversion failed: %s", e)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
