import re
import logging
from pathlib import Path
from packaging import version
from datetime import date
from rdflib import Graph, Literal, URIRef, Namespace
from rdflib.namespace import XSD, DCTERMS, OWL

logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")

DCAT = Namespace("http://www.w3.org/ns/dcat#")

# Option: if True, include only the latest patch for each (MAJOR, MINOR) line among prior versions.
# Example: for 1.2.0, 1.2.1, 1.2.2 -> keep only 1.2.2.
LATEST_PER_MINOR = True


def move_ontology_block_to_top(ttl_text: str, ontology_iri: str) -> str:
    # Find the *ontology* subject block (avoid earlier occurrences where the IRI appears as an object).
    start = ttl_text.find(f"<{ontology_iri}> a owl:Ontology")
    if start == -1:
        return ttl_text

    # Turtle blocks in your file are separated by a blank line.
    end = ttl_text.find("\n\n", start)
    if end == -1:
        end = len(ttl_text)
    else:
        end += 2  # keep the blank line separator

    block = ttl_text[start:end].strip() + "\n\n"
    rest = ttl_text[:start] + ttl_text[end:]

    # Keep @prefix/@base lines at the very top.
    header_re = re.compile(r"(?s)^(?:@prefix[^\n]*\n|@base[^\n]*\n)+\n")
    hm = header_re.match(rest)
    if hm:
        header = hm.group(0)
        body = rest[len(header) :].lstrip()
        return header + block + body

    return block + rest.lstrip()


def get_previous_versions(directory: Path, current_version_str: str, latest_per_minor: bool = False) -> list[str]:
    """
    Returns versions found in directory that are strictly lower than current_version_str.

    - If latest_per_minor is False: returns all prior versions (sorted ascending).
    - If latest_per_minor is True: returns only the latest patch for each (MAJOR, MINOR) line
      among prior versions (sorted ascending).

    Assumes filename format: 'health-ri-ontology-v<MAJOR>.<MINOR>.<PATCH>.ttl'
    """
    pattern = r"^health-ri-ontology-v(\d+\.\d+\.\d+)\.ttl$"
    current_v = version.parse(current_version_str)

    prior: list[tuple[object, str]] = []
    for f in Path(directory).glob("health-ri-ontology-v*.ttl"):
        m = re.match(pattern, f.name)
        if not m:
            continue
        v_str = m.group(1)
        try:
            v_obj = version.parse(v_str)
        except version.InvalidVersion:
            continue

        if v_obj < current_v:
            prior.append((v_obj, v_str))

    if not latest_per_minor:
        prior.sort(key=lambda x: x[0])
        return [v_str for _, v_str in prior]

    # Keep only the latest patch for each (major, minor) among prior versions
    best_by_minor: dict[tuple[int, int], tuple[object, str]] = {}
    for v_obj, v_str in prior:
        release = getattr(v_obj, "releaseU", None)  # force miss? no; keep safe fallback below

    best_by_minor = {}
    for v_obj, v_str in prior:
        release = getattr(v_obj, "release", None)
        if not release or len(release) < 2:
            continue
        major, minor = int(release[0]), int(release[1])
        key = (major, minor)
        if key not in best_by_minor or v_obj > best_by_minor[key][0]:
            best_by_minor[key] = (v_obj, v_str)

    selected = list(best_by_minor.values())
    selected.sort(key=lambda x: x[0])
    return [v_str for _, v_str in selected]


def make_ontology_version_iri(version_str: str) -> URIRef:
    # Keep consistent with OWL.versionIRI in this script
    return URIRef(f"https://w3id.org/health-ri/ontology/v{version_str}")


def get_latest_ttl_file(directory):
    """
    Finds the latest TTL file in the specified directory based on semantic versioning
    embedded in the filename. It assumes the filename format:
    'health-ri-ontology-v<MAJOR>.<MINOR>.<PATCH>.ttl'.

    Args:
        directory (str or Path): Path to the directory containing the TTL files.

    Returns:
        Tuple[Path or None, str or None]: Path to the latest versioned TTL file and its version string,
        or (None, None) if no valid file is found.
    """
    pattern = r"^health-ri-ontology-v(\d+\.\d+\.\d+)\.ttl$"
    latest_version = None
    latest_file = None
    version_str = None

    logging.debug(f"Looking for TTL files in: {directory.resolve()}")

    for file in Path(directory).glob("health-ri-ontology-v*.ttl"):
        logging.debug(f"Checking file: {file.name}")
        match = re.match(pattern, file.name)
        if match:
            file_version = match.group(1)
            logging.debug(f"Matched version: {file_version}")
            try:
                file_version_obj = version.parse(file_version)
                if latest_version is None or file_version_obj > latest_version:
                    latest_version = file_version_obj
                    latest_file = file
                    version_str = file_version
            except version.InvalidVersion:
                logging.info(f"Skipping invalid version: {file_version}")

    return latest_file, version_str


