# Contribution Channels

Outside specific [Calls for Community Review](call-for-community-review.md), you can contribute at any time by submitting one of the following types of input:

## Report an Error in the OntoUML or gUFO Ontology

If you identify an error, inconsistency, ambiguity, or omission in any of the HRIO artifacts (including diagrams, models, or OWL files), please let us know.

<div class="button-grid" markdown>

[Report an Ontology Error](https://github.com/health-ri/semantic-interoperability/issues/new?template=ontology-error-report.yml){ .md-button }

</div>

Typical reports may include:

- Incorrect use of stereotypes or relations
- Mislabeled or ambiguous classes
- Discrepancies between diagrams and OWL implementation
- Logical contradictions or violations of ontological principles

## Request a New Concept to Be Added

If you believe a concept is missing from the Health-RI Ontology (HRIO) and should be included (e.g., a new domain-specific class or relation), please use the form below to propose it.

<div class="button-grid" markdown>

[Request a New Concept](https://github.com/health-ri/semantic-interoperability/issues/new?template=concept-request.yml){ .md-button }

</div>

Your request should ideally include:

- A clear label and definition for the proposed concept
- Its relevance within the Health-RI context
- References, standards, or examples supporting the need for this concept

## Other Contributions or Collaboration Requests

For all other types of contributions—including documentation suggestions, collaboration offers, use case proposals, or questions about modeling and alignment—please use the general-purpose form below.

<div class="button-grid" markdown>

[Other Contribution or Request](https://github.com/health-ri/semantic-interoperability/issues/new?template=other-contribution.yml){ .md-button }

</div>

Examples of valid submissions:

- Proposing a new use case to guide modeling efforts
- Requesting clarification about specific OntoUML patterns
- Suggesting improvements to model documentation
- Offering to align a dataset with the Health-RI Ontology (HRIO)

## Contribute SSSOM Mappings

!!! tip "Optional helper for mapping submissions"

    Before submitting a mapping, you can use the **HRIO Mapping Assistant (GPT)** to draft a candidate predicate/target and gather evidence snippets:

    <div class="button-grid">
    [Open HRIO Mapping Assistant](https://chatgpt.com/g/g-6990a7e348c4819190ef2de88503ff5e-hrio-mapping-assistant){ .md-button .md-button--primary }
    </div>

    *Always verify against HRIO documentation and follow the governance rules for curated/public mappings.*

You can contribute to the Health-RI **SSSOM mapping set** (manually curated) in two ways:

<div class="button-grid" markdown>

[Propose a SSSOM Mapping](https://github.com/health-ri/semantic-interoperability/issues/new?template=sssom-new-mapping.yml){ .md-button }

</div>

1. **Preferred: Submit the issue form**
    Use our **[SSSOM mapping issue form](https://github.com/health-ri/semantic-interoperability/issues/new?template=sssom-new-mapping.yml)** to add a single mapping row. Fill in the required fields; Health-RI curators will review and integrate your contribution.

2. **Alternative: Use the Excel template**
    Download the **[XLSX template](https://raw.githubusercontent.com/Health-RI/semantic-interoperability/refs/heads/main/resources/mappings_template.xlsx)** and enter:

    - the mapping row(s) in the **mappings** sheet, and
    - all CURIE prefix bindings in the **prefix** sheet.
        Attach the completed file to a new issue; we'll review and add it.

Both methods ensure your contribution is reviewed and incorporated into the official Health-RI SSSOM mapping set.

For more details, see the [Mapping Set documentation](../method/mapping-schema.md). For curation rules (e.g., mapping lifecycle, `replaces`, evidence expectations), see the [Mapping Governance](../method/mapping-governance.md) page.

### Submission checklist (for contributors)

- All **mandatory** fields are present and correctly formatted.
- Optional values (if provided) use valid identifiers (e.g., ORCID IDs, resolvable URIs, SEMAPV terms).
- If pinning a version, `object_source` is a **specific version URI** (not a generic/latest URI).

## Submission Process

Each of the forms linked above will guide you through the required fields. Submissions are publicly visible as GitHub Issues in our repository and are reviewed regularly by the modeling and coordination teams.

By submitting, you agree to have your contributions used in future releases of the model and/or documentation. Attribution will be provided where applicable.

Thank you for your interest in improving semantic interoperability and helping build a robust reference ontology for health and life sciences.
