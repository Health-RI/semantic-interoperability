# Contributing to the Health-RI Semantic Interoperability Effort

We welcome community feedback and contributions to help improve the quality, coverage, and clarity of the models and ontologies developed as part of Health-RI's semantic interoperability initiative.

To streamline the contribution process, we provide structured submission forms that help ensure your input is reviewed and addressed efficiently. Choose one of the options below to open the appropriate GitHub Issue form:

<div class="button-grid" markdown>

[Report an Ontology Error](https://github.com/health-ri/semantic-interoperability/issues/new?template=ontology-error-report.yml){ .md-button }

[Request a New Concept](https://github.com/health-ri/semantic-interoperability/issues/new?template=concept-request.yml){ .md-button }

[Other Contribution or Request](https://github.com/health-ri/semantic-interoperability/issues/new?template=other-contribution.yml){ .md-button }

[Propose a SSSOM Mapping](https://github.com/Health-RI/semantic-interoperability/issues/new?template=sssom-new-mapping.yml){ .md-button }

</div>

The sections below explain each type of contribution in more detail and link to the corresponding submission form.

## Contribution Channels

You can contribute to this effort by submitting one of the following types of input:

### Report an Error in the OntoUML or gUFO Ontology

If you identify an error, inconsistency, ambiguity, or omission in any of the semantic artifacts (including diagrams, models, or OWL files), please let us know.
[Click here to submit an ontology error report.](https://github.com/health-ri/semantic-interoperability/issues/new?template=ontology-error-report.yml)

Typical reports may include:

- Incorrect use of stereotypes or relations
- Mislabeled or ambiguous classes
- Discrepancies between diagrams and OWL implementation
- Logical contradictions or violations of ontological principles

### Request a New Concept to Be Added

If you believe a concept is missing from the ontology and should be included (e.g., a new domain-specific class or relation), please use the form below to propose it.
[Click here to request a new concept.](https://github.com/health-ri/semantic-interoperability/issues/new?template=concept-request.yml)

Your request should ideally include:

- A clear label and definition for the proposed concept
- Its relevance within the Health-RI context
- References, standards, or examples supporting the need for this concept

### Other Contributions or Collaboration Requests

For all other types of contributions—including documentation suggestions, collaboration offers, use case proposals, or questions about modeling and alignment—please use the general-purpose form below.
[Click here to submit a general contribution or request.](https://github.com/health-ri/semantic-interoperability/issues/new?template=other-contribution.yml)

Examples of valid submissions:

- Proposing a new use case to guide modeling efforts
- Requesting clarification about specific OntoUML patterns
- Suggesting improvements to model documentation
- Offering to align a dataset with the reference ontology

### Contribute SSSOM Mappings

You can contribute to the Health-RI **SSSOM mapping set** (manually curated) in two ways:

1. **Preferred: Submit the issue form**
   Use our **[SSSOM mapping issue form](https://github.com/Health-RI/semantic-interoperability/issues/new?template=sssom-new-mapping.yml)** to add a single mapping row. Fill in the required fields; Health-RI curators will review and integrate your contribution.

2. **Alternative: Use the Excel template**
   Download the **[XLSX template](https://raw.githubusercontent.com/Health-RI/semantic-interoperability/refs/heads/main/resources/mappings_template.xlsx)** and enter:
   - the mapping row(s) in the **mappings** sheet, and
   - all CURIE prefix bindings in the **prefix** sheet.
   Attach the completed file to a new issue; we'll review and add it.

Both methods ensure your contribution is reviewed and incorporated into the official Health-RI SSSOM mapping set.

For more details, see the [Mapping Set documentation](method/mapping-schema.md).

#### Submission checklist (for contributors)

- All **mandatory** fields are present and correctly formatted.
- Optional values (if provided) use valid identifiers (e.g., ORCID IDs, resolvable URIs, SEMAPV terms).
- If pinning a version, `object_source` is a **specific version URI** (not a generic/latest URI).

## Submission Process

Each of the forms linked above will guide you through the required fields. Submissions are publicly visible as GitHub Issues in our repository and are reviewed regularly by the modeling and coordination teams.

By submitting, you agree to have your contributions used in future releases of the model and/or documentation. Attribution will be provided where applicable.

Thank you for your interest in improving semantic interoperability and helping build a robust reference ontology for health and life sciences.
