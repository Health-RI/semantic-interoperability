import re
import subprocess
import logging
from pathlib import Path
from packaging import version
from bs4 import BeautifulSoup
import shutil


def get_latest_ontology_ttl_file(directory: Path):
    """
    Finds the latest versioned TTL file in the given directory based on semantic versioning
    embedded in the filename (e.g., 'health-ri-ontology-v1.2.3.ttl').

    Args:
        directory (Path): Directory containing versioned TTL files.

    Returns:
        tuple[Path | None, Version | None]: The path to the latest TTL file and its parsed version,
        or (None, None) if no valid files are found.
    """
    pattern = r"health-ri-ontology-v(\d+\.\d+\.\d+)\.ttl"
    latest_file = None
    latest_version = None

    for file in directory.glob("health-ri-ontology-v*.ttl"):
        match = re.match(pattern, file.name)
        if match:
            file_version = version.parse(match.group(1))
            if latest_version is None or file_version > latest_version:
                latest_version = file_version
                latest_file = file

    return latest_file, latest_version


def get_latest_vocabulary_ttl_file(directory: Path):
    """
    Finds the latest versioned TTL file for the vocabulary based on semantic versioning
    embedded in the filename (e.g., 'health-ri-vocabulary-v1.2.3.ttl').
    """
    pattern = r"health-ri-vocabulary-v(\d+\.\d+\.\d+)\.ttl"
    latest_file = None
    latest_version = None

    for file in directory.glob("health-ri-vocabulary-v*.ttl"):
        match = re.match(pattern, file.name)
        if match:
            file_version = version.parse(match.group(1))
            if latest_version is None or file_version > latest_version:
                latest_version = file_version
                latest_file = file

    return latest_file, latest_version


def fix_internal_links_in_html(file_path: Path):
    """
    Fixes PyLODE-generated HTML links that use absolute `file://` paths, converting them
    to relative fragment identifiers (e.g., '#AnchorName').

    Args:
        file_path (Path): Path to the HTML file to patch.
    """
    try:
        html = file_path.read_text(encoding="utf-8")
        # Replace href="file:///.../specification.html#SomeAnchor" → href="#SomeAnchor"
        fixed_html = re.sub(r'href="file://[^"]*/specification\.html#([^"]+)"', r'href="#\1"', html)
        file_path.write_text(fixed_html, encoding="utf-8")
        logging.info("Patched internal file:// links to use relative anchors (#...).")
    except Exception as e:
        logging.warning(f"Could not patch internal links: {e}")


def sort_toc_sections_in_html(file_path: Path, section_ids=("classes", "annotationproperties")):
    """
    Sorts nested Table of Contents (ToC) lists alphabetically.

    Notes:
    - Keeps the top-level ToC groups in their original order.
    - Sorts each nested group (e.g., Classes, Object properties, Data properties, etc.)
      alphabetically by the visible label.
    - The `section_ids` parameter is kept for backward compatibility but is not used.
    """
    try:
        html = file_path.read_text(encoding="utf-8")
        soup = BeautifulSoup(html, "html.parser")

        toc = soup.find(id="toc")
        if not toc:
            logging.info("No #toc found; nothing to sort.")
            return

        def _label_for_li(li) -> str:
            a = li.find("a")
            if a and a.get_text(strip=True):
                return a.get_text(strip=True)
            return li.get_text(" ", strip=True)

        changed = False

        # Sort nested TOC lists; pyLODE commonly uses ul.second / ul.third
        for ul in toc.select("ul.second, ul.third"):
            items = ul.find_all("li", recursive=False)
            if len(items) < 2:
                continue

            indexed_items = list(enumerate(items))
            indexed_items_sorted = sorted(
                indexed_items,
                key=lambda pair: (_label_for_li(pair[1]).casefold(), pair[0]),  # stable tie-breaker
            )

            if [li for _, li in indexed_items_sorted] != items:
                ul.clear()
                for _, li in indexed_items_sorted:
                    ul.append(li)
                changed = True

        if changed:
            file_path.write_text(str(soup), encoding="utf-8")
            logging.info("Sorted nested Table of Contents entries alphabetically.")
        else:
            logging.info("ToC already sorted; no changes applied.")
    except Exception as e:
        logging.warning(f"Could not sort ToC sections: {e}")


