# SSSOM Mapping Set

One of the key deliverables of the Health-RI Semantic Interoperability Initiative is a **SSSOM mapping set**. This mapping set is **manually curated**, reflecting the efforts of both the dedicated mapping team and external collaborators. For the conceptual background and rationale behind our mappings, see the [Mapping Strategy](./mapping-strategy.md).

This page documents the mappings curated and published by Health-RI. Partners may also embed mappings directly into their own ontologies, as explained in the [Mapping Strategy](./mapping-strategy.md).

## Permanent URIs

We offer several stable and accessible URIs for accessing the mapping set in different formats:

- `https://w3id.org/health-ri/semantic-interoperability/mappings` — Redirects to the **TTL** version of the SSSOM mappings.
- `https://w3id.org/health-ri/semantic-interoperability/mappings/ttl` — Redirects to the **TTL** version of the SSSOM mappings.
- `https://w3id.org/health-ri/semantic-interoperability/mappings/tsv` — Redirects to the **TSV** version of the SSSOM mappings.

## Versioning Strategy

Unlike the Health-RI Ontology (which may use semantic versioning or other schemes), the **mapping set versioning** is based on the **YYYY-MM-DD** format, corresponding to its **publication date**.
There will be **at most one version released per day**.

Importantly, **mappings cannot be removed** once they’re published. To revise a mapping (e.g., if it was erroneous or needs replacement), we use the `replaces` field to refer back to the original entry that the new one supersedes.

## SSSOM File Schema

Below is the schema for the SSSOM TSV file, with each field’s link to the specification, expected datatype, cardinality, mandatory status, a concise description, and an illustrative example:

