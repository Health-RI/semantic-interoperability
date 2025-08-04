import re
import subprocess
import logging
from pathlib import Path
from packaging import version
from bs4 import BeautifulSoup  # New dependency


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
            r'href="file://[^"]*/specification\.html#([^"]+)"', r'href="#\1"', html
        )
        file_path.write_text(fixed_html, encoding="utf-8")
        logging.info("Patched internal file:// links to use relative anchors (#...).")
    except Exception as e:
        logging.warning(f"Could not patch internal links: {e}")


def sort_toc_sections_in_html(
    file_path: Path, section_ids=("classes", "annotationproperties")
):
    """
    Sorts the list items under 'Classes' and 'Annotation Properties' in the Table of Contents.
    """
    try:
        html = file_path.read_text(encoding="utf-8")
        soup = BeautifulSoup(html, "html.parser")

        for section_id in section_ids:
            toc_anchor = soup.find("a", href=f"#{section_id}")
            if toc_anchor:
                parent_li = toc_anchor.find_parent("li")
                ul_second = parent_li.find("ul", class_="second")
                if ul_second:
                    list_items = ul_second.find_all("li")
                    sorted_items = sorted(list_items, key=lambda li: li.a.text.lower())
                    ul_second.clear()
                    for li in sorted_items:
                        ul_second.append(li)
        file_path.write_text(str(soup), encoding="utf-8")
        logging.info(f"Sorted Table of Contents entries for sections: {section_ids}")
    except Exception as e:
        logging.warning(f"Could not sort ToC sections: {e}")


def insert_logo_in_html(
    file_path: Path,
    logo_url="../assets/images/health-ri-logo-blue.png",
    alt_text="Health-RI Logo",
):
    """
    Inserts a logo image at the top of the HTML body.
    """
    try:
        html = file_path.read_text(encoding="utf-8")
        soup = BeautifulSoup(html, "html.parser")

        # Find the body and insert logo at the top
        body = soup.body
        if body:
            img_tag = soup.new_tag(
                "img",
                src=logo_url,
                alt=alt_text,
                style="max-height: 80px; margin-bottom: 1em;",
            )
            body.insert(0, img_tag)
            file_path.write_text(str(soup), encoding="utf-8")
            logging.info("Inserted logo at the top of the HTML.")
        else:
            logging.warning("No <body> tag found. Logo not inserted.")
    except Exception as e:
        logging.warning(f"Could not insert logo: {e}")


def main():
    logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")

    # Define directories
    base_dir = Path(__file__).resolve().parent.parent
    ttl_dir = base_dir / "ontologies"
    output_file = base_dir / "docs/ontology/specification.html"

    latest_ttl = get_latest_ttl_file(ttl_dir)
    if not latest_ttl:
        logging.warning("No valid TTL files found in 'ontologies/'. No specification will be produced.")
        return

    logging.info(f"Generating specification from: {latest_ttl}")
    try:
        subprocess.run(["pylode", str(latest_ttl), "-o", str(output_file)], check=True)
        logging.info(f"Specification generated at: {output_file}")

        # Post-process the file to fix broken internal links
        fix_internal_links_in_html(output_file)
        sort_toc_sections_in_html(output_file)
        insert_logo_in_html(output_file)

    except subprocess.CalledProcessError as e:
        logging.error(f"PyLODE generation failed: {e}")


if __name__ == "__main__":
    main()
