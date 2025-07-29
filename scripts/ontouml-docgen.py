import json
import argparse
from pathlib import Path
from packaging import version
import re


def has_meaningful_content(pkg, diagrams_by_owner):
    # 1. Direct description
    if pkg.get("description"):
        return True

    # 2. Any diagram with description
    for diagram in diagrams_by_owner.get(pkg["id"], []):
        if diagram.get("description"):
            return True

    # 3. Any subpackage with meaningful content
    for content in pkg.get("contents") or []:
        if content.get("type") == "Package":
            if has_meaningful_content(content, diagrams_by_owner):
                return True

    return False


def clean_text(text):
    """
    Replaces problematic characters (like �) with a space.

    Args:
        text (str): The original text.

    Returns:
        str: The cleaned text.
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
        owner_id = diagram["owner"]["id"]
        diagrams_by_owner.setdefault(owner_id, []).append(diagram)
    return diagrams_by_owner


def find_image_for_element(element_name, images_folder):
    """
    Searches for an image file corresponding to an element by its name in the specified folder.

    Args:
        element_name (str): The name of the element to find the image for.
        images_folder (str or Path): Path to the folder containing images.

    Returns:
        Path or None: The path to the image file if found, otherwise None.
    """
    if not images_folder:  # Ensure images_folder is valid
        return None

    # Check for a match in the images folder
    image_extensions = [".png", ".jpg", ".jpeg"]
    for ext in image_extensions:
        image_path = Path(images_folder) / f"{element_name}{ext}"
        if image_path.exists():
            return image_path
    return None


def process_package(pkg, diagrams_by_owner, images_folder, level=2):
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
            sub_output = process_package(
                content, diagrams_by_owner, images_folder, level + 1
            )
            if sub_output:
                content_lines.extend(sub_output)

    # Do NOT print anything if no meaningful content exists
    if not pkg.get("description") and not diagram_lines and not content_lines:
        return []

    # Now it's safe to render this package
    lines = [f"{heading_prefix} {name}", ""]

    image = find_image_for_element(diagram.get("name", ""), images_folder)
    if image:
        relative_image_path = Path("assets/images") / image.name
        diagram_lines.append(f"![{diagram_name}]({relative_image_path})")
        diagram_lines.append("")

    if pkg.get("description"):
        lines.append(clean_text(pkg["description"]))
        lines.append("")

    lines.extend(diagram_lines)
    lines.extend(content_lines)

    return lines


def generate_markdown(data, images_folder=None):
    """
    Generates the complete Markdown documentation from the given data.

    Args:
        data (dict): The data representing the OntoUML model, including information about packages and diagrams.
        images_folder (str or Path, optional): Path to the folder containing images to include in the documentation.

    Returns:
        str: The generated Markdown documentation as a string.
    """
    lines = [f"# {clean_text(data['name'])}", ""]

    model = data.get("model", {})
    contents = model.get("contents") or []

    diagrams_by_owner = index_diagrams_by_owner(data.get("diagrams", []))

    # Process each top-level package
    for top_level_pkg in contents:
        section = process_package(top_level_pkg, diagrams_by_owner, images_folder)
        if section:  # Only add non-empty sections
            lines.extend(section)

    return "\n".join(lines)


def get_latest_json_file(directory):
    """
    Finds the latest JSON file in the specified directory based on semantic versioning.

    Args:
        directory (str or Path): Path to the directory containing JSON files.

    Returns:
        Path: Path to the latest JSON file.
    """
    pattern = r"Health-RI Ontology-v(\d+\.\d+\.\d+)\.json"
    latest_version = None
    latest_file = None

    for file in Path(directory).glob("Health-RI Ontology-v*.json"):
        match = re.match(pattern, file.name)
        if match:
            file_version = match.group(1)
            try:
                file_version_obj = version.parse(file_version)
                if latest_version is None or file_version_obj > latest_version:
                    latest_version = file_version_obj
                    latest_file = file
            except version.InvalidVersion:
                print(f"Skipping invalid version: {file_version}")

    return latest_file


def main():
    """
    The main entry point of the script. It parses command-line arguments, loads the OntoUML JSON data,
    generates Markdown documentation, and writes it to the specified output file.
    """

    images_folder = Path("docs/ontology/assets/images")
    images_folder.mkdir(parents=True, exist_ok=True)

    parser = argparse.ArgumentParser(
        description="Generate Markdown documentation from OntoUML JSON export."
    )
    parser.add_argument(
        "output_md",
        nargs="?",
        default="docs/ontology/ontology.md",
        help="Path to write the Markdown output file",
    )

    args = parser.parse_args()

    # Automatically determine the latest JSON file
    ontologies_dir = Path("ontologies")
    latest_json = get_latest_json_file(ontologies_dir)
    if latest_json:
        print(f"Using latest JSON file: {latest_json}")
        data = load_json(latest_json)
    else:
        print("No valid JSON files found.")
        return

    images_folder = Path("docs/ontology/assets/images")
    markdown_output = generate_markdown(data, images_folder=images_folder)

    Path(args.output_md).write_text(markdown_output, encoding="utf-8")
    print(f"Documentation written to: {args.output_md}")


if __name__ == "__main__":
    main()