| Field                                                                                        | Type                  | Cardinality | Mandatory | Description                                            | Example                                                | Provided by              |
| -------------------------------------------------------------------------------------------- | --------------------- | ----------- | --------- | ------------------------------------------------------ | ------------------------------------------------------ | ------------------------ |
| [record_id](https://mapping-commons.github.io/sssom/record_id/)                              | EntityReference       | 1           | Yes       | Unique ID of the mapping record                        | `http://health-ri.org/mappings/rec123`                 | Curator                  |
| [subject_id](https://mapping-commons.github.io/sssom/subject_id/)                            | EntityReference       | 1           | Yes       | Identifier of the subject entity                       | `fhir:Patient`                                         | Contributor              |
| [subject_label](https://mapping-commons.github.io/sssom/subject_label/)                      | String                | 0..1        | No        | Label of the subject entity                            | `Patient`                                              | Contributor              |
| [predicate_id](https://mapping-commons.github.io/sssom/predicate_id/)                        | EntityReference       | 1           | Yes       | Relation linking subject and object                    | `hriv:hasExactMeaning`                                 | Contributor              |
| [predicate_modifier](https://mapping-commons.github.io/sssom/predicate_modifier/)            | PredicateModifierEnum | 0..1        | No        | A modifier for negating the predicate[^1]              | `Not`                                                  | Contributor              |
| [object_id](https://mapping-commons.github.io/sssom/object_id/)                              | EntityReference       | 1           | Yes       | Identifier of the object entity                        | `hrio:Person`                                          | Contributor              |
| [object_label](https://mapping-commons.github.io/sssom/object_label/)                        | String                | 0..1        | No        | Label of the object entity                             | `Person`                                               | Contributor              |
| [object_category](https://mapping-commons.github.io/sssom/object_category/)                  | String                | 0..1        | No        | OntoUML stereotype of the object                       | `Kind`                                                 | Contributor              |
| [mapping_justification](https://mapping-commons.github.io/sssom/mapping_justification/)      | EntityReference       | 1           | Yes       | Method or rationale for creating a mapping[^2]         | `semapv:ManualMappingCuration`                         | Contributor (or Default) |
| [author_id](https://mapping-commons.github.io/sssom/author_id/)                              | EntityReference(s)    | 1..*        | Yes       | Identifier(s) of who created the mapping               | `orcid:0000-0003-2736-7817`                            | Contributor              |
| [author_label](https://mapping-commons.github.io/sssom/author_label/)                        | String(s)             | 0..*        | No        | Name(s) of the mapping author(s)                       | `Pedro P. F. Barcelos`                                 | Contributor              |
| [reviewer_id](https://mapping-commons.github.io/sssom/reviewer_id/)                          | EntityReference(s)    | 0..*        | No        | Identifier(s) of mapping reviewer(s)                   | `orcid:0000-0001-2345-6789`                            | Contributor              |
| [reviewer_label](https://mapping-commons.github.io/sssom/reviewer_label/)                    | String(s)             | 0..*        | No        | Name(s) of the mapping reviewer(s)                     | `Jane Doe`                                             | Contributor              |
| [creator_id](https://mapping-commons.github.io/sssom/creator_id/)                            | EntityReference       | 1           | Yes       | Agent responsible for publishing the mapping           | `https://w3id.org/health-ri/semantic-interoperability` | System (Fixed)           |
| [creator_label](https://mapping-commons.github.io/sssom/creator_label/)                      | String                | 1           | Yes       | Name of the publishing agent                           | `Health-RI Semantic Interoperability Initiative`       | System (Fixed)           |
| [license](https://mapping-commons.github.io/sssom/license/)                                  | NonRelativeURI        | 1           | Yes       | License governing mapping use                          | `https://creativecommons.org/licenses/by/4.0/`         | Contributor (or Default) |
| [subject_type](https://mapping-commons.github.io/sssom/subject_type/)                        | EntityTypeEnum        | 0..1        | No        | Type of the subject entity                             | `owl:Class`                                            | Contributor              |
| [subject_source](https://mapping-commons.github.io/sssom/subject_source/)                    | EntityReference       | 0..1        | No        | Source vocabulary of the subject entity                | `http://hl7.org/fhir`                                  | Contributor              |
| [subject_source_version](https://mapping-commons.github.io/sssom/subject_source_version/)    | String                | 0..1        | No        | Version of the subject source                          | `R4`                                                   | Contributor              |
| [object_source_version](https://mapping-commons.github.io/sssom/object_source_version/)      | String                | 0..1        | No        | Version of the Health-RI ontology used for the mapping | `0.9.1`                                                | Contributor (or Default) |
| [mapping_date](https://mapping-commons.github.io/sssom/mapping_date/)                        | Date                  | 1           | Yes       | Date when mapping was created (format: YYYY-MM-DD)     | `2025-07-02`                                           | Contributor              |
| [publication_date](https://mapping-commons.github.io/sssom/publication_date/)                | Date                  | 1           | Yes       | Date when mapping was published (format: YYYY-MM-DD)   | `2025-07-30`                                           | System (Generated)       |
| [comment](https://mapping-commons.github.io/sssom/comment/)                                  | String                | 0..1        | No        | Free-text notes about the mapping                      | `Reviewed for consistency with ontology v0.9.1.`       | Contributor              |
| [replaces](https://www.dublincore.org/specifications/dublin-core/dcmi-terms/terms/replaces/) | EntityReference(s)    | 0..*        | No        | Indicates that this mapping record replaces another    | `http://health-ri.org/mappings/rec122`                 | Contributor              |

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
| [EntityReference](https://mapping-commons.github.io/sssom/EntityReference/)    | A CURIE or URI referring to an entity in a vocabulary or ontology.              | `fhir:Patient`                                           |
| [EntityReference(s)](https://mapping-commons.github.io/sssom/EntityReference/) | One or more CURIEs or URIs referring to entities in vocabularies or ontologies. | `orcid:0000-0003-2736-7817 \| orcid:0000-0001-2345-6789` |
| [String](https://mapping-commons.github.io/sssom/String/)                      | A literal string value, typically plain text.                                   | `Patient`                                                |
| [String(s)](https://mapping-commons.github.io/sssom/String/)                   | One or more literal string values, typically plain text.                        | `Pedro P. F. Barcelos \| Jane Doe`                       |
| [NonRelativeURI](https://mapping-commons.github.io/sssom/NonRelativeURI/)      | An absolute URI (non-relative), typically identifying a web resource.           | `https://creativecommons.org/licenses/by/4.0/`           |
| [EntityTypeEnum](https://mapping-commons.github.io/sssom/EntityTypeEnum/)      | A controlled vocabulary of entity types (e.g., `owl:Class`, `rdf:Property`).    | `owl:Class`                                              |
| [Date](https://mapping-commons.github.io/sssom/Date/)                          | A calendar date in ISO 8601 format (YYYY-MM-DD).                                | `2025-07-02`                                             |

### Default Values

Some fields in the schema have predefined default values automatically assigned when contributors do not provide them:

- **mapping_justification** – Defaults to `semapv:ManualMappingCuration`.
- **license** – Defaults to `https://creativecommons.org/licenses/by/4.0/`.
- **object_source** – Defaults to `http://w3id.org/health-ri/ontology`.
- **object_source_version** – Defaults to the ontology's latest version number. E.g., `1.0.0`.
- **mapping_date** - Defaults to the date the contribution was received via GitHub issue.

## How to Contribute

We welcome contributions to expand and refine the mapping set. You can contribute in two ways:

1. **Preferred: Submit the Issue Form**
   Use our **[SSSOM mapping issue form](https://github.com/Health-RI/semantic-interoperability/issues/new?template=sssom-new-mapping.yml)** to add a single mapping row. Fill in the required fields and submit; Health-RI curators will review and integrate your contribution.

2. **Alternative: Use the Excel template**

Download the **[XLSX template](https://raw.githubusercontent.com/Health-RI/semantic-interoperability/refs/heads/main/resources/mappings_template.xlsx)** and enter:

- the mapping row(s) in the mappings sheet, and
- all CURIE prefix bindings in the prefix sheet.

Attach the completed file to a new issue and we will review and add it. In the template, field headers are color-coded as follows:

- mandatory with no default have a black background;
- mandatory with a fixed default are purple and pre-filled;
- mandatory with a variable default are purple and not pre-filled;
- optional are green.

Both methods ensure your contribution is reviewed and incorporated into the official Health-RI SSSOM mapping set.

### **Submission checklist (for contributors)**

Before submitting, please verify the following to ensure your contribution is complete and compliant with the schema:

- All **mandatory** contributor fields are present and correctly formatted.
- Any optional values provided use valid identifiers (e.g., ORCIDs, resolvable URIs, SEMAPV terms).
- If pinning a version, `object_source` is a specific version URI (not a generic one).

<!-- Footnotes -->
[^1]: May either be set to `Not` (its only valid value) or left empty. It is used specifically to express a negated mapping predicate.
[^2]: Currently, the only acceptable value for `mapping_justification` is `semapv:ManualMappingCuration`, or a comparable alternative subject to curator evaluation. This constraint is essential for maintaining the necessary semantic alignment.
