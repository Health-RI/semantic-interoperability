import json
import argparse
from pathlib import Path
from packaging import version
import re

def load_json(input_path):
    """
    Loads a JSON file from the specified path and returns the parsed content.

    Args:
        input_path (str or Path): Path to the JSON file.

    Returns:
        dict: Parsed JSON content as a dictionary.
    """
    with open(input_path, "r", encoding="utf-8") as f:
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
    image_extensions = ['.png', '.jpg', '.jpeg']
    for ext in image_extensions:
        image_path = Path(images_folder) / f"{element_name}{ext}"
        if image_path.exists():
            return image_path
    return None

def process_package(pkg, diagrams_by_owner, images_folder, level=2):
    """
    Processes a package and generates the corresponding Markdown lines for the package and its contents.

    Args:
        pkg (dict): A dictionary representing a package, which may contain a 'name', 'description', 'id',
                    and other metadata.
        diagrams_by_owner (dict): A dictionary of diagrams indexed by owner ID.
        images_folder (str or Path): Path to the folder containing images for diagrams and packages.
        level (int): The Markdown heading level to use for this package.

    Returns:
        list: A list of strings representing the Markdown content for this package and its contents.
    """
    heading_prefix = "#" * level
    lines = [f"{heading_prefix} {pkg['name']}", ""]

    if pkg.get("description"):
        lines.append(str(pkg["description"]))
        lines.append("")

    # Check if there is a matching image for the package
    image = find_image_for_element(pkg["name"], images_folder)
    if image:
        relative_image_path = Path(images_folder) / image.name  # Directly use the user-provided images_folder
        lines.append(f"![{pkg['name']}]({relative_image_path})")
        lines.append("")

    # Process diagrams associated with the package
    for diagram in diagrams_by_owner.get(pkg["id"], []):
        lines.append(f"{'#' * (level + 1)} {diagram['name']}")
        lines.append("")
        lines.append(str(diagram.get("description") or ""))
        lines.append("")

        # Check if there is a matching image for the diagram
        image = find_image_for_element(diagram['name'], images_folder)
        if image:
            relative_image_path = Path(images_folder) / image.name  # Directly use the user-provided images_folder
            lines.append(f"![{diagram['name']}]({relative_image_path})")
            lines.append("")

    # Recursively process sub-packages
    contents = pkg.get("contents") or []
    for content in contents:
        if content["type"] == "Package":
            lines.extend(process_package(content, diagrams_by_owner, images_folder, level=level + 1))

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
    lines = [f"# {data['name']}", ""]

    model = data.get("model", {})
    contents = model.get("contents") or []

    diagrams_by_owner = index_diagrams_by_owner(data.get("diagrams", []))

    # Process each top-level package
    for top_level_pkg in contents:
        lines.extend(process_package(top_level_pkg, diagrams_by_owner, images_folder))

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

    parser = argparse.ArgumentParser(description="Generate Markdown documentation from OntoUML JSON export.")
    parser.add_argument("output_md", nargs="?", default="docs/ontology/ontology.md", help="Path to write the Markdown output file")

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
