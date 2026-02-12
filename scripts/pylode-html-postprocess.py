#!/usr/bin/env python3
"""
pylode-html-postprocess.py

BeautifulSoup + rdflib post-processing for PyLODE-generated HTML specifications.

Preserved (legacy) behaviors from docgen-pylode.py:
- Patch internal file:// links that target specification.html#Anchor -> #Anchor
- Sort nested ToC lists (ul.second / ul.third) alphabetically
- Insert Health-RI logo (idempotent)
- Inject responsive TOC/content split CSS (idempotent via style id)

New ontology behaviors:
- Restructure ONLY the #classes section into top-level package subsections (H3)
- Insert maturity badge after each package heading (vs:term_status on top-level package)
- Add Synonyms row to each class block from skos:altLabel (idempotent)
- Rebuild the "Classes" ToC subtree to reflect package grouping
- Lightweight validations (class count unchanged, unique anchors, ToC targets exist)

Designed to be idempotent.

Exit codes:
- 0: success
- 1: generic failure
- 2: input/structure error
"""

from __future__ import annotations

import argparse
import logging
import re
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import DefaultDict, Dict, List, Optional, Sequence, Set, Tuple
from urllib.parse import quote

import rdflib
from bs4 import BeautifulSoup, NavigableString, Tag
from rdflib.namespace import RDFS, SKOS, DCTERMS

VS = rdflib.Namespace("http://www.w3.org/2003/06/sw-vocab-status/ns#")

_INTERNAL_LINK_FIX_RE = re.compile(r'href="file://[^"]*/specification\.html#([^"]+)"')
MATURITY_DOCS_URL = "https://health-ri.github.io/semantic-interoperability/method/ontology-validation/"


# ---------------------------
# HTML helpers (legacy)
# ---------------------------


def remove_is_defined_by_rows(soup: BeautifulSoup) -> int:
    """
    Remove PyLODE-rendered 'Is Defined By' rows from entity tables.
    Idempotent: removing an already-removed row is a no-op.
    """
    removed = 0
    for block in soup.select("div.property.entity"):
        table = block.find("table")
        if not table:
            continue
        for tr in list(table.find_all("tr")):
            th = tr.find("th")
            if th and th.get_text(strip=True).casefold() == "is defined by":
                tr.decompose()
                removed += 1
    return removed


def fix_internal_links_raw(html: str) -> str:
    """Preserve legacy behavior: only patch file://.../specification.html#Anchor -> #Anchor."""
    return _INTERNAL_LINK_FIX_RE.sub(r'href="#\1"', html)


def apply_responsive_toc_split_css(
    soup: BeautifulSoup,
    *,
    min_toc_px: int = 280,
    toc_vw: int = 20,
    max_toc_px: int = 420,
) -> None:
    head = soup.head
    if head is None:
        logging.warning("No <head> tag found; cannot inject CSS override.")
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

    style_tag.string = "\n" + css + "\n"


def insert_logo(
    soup: BeautifulSoup,
    *,
    logo_url: str = "../assets/images/health-ri-logo-blue.png",
    alt_text: str = "Health-RI Logo",
) -> None:
    body = soup.body
    if body is None:
        logging.warning("No <body> tag found; logo not inserted.")
        return

    # Idempotency guard
    if body.find("img", attrs={"src": logo_url}) is not None:
        return

    img_tag = soup.new_tag(
        "img",
        src=logo_url,
        alt=alt_text,
        style="max-height: 80px; margin-bottom: 1em;",
    )
    body.insert(0, img_tag)


def sort_toc_nested_lists(soup: BeautifulSoup) -> None:
    toc = soup.find(id="toc")
    if not toc:
        return

    def label_for_li(li: Tag) -> str:
        a = li.find("a")
        if a and a.get_text(strip=True):
            return a.get_text(strip=True)
        return li.get_text(" ", strip=True)

    for ul in toc.select("ul.second, ul.third"):
        items = ul.find_all("li", recursive=False)
        if len(items) < 2:
            continue

        indexed = list(enumerate(items))
        indexed_sorted = sorted(indexed, key=lambda pair: (label_for_li(pair[1]).casefold(), pair[0]))
        if [li for _, li in indexed_sorted] != items:
            ul.clear()
            for _, li in indexed_sorted:
                ul.append(li)