def get_immediate_previous_version(directory: Path, current_version_str: str) -> str | None:
    """
    Returns the highest version strictly lower than current_version_str, based on versions
    present as files in the directory (SemVer ordering).
    """
    pattern = r"^health-ri-ontology-v(\d+\.\d+\.\d+)\.ttl$"
    current_v = version.parse(current_version_str)

    best_v_obj = None
    best_v_str = None

    for f in Path(directory).glob("health-ri-ontology-v*.ttl"):
        m = re.match(pattern, f.name)
        if not m:
            continue
        v_str = m.group(1)
        try:
            v_obj = version.parse(v_str)
        except version.InvalidVersion:
            continue

        if v_obj < current_v and (best_v_obj is None or v_obj > best_v_obj):
            best_v_obj = v_obj
            best_v_str = v_str

    return best_v_str


def move_subject_block_after(ttl_text: str, subject_iri: str, anchor_iri: str) -> str:
    # Preserve @prefix/@base header at the very top
    header_re = re.compile(r"(?s)^(?:@prefix[^\n]*\n|@base[^\n]*\n)+\n")
    hm = header_re.match(ttl_text)
    header = hm.group(0) if hm else ""
    body = ttl_text[len(header) :] if hm else ttl_text

    def block_regex(iri: str) -> re.Pattern:
        # Match a subject block starting at beginning of a line, until blank line or end of file
        return re.compile(rf"(?ms)^<{re.escape(iri)}>\s.*?(?:\n\n|\Z)")

    subj_re = block_regex(subject_iri)
    anc_re = block_regex(anchor_iri)

    subj_m = subj_re.search(body)
    anc_m = anc_re.search(body)
    if not subj_m or not anc_m:
        return ttl_text

    subj_block = subj_m.group(0).strip() + "\n\n"
    body_wo_subj = body[: subj_m.start()] + body[subj_m.end() :]

    # Re-find anchor after removal (safe even if subject was above anchor)
    anc_m2 = anc_re.search(body_wo_subj)
    if not anc_m2:
        return header + body_wo_subj

    insert_at = anc_m2.end()
    before = body_wo_subj[:insert_at]
    after = body_wo_subj[insert_at:].lstrip("\n")

    if not before.endswith("\n\n"):
        before = before.rstrip("\n") + "\n\n"

    return header + before + subj_block + after.lstrip()


def should_merge_metadata(graph: Graph) -> bool:
    """
    Determines whether metadata should be merged by checking if
    the triple ?s dct:issued "2025-05-20"^^xsd:date already exists.

    Args:
        graph (Graph): The RDF graph to check.

    Returns:
        bool: True if the metadata is NOT present and should be merged; False otherwise.
    """
    issued_literal = Literal("2025-05-20", datatype=XSD.date)

    for _ in graph.subjects(predicate=DCTERMS.issued, object=issued_literal):
        return False  # Metadata already present
    return True  # Metadata not present


def bind_common_prefixes(graph: Graph) -> None:
    """
    Binds commonly used prefixes to the given RDFLib graph.
    """
    graph.bind("rdf", "http://www.w3.org/1999/02/22-rdf-syntax-ns#")
    graph.bind("rdfs", "http://www.w3.org/2000/01/rdf-schema#")
    graph.bind("owl", "http://www.w3.org/2002/07/owl#")
    graph.bind("xsd", "http://www.w3.org/2001/XMLSchema#")
    graph.bind("gufo", "http://purl.org/nemo/gufo#")
    graph.bind("hrio", "https://w3id.org/health-ri/ontology#")
    graph.bind("dct", DCTERMS)
    graph.bind("mod", "https://w3id.org/mod#")
    graph.bind("dcat", DCAT)


