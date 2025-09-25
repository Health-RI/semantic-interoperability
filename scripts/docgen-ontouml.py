import json
from pathlib import Path
from packaging import version
import re
import os
import logging
from urllib.parse import quote


def has_meaningful_content(pkg, diagrams_by_owner):
    """
    Determines whether a package contains meaningful content such as a description,
    diagrams with descriptions, or sub-packages with meaningful content. This check
    is performed recursively to support arbitrarily nested packages.

    Args:
        pkg (dict): The package to evaluate.
        diagrams_by_owner (dict): A dictionary mapping owner IDs to their corresponding diagrams.

    Returns:
        bool: True if the package or any of its contents contain meaningful information, False otherwise.
    """
    # 1. Direct description
    if pkg.get("description"):
        return True

    # 2. Any diagram with description
    for diagram in diagrams_by_owner.get(pkg["id"], []):
        if diagram.get("description"):
            return True

    # 3. Any subpackage with meaningful content (recursive)
    for content in pkg.get("contents") or []:
        if content.get("type") == "Package":
            if has_meaningful_content(content, diagrams_by_owner):
                return True

    return False


def clean_text(text):
    """
    Replaces problematic or non-decodable characters (like �) with a space.
    The character � is often used to represent unknown or invalid bytes in text
    when decoding from a different or corrupted encoding.

    Args:
        text (str): The original text.

    Returns:
        str: The cleaned text with problematic characters replaced.
    """
    if not isinstance(text, str):
        return text
    return text.replace("�", " ")


def load_json(input_path):
    """
    Loads a JSON file from the specified path and returns the parsed content.

    Args:
        input_path (str or Path): Path to the JSON file.

    Returns:
        dict: Parsed JSON content as a dictionary.
    """
    with open(input_path, "r", encoding="utf-8", errors="replace") as f:
        return json.load(f)


def index_diagrams_by_owner(diagrams):
    """
    Indexes diagrams by their owner's ID, organizing them into a dictionary.

    Args:
        diagrams (list): A list of diagrams, each containing an 'owner' key with an 'id'.

    Returns:
        dict: A dictionary where the key is the owner ID and the value is a list of diagrams owned by that ID.
    """
    diagrams_by_owner = {}
    for diagram in diagrams:
        owner_id = diagram.get("owner", {}).get("id")
        if owner_id is None:
            continue
        diagrams_by_owner.setdefault(owner_id, []).append(diagram)
    return diagrams_by_owner


def find_image_for_element(element_name, images_folder):
    """
    Searches for an image file corresponding to a given element name in the specified folder.

    The function looks for files named as <element_name> with any of the supported image extensions.
    It returns the first matching image found.

    Args:
        element_name (str): The name of the element (e.g., a diagram or package name).
        images_folder (str or Path): Path to the folder containing image files.

    Returns:
        Path or None: The path to the matching image file if found, otherwise None.
    """
    images_folder = Path(images_folder)  # Ensure it's a Path object

    if not images_folder.exists():
        return None

    image_extensions = [".png", ".jpg", ".jpeg"]
    for ext in image_extensions:
        image_path = images_folder / f"{element_name}{ext}"
        if image_path.exists():
            return image_path

    return None


def process_package(pkg, diagrams_by_owner, images_folder, level=2):
    """
    Recursively processes a package and its sub-packages to generate corresponding Markdown lines.

    Args:
        pkg (dict): The current package being processed.
        diagrams_by_owner (dict): A dictionary mapping owner IDs to their corresponding diagrams.
        images_folder (str or Path): Path to the folder containing images.
        level (int, optional): The current header level in the Markdown document. Defaults to 2.

    Returns:
        list of str: A list of Markdown-formatted lines representing the content of the package.
    """
    if not pkg.get("name") or not has_meaningful_content(pkg, diagrams_by_owner):
        return []

    name = clean_text(pkg["name"])
    heading_prefix = "#" * level

    diagram_lines = []
    for diagram in diagrams_by_owner.get(pkg["id"], []):
        if not diagram.get("description"):
            continue  # skip diagrams without description

        diagram_name = clean_text(diagram.get("name") or "(unnamed diagram)")
        diagram_lines.append(f"{'#' * (level + 1)} {diagram_name}")
        diagram_lines.append("")

        image = find_image_for_element(diagram.get("name", ""), images_folder)
        if image:
            relative_image_path = Path("assets/images") / image.name
            diagram_lines.append(f"![{diagram_name}]({relative_image_path})")
            diagram_lines.append("")

        diagram_lines.append(clean_text(diagram["description"]))
        diagram_lines.append("")

    # Process sub-packages
    content_lines = []
    for content in pkg.get("contents") or []:
        if content.get("type") == "Package":
            sub_output = process_package(content, diagrams_by_owner, images_folder, level + 1)
            if sub_output:
                content_lines.extend(sub_output)

    # Do NOT print anything if no meaningful content exists
    if not pkg.get("description") and not diagram_lines and not content_lines:
        return []

    # Now it's safe to render this package
    lines = [f"{heading_prefix} {name}", ""]

    if pkg.get("description"):
        lines.append(clean_text(pkg["description"]))
        lines.append("")

    lines.extend(diagram_lines)
    lines.extend(content_lines)

    return lines


