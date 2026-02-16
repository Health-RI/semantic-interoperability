# Ontology Note Classification and Visual Conventions

This page defines the standardized system of note tags, categories, and color conventions used in UML/OntoUML diagrams for ontology engineering work.
It ensures consistent visual annotation, semantic clarity, and readability across diagrams produced in Visual Paradigm (VP).

## Purpose & Scope

This guide standardizes how ontology modelers should:

- Classify and label UML notes according to their role (e.g., semantics, constraints and derivation rules, rationale, etc.).
- Apply consistent colors and anchoring rules within Visual Paradigm diagrams.
- Maintain visual clarity, traceability, and stylistic uniformity across Health-RI ontology artifacts.

The scope covers all ontology-related UML diagrams, including those representing OntoUML, HRIO, or HRIV concepts.
It excludes notation for formal constraint syntax itself or purely graphical conventions unrelated to note usage.

## Note Categories and Colors

Palette convention (RxCy): Visual Paradigm (VP) defines a fixed color grid within its Formats window, shown below.

<figure>
  <img src="../assets/images/color-table.png" alt="Visual Paradigm formatting window showing the color grid. The top row (R1), highlighted in red, contains the color options used for note categories." width="720">
  <figcaption><em>Figure.</em> Visual Paradigm formatting window with the color grid.
  The top row (R1), marked in red, shows the color options used for note categories (columns C2–C8).</figcaption>
</figure>

Each cell in the grid can be identified using a Row × Column notation (RxCy), where R1C1 means "Row 1, Column 1." The top row (R1) contains the main palette options, and the first column (R1C1) is white. The highlighted red rectangle in the image marks that top row (R1), from which all category colors are selected.

| Tag      | Category               | What goes here                                | Typical contents                                                                                           | Color (VP slot — Name[^name] — HEX)                                                                                                                              |
| -------- | ---------------------- | --------------------------------------------- | ---------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **SEMI** | Semantics & intent     | Clarify meaning beyond the stereotype/name    | term definition, conceptual nuance, OntoUML meaning, disambiguation                                        | R1C7 — Lavender Blue — <div style="background-color:#C0C0FF;width:90px;height:22px;border:1px solid #999;text-align:center;line-height:22px;">#C0C0FF</div>      |
| **CNST** | Constraint rules       | Plain-language paraphrase of constraint rules | paraphrase of constraint rules, invariants, pre/postconditions, multiplicity rationales (no formal syntax) | R1C2 — Spanish Pink — <div style="background-color:#FFC0C0;width:90px;height:22px;border:1px solid #999;text-align:center;line-height:22px;">#FFC0C0</div>       |
| **DRIV** | Derivation rules       | Plain-language paraphrase of derivation rules | paraphrase of derivation rules, derived facts, deterministic inferences (no formal syntax)                 | R1C5 — Tea Green — <div style="background-color:#C0FFC0;width:90px;height:22px;border:1px solid #999;text-align:center;line-height:22px;">#C0FFC0</div>          |
| **RATL** | Rationale              | Why a design choice was made                  | trade-offs, rejected alternatives, decision logs                                                           | R1C8 — Brilliant Lavender — <div style="background-color:#FFC0FF;width:90px;height:22px;border:1px solid #999;text-align:center;line-height:22px;">#FFC0FF</div> |
| **SCOP** | Scope & assumptions    | Boundaries of what the model covers           | simplifying assumptions, context limits, applicability conditions                                          | R1C6 — Celeste — <div style="background-color:#C0FFFF;width:90px;height:22px;border:1px solid #999;text-align:center;line-height:22px;">#C0FFFF</div>            |
| **TRAC** | Traceability & sources | Where a model element comes from              | requirement IDs, standards clauses, tickets, citations                                                     | R1C3 — Very Pale Orange — <div style="background-color:#FFE0C0;width:90px;height:22px;border:1px solid #999;text-align:center;line-height:22px;">#FFE0C0</div>   |
| **EXMP** | Examples & usage       | Small, concrete examples                      | valid/invalid instances, mini sequence snippets                                                            | R1C1 — White — <div style="background-color:#FFFFFF;width:90px;height:22px;border:1px solid #999;text-align:center;line-height:22px;">#FFFFFF</div>              |
| **TODO** | Action items           | Work to do on the model                       | "rename this," "split class," "add scenario X"                                                             | R1C4 — Very Pale Yellow — <div style="background-color:#FFFFC0;width:90px;height:22px;border:1px solid #999;text-align:center;line-height:22px;">#FFFFC0</div>   |