def merge_ttl_files(latest_a: Path, b_path: Path, version_str: str):
    """
    Merges TTL file B into the latest version of TTL file A and overwrites A.
    Also adds dct:modified, owl:versionInfo, owl:versionIRI, two dct:conformsTo triples,
    and dcat:hasVersion for prior versions found in the versioned folder.

    Args:
        latest_a (Path): Path to the latest TTL file A.
        b_path (Path): Path to file B.
        version_str (str): The version string to include in metadata triples.
    """
    g_a = Graph()
    g_a.parse(latest_a, format="turtle")

    g_b = Graph()
    g_b.parse(b_path, format="turtle")

    g_a += g_b
    for prefix, ns in g_b.namespace_manager.namespaces():
        g_a.bind(prefix, ns, override=False)

    today = date.today().isoformat()

    ontology_uri = URIRef("https://w3id.org/health-ri/ontology")
    version_iri = URIRef(f"https://w3id.org/health-ri/ontology/v{version_str}")
    conforms_to_vpp = URIRef(f"https://w3id.org/health-ri/ontology/v{version_str}/vpp")
    conforms_to_json = URIRef(f"https://w3id.org/health-ri/ontology/v{version_str}/json")

    g_a.add((ontology_uri, DCTERMS.modified, Literal(today, datatype=XSD.date)))
    g_a.add((ontology_uri, OWL.versionInfo, Literal(version_str)))
    g_a.add((ontology_uri, OWL.versionIRI, version_iri))
    g_a.add((ontology_uri, DCTERMS.conformsTo, conforms_to_vpp))
    g_a.add((ontology_uri, DCTERMS.conformsTo, conforms_to_json))

    # owl:priorVersion: point to the immediate predecessor version IRI (highest < current)
    prev_version_str = get_immediate_previous_version(latest_a.parent, version_str)
    if prev_version_str:
        prev_version_iri = URIRef(f"https://w3id.org/health-ri/ontology/v{prev_version_str}")

        # Make reruns idempotent
        for o in list(g_a.objects(version_iri, OWL.priorVersion)):
            g_a.remove((version_iri, OWL.priorVersion, o))

        g_a.add((version_iri, OWL.priorVersion, prev_version_iri))

    # dcat:hasVersion: prior versions from the versioned folder
    for o in list(g_a.objects(ontology_uri, DCAT.hasVersion)):
        g_a.remove((ontology_uri, DCAT.hasVersion, o))

    version_dir = latest_a.parent
    prior_versions = get_previous_versions(version_dir, version_str, latest_per_minor=LATEST_PER_MINOR)
    for prev_v in prior_versions:
        g_a.add((ontology_uri, DCAT.hasVersion, make_ontology_version_iri(prev_v)))

    bind_common_prefixes(g_a)

    ttl_text = g_a.serialize(format="turtle")
    ttl_text = move_ontology_block_to_top(ttl_text, "https://w3id.org/health-ri/ontology")
    ttl_text = move_subject_block_after(
        ttl_text,
        f"https://w3id.org/health-ri/ontology/v{version_str}",
        "https://w3id.org/health-ri/ontology",
    )
    latest_a.write_text(ttl_text, encoding="utf-8")
    logging.info(f"Metadata successfully merged. File saved to: {latest_a.resolve()}")
    logging.info(
        f"Added dct:modified = {today}, owl:versionInfo = {version_str}, owl:versionIRI = {version_iri}, "
        f"dct:conformsTo = {conforms_to_vpp}, dct:conformsTo = {conforms_to_json}, "
        f"dcat:hasVersion count = {len(prior_versions)} (latest-per-minor={LATEST_PER_MINOR})"
    )


if __name__ == "__main__":
    script_dir = Path(__file__).resolve().parent
    directory = script_dir.parent / "ontologies" / "versioned"
    ttl_metadata_path = script_dir / "utils" / "metadata-template.ttl"

    latest_gufo_path, version_str = get_latest_ttl_file(directory)

    if latest_gufo_path and version_str and ttl_metadata_path.exists():
        current_graph = Graph()
        current_graph.parse(latest_gufo_path, format="turtle")

        if should_merge_metadata(current_graph):
            merge_ttl_files(latest_gufo_path, ttl_metadata_path, version_str)
        else:
            logging.info(f"Metadata already present in: {latest_gufo_path.name}")
    else:
        if not latest_gufo_path:
            logging.warning(f"No valid TTL file found in: {directory}")
        if not ttl_metadata_path.exists():
            logging.warning(f"Metadata file not found at: {ttl_metadata_path.resolve()}")