def maturity_badge(term_status: str) -> Optional[tuple[str, str]]:
    """
    Returns (badge_url, alt_text) for a given vs:term_status.
    Badge style matches Shields' /badge/<label>-<message>-<color>.
    """
    # Follow your requested strings for stage 1 and stage 4.
    mapping = {
        "int": ("Maturity_level", "internal_work_(int):_stage_1_of_4", "ff0400"),
        "irv": ("Maturity_level", "internal_review_(irv):_stage_2_of_4", "ffae00"),
        "erv": ("Maturity_level", "external_review_(erv):_stage_3_of_4", "007bff"),
        "pub": ("Maturity_level", "Published_(pub):_stage_4_of_4", "009e15"),
    }
    if term_status not in mapping:
        return None

    label, message, color = mapping[term_status]

    # Encode like the example: keep underscores/parentheses; ensure ":" becomes %3A.
    label_enc = quote(label, safe="_-()")
    message_enc = quote(message, safe="_-()")
    badge_url = f"https://img.shields.io/badge/{label_enc}-{message_enc}-{color}"

    alt_text = f"{label} {message}".replace("_", " ")
    return badge_url, alt_text


# ---------------------------
# Generic helpers
# ---------------------------


def slug_id(s: str) -> str:
    s = s.strip().casefold()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    s = re.sub(r"-{2,}", "-", s).strip("-")
    return s or "x"


def extract_display_label(h3: Optional[Tag]) -> str:
    """Extract label from <h3> ignoring <sup> markers by taking only direct text nodes."""
    if h3 is None:
        return ""
    texts = [t.strip() for t in h3.find_all(string=True, recursive=False)]
    texts = [t for t in texts if t]
    return " ".join(texts).strip()


def is_entity_block(node: Tag) -> bool:
    if not isinstance(node, Tag):
        return False
    if node.name != "div":
        return False
    classes = set(node.get("class") or [])
    return "property" in classes and "entity" in classes


def find_table_row_code_value(block: Tag, header_text: str) -> Optional[str]:
    table = block.find("table")
    if table is None:
        return None
    for tr in table.find_all("tr"):
        th = tr.find("th")
        if th and th.get_text(strip=True) == header_text:
            code = tr.find("code")
            if code:
                return code.get_text(strip=True)
            td = tr.find("td")
            return td.get_text(" ", strip=True) if td else None
    return None


def upsert_table_row(
    soup: BeautifulSoup,
    table: Tag,
    *,
    header_text: str,
    value_text: str,
    after_header: Optional[str] = None,
) -> None:
    # Update existing
    for tr in table.find_all("tr"):
        th = tr.find("th")
        if th and th.get_text(strip=True).casefold() == header_text.casefold():
            td = tr.find("td")
            if td is None:
                td = soup.new_tag("td")
                tr.append(td)
            td.clear()
            td.append(NavigableString(value_text))
            return

    # Insert new row
    tr_new = soup.new_tag("tr")
    th_new = soup.new_tag("th")
    th_new.append(NavigableString(header_text))
    td_new = soup.new_tag("td")
    td_new.append(NavigableString(value_text))
    tr_new.append(th_new)
    tr_new.append(td_new)

    inserted = False
    if after_header:
        for tr in table.find_all("tr"):
            th = tr.find("th")
            if th and th.get_text(strip=True).casefold() == after_header.casefold():
                tr.insert_after(tr_new)
                inserted = True
                break

    if not inserted:
        tbody = table.find("tbody") or table
        tbody.append(tr_new)


# ---------------------------
# RDF helpers
# ---------------------------


def parse_ttl(ttl_path: Path) -> rdflib.Graph:
    g = rdflib.Graph()
    g.parse(ttl_path, format="turtle")
    return g


