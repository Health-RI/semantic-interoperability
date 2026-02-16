# AI Assistants

We provide two specialized GPT assistants:

- The [**Health-RI Semantic Interoperability Guide**](#health-ri-semantic-interoperability-guide-gpt): explains the Health-RI Semantic Interoperability Initiative and help you navigate its artifacts.
- The [**HRIO Mapping Assistant**](#hrio-mapping-assistant-gpt): helps you draft HRIO meaning mappings in a consistent, reviewable way.

!!! warning "Authoritative sources"

    These assistants are navigation and drafting aids. Treat the documentation pages and **w3id PIDs** as authoritative references, and always validate before publishing or reusing outputs.

!!! warning "Privacy"

    Avoid pasting sensitive, unpublished, or restricted information into the assistants.

## Which assistant should I use?

| If you want to…                                                                                 | Use this assistant                  |
| ----------------------------------------------------------------------------------------------- | ----------------------------------- |
| Understand the initiative, approach, and artifacts (HRIO, HRIV, deliverables, PIDs, governance) | **Semantic Interoperability Guide** |
| Draft a meaning mapping from a schema term/concept to HRIO (HRIV predicate + justification)     | **HRIO Mapping Assistant**          |

## Health-RI Semantic Interoperability Guide (GPT)

Use this assistant to explain the initiative in plain terms and point you to the right pages and stable identifiers (w3id PIDs).

<div class="button-gridc" markdown>
[Open the Semantic Interoperability Guide (GPT)](https://chatgpt.com/g/g-6992c8eb8780819185f0922ac33d79ce-health-ri-semantic-interoperability-guide){ .md-button .md-button--primary }
</div>

### Typical questions it can help with

- What is the Health-RI Semantic Interoperability Initiative?
- Give me a tour of the project’s main artifacts.
- Where can I find the latest official HRIO release (docs/spec/TTL/SHACL)?
- Explain HRIO and HRIV (Mapping Vocabulary) and how they should be used.
- How should I cite an ontology or mapping release (and when should I prefer versioned PIDs)?

### Recommended usage

- Use it to navigate the site and learn concepts.
- When you need a stable reference, prefer **versioned** PIDs for citations and reproducibility.

## HRIO Mapping Assistant (GPT)

Use this assistant to draft a meaning mapping from an external term/concept to HRIO, aligned with the project’s mapping strategy and governance.

<div class="button-gridc" markdown>
[Open the HRIO Mapping Assistant (GPT)](https://chatgpt.com/g/g-6990a7e348c4819190ef2de88503ff5e-hrio-mapping-assistant){ .md-button .md-button--primary }
</div>

### What it produces

- Exactly **one** proposed HRIV predicate:
    - `hriv:hasExactMeaning` / `hriv:hasBroaderMeaningThan` / `hriv:hasNarrowerMeaningThan`
- A **confidence %**
- **Evidence snippets** you can use to justify and review the mapping

!!! tip "Drafting aid only"

    Always confirm against HRIO documentation and apply the review/curation rules described in **Mapping Governance**.

### What to provide (best results)

Copy/paste and fill the fields below:

- **Source artifact**: name + version/date (or URL)
- **Term**: label + identifier (IRI/code)
- **Definition**: the authoritative definition (if available)
- **Context of use**: what the term is used for in the source (and any constraints)
- **Candidate HRIO concept(s)** (optional): if you already have candidates

### Output you can paste into a mapping workflow

Use the result to populate or refine:

- HRIV predicate choice (exact / broader / narrower meaning)
- Justification notes / provenance
- A draft SSSOM row (if you maintain mappings as a separate artifact)

## Feedback and correction loop

If an assistant output conflicts with the documentation:

1. Treat the docs/PIDs as authoritative.
2. Adjust the mapping or interpretation.
3. If needed, open an issue/discussion in the repository so the documentation can be improved.