Color selection rule: Use the top row (R1) of the VP color palette, choosing columns C1–C8 as indicated in the table above. Visual Paradigm's default note color (blue) is intentionally excluded so each note gets a unique category color.

## Note Usage and Diagramming Rules

### Categories & Content

- Exactly one category per note — never mix categories in the same note.
- Keep notes concise; link out for detailed context when necessary.
- Do not write formal constraint or derivation syntax (e.g., SHACL, SPARQL, OCL) inside CNST or DRIV notes. These notes contain plain-language descriptions only; the formal expressions live in the external SHACL artifact.
- Treat CNST, DRIV, and SEMI as authoritative; other categories are guidance.

### Forms & Anchoring

- A note can appear in one of three forms:
    1. Anchored to a single class, relation, or another note.
    2. Anchored to multiple classes/relations/notes.
    3. No anchor (interpreted as diagram-wide).
- Always anchor a note when it refers to specific elements; do not leave it anchorless if it targets a particular class, relation, or note.
- **CNST and DRIV notes must be anchored.** Anchor to the element governed by the rule that the note paraphrases.

### Text Formatting

- Use plain ASCII where possible; avoid emphasis (bold, italics, underline, highlighting) except for the required tokens described below.
- General rule (all categories except CNST and DRIV): start the note with the tag and a colon, then a space, then the text. Example: `SEMI: This clarifies the meaning of …`
- **CNST and DRIV formatting:** start with a bold prefix that includes the tag and the rule name in parentheses, then a colon, then a space, then the short description.
- Prefer short sentences; use lists only when clarity truly improves (hyphen `-` list, no nested lists).
- All note text must be fully visible in the diagram and in exports (PNG). Resize or wrap text instead of truncating.

!!! warning "Rule names in notes"

    Rule names appear in parentheses in the `CNST` and `DRIV` prefixes so that each note can be associated with its complete definition in the corresponding SHACL artifact. The ontology diagrams contain only the readable description; the formal rules live in the external SHACL file.

!!! note

    Rule names must follow the constraint naming rules defined in [Ontology Rules and SHACL Implementation](./ontology-rules.md).

!!! info "Rules in `int` stage diagrams (no SHACL formalization yet)"

    A constraint or derivation rule shown in a diagram in the `int` stage may not yet have been formalized in SHACL. In that case, its note may omit the rule name in parentheses and use only the tag prefix (`CNST:` or `DRIV:`) followed by a provisional description. Such notes do not claim a stable link to the SHACL artifact.

    Once the rule has been formalized in SHACL, the corresponding note **must** be updated to follow the standard format with the rule name in parentheses (`**CNST (RuleName):** …` or `**DRIV (RuleName):** …`). All `CNST` and `DRIV` notes that refer to implemented SHACL constraints or derivation rules are required to carry their rule names.

### Color & Borders

- Fill color must match the category table (R1C2…R1C8). Custom colors are forbidden.
- Keep default font, font size, border color, and border weight; do not use shadows, gradients, icons, or emojis.

### Positioning & Routing

- Place notes close to their target (roughly one element's width away or less).
- To avoid enlarging exported images, keep notes within the diagram's current bounds: align notes along the outer edges of the outermost elements and avoid placing notes beyond those edges so the canvas does not expand.
- Diagram-wide (no-anchor) notes should be placed on the right side of the diagram and, when multiple, aligned vertically.
- Route connectors orthogonally, shortest path; avoid crossing other connectors or key diagram lines.

### Diagram Cleanliness

- Do not overlap notes with element bodies, labels, or compartments.
- If two notes would collide, stack them vertically with equal spacing and parallel connectors.

## Example Snippets

<!-- TODO: Update so all use real examples. -->

- **SEMI:** "Encounter" denotes a healthcare interaction episode; not a location stay.
- **CNST (OneActiveIdentifier):** context Patient must have exactly one active Identifier.
- **DRIV (CreatesOnBehalfOfRule):** If an Administrative Gender Recognition mediates both an Administrative Gender Recognition Agent and an Administrative Gender Recognizing Organization, then the Agent creates on behalf of the Organization.
- **RATL:** Kept 'Episode' separate from 'Visit' to allow cross-facility grouping.
- **TRAC:** Derived from Req HRI-EPI-012 and SNOMED CT 123456.
- **SCOP:** "Non-binary Gender Identity" may be further specialized if needed.

## References

[^name]: Names obtained from the [color-name website](https://www.color-name.com/).