def insert_logo_in_html(
    file_path: Path,
    logo_url="../assets/images/health-ri-logo-blue.png",
    alt_text="Health-RI Logo",
):
    """
    Inserts a logo image at the top of the HTML document's <body> section. The logo is inserted before any existing body content.

    Args:
        file_path (Path): Path to the HTML file.
        logo_url (str): Relative URL of the logo image to embed.
        alt_text (str): Alternative text for the logo image.
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

def apply_responsive_toc_split_css(
    file_path: Path,
    min_toc_px: int = 280,
    toc_vw: int = 20,
    max_toc_px: int = 420,
):
    """
    Inject a CSS override for PyLODE's fixed right-hand TOC layout.

    Why:
    - PyLODE sets #toc { position: fixed; width: 180px; }
    - and #content { width: calc(100% - 150px); }
    So table/td-based logic won't work; we override those rules via CSS.
    """
    try:
        html = file_path.read_text(encoding="utf-8")
        soup = BeautifulSoup(html, "html.parser")

        head = soup.head
        if not head:
            logging.info("No <head> found; cannot inject CSS override.")
            return

        clamp = f"clamp({int(min_toc_px)}px, {int(toc_vw)}vw, {int(max_toc_px)}px)"
        css = f"""
/* Health-RI override: responsive toc/content split */
#toc {{
  width: {clamp} !important;
  box-sizing: border-box !important;
}}
#content {{
  margin-right: {clamp} !important;
  width: auto !important;
}}
""".strip()

        style_id = "healthri-toc-split-override"
        style_tag = soup.find("style", attrs={"id": style_id})
        if style_tag is None:
            style_tag = soup.new_tag("style", id=style_id)
            head.append(style_tag)

        # Replace contents (idempotent)
        style_tag.string = "\n" + css + "\n"

        file_path.write_text(str(soup), encoding="utf-8")
        logging.info(f"Injected responsive TOC/content split CSS: {clamp}")
    except Exception as e:
        logging.warning(f"Could not inject responsive TOC/content split CSS: {e}")


def main():
    """
    Main execution function. Generates the HTML specification using PyLODE from the
    latest versioned TTL file, applies post-processing (link fixing, ToC sorting, logo insertion),
    and saves the result to:

    - docs/ontology/specification-ontology.html
    - ontologies/latest/documentations/specification.html
    - ontologies/versioned/documentations/specification-v<version>.html

    It will only execute PyLODE if the versioned output for the detected version
    does not already exist. Otherwise, it will skip generation and (idempotently)
    repair missing "latest" and "docs" copies from the versioned file.

    IMPORTANT (no-regression behavior):
    - When reusing an existing versioned HTML, we apply link fixing + TOC sorting ONLY to the
      docs/latest copies (we do NOT rewrite the versioned artifact).
    """
    logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")

    # Define directories
    base_dir = Path(__file__).resolve().parent.parent
    ttl_dir = base_dir / "ontologies" / "versioned"
    output_file = base_dir / "docs/ontology/specification-ontology.html"
    output_file.parent.mkdir(parents=True, exist_ok=True)

    latest_ttl, latest_version = get_latest_ontology_ttl_file(ttl_dir)
    if not latest_ttl:
        logging.warning("No valid TTL files found in 'ontologies/versioned/'. No specification will be produced.")
        # Continue on to vocabulary below even if ontology is missing
    else:
        # Paths that depend on ontology version
        version_str = str(latest_version)
        versioned_output = base_dir / f"ontologies/versioned/documentations/specification-v{version_str}.html"
        latest_output = base_dir / "ontologies/latest/documentations/specification.html"
        latest_output.parent.mkdir(parents=True, exist_ok=True)
        versioned_output.parent.mkdir(parents=True, exist_ok=True)

        # --- Early-exit gate for ontology spec ---
        if versioned_output.exists():
            # Rebuild docs + latest from the canonical versioned file,
            # then enforce fixes on docs and propagate to latest (do not rewrite versioned).
            shutil.copyfile(versioned_output, output_file)

            fix_internal_links_in_html(output_file)
            sort_toc_sections_in_html(output_file)
            apply_responsive_toc_split_css(output_file)

            shutil.copyfile(output_file, latest_output)

            logging.info(
                f"Ontology specification for v{version_str} already exists "
                f"({versioned_output}). Skipped regeneration; synced latest/docs (with enforced TOC sort)."
            )
        else:
            # Run PyLODE only when the versioned file does not exist
            logging.info(f"Generating specification from: {latest_ttl}")
            try:
                subprocess.run(["pylode", str(latest_ttl), "-o", str(output_file)], check=True)
                logging.info(f"Specification generated at: {output_file}")

                # Post-process the file to fix broken internal links
                fix_internal_links_in_html(output_file)
                sort_toc_sections_in_html(output_file)
                insert_logo_in_html(output_file)
                apply_responsive_toc_split_css(output_file)

                # Save versioned + latest copies
                shutil.copyfile(output_file, versioned_output)
                logging.info(f"Copied versioned specification to: {versioned_output}")

                shutil.copyfile(output_file, latest_output)
                logging.info(f"Copied specification to: {latest_output}")

            except subprocess.CalledProcessError as e:
                logging.error(f"PyLODE generation failed: {e}")

    # Generate specification for the Mapping Vocabulary ===
    vocab_ttl_dir = base_dir / "vocabulary" / "versioned"
    vocab_output_file = base_dir / "docs/method/specification-vocabulary.html"
    vocab_output_file.parent.mkdir(parents=True, exist_ok=True)

    vocab_ttl, vocab_version = get_latest_vocabulary_ttl_file(vocab_ttl_dir)
    if not vocab_ttl:
        logging.warning(
            "No valid TTL files found in 'vocabulary/versioned/'. No vocabulary specification will be produced."
        )
    else:
        vocab_version_str = str(vocab_version)
        vocab_versioned_output = (
            base_dir / f"vocabulary/versioned/documentations/specification-v{vocab_version_str}.html"
        )
        vocab_latest_output = base_dir / "vocabulary/latest/documentations/specification.html"
        vocab_versioned_output.parent.mkdir(parents=True, exist_ok=True)
        vocab_latest_output.parent.mkdir(parents=True, exist_ok=True)

        # --- Early-exit gate for vocabulary spec ---
        if vocab_versioned_output.exists():
            # Rebuild docs + latest from the canonical versioned file,
            # then enforce fixes on docs and propagate to latest (do not rewrite versioned).
            shutil.copyfile(vocab_versioned_output, vocab_output_file)

            fix_internal_links_in_html(vocab_output_file)
            sort_toc_sections_in_html(vocab_output_file)
            apply_responsive_toc_split_css(vocab_output_file)

            shutil.copyfile(vocab_output_file, vocab_latest_output)

            logging.info(
                f"Vocabulary specification for v{vocab_version_str} already exists "
                f"({vocab_versioned_output}). Skipped regeneration; synced latest/docs (with enforced TOC sort)."
            )
        else:
            logging.info(f"Generating vocabulary specification from: {vocab_ttl}")
            try:
                subprocess.run(
                    ["pylode", str(vocab_ttl), "-o", str(vocab_output_file)],
                    check=True,
                )
                logging.info(f"Vocabulary specification generated at: {vocab_output_file}")

                # Post-process the file
                fix_internal_links_in_html(vocab_output_file)
                sort_toc_sections_in_html(vocab_output_file)
                insert_logo_in_html(vocab_output_file)
                apply_responsive_toc_split_css(vocab_output_file)

                # Save versioned + latest copies
                shutil.copyfile(vocab_output_file, vocab_versioned_output)
                logging.info(f"Copied versioned vocabulary specification to: {vocab_versioned_output}")

                shutil.copyfile(vocab_output_file, vocab_latest_output)
                logging.info(f"Copied vocabulary specification to: {vocab_latest_output}")

            except subprocess.CalledProcessError as e:
                logging.error(f"PyLODE generation for vocabulary failed: {e}")


if __name__ == "__main__":
    main()