def generate_markdown(
    data,
    version_str,
    images_folder=None,
    image_path_prefix="assets/images",
    encode_image_path=False,
):
    """
    Generates the complete Markdown documentation from the given OntoUML JSON data.

    Args:
        data (dict): The OntoUML model data.
        version_str (str): Version string to include in the document.
        images_folder (str or Path, optional): Directory containing image files.
        image_path_prefix (str): Prefix used for image links in the Markdown.
        encode_image_path (bool): If True, percent-encode spaces in image paths.

    Returns:
        str: The full Markdown-formatted documentation.
    """

    def process_package_with_prefix(pkg, diagrams_by_owner, images_folder, level=2):
        if not pkg.get("name") or not has_meaningful_content(pkg, diagrams_by_owner):
            return []

        name = clean_text(pkg["name"])
        heading_prefix = "#" * level

        diagram_lines = []
        for diagram in diagrams_by_owner.get(pkg["id"], []):
            if not diagram.get("description"):
                continue

            diagram_name = clean_text(diagram.get("name") or "(unnamed diagram)")
            diagram_lines.append(f"{'#' * (level + 1)} {diagram_name}")
            diagram_lines.append("")

            image = find_image_for_element(diagram.get("name", ""), images_folder)
            if image:
                relative_image_path = Path(image_path_prefix) / image.name
                relative_image_path = str(relative_image_path).replace("\\", "/")
                if encode_image_path:
                    relative_image_path = quote(relative_image_path)
                diagram_lines.append(f"![{diagram_name}]({relative_image_path})")
                diagram_lines.append("")

            diagram_lines.append(clean_text(diagram["description"]))
            diagram_lines.append("")

        content_lines = []
        for content in pkg.get("contents") or []:
            if content.get("type") == "Package":
                sub_output = process_package_with_prefix(content, diagrams_by_owner, images_folder, level + 1)
                if sub_output:
                    content_lines.extend(sub_output)

        if not pkg.get("description") and not diagram_lines and not content_lines:
            return []

        lines = [f"{heading_prefix} {name}", ""]
        if pkg.get("description"):
            lines.append(clean_text(pkg["description"]))
            lines.append("")

        lines.extend(diagram_lines)
        lines.extend(content_lines)
        return lines

    title = clean_text(data.get("name", "(unnamed model)"))
    lines = [f"# {title}", f"*Version {version_str}*", ""]
    model = data.get("model", {})
    contents = model.get("contents") or []
    diagrams_by_owner = index_diagrams_by_owner(data.get("diagrams", []))

    for top_level_pkg in contents:
        section = process_package_with_prefix(top_level_pkg, diagrams_by_owner, images_folder)
        if section:
            lines.extend(section)

    return "\n".join(lines)


def get_latest_json_file(directory):
    """
    Finds the latest JSON file in the specified directory based on semantic versioning
    embedded in the filename. It assumes the filename format:
    'health-ri-ontology-v<MAJOR>.<MINOR>.<PATCH>.json'.

    Args:
        directory (str or Path): Path to the directory containing the JSON files.

    Returns:
        Path or None: Path to the latest versioned JSON file, or None if no valid file is found.
    """
    pattern = r"health-ri-ontology-v(\d+\.\d+\.\d+)\.json"
    latest_version = None
    latest_file = None

    for file in Path(directory).glob("health-ri-ontology-v*.json"):
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

    return latest_file, str(latest_version) if latest_version else None