def build_rdf_indexes(g: rdflib.Graph) -> Tuple[
    Dict[str, List[str]],  # class_iri -> alt labels
    Dict[str, str],  # class_iri -> package_iri
    Dict[str, str],  # package_iri -> rdfs:label
    Dict[str, str],  # package_iri -> vs:term_status
    Set[str],  # package node IRIs present in TTL
]:
    class_to_alt: DefaultDict[str, List[str]] = defaultdict(list)
    for s, o in g.subject_objects(SKOS.altLabel):
        class_to_alt[str(s)].append(str(o))

    class_to_pkg: Dict[str, str] = {}
    pkg_nodes: Set[str] = set()

    for s, o in g.subject_objects(DCTERMS.isPartOf):
        s_iri = str(s)
        o_iri = str(o)
        class_to_pkg[s_iri] = o_iri
        if "#package/" in o_iri:
            pkg_nodes.add(o_iri)

    # Collect package nodes from any subject that looks like a package
    for s, _, _ in g:
        s_iri = str(s)
        if "#package/" in s_iri:
            pkg_nodes.add(s_iri)

    pkg_to_label: Dict[str, str] = {}
    for s, o in g.subject_objects(RDFS.label):
        s_iri = str(s)
        if "#package/" in s_iri:
            pkg_to_label[s_iri] = str(o)

    pkg_to_status: Dict[str, str] = {}
    for s, o in g.subject_objects(VS.term_status):
        s_iri = str(s)
        if "#package/" in s_iri:
            pkg_to_status[s_iri] = str(o)
            pkg_nodes.add(s_iri)

    return dict(class_to_alt), class_to_pkg, pkg_to_label, pkg_to_status, pkg_nodes


def package_path_segment(package_iri: str) -> Optional[str]:
    marker = "#package/"
    idx = package_iri.find(marker)
    if idx < 0:
        return None
    tail = package_iri[idx + len(marker) :]
    if not tail:
        return None
    return tail.split("/")[0]


def top_level_package_iri(package_iri: str, segment: str) -> str:
    marker = "#package/"
    idx = package_iri.find(marker)
    if idx < 0:
        return package_iri.rsplit("/", 1)[0] + "/" + segment
    base = package_iri[: idx + len(marker)]
    return base + segment


def maturity_text(term_status: str) -> Optional[str]:
    mapping = {
        "int": (1, "Internal work"),
        "irv": (2, "Internal review"),
        "erv": (3, "External review"),
        "pub": (4, "Published"),
    }
    if term_status not in mapping:
        return None
    n, label = mapping[term_status]
    return f"Maturity stage {n} of 4 — {label} ({term_status})"


# ---------------------------
# Classes restructuring
# ---------------------------


@dataclass(frozen=True)
class ClassEntry:
    class_iri: str
    anchor_id: str
    display_label: str
    block: Tag


@dataclass(frozen=True)
class PackageMeta:
    key: str
    segment: Optional[str]
    label: str
    heading_id: str
    term_status: Optional[str]
    resolved_in_ttl: bool


def _ensure_unique_id(existing_ids: set, base_id: str) -> str:
    if base_id not in existing_ids:
        existing_ids.add(base_id)
        return base_id
    i = 2
    while f"{base_id}-{i}" in existing_ids:
        i += 1
    new_id = f"{base_id}-{i}"
    existing_ids.add(new_id)
    return new_id


def _is_inserted_package_heading(node: Tag) -> bool:
    return node.name == "h3" and (node.get("id") or "").startswith("pkg-")


def _is_inserted_maturity_line(node: Tag) -> bool:
    classes = set(node.get("class") or [])
    return node.name == "p" and "maturity" in classes


def collect_class_entries(classes_section: Tag) -> List[ClassEntry]:
    entries: List[ClassEntry] = []
    for block in classes_section.find_all("div", class_=["property", "entity"], recursive=False):
        if not is_entity_block(block):
            continue
        anchor_id = block.get("id")
        if not anchor_id:
            raise ValueError("Found class block without an id attribute.")
        class_iri = find_table_row_code_value(block, "IRI")
        if not class_iri:
            raise ValueError(f"Class block {anchor_id} missing IRI row; cannot match reliably.")
        display_label = extract_display_label(block.find("h3"))
        entries.append(ClassEntry(class_iri=class_iri, anchor_id=anchor_id, display_label=display_label, block=block))
    return entries


