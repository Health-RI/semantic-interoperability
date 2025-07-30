import re
import subprocess
from pathlib import Path
from packaging import version


def get_latest_ttl_file(directory: Path):
    pattern = r"Health-RI Ontology-v(\d+\.\d+\.\d+)\.ttl"
    latest_file = None
    latest_version = None

    for file in directory.glob("Health-RI Ontology-v*.ttl"):
        match = re.match(pattern, file.name)
        if match:
            file_version = version.parse(match.group(1))
            if latest_version is None or file_version > latest_version:
                latest_version = file_version
                latest_file = file

    return latest_file


def main():
    # Run from root where 'ontologies/' and 'docs/' are present
    base_dir = Path(__file__).resolve().parent.parent
    ttl_dir = base_dir / "ontologies"
    output_file = base_dir / "docs/ontology/specification.html"

    latest_ttl = get_latest_ttl_file(ttl_dir)
    if not latest_ttl:
        print("No valid TTL files found.")
        return

    print(f"Generating specification from: {latest_ttl}")
    subprocess.run([
        "pylode",
        str(latest_ttl),
        "-o",
        str(output_file)
    ], check=True)


if __name__ == "__main__":
    main()
