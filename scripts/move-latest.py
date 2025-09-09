import re
import logging
from pathlib import Path
from packaging import version
import shutil

logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")


def get_latest_file(directory, extension):
    """
    Finds the latest file based on semantic versioning embedded in the filename.

    Args:
        directory (Path): Directory to search files in.
        extension (str): File extension to filter files by (e.g., 'json', 'ttl', 'vpp').

    Returns:
        Path or None: Path to the latest file or None if no matching file is found.
    """
    pattern = rf"^health-ri-ontology-v(\d+\.\d+\.\d+)\.{extension}$"
    latest_version = None
    latest_file = None

    for file in directory.glob(f"health-ri-ontology-v*.{extension}"):
        match = re.match(pattern, file.name)
        if match:
            file_version = match.group(1)
            try:
                file_version_obj = version.parse(file_version)
                if latest_version is None or file_version_obj > latest_version:
                    latest_version = file_version_obj
                    latest_file = file
            except version.InvalidVersion:
                logging.warning(f"Skipping invalid version: {file_version}")

    return latest_file


def copy_latest_files(versioned_dir, latest_dir, extensions):
    """
    Copies the latest versioned files to the 'latest' directory without version numbers.

    Args:
        versioned_dir (Path): Directory containing versioned files.
        latest_dir (Path): Directory where latest files will be copied.
        extensions (list): List of file extensions to process.
    """
    latest_dir.mkdir(parents=True, exist_ok=True)

    for ext in extensions:
        latest_file = get_latest_file(versioned_dir, ext)
        if latest_file:
            destination_file = latest_dir / f"health-ri-ontology.{ext}"
            shutil.copy2(latest_file, destination_file)
            logging.info(f"Copied '{latest_file.name}' to '{destination_file}'")
        else:
            logging.warning(f"No file found for extension '{ext}'")


if __name__ == "__main__":
    script_dir = Path(__file__).resolve().parent
    versioned_dir = script_dir.parent / "ontologies" / "versioned"
    latest_dir = script_dir.parent / "ontologies" / "latest"

    file_extensions = ["json", "ttl", "vpp"]

    copy_latest_files(versioned_dir, latest_dir, file_extensions)