def compute_groups_and_meta(
    soup: BeautifulSoup,
    entries: Sequence[ClassEntry],
    *,
    class_to_pkg: Dict[str, str],
    pkg_to_label: Dict[str, str],
    pkg_to_status: Dict[str, str],
    pkg_nodes: Set[str],
) -> Tuple[Dict[str, List[ClassEntry]], Dict[str, PackageMeta]]:
    groups: DefaultDict[str, List[ClassEntry]] = defaultdict(list)
    meta: Dict[str, PackageMeta] = {}

    existing_ids = {tag.get("id") for tag in soup.find_all(attrs={"id": True})}

    for e in entries:
        pkg_iri = class_to_pkg.get(e.class_iri)
        if not pkg_iri:
            logging.warning(f"Class has no dcterms:isPartOf; grouping as Unassigned: {e.class_iri}")
            key = "Unassigned"
            if key not in meta:
                heading_id = _ensure_unique_id(existing_ids, "pkg-unassigned")
                meta[key] = PackageMeta(
                    key=key,
                    segment=None,
                    label="Unassigned",
                    heading_id=heading_id,
                    term_status=None,
                    resolved_in_ttl=True,
                )
            groups[key].append(e)
            continue

        segment = package_path_segment(pkg_iri)
        if not segment:
            logging.warning(f"Could not parse package segment; grouping as Unassigned: {e.class_iri} -> {pkg_iri}")
            key = "Unassigned"
            if key not in meta:
                heading_id = _ensure_unique_id(existing_ids, "pkg-unassigned")
                meta[key] = PackageMeta(
                    key=key,
                    segment=None,
                    label="Unassigned",
                    heading_id=heading_id,
                    term_status=None,
                    resolved_in_ttl=True,
                )
            groups[key].append(e)
            continue

        key = segment
        top_pkg_iri = top_level_package_iri(pkg_iri, segment)

        if top_pkg_iri in pkg_nodes:
            # Package exists in TTL: label is mandatory
            if top_pkg_iri not in pkg_to_label:
                raise ValueError(f"ERROR: top-level package exists but is missing rdfs:label: {top_pkg_iri}")
            label = pkg_to_label[top_pkg_iri]
            if not label.strip():
                raise ValueError(f"ERROR: top-level package has empty rdfs:label: {top_pkg_iri}")
            term_status = pkg_to_status.get(top_pkg_iri)
            resolved = True
        else:
            logging.warning(
                f"Package not present in TTL; using segment label and omitting maturity: {pkg_iri} (segment={segment})"
            )
            label = segment
            term_status = None
            resolved = False

        if key not in meta:

            heading_id = _ensure_unique_id(existing_ids, f"pkg-{slug_id(segment)}")
            meta[key] = PackageMeta(
                key=key,
                segment=segment,
                label=label,
                heading_id=heading_id,
                term_status=term_status,
                resolved_in_ttl=resolved,
            )

        groups[key].append(e)

    return dict(groups), meta


