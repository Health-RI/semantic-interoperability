import re
import subprocess
import logging
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


def fix_internal_links_in_html(file_path: Path):
    """
    Replaces absolute file:// links to internal anchors with relative '#anchor' links.
    """
    try:
        html = file_path.read_text(encoding="utf-8")
        # Replace href="file:///.../specification.html#SomeAnchor" → href="#SomeAnchor"
        fixed_html = re.sub(
            r'href="file://[^"]*/specification\.html#([^"]+)"',
            r'href="#\1"',
            html
        )
        file_path.write_text(fixed_html, encoding="utf-8")
        logging.info("Patched internal file:// links to use relative anchors (#...).")
    except Exception as e:
        logging.warning(f"Could not patch internal links: {e}")


def main():
    logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")

    # Define directories
    base_dir = Path(__file__).resolve().parent.parent
    ttl_dir = base_dir / "ontologies"
    output_file = base_dir / "docs/ontology/specification.html"

    latest_ttl = get_latest_ttl_file(ttl_dir)
    if not latest_ttl:
        logging.error("No valid TTL files found in 'ontologies/'.")
        return

    logging.info(f"Generating specification from: {latest_ttl}")
    try:
        subprocess.run([
            "pylode",
            str(latest_ttl),
            "-o",
            str(output_file)
        ], check=True)
        logging.info(f"Specification generated at: {output_file}")

        # Post-process the file to fix broken internal links
        fix_internal_links_in_html(output_file)

    except subprocess.CalledProcessError as e:
        logging.error(f"PyLODE generation failed: {e}")


if __name__ == "__main__":
    main()
