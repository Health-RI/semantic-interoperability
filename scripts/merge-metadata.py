import re
import logging
from pathlib import Path
from packaging import version
from rdflib import Graph

logging.basicConfig(level=logging.INFO)

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
    print(f"Merged and saved to: {latest_a.resolve()}")


if __name__ == "__main__":
    directory = Path("../ontologies")
    ttl_metadata_path = Path("utils/metadata-template.ttl")

    latest_gufo_path = get_latest_ttl_file(directory)

    if latest_gufo_path and ttl_metadata_path.exists():
        merge_ttl_files(latest_gufo_path, ttl_metadata_path)
    else:
        if not latest_gufo_path:
            print("No valid TTL file found in:", directory)
        if not ttl_metadata_path.exists():
            print("Metadata file not found at:", ttl_metadata_path.resolve())