def restructure_classes_section(
    soup: BeautifulSoup,
    classes_section: Tag,
    *,
    class_to_pkg: Dict[str, str],
    pkg_to_label: Dict[str, str],
    pkg_to_status: Dict[str, str],
    pkg_nodes: Set[str],
) -> Tuple[List[PackageMeta], Dict[str, List[ClassEntry]], List[ClassEntry]]:
    h2 = classes_section.find("h2")
    if h2 is None:
        raise ValueError("No <h2> found in #classes section.")

    entries = collect_class_entries(classes_section)
    before_count = len(entries)

    # Extract preamble nodes (between h2 and first entity block),
    # but DO NOT preserve previously inserted package headings/maturity lines.
    preamble: List[object] = []
    node = h2.next_sibling
    while node is not None:
        nxt = node.next_sibling

        if isinstance(node, Tag) and is_entity_block(node):
            break

        if isinstance(node, Tag) and (_is_inserted_package_heading(node) or _is_inserted_maturity_line(node)):
            node.extract()  # drop previously inserted structure
            node = nxt
            continue

        if isinstance(node, NavigableString):
            if node.strip():
                preamble.append(node.extract())
            else:
                node.extract()  # drop whitespace
            node = nxt
            continue

        if isinstance(node, Tag):
            preamble.append(node.extract())
            node = nxt
            continue

        node = nxt

    # Extract class blocks
    for e in entries:
        e.block.extract()

    # Remove everything else after h2 (previous package headings, maturity lines, etc.)
    while h2.next_sibling is not None:
        sib = h2.next_sibling
        if isinstance(sib, NavigableString):
            sib.extract()
        else:
            sib.decompose()

    # Reinsert preamble
    for n in preamble:
        classes_section.append(n)

    groups, meta = compute_groups_and_meta(
        soup,
        entries,
        class_to_pkg=class_to_pkg,
        pkg_to_label=pkg_to_label,
        pkg_to_status=pkg_to_status,
        pkg_nodes=pkg_nodes,
    )

    pkg_keys = list(groups.keys())
    pkg_keys.sort(
        key=lambda k: (k.casefold() == "unassigned", meta[k].label.casefold(), (meta[k].segment or "").casefold())
    )
    packages_in_order: List[PackageMeta] = [meta[k] for k in pkg_keys]

    for pkg in packages_in_order:
        h3 = soup.new_tag("h3", id=pkg.heading_id)
        pkg_heading_text = pkg.label if pkg.key.casefold() == "unassigned" else f"Package: {pkg.label}"
        h3.append(NavigableString(pkg_heading_text))
        classes_section.append(h3)


        if pkg.term_status:
            mtxt = maturity_text(pkg.term_status)
            if mtxt:
                badge = maturity_badge(pkg.term_status)
                if badge:
                    badge_url, alt_text = badge

                    p = soup.new_tag("p")
                    p["class"] = "maturity"

                    a = soup.new_tag("a", href=MATURITY_DOCS_URL)
                    img = soup.new_tag("img", src=badge_url, alt=alt_text)
                    # optional: keep badge aligned nicely
                    img["style"] = "vertical-align: middle;"

                    a.append(img)
                    p.append(a)
                    classes_section.append(p)
                else:
                    logging.warning(
                        f"Unknown vs:term_status value; omitting maturity badge: {pkg.label} -> {pkg.term_status}"
                    )
            else:
                logging.warning(
                    f"Unknown vs:term_status value; omitting maturity line: {pkg.label} -> {pkg.term_status}"
                )
        else:
            if pkg.resolved_in_ttl:
                logging.warning(f"Missing vs:term_status for package; omitting maturity line: {pkg.label}")

        cls_entries = groups[pkg.key]
        cls_entries.sort(key=lambda e: (e.display_label.casefold(), e.class_iri))
        for e in cls_entries:
            classes_section.append(e.block)

    # Post-check: count unchanged
    after_count = len(classes_section.select("div.property.entity"))
    if after_count != before_count:
        raise ValueError(f"ERROR: Class count changed after restructuring (before={before_count}, after={after_count})")

    return packages_in_order, groups, entries


def _ensure_synonyms_header_link(soup: BeautifulSoup, th: Tag) -> None:
    """
    Ensure the Synonyms header cell contains a hover_property link to skos:altLabel,
    matching PyLODE's style for other predicate-linked headers.
    """
    href = str(SKOS.altLabel)
    title = "An alternative lexical label for a resource. Defined in SKOS."
    th.clear()
    a = soup.new_tag("a", href=href)
    a["class"] = "hover_property"
    a["title"] = title
    a.append(NavigableString("Synonyms"))
    th.append(a)


