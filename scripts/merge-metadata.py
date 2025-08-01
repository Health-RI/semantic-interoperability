import re
import logging
from pathlib import Path
from packaging import version
from rdflib import Graph, Literal, Namespace
from rdflib.namespace import XSD

logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")


def get_latest_ttl_file(directory):
    """
    Finds the latest TTL file in the specified directory based on semantic versioning
    embedded in the filename. It assumes the filename format:
    'Health-RI Ontology-v<MAJOR>.<MINOR>.<PATCH>.ttl'.

    Args:
        directory (str or Path): Path to the directory containing the TTL files.

    Returns:
        Path or None: Path to the latest versioned TTL file, or None if no valid file is found.
    """
    pattern = r"^Health-RI Ontology-v(\d+\.\d+\.\d+)\.ttl$"
    latest_version = None
    latest_file = None

    for file in Path(directory).glob("Health-RI Ontology-v*.ttl"):
        match = re.match(pattern, file.name)
        if match:
            file_version = match.group(1)
            try:
                file_version_obj = version.parse(file_version)
                if latest_version is None or file_version_obj > latest_version:
                    latest_version = file_version_obj
                    latest_file = file
            except version.InvalidVersion:
                logging.info(f"Skipping invalid version: {file_version}")

    return latest_file


def should_merge_metadata(graph: Graph) -> bool:
    """
    Determines whether metadata should be merged by checking if
    the triple ?s dct:issued "2025-05-20"^^xsd:date already exists.

    Args:
        graph (Graph): The RDF graph to check.

    Returns:
        bool: True if the metadata is NOT present and should be merged; False otherwise.
    """
    DCT = Namespace("http://purl.org/dc/terms/")
    issued_literal = Literal("2025-05-20", datatype=XSD.date)

    for _ in graph.subjects(predicate=DCT.issued, object=issued_literal):
        return False  # Metadata already present
    return True  # Metadata not present


def merge_ttl_files(latest_a: Path, b_path: Path):
    """
    Merges TTL file B into the latest version of TTL file A and overwrites A.

    Args:
        latest_a (Path): Path to the latest TTL file A.
        b_path (Path): Path to file B.
    """
    g_a = Graph()
    g_a.parse(latest_a, format="turtle")

    g_b = Graph()
    g_b.parse(b_path, format="turtle")

    g_a += g_b

    # Explicitly bind prefixes (important for serialization output)
    g_a.bind("rdf", "http://www.w3.org/1999/02/22-rdf-syntax-ns#")
    g_a.bind("rdfs", "http://www.w3.org/2000/01/rdf-schema#")
    g_a.bind("owl", "http://www.w3.org/2002/07/owl#")
    g_a.bind("xsd", "http://www.w3.org/2001/XMLSchema#")
    g_a.bind("gufo", "http://purl.org/nemo/gufo#")
    g_a.bind("health-ri", "https://w3id.org/health-ri/ontology#")

    # Overwrite file A with the merged graph
    g_a.serialize(destination=latest_a, format="turtle")
    logging.info(f"Metadata sucessfully merged. File saved to: {latest_a.resolve()}")


if __name__ == "__main__":
    directory = Path("../ontologies")
    ttl_metadata_path = Path("scripts/utils/metadata-template.ttl")

    latest_gufo_path = get_latest_ttl_file(directory)

    if latest_gufo_path and ttl_metadata_path.exists():
        current_graph = Graph()
        current_graph.parse(latest_gufo_path, format="turtle")

        if should_merge_metadata(current_graph):
            merge_ttl_files(latest_gufo_path, ttl_metadata_path)
        else:
            logging.info(f"Metadata already present in: {latest_gufo_path.name}")
    else:
        if not latest_gufo_path:
            logging.warning(f"No valid TTL file found in: {directory}")
        if not ttl_metadata_path.exists():
            logging.warning(
                f"Metadata file not found at: {ttl_metadata_path.resolve()}"
            )
