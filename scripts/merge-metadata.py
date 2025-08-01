import re
import logging
from pathlib import Path
from packaging import version
from datetime import date
from rdflib import Graph, Literal, URIRef
from rdflib.namespace import XSD, DCTERMS, DCAT

logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")


def get_latest_ttl_file(directory):
    """
    Finds the latest TTL file in the specified directory based on semantic versioning
    embedded in the filename. It assumes the filename format:
    'Health-RI Ontology-v<MAJOR>.<MINOR>.<PATCH>.ttl'.

    Args:
        directory (str or Path): Path to the directory containing the TTL files.

    Returns:
        Tuple[Path or None, str or None]: Path to the latest versioned TTL file and its version string,
        or (None, None) if no valid file is found.
    """
    pattern = r"^Health-RI Ontology-v(\d+\.\d+\.\d+)\.ttl$"
    latest_version = None
    latest_file = None
    version_str = None

    logging.debug(f"Looking for TTL files in: {directory.resolve()}")

    for file in Path(directory).glob("Health-RI Ontology-v*.ttl"):
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
    graph.bind("health-ri", "https://w3id.org/health-ri/ontology#")
    graph.bind("dct", DCTERMS)
    graph.bind("dcat", DCAT)


def merge_ttl_files(latest_a: Path, b_path: Path, version_str: str):
    """
    Merges TTL file B into the latest version of TTL file A and overwrites A.
    Also adds dct:modified and dcat:version triples if metadata was merged.

    Args:
        latest_a (Path): Path to the latest TTL file A.
        b_path (Path): Path to file B.
        version_str (str): The version string to include in dcat:version.
    """
    g_a = Graph()
    g_a.parse(latest_a, format="turtle")

    g_b = Graph()
    g_b.parse(b_path, format="turtle")

    g_a += g_b

    # Add dct:modified and dcat:version triples
    today = date.today().isoformat()
    modified_literal = Literal(today, datatype=XSD.date)
    version_literal = Literal(version_str)

    ontology_uri = URIRef("https://w3id.org/health-ri/ontology")

    g_a.add((ontology_uri, DCTERMS.modified, modified_literal))
    g_a.add((ontology_uri, DCAT.version, version_literal))

    bind_common_prefixes(g_a)

    g_a.serialize(destination=latest_a, format="turtle")
    logging.info(f"Metadata successfully merged. File saved to: {latest_a.resolve()}")
    logging.info(f"Added dct:modified = {today} and dcat:version = {version_str}")


if __name__ == "__main__":
    script_dir = Path(__file__).resolve().parent
    directory = script_dir.parent / "ontologies"
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