def main():
    """
    The main entry point of the script. It loads the latest OntoUML JSON data,
    generates Markdown documentation, and writes it to multiple output files.
    """
    logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")

    # Ensure script runs from project root
    os.chdir(Path(__file__).parent.parent.resolve())

    # Define paths
    images_folder = Path("ontologies/latest/images")
    images_folder.mkdir(parents=True, exist_ok=True)

    ontologies_dir = Path("ontologies/versioned")
    latest_dir = Path("ontologies/latest")
    versioned_docs_dir = ontologies_dir / "documentations"
    latest_docs_dir = latest_dir / "documentations"
    output_path_main = Path("docs/ontology/documentation.md")

    versioned_docs_dir.mkdir(parents=True, exist_ok=True)
    latest_docs_dir.mkdir(parents=True, exist_ok=True)

    latest_json, version_str = get_latest_json_file(ontologies_dir)
    if latest_json and version_str:
        logging.info(f"Using latest JSON file: {latest_json}")
    else:
        logging.info("No valid JSON files found.")
        return

    # Paths that depend on the detected version
    versioned_md_name = f"documentation-v{version_str}.md"
    versioned_md_path = versioned_docs_dir / versioned_md_name
    latest_md_path = latest_docs_dir / "documentation.md"
    output_path_main = Path("docs/ontology/documentation.md")  # keep this path

    # --- Early exit gate: if this version is already documented, skip regeneration but always sync copies ---
    if versioned_md_path.exists():
        # Ensure parents exist (defensive)
        output_path_main.parent.mkdir(parents=True, exist_ok=True)
        latest_md_path.parent.mkdir(parents=True, exist_ok=True)

        # Rebuild docs copy with new image prefix (../../ontologies/latest/images)
        data = load_json(latest_json)

        markdown_main = generate_markdown(
            data,
            version_str,
            images_folder,
            image_path_prefix="../../ontologies/latest/images",
            encode_image_path=True,
        )
        output_path_main.write_text(markdown_main, encoding="utf-8")
        logging.info(f"Rebuilt docs copy with unified image path: {output_path_main}")

        # Rebuild latest copy (../images)
        markdown_latest = generate_markdown(
            data,
            version_str,
            images_folder,
            image_path_prefix="../images",
            encode_image_path=True,
        )
        latest_md_path.write_text(markdown_latest, encoding="utf-8")
        logging.info(f"Refreshed latest documentation at: {latest_md_path}")

        # Rebuild versioned copy (../../latest/images) so archives also use unified paths
        markdown_versioned = generate_markdown(
            data,
            version_str,
            images_folder,
            image_path_prefix="../../latest/images",
            encode_image_path=True,
        )
        versioned_md_path.write_text(markdown_versioned, encoding="utf-8")
        logging.info(f"Rebuilt versioned documentation with unified image path: {versioned_md_path}")

        logging.info(
            f"Documentation for v{version_str} already exists ({versioned_md_path}). Skipped regeneration; synced docs/latest."
        )
        return

    # ------------------------------------------------------------------------------

    # Only load & generate if we actually need to write new docs
    data = load_json(latest_json)

    # 1. Main Markdown output (docs/ontology/documentation.md)
    markdown_main = generate_markdown(
        data,
        version_str,
        images_folder,
        image_path_prefix="../../ontologies/latest/images",
        encode_image_path=True,
    )
    output_path_main.write_text(markdown_main, encoding="utf-8")

    # 2. Versioned Markdown copy (ontologies/versioned/documentations/...)
    markdown_versioned = generate_markdown(
        data,
        version_str,
        images_folder,
        image_path_prefix="../../latest/images",
        encode_image_path=True,
    )
    versioned_md_path.write_text(markdown_versioned, encoding="utf-8")

    # 3. Latest Markdown copy (ontologies/latest/documentations/documentation.md)
    markdown_latest = generate_markdown(
        data,
        version_str,
        images_folder,
        image_path_prefix="../images",
        encode_image_path=True,
    )
    latest_md_path.write_text(markdown_latest, encoding="utf-8")


if __name__ == "__main__":
    main()