def add_synonyms(
    soup: BeautifulSoup,
    classes_section: Tag,
    *,
    class_to_alt: Dict[str, List[str]],
) -> int:
    changed = 0
    for block in classes_section.find_all("div", class_=["property", "entity"], recursive=False):
        if not is_entity_block(block):
            continue

        class_iri = find_table_row_code_value(block, "IRI")
        if not class_iri:
            continue

        synonyms = class_to_alt.get(class_iri) or []
        if not synonyms:
            continue

        table = block.find("table")
        if table is None:
            continue

        # Use text nodes only (avoid HTML injection).
        value = ", ".join(synonyms)

        # Update existing row if present (and ensure linked header)
        for tr in table.find_all("tr"):
            th = tr.find("th")
            if th and th.get_text(strip=True).casefold() == "synonyms":
                _ensure_synonyms_header_link(soup, th)
                td = tr.find("td")
                if td is None:
                    td = soup.new_tag("td")
                    tr.append(td)
                td.clear()
                td.append(NavigableString(value))
                changed += 1
                break
        else:
            # Insert new row with linked header
            tr_new = soup.new_tag("tr")
            th_new = soup.new_tag("th")
            _ensure_synonyms_header_link(soup, th_new)
            td_new = soup.new_tag("td")
            td_new.append(NavigableString(value))
            tr_new.append(th_new)
            tr_new.append(td_new)

            after = "Description" if find_table_row_code_value(block, "Description") is not None else "IRI"
            inserted = False
            for tr in table.find_all("tr"):
                th = tr.find("th")
                if th and th.get_text(strip=True).casefold() == after.casefold():
                    tr.insert_after(tr_new)
                    inserted = True
                    break
            if not inserted:
                tbody = table.find("tbody") or table
                tbody.append(tr_new)

            changed += 1

    return changed


def rewrite_classes_toc(
    soup: BeautifulSoup,
    packages_in_order: Sequence[PackageMeta],
    groups: Dict[str, List[ClassEntry]],
) -> None:
    toc = soup.find(id="toc")
    if toc is None:
        logging.warning("No #toc found; cannot rewrite Classes ToC.")
        return

    classes_link = toc.find("a", href="#classes")
    if classes_link is None:
        logging.warning('No ToC entry for Classes (a[href="#classes"]); cannot rewrite Classes ToC.')
        return

    classes_li = classes_link.find_parent("li")
    if classes_li is None:
        logging.warning("Could not find parent <li> for Classes ToC entry.")
        return

    # Remove existing nested list(s)
    for ul in list(classes_li.find_all("ul", class_="second", recursive=False)):
        ul.decompose()

    new_ul = soup.new_tag("ul")
    new_ul["class"] = "second"

    for pkg in packages_in_order:
        li_pkg = soup.new_tag("li")
        a_pkg = soup.new_tag("a", href=f"#{pkg.heading_id}")
        pkg_toc_text = pkg.label if pkg.key.casefold() == "unassigned" else f"Package: {pkg.label}"
        a_pkg.append(NavigableString(pkg_toc_text))
        li_pkg.append(a_pkg)

        ul_third = soup.new_tag("ul")
        ul_third["class"] = "third"

        cls_entries = list(groups.get(pkg.key, []))
        cls_entries.sort(key=lambda e: (e.display_label.casefold(), e.class_iri))

        for e in cls_entries:
            li_cls = soup.new_tag("li")
            a_cls = soup.new_tag("a", href=f"#{e.anchor_id}")
            a_cls.append(NavigableString(e.display_label))
            li_cls.append(a_cls)
            ul_third.append(li_cls)

        li_pkg.append(ul_third)
        new_ul.append(li_pkg)

    classes_li.append(new_ul)


def validate_classes_structure(soup: BeautifulSoup, classes_section: Tag) -> None:
    ids = [b.get("id") for b in classes_section.select("div.property.entity[id]")]
    ids = [i for i in ids if i]
    if len(ids) != len(set(ids)):
        raise ValueError("ERROR: Duplicate class anchor ids detected in #classes section.")

    toc = soup.find(id="toc")
    if toc:
        for a in toc.select('a[href^="#"]'):
            href = a.get("href", "")
            target = href[1:]
            if target and soup.find(id=target) is None:
                logging.warning(f"ToC/anchor link target not found: {href}")


