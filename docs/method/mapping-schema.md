# The Health-RI SSSOM Mapping Set Schema

One of the key deliverables of the Health-RI Semantic Interoperability Initiative is a SSSOM mapping set. This mapping set is manually curated, reflecting the efforts of both the dedicated mapping team and external collaborators. In line with work that treats mappings as first-class artifacts separating meaning (data element concepts) from representation, Health-RI uses SSSOM to support semantic traceability and reuse across standards (e.g., FHIR [8], OMOP [11], openEHR [9]) [29]. For the initiative-level conceptual background (including our definition of semantic traceability), see our [academic paper](https://raw.githubusercontent.com/Health-RI/semantic-interoperability/main/documents/preprints/enabling-semantic-traceability-in-health-data-v1.1.0.pdf) [30]. For the mapping-specific conceptual background and rationale behind our mappings, see the [Mapping Strategy](./mapping-strategy.md).

This page documents the mappings curated and published by Health-RI. Partners may also embed mappings directly into their own ontologies, as explained in the [Mapping Strategy](./mapping-strategy.md).

!!! tip "Want to browse the mappings?"
    For an interactive view of the **already created** mappings, see **[Mappings](../ontology/mappings.md)**.

## Permanent URIs

We offer several stable and accessible URIs for accessing the mapping set in different formats, supporting long-term findability and reuse in FAIR-aligned infrastructures [1], [18]:

- `https://w3id.org/health-ri/semantic-interoperability/mappings` — Redirects to the TTL version of the SSSOM mappings.
- `https://w3id.org/health-ri/semantic-interoperability/mappings/ttl` — Redirects to the TTL version of the SSSOM mappings.
- `https://w3id.org/health-ri/semantic-interoperability/mappings/tsv` — Redirects to the TSV version of the SSSOM mappings.

!!! tip "What are Permanent (Persistent) URIs?"
    See [W3C Cool URIs don't change](https://www.w3.org/Provider/Style/URI) for the design principles behind stable, resolvable identifiers, and the [w3id community service](https://w3id.org/) for implementing them in practice.

## Versioning Strategy

As per the authoritative policy in the [Mapping Governance page's Versioning and Change Control](./mapping-governance.md#versioning-and-change-control) section, releases are dated `YYYY-MM-DD` (at most one per calendar day) and records are **append-only** via `replaces`.

For lifecycle states, approvals, and publication policy, see the [Governance, Lifecycle, and Validation of the Health-RI SSSOM Mapping Set](./mapping-governance.md) page.

!!! tip "Why append-only?"
    An append-only approach (immutable log) preserves a complete audit trail, makes releases reproducible, and avoids ambiguity about which version of a mapping was used.

## SSSOM File Schema

SSSOM-based mapping sets have been used to operationalize semantic traceability by enabling meaning-level correspondences across heterogeneous standards while preserving separations between concepts and representations [29].

!!! note "Language tags for labels"
    The `subject_label` and `object_label` fields **must** be language-tagged (RDF langstrings), e.g., `Patient@en`, `Patiënt@nl`.

!!! info "What is a language-tagged string?"
    In RDF, a *language-tagged string* is a literal paired with a BCP 47 language tag (e.g., `Patient@en`, `Patiënt@nl`). See: [W3C RDF Schema 1.1 (`rdf:langString`)](https://www.w3.org/TR/rdf-schema/) and [RFC 5646 (BCP 47 tags)](https://datatracker.ietf.org/doc/html/rfc5646).

Below is the schema for the SSSOM TSV file, with each field's link to the specification, expected datatype, cardinality, mandatory status, a concise description, and an illustrative example:

| Field                                                                                        | Type                  | Cardinality | Mandatory | Description                                                                      | Example                                                | Provided by              |
| -------------------------------------------------------------------------------------------- | --------------------- | ----------- | --------- | -------------------------------------------------------------------------------- | ------------------------------------------------------ | ------------------------ |
| [record_id](https://mapping-commons.github.io/sssom/record_id/)                              | EntityReference       | 1           | Yes       | Unique ID of the mapping record                                                  | `hrim:1c56bebe`[^hrim]                                 | Curator                  |
| [subject_id](https://mapping-commons.github.io/sssom/subject_id/)                            | EntityReference       | 1           | Yes       | Identifier of the subject entity                                                 | `fhir:Patient`                                         | Contributor              |
| [subject_label](https://mapping-commons.github.io/sssom/subject_label/)                      | String                | 0..1        | No        | Language-tagged label of the subject entity                                      | `Patient@en`                                           | Contributor              |
| [predicate_id](https://mapping-commons.github.io/sssom/predicate_id/)[^predicate_id_allowed] | EntityReference       | 1           | Yes       | A Health-RI Mapping Vocabulary (HRIV) object property linking subject and object | `hriv:hasExactMeaning`                                 | Contributor              |
| [predicate_modifier](https://mapping-commons.github.io/sssom/predicate_modifier/)            | PredicateModifierEnum | 0..1        | No        | A modifier for negating the predicate[^predicate_modifier]                       | `Not`                                                  | Contributor              |
| [object_id](https://mapping-commons.github.io/sssom/object_id/)                              | EntityReference       | 1           | Yes       | Identifier of the object entity                                                  | `hrio:Person`                                          | Contributor              |
| [object_label](https://mapping-commons.github.io/sssom/object_label/)                        | String                | 0..1        | No        | Language-tagged label of the object entity                                       | `Person@en`                                            | Contributor              |
| [object_category](https://mapping-commons.github.io/sssom/object_category/)                  | String                | 0..1        | No        | OntoUML stereotype of the object                                                 | `Kind`                                                 | Contributor              |
| [mapping_justification](https://mapping-commons.github.io/sssom/mapping_justification/)      | EntityReference       | 1           | Yes       | Method or rationale for creating a mapping[^mapping_justification]               | `semapv:ManualMappingCuration`                         | Contributor (or Default) |
| [author_id](https://mapping-commons.github.io/sssom/author_id/)                              | EntityReference(s)    | 1..*        | Yes       | Identifier(s) of who created the mapping                                         | `orcid:0000-0003-2736-7817`                            | Contributor              |
| [author_label](https://mapping-commons.github.io/sssom/author_label/)                        | String(s)             | 0..*        | No        | Name(s) of the mapping author(s)                                                 | `Pedro P. F. Barcelos`                                 | Contributor              |
| [reviewer_id](https://mapping-commons.github.io/sssom/reviewer_id/)                          | EntityReference(s)    | 1..*        | Yes       | Identifier(s) of mapping reviewer(s) (at least one required)                     | `orcid:0000-0001-2345-6789`                            | Contributor              |
| [reviewer_label](https://mapping-commons.github.io/sssom/reviewer_label/)                    | String(s)             | 0..*        | No        | Name(s) of the mapping reviewer(s)                                               | `Jane Doe`                                             | Contributor              |
| [creator_id](https://mapping-commons.github.io/sssom/creator_id/)                            | EntityReference       | 1           | Yes       | Agent responsible for publishing the mapping                                     | `https://w3id.org/health-ri/semantic-interoperability` | System (Fixed)           |
| [creator_label](https://mapping-commons.github.io/sssom/creator_label/)                      | String                | 1           | Yes       | Name of the publishing agent                                                     | `Health-RI Semantic Interoperability Initiative`       | System (Fixed)           |
| [license](https://mapping-commons.github.io/sssom/license/)                                  | NonRelativeURI        | 1           | Yes       | License governing mapping use                                                    | `https://creativecommons.org/licenses/by/4.0/`         | Contributor (or Default) |
| [subject_type](https://mapping-commons.github.io/sssom/subject_type/)                        | EntityTypeEnum        | 0..1        | No        | Type of the subject entity                                                       | `owl class`                                            | Contributor              |
| [subject_source](https://mapping-commons.github.io/sssom/subject_source/)                    | EntityReference       | 0..1        | No        | Source vocabulary of the subject entity                                          | `https://hl7.org/fhir`                                 | Contributor              |
| [subject_source_version](https://mapping-commons.github.io/sssom/subject_source_version/)    | String                | 0..1        | No        | Version of the subject source                                                    | `R4`                                                   | Contributor              |
| [object_source_version](https://mapping-commons.github.io/sssom/object_source_version/)      | String                | 0..1        | No        | Version of the Health-RI Ontology (HRIO) used for the mapping                    | `0.9.1`                                                | Contributor (or Default) |
| [mapping_date](https://mapping-commons.github.io/sssom/mapping_date/)                        | Date                  | 1           | Yes       | Date when mapping was created (format: YYYY-MM-DD)                               | `2025-07-02`                                           | Contributor              |
| [publication_date](https://mapping-commons.github.io/sssom/publication_date/)                | Date                  | 1           | Yes       | Date when mapping was published (format: YYYY-MM-DD)                             | `2025-07-30`                                           | System (Generated)       |
| [comment](https://mapping-commons.github.io/sssom/comment/)                                  | String                | 0..1        | No        | Free-text notes about the mapping                                                | `Reviewed for consistency with ontology v0.9.1.`       | Contributor              |
| [replaces](https://www.dublincore.org/specifications/dublin-core/dcmi-terms/terms/replaces/) | EntityReference(s)    | 0..*        | No        | Indicates that this mapping record replaces another                              | `hrim:1c56bebe`                                        | Contributor              |

!!! note "Identity distinctness (two-person rule)"
    For every row, the set of `author_id` values **must be disjoint** from the set of `reviewer_id` values. This is validated at publication time (see the [Mappings Governance](./mapping-governance.md) page).

!!! note "Uniqueness of `hriv:hasExactMeaning` (current rows)"
    For any given `subject_id`, there may be **at most one** *current* row with `predicate_id = hriv:hasExactMeaning` (i.e., not superseded via `replaces`, and with no `predicate_modifier = Not`). Rationale: Strategy requires a single exact meaning per concept; "current" follows the append-only supersession model. See the [Mappings Governance](./mapping-governance.md) page for the publication-time check.

!!! note "Responsible initiative (publisher)"
    The mapping-set's `creator_id` and `creator_label` identify the initiative responsible for making the resource available (i.e., the Health-RI Semantic Interoperability Initiative). SSSOM defines no per-row "curator" slot. The curator's approval is recorded in the publication workflow.

!!! note "If you negate a predicate"
    When `predicate_modifier` is set to `Not`, include a brief rationale in `comment` explaining **why** the negation applies. See the [Mapping Governance page's Justification and Evidence section](./mapping-governance.md#justification-and-evidence) for the policy.

!!! warning "HRIV predicates are not OWL equivalence/subsumption"
    `hriv:hasExactMeaning`, `hriv:hasBroaderMeaningThan`, and `hriv:hasNarrowerMeaningThan` express **meaning-level** links for traceability and reuse. They must not be interpreted as OWL class axioms (e.g., `owl:equivalentClass`, `rdfs:subClassOf`) or as evidence of class identity across standards. [22], [19]

!!! tip "Record versions precisely for reproducibility"
    When available, always provide an exact source release identifier in `subject_source_version` and `object_source_version` (not just a major family like "R4"). This makes it clear which standard/ontology release your mapping was evaluated against. [8], [9], [11]

### Responsibility Legend

The following legend explains who is responsible for providing or assigning each field in the schema, clarifying whether values come from contributors, curators, or are system-generated:

- **Contributor** – Must be provided in PRs.
- **Curator** – Added manually by Health-RI curators.
- **Contributor (or Default)** – Contributor should provide this; if omitted, the system assigns a default.
- **System (Fixed)** – Always set to a fixed value, cannot be changed.
- **System (Generated)** – Automatically assigned at publication time, not editable.

### Type Legend

The following table lists and defines all datatypes used in the schema above, according to the [SSSOM specification](https://mapping-commons.github.io/sssom/):

| Type                                                                           | Definition                                                                      | Example                                                  |
| ------------------------------------------------------------------------------ | ------------------------------------------------------------------------------- | -------------------------------------------------------- |
| [EntityReference](https://mapping-commons.github.io/sssom/EntityReference/)    | A CURIE[^curie] or URI referring to an entity in a vocabulary or ontology.      | `fhir:Patient`                                           |
| [EntityReference(s)](https://mapping-commons.github.io/sssom/EntityReference/) | One or more CURIEs or URIs referring to entities in vocabularies or ontologies. | `orcid:0000-0003-2736-7817 \| orcid:0000-0001-2345-6789` |
| [String](https://mapping-commons.github.io/sssom/String/)                      | A literal string value, typically plain text.                                   | `Patient`                                                |
| [String(s)](https://mapping-commons.github.io/sssom/String/)                   | One or more literal string values, typically plain text.                        | `Pedro P. F. Barcelos \| Jane Doe`                       |
| [NonRelativeURI](https://mapping-commons.github.io/sssom/NonRelativeURI/)      | An absolute URI (non-relative), typically identifying a web resource.           | `https://creativecommons.org/licenses/by/4.0/`           |
| [EntityTypeEnum](https://mapping-commons.github.io/sssom/EntityTypeEnum/)      | A controlled vocabulary of entity types (e.g., `owl class`, `rdf property`).    | `owl class`                                              |
| [Date](https://mapping-commons.github.io/sssom/Date/)                          | A calendar date in ISO 8601 format (YYYY-MM-DD).                                | `2025-07-02`                                             |

### Default Values

Some fields in the schema have predefined default values automatically assigned when contributors do not provide them:

- **mapping_justification** – Defaults to `semapv:ManualMappingCuration`.
- **license** – Defaults to `https://creativecommons.org/licenses/by/4.0/`.
- **object_source_version** – Defaults to HRIO's latest version number. E.g., `1.0.0`.
- **mapping_date** - Defaults to the date the contribution was received via GitHub issue.

!!! note "Defaults are resolved to concrete values"
    Defaults such as `object_source_version` and `mapping_date` are resolved to specific values at curation time and stored in the record.
    They are not interpreted as "floating latest" values.

## How to Contribute

We welcome contributions to expand and refine the mapping set. Choose one of the following methods:

### Preferred: Submit the issue form

Use our **[SSSOM mapping issue form](https://github.com/Health-RI/semantic-interoperability/issues/new?template=sssom-new-mapping.yml)** to add a single mapping row. Fill in the required fields and submit; Health-RI curators will review and integrate your contribution.

### Alternative: Use the Excel template

Download the **[XLSX template](https://raw.githubusercontent.com/Health-RI/semantic-interoperability/refs/heads/main/resources/mappings_template.xlsx)** and enter:

- the mapping row(s) in the mappings sheet, and
- all CURIE prefix bindings in the prefix sheet.

Attach the completed file to a new GitHub issue; we will review it and add the mappings to the official set.

!!! note "CURIE prefixes must be declared consistently"
    If you introduce any new CURIE prefix, declare it in the prefix sheet (XLSX) or the submission so that others can resolve it. Use official namespace URIs and stable community identifiers whenever possible.

In the template, field headers are color-coded as follows:

- mandatory with no default have a black background;
- mandatory with a fixed default are purple and pre-filled;
- mandatory with a variable default are purple and not pre-filled;
- optional are green.

Both methods ensure your contribution is reviewed and incorporated into the official Health-RI SSSOM mapping set.

### Submission checklist for contributors

!!! tip "Quick check: are your URIs valid?"
    Before submitting, verify that all HTTP URIs resolve and are well-formed. A simple online check: <https://0mg.github.io/tools/uri/>

Before submitting, please verify the following to ensure your contribution is complete and compliant with the schema:

- All **mandatory** contributor fields are present and correctly formatted.
- All `subject_label` and `object_label` fields you provide are language-tagged (e.g., `Patient@en`, `Patiënt@nl`).
- Any optional values provided use valid identifiers (e.g., ORCID IDs, resolvable URIs, SEMAPV terms).

## References

[1] Wilkinson, M. D., et al. (2016). The FAIR guiding principles for scientific data management and stewardship. *Scientific Data, 3*(1), 160018. https://doi.org/10.1038/sdata.2016.18

[8] HL7 International. (2023). *FHIR Release 5*. Retrieved December 1, 2025, from https://www.hl7.org/fhir/R5/

[9] openEHR Foundation. (2020). *Architecture overview*. Retrieved December 1, 2025, from https://specifications.openehr.org/releases/BASE/latest/architecture_overview.html

[11] Observational Health Data Sciences and Informatics. (2014). *OMOP Common Data Model*. Retrieved December 1, 2025, from https://ohdsi.github.io/CommonDataModel/

[18] Guizzardi, G. (2020). Ontology, ontologies and the "I" of FAIR. *Data Intelligence, 2*(1–2), 181–191. https://doi.org/10.1162/dint_a_00040

[19] Guarino, N. (1998). *Formal ontology in information systems: Proceedings of the 1st International Conference (FOIS '98), June 6–8, 1998, Trento, Italy* (1st ed.). IOS Press.

[22] Guizzardi, G., & Guarino, N. (2024). Explanation, semantics, and ontology. *Data & Knowledge Engineering, 153*, 102325. https://doi.org/10.1016/j.datak.2024.102325

[29] Zhang, S., Smits, A., Brochhausen, M., Solbrig, H. E., & Wilkinson, M. D. (2021). Operationalizing the ISO/IEC 11179 metadata registry model for semantic findability, interoperability and reuse of complex data elements. *International Journal on Semantic Web and Information Systems, 17*(4), 1–33. https://doi.org/10.4018/IJSWIS.2021100101

[30] Barcelos, P. P. F., van Ulzen, N., Groeneveld, R., Konrad, A., Khalid, Q., Zhang, S., Trompert, A., & Vos, J. (n.d.). *Enabling Semantic Traceability in Health Data: The Health-RI Semantic Interoperability Initiative* (manuscript approved at SWAT4HCLS 2026, v1.1.1). [Download link.](https://raw.githubusercontent.com/Health-RI/semantic-interoperability/main/documents/preprints/enabling-semantic-traceability-in-health-data-v1.1.0.pdf).

<!-- Footnotes -->
[^hrim]: `hrim` is the prefix for <https://w3id.org/health-ri/semantic-interoperability/mappings#>
[^predicate_id_allowed]: Allowed values: `hriv:hasExactMeaning`, `hriv:hasBroaderMeaningThan`, `hriv:hasNarrowerMeaningThan`.
[^predicate_modifier]: May either be set to `Not` (its only valid value) or left empty. It is used specifically to express a negated mapping predicate.
[^mapping_justification]: Currently, the only acceptable value for `mapping_justification` is `semapv:ManualMappingCuration`, or a comparable alternative subject to curator evaluation. This constraint is essential for maintaining the necessary semantic alignment.
[^curie]: W3C CURIE Syntax 1.0 (compact URIs): <https://www.w3.org/TR/curie/>
