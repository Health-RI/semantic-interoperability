# AI Assistants

!!! warning "Archived project tools"

    The Health-RI Semantic Interoperability Initiative has been **discontinued**. The assistants documented on this page are retained as archival aids and are not actively maintained. If they remain accessible, their outputs are not reviewed, curated, or published by an active Health-RI Semantic Interoperability Initiative workflow.

    See [Initiative Status](../status.md).

The initiative created two specialized GPT assistants:

- The [**Health-RI Semantic Interoperability Guide**](#health-ri-semantic-interoperability-guide-gpt): explains the Health-RI Semantic Interoperability Initiative and helps navigate its archived artifacts.
- The [**HRIO Mapping Assistant**](#hrio-mapping-assistant-gpt): helps draft HRIO meaning mappings in a consistent, reviewable way.

!!! warning "Authoritative sources"

    These assistants are navigation and drafting aids. Treat the published documentation pages and **w3id PIDs** as the authoritative archival references, and always validate outputs before reuse.

!!! warning "Privacy"

    Avoid pasting sensitive, unpublished, or restricted information into the assistants.

## Which assistant should I use?

| If you want to…                                                                                 | Use this assistant                  |
| ----------------------------------------------------------------------------------------------- | ----------------------------------- |
| Understand the initiative, approach, and artifacts (HRIO, HRIV, deliverables, PIDs, governance) | **Semantic Interoperability Guide** |
| Draft a meaning mapping from a schema term/concept to HRIO (HRIV predicate + justification)     | **HRIO Mapping Assistant**          |

## Health-RI Semantic Interoperability Guide (GPT)

If it remains accessible, use this assistant to explain the archived initiative in plain terms and point you to relevant pages and stable identifiers (w3id PIDs).

<div class="button-grid button-grid--wide" markdown>
[Open the Semantic Interoperability Guide (GPT)](https://chatgpt.com/g/g-6992c8eb8780819185f0922ac33d79ce-health-ri-semantic-interoperability-guide){ .md-button .md-button--primary }
</div>

### Typical questions it can help with

- What was the Health-RI Semantic Interoperability Initiative?
- Give me a tour of the project's main artifacts.
- Where can I find the final official HRIO release (docs/spec/TTL/SHACL)?
- Explain HRIO and HRIV (Mapping Vocabulary) and how they were intended to be used.
- How should I cite an ontology or mapping release (and when should I prefer versioned PIDs)?

### Recommended usage

- Use it to navigate the archived site and learn concepts.
- When you need a stable reference, prefer **versioned** PIDs for citations and reproducibility.
- Verify answers against the published documentation because the assistant is not actively maintained.

## HRIO Mapping Assistant (GPT)

If it remains accessible, use this assistant to draft a meaning mapping from an external term/concept to HRIO, aligned with the initiative's documented mapping strategy and governance.

<div class="button-grid button-grid--wide" markdown>
[Open the HRIO Mapping Assistant (GPT)](https://chatgpt.com/g/g-6990a7e348c4819190ef2de88503ff5e-hrio-mapping-assistant){ .md-button .md-button--primary }
</div>

For detailed guidance on scope, evidence rules, limitations, output structure, and prompt traceability, see the [HRIO Mapping Assistant User Guide](mapping-assistant.md).

### What it produces

- Exactly **one** proposed HRIV predicate:
    - `hriv:hasExactMeaning` / `hriv:hasBroaderMeaningThan` / `hriv:hasNarrowerMeaningThan`
- A **confidence %**
- **Evidence snippets** you can use to justify and review the mapping

!!! tip "Archived drafting aid only"

    Always confirm against HRIO documentation and apply the review principles described in **Mapping Governance** yourself. There is no active Health-RI review, curation, or publication workflow for assistant outputs.

### What to provide (best results)

Copy/paste and fill the fields below:

- **Source artifact**: name + version/date (or URL)
- **Term**: label + identifier (IRI/code)
- **Definition**: the authoritative definition (if available)
- **Context of use**: what the term is used for in the source (and any constraints)
- **Candidate HRIO concept(s)** (optional): if you already have candidates

### Output you can use in your own mapping workflow

Use the result to populate or refine:

- HRIV predicate choice (exact / broader / narrower meaning)
- Justification notes / provenance
- A draft SSSOM row (if you maintain mappings as a separate artifact)

## Validation and corrections

If an assistant output conflicts with the published documentation or released artifacts, treat the documentation and versioned PIDs as authoritative. Because the initiative is discontinued, there is no active project correction or integration loop for assistant outputs.