def postprocess_html(
    html_in: Path,
    ttl_path: Optional[Path],
    html_out: Path,
    *,
    do_link_fix: bool,
    do_toc_sort: bool,
    do_logo: bool,
    logo_url: str,
    logo_alt: str,
    do_toc_css: bool,
    do_classes_restructure: bool,
    do_synonyms: bool,
) -> None:
    raw = html_in.read_text(encoding="utf-8")
    if do_link_fix:
        raw = fix_internal_links_raw(raw)

    soup = BeautifulSoup(raw, "html.parser")
    n = remove_is_defined_by_rows(soup)
    if n:
        logging.info(f"Removed {n} 'Is Defined By' rows from HTML.")

    if do_logo:
        insert_logo(soup, logo_url=logo_url, alt_text=logo_alt)
    if do_toc_css:
        apply_responsive_toc_split_css(soup)
    if do_toc_sort:
        sort_toc_nested_lists(soup)

    class_to_alt: Dict[str, List[str]] = {}
    class_to_pkg: Dict[str, str] = {}
    pkg_to_label: Dict[str, str] = {}
    pkg_to_status: Dict[str, str] = {}
    pkg_nodes: Set[str] = set()

    if ttl_path is not None:
        g = parse_ttl(ttl_path)
        class_to_alt, class_to_pkg, pkg_to_label, pkg_to_status, pkg_nodes = build_rdf_indexes(g)

    classes_section = soup.find(id="classes")
    packages_in_order: List[PackageMeta] = []
    groups: Dict[str, List[ClassEntry]] = {}

    if do_classes_restructure:
        if ttl_path is None:
            raise ValueError("Classes restructuring requires --ttl.")
        if classes_section is None:
            raise ValueError("No #classes section found, but classes restructuring was requested.")
        if not pkg_nodes:
            logging.info("No #package/ collections detected in TTL; skipping Classes restructuring.")
        else:
            packages_in_order, groups, _ = restructure_classes_section(
                soup,
                classes_section,
                class_to_pkg=class_to_pkg,
                pkg_to_label=pkg_to_label,
                pkg_to_status=pkg_to_status,
                pkg_nodes=pkg_nodes,
            )
            rewrite_classes_toc(soup, packages_in_order, groups)

    if do_synonyms and ttl_path is not None and classes_section is not None:
        n = add_synonyms(soup, classes_section, class_to_alt=class_to_alt)
        if n:
            logging.info(f"Inserted/updated synonyms for {n} class blocks.")

    if classes_section is not None:
        validate_classes_structure(soup, classes_section)

    html_out.parent.mkdir(parents=True, exist_ok=True)
    html_out.write_text(str(soup), encoding="utf-8")


def main() -> int:
    logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")

    ap = argparse.ArgumentParser()
    ap.add_argument("--html-in", required=True, type=Path, help="Input HTML file.")
    ap.add_argument("--html-out", type=Path, default=None, help="Output HTML file (default: overwrite input).")
    ap.add_argument("--ttl", type=Path, default=None, help="TTL file used for RDF-driven edits (packages, synonyms).")

    ap.add_argument("--no-link-fix", action="store_true", help="Disable legacy internal link fix.")
    ap.add_argument("--no-toc-sort", action="store_true", help="Disable legacy ToC nested sorting.")
    ap.add_argument("--no-logo", action="store_true", help="Disable logo insertion.")
    ap.add_argument("--logo-url", default="../assets/images/health-ri-logo-blue.png", help="Logo URL to insert.")
    ap.add_argument("--logo-alt", default="Health-RI Logo", help="Logo alt text.")
    ap.add_argument("--no-toc-css", action="store_true", help="Disable responsive TOC CSS injection.")
    ap.add_argument(
        "--no-classes-restructure", action="store_true", help="Disable package grouping / ToC rewrite for Classes."
    )
    ap.add_argument("--no-synonyms", action="store_true", help="Disable inserting/updating Synonyms rows.")

    args = ap.parse_args()

    if not args.html_in.exists():
        logging.error(f"HTML input not found: {args.html_in}")
        return 2
    if args.ttl is not None and not args.ttl.exists():
        logging.error(f"TTL not found: {args.ttl}")
        return 2

    html_out = args.html_out or args.html_in

    try:
        postprocess_html(
            html_in=args.html_in,
            ttl_path=args.ttl,
            html_out=html_out,
            do_link_fix=not args.no_link_fix,
            do_toc_sort=not args.no_toc_sort,
            do_logo=not args.no_logo,
            logo_url=args.logo_url,
            logo_alt=args.logo_alt,
            do_toc_css=not args.no_toc_css,
            do_classes_restructure=not args.no_classes_restructure,
            do_synonyms=not args.no_synonyms,
        )
        logging.info(f"Post-processed HTML written to: {html_out}")
        return 0
    except ValueError as e:
        logging.error(str(e))
        return 2
    except Exception as e:
        logging.exception(f"Post-processing failed: {e}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
