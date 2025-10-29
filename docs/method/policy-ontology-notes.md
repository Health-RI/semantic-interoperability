# Ontology Note Classification and Visual Conventions

This page defines the standardized system of note tags, categories, and color conventions used in UML/OntoUML diagrams for ontology engineering work.
It ensures consistent visual annotation, semantic clarity, and readability across diagrams produced in Visual Paradigm (VP).

## Purpose & Scope

This guide standardizes how ontology modelers should:
- Classify and label UML notes according to their role (e.g., semantics, constraints, rationale).
- Apply consistent colors and anchoring rules within Visual Paradigm diagrams.
- Maintain visual clarity, traceability, and stylistic uniformity across Health-RI ontology artifacts.

The scope covers all ontology-related UML diagrams, including those representing OntoUML, HRIO, or HRIV concepts.
It excludes notation for OCL syntax itself or purely graphical conventions unrelated to note usage.

## Note Categories and Colors

| Tag  | Category               | What goes here                                | Typical contents                                                                       | Color (VP slot[^rxcy] — Name[^name]  • HEX) |
| ---- | ---------------------- | --------------------------------------------- | -------------------------------------------------------------------------------------- | ------------------------------------------- |
| SEMI | Semantics & intent     | Clarify meaning beyond the stereotype/name    | term definition, conceptual nuance, OntoUML meaning, disambiguation                    | R1C7 — Lavender Blue • #C0C0FF              |
| CNST | Constraints & rules    | Plain-text paraphrase of constraints (no OCL) | paraphrase of OCL constraints, invariants, pre/postconditions, multiplicity rationales | R1C2 — Spanish Pink • #FFC0C0               |
| RATL | Rationale              | Why a design choice was made                  | trade-offs, rejected alternatives, decision logs                                       | R1C8 — Brilliant Lavender • #FFC0FF         |
| SCOP | Scope & assumptions    | Boundaries of what the model covers           | simplifying assumptions, context limits, applicability conditions                      | R1C6 — Celeste • #C0FFFF                    |
| TRAC | Traceability & sources | Where a model element comes from              | requirement IDs, standards clauses, tickets, citations                                 | R1C3 — Very Pale Orange • #FFE0C0           |
| EXMP | Examples & usage       | Small, concrete examples                      | valid/invalid instances, mini sequence snippets                                        | R1C4 — Very Pale Yellow • #FFFFC0           |
| TODO | Action items           | Work to do on the model                       | “rename this,” “split class,” “add scenario X”                                         | R1C5 — Tea Green • #C0FFC0                  |

Color selection rule:
Use the first row of the VP color palette and select the indicated column (R1C2…R1C8). The first column is white—skip it[^no-default-blue].

## Note Usage and Diagramming Rules

### Categories & Content
- Exactly one category per note — never mix categories in the same note.
- Keep notes concise; link out for detailed context when necessary.
- Do not write OCL expressions inside CNST notes. These notes contain plain-text paraphrases of OCL.
- Treat CNST and SEMI as authoritative; other categories are guidance.

### Forms & Anchoring
- A note can appear in one of three forms:
  1. Anchored to a single class, relation, or another note.
  2. Anchored to multiple classes/relations/notes.
  3. No anchor (interpreted as diagram-wide).
- Always anchor a note when it refers to specific elements; do not leave it anchorless if it targets a particular class, relation, or note.
- CNST notes must be anchored (no diagram-wide CNST). Anchor to the element that holds the OCL; the note contains the plain-text paraphrase of that OCL.
- Use multiple anchors only if the same content genuinely applies to several elements.

### Text Formatting
- Use plain ASCII where possible; avoid emphasis (bold, italics, underline, highlighting) except for the tag token, which must be bold.
- The first token must be the tag and a colon (e.g., **CNST:**), followed by a single space and the text.
- Prefer short sentences; use lists only when clarity truly improves (hyphen `-` list, no nested lists).
- All note text must be fully visible in the diagram and in exports (PNG). Resize or wrap text instead of truncating.

### Color & Borders
- Fill color must match the category table (R1C2…R1C8). Custom colors are forbidden.
- Keep default font, font size, border color, and border weight; do not use shadows, gradients, icons, or emojis.

### Positioning & Routing
- Place notes close to their target (roughly one element’s width away or less).
- To avoid enlarging exported images, keep notes within the diagram’s current bounds: align notes along the outer edges of the outermost elements and avoid placing notes beyond those edges so the canvas does not expand.
- Diagram-wide (no-anchor) notes should be placed on the right side of the diagram and, when multiple, aligned vertically.
- Route connectors orthogonally, shortest path; avoid crossing other connectors or key diagram lines.

### Diagram Cleanliness
- Do not overlap notes with element bodies, labels, or compartments.
- If two notes would collide, stack them vertically with equal spacing and parallel connectors.

## Example Snippets

<!-- TODO: Update using real examples. -->
* `SEMI: "Encounter" denotes a healthcare interaction episode; not a location stay.`
* `CNST: context Patient must have exactly one active Identifier.`
* `RATL: Kept 'Episode' separate from 'Visit' to allow cross-facility grouping.`
* `TRAC: Derived from Req HRI-EPI-012 and SNOMED CT 123456.`

## References

[^name]: Names obtained from the [color-name website](https://www.color-name.com/).
[^rxcy]: RxCy indicate the row and column of Visual Paradigm’s default color table.
[^no-default-blue]: The VP default note color (blue) is intentionally excluded so each note gets a unique category color.
