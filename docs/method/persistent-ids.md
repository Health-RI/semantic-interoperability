# Persistent Identifiers (PIDs)

This page lists the **persistent, stable, and dereferenceable identifiers (PIDs)** established by the Health-RI Semantic Interoperability Initiative. These URIs support semantic interoperability, long-term accessibility, and alignment with FAIR principles.

!!! note "Archival status"

    The Health-RI Semantic Interoperability Initiative has been discontinued. The unversioned or "latest" PIDs documented below continue to resolve to the **final available published artifacts** and are not expected to advance to new initiative releases. Versioned PIDs remain the preferred references for reproducible citation.

!!! tip "Choosing the right PID (formats)"

    Some PIDs can open in different formats depending on how the link is accessed.

    - Use the **about URI** (e.g., `https://w3id.org/health-ri/ontology`) to let the system pick a suitable format automatically.
    - Use an **explicit format URI** (e.g., `/ontology/ttl`, `/ontology/json`, `/mapping-vocabulary/spec`) when you need a specific format.

    Note: browsers usually open HTML pages, while RDF tools can request RDF (e.g., Turtle). You may also be forwarded to GitHub or the documentation site—this is expected; the `w3id.org` link is the stable PID.

## Initiative-Wide Identifier

### URI: `https://w3id.org/health-ri/semantic-interoperability`

This URI refers to the Semantic Interoperability Initiative as a whole. It provides persistent access to the initiative's public-facing resources and is suitable for citing the initiative in publications, websites, and metadata records. For a scholarly citation of the initiative's conceptual rationale, cite the [academic paper](https://w3id.org/health-ri/semantic-interoperability/documents/preprints/enabling-semantic-traceability-in-health-data-v1.1.0.pdf) (and optionally include this URI as the project identifier).

## ChatGPT Assistants / Guides

These PIDs are **simple redirects** (no content negotiation):

- `https://w3id.org/health-ri/semantic-interoperability/hrio-mapping-assistant`
- `https://w3id.org/health-ri/semantic-interoperability/health-ri-semantic-interoperability-guide`

The assistants are retained as archival aids and are not maintained as part of an active Health-RI development, review, or release workflow.

## Documents

Project documents stored in the Semantic Interoperability repository are exposed under:

`https://w3id.org/health-ri/semantic-interoperability/documents/<path>`

This PID pattern redirects to the corresponding file under `documents/` on the `main` branch.

Example:

- `https://w3id.org/health-ri/semantic-interoperability/documents/preprints/enabling-semantic-traceability-in-health-data-v1.1.0.pdf`
    → Preprint PDF (stable PID; file hosted on GitHub)

## Ontology Identifier

### URI: `https://w3id.org/health-ri/ontology`

This is the **main identifier for the Health-RI Ontology (HRIO)** and resolves to the final available published ontology version under this initiative. The namespace IRI for HRIO terms is `https://w3id.org/health-ri/ontology#` (prefix `hrio:`).
In a browser, this typically opens the HTML documentation; RDF tools typically obtain Turtle (or JSON, if requested).

### Identifiers for the **Final / Latest Ontology Version**

These URIs point to the **final available published release** of the Health-RI Ontology and related documentation formats.

| PID                       | Description                                          |
| ------------------------- | ---------------------------------------------------- |
| `/ontology/ttl`           | OWL ontology in Turtle format                        |
| `/ontology/documentation` | HTML rendering of the OntoUML ontology documentation |
| `/ontology/specification` | HTML rendering of the gUFO ontology documentation    |
| `/ontology/json`          | OntoUML model exported as JSON                       |
| `/ontology/vpp`           | OntoUML model file in Visual Paradigm format         |
| `/ontology/shacl`         | SHACL constraint and derivation rules                |

Each of these URIs redirects to the final available version of the resource.

!!! tip

    You can use either `/doc` or `/documentation`, and `/spec` or `/specification` — both forms are valid and equivalent.

!!! note

    Our SHACL file uses the `.shacl` extension and Turtle serialization.

!!! warning "Citing vs browsing"

    Use **versioned** PIDs (e.g., `/ontology/vX.Y.Z/...`) when citing HRIO in papers, metadata, or data releases to ensure reproducibility.
    Use the unversioned/latest PIDs (e.g., `/ontology/ttl`, `/ontology/doc`) for convenient access to the final available published artifacts.

### Identifiers for **Versioned Ontology Releases**

To support traceability and reproducibility, each ontology release is also available via **version-specific URIs**. Each versioned release of the Health-RI Ontology is identified by its own dedicated URI in the format **`https://w3id.org/health-ri/ontology/vX.Y.Z`**. This URI is used as the `owl:versionIRI` in the ontology metadata.

See also:

- [Versioning Strategy for Ontology Releases](./ontology-versioning.md)
- [Initiative Publications](./publications.md)

#### Format

`https://w3id.org/health-ri/ontology/vX.Y.Z/{format}`

Where:

- `X.Y.Z` is the HRIO release version identifier (see the [Ontology Versioning Policy](./ontology-versioning.md)) (e.g., `2.0.0`)
- `{format}` is one of:
    - `ttl` — OWL ontology (Turtle)
    - `vpp` — OntoUML model (Visual Paradigm)
    - `json` — OntoUML model (JSON)
    - `shacl` — SHACL constraint and derivation rules (Turtle)
    - `documentation` — OntoUML documentation (Markdown source, rendered as HTML)
    - `specification` — gUFO HTML documentation

!!! tip

    You can also use the version URI without a `{format}` (e.g., `/v0.6.0`): browsers open the HTML specification, while RDF tools default to Turtle (or JSON if requested).

#### Examples

- `https://w3id.org/health-ri/ontology/v0.6.0/ttl`
    → Ontology in Turtle format for version 0.6.0

- `https://w3id.org/health-ri/ontology/v0.6.0/vpp`
    → Visual Paradigm project file for version 0.6.0

- `https://w3id.org/health-ri/ontology/v0.9.1/documentation`
    → Documentation (Markdown source, rendered as HTML) for OntoUML ontology version 0.9.1

- `https://w3id.org/health-ri/ontology/v0.6.0/specification`
    → HTML documentation for gUFO ontology version 0.6.0

- `https://w3id.org/health-ri/ontology/v0.11.9/shacl`
    → SHACL shapes for version 0.11.9

## SSSOM Mappings PIDs

The following PIDs provide **stable access to the final/latest SSSOM mapping set** produced by the initiative, in both Turtle (TTL) and TSV formats.

### Final / Latest Mappings

- **URI (about / negotiated):**
    `https://w3id.org/health-ri/semantic-interoperability/mappings`
    *(browsers typically open TSV; RDF tools default to Turtle; also available explicitly as `/mappings/ttl` and `/mappings/tsv`)*

- **URI (TTL, explicit):**
    `https://w3id.org/health-ri/semantic-interoperability/mappings/ttl`

- **URI (TSV, explicit):**
    `https://w3id.org/health-ri/semantic-interoperability/mappings/tsv`

These PIDs redirect to the canonical files in the Health-RI GitHub repository (branch `main`). Under the discontinued initiative, they are retained as stable access points to the final available mapping artifacts and are not expected to advance to new releases.

#### Examples

- `https://w3id.org/health-ri/semantic-interoperability/mappings`
    → Final/latest SSSOM mappings. Negotiated: TSV in a browser; TTL for RDF tools

- `https://w3id.org/health-ri/semantic-interoperability/mappings/tsv`
    → Final/latest SSSOM mappings in TSV (`.tsv`)

## Mapping Vocabulary PIDs

The **Health-RI Mapping Vocabulary** defines terms used in our mapping work. The PIDs below provide stable access to the final/latest vocabulary and to versioned snapshots.

### Final / Latest Vocabulary

- **URI (about / negotiated):**
    `https://w3id.org/health-ri/mapping-vocabulary`
    *(browsers typically open the HTML specification; RDF tools default to Turtle; also available explicitly as `/mapping-vocabulary/ttl` and `/mapping-vocabulary/spec`)*

- **URI (TTL, explicit):**
    `https://w3id.org/health-ri/mapping-vocabulary/ttl`

- **URI (HTML specification):**
    `https://w3id.org/health-ri/mapping-vocabulary/specification`
    *(alias: `/mapping-vocabulary/spec`)*

!!! tip

    Both `/spec` and `/specification` are valid and equivalent for the vocabulary specification.

#### Examples

- `https://w3id.org/health-ri/mapping-vocabulary`
    → Final/latest vocabulary. Negotiated: HTML specification in a browser; TTL for RDF tools

- `https://w3id.org/health-ri/mapping-vocabulary/spec`
    → Final/latest HTML specification

### Versioned Vocabulary

Versioned PIDs include an explicit `vX.Y.Z` segment and resolve to immutable artifacts for that release.

- **URI (about / negotiated):**
    `https://w3id.org/health-ri/mapping-vocabulary/vX.Y.Z`
    *(browsers open the HTML specification; RDF tools default to Turtle; also available explicitly as `/vX.Y.Z/ttl` and `/vX.Y.Z/spec`)*

- **URI (TTL, explicit):**
    `https://w3id.org/health-ri/mapping-vocabulary/vX.Y.Z/ttl`

- **URI (HTML specification):**
    `https://w3id.org/health-ri/mapping-vocabulary/vX.Y.Z/specification`
    *(alias: `/vX.Y.Z/spec`)*

#### Examples

- `https://w3id.org/health-ri/mapping-vocabulary/v1.0.0`
    → Vocabulary version `v1.0.0`. Negotiated: HTML specification in a browser; RDF tools default to Turtle

- `https://w3id.org/health-ri/mapping-vocabulary/v1.0.0/spec`
    → HTML specification for version `v1.0.0`

## Overview of Persistent Identifiers

| PID                                                                    | Description                                   | Behavior                                                     | Example                                                                                                                                                                                                                                                                |
| ---------------------------------------------------------------------- | --------------------------------------------- | ------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `/semantic-interoperability`                                           | Project-level identifier                      | Forwards to documentation site                               | [https://w3id.org/health-ri/semantic-interoperability](https://w3id.org/health-ri/semantic-interoperability)                                                                                                                                                           |
| `/semantic-interoperability/git`                                       | Source code and data repository               | Forwards to GitHub                                           | [https://w3id.org/health-ri/semantic-interoperability/git](https://w3id.org/health-ri/semantic-interoperability/git)                                                                                                                                                   |
| `/semantic-interoperability/hrio-mapping-assistant`                    | HRIO Mapping Assistant (ChatGPT)              | Forwards to the ChatGPT assistant                            | [https://w3id.org/health-ri/semantic-interoperability/hrio-mapping-assistant](https://w3id.org/health-ri/semantic-interoperability/hrio-mapping-assistant)                                                                                                             |
| `/semantic-interoperability/health-ri-semantic-interoperability-guide` | Semantic Interoperability Guide (ChatGPT)     | Forwards to the ChatGPT guide                                | [https://w3id.org/health-ri/semantic-interoperability/health-ri-semantic-interoperability-guide](https://w3id.org/health-ri/semantic-interoperability/health-ri-semantic-interoperability-guide)                                                                       |
| `/semantic-interoperability/documents/{path}`                          | Project documents                             | Forwards to the raw file on GitHub (`main`)                  | [https://w3id.org/health-ri/semantic-interoperability/documents/preprints/enabling-semantic-traceability-in-health-data-v1.1.0.pdf](https://w3id.org/health-ri/semantic-interoperability/documents/preprints/enabling-semantic-traceability-in-health-data-v1.1.0.pdf) |
| `/ontology`                                                            | Ontology root (about URI)                     | Forwards to HTML documentation (browser) or TTL/JSON (tools) | [https://w3id.org/health-ri/ontology](https://w3id.org/health-ri/ontology)                                                                                                                                                                                             |
| `/ontology/ttl`                                                        | Final/latest ontology in Turtle format        | Forwards to final/latest `.ttl` file (GitHub)                | [https://w3id.org/health-ri/ontology/ttl](https://w3id.org/health-ri/ontology/ttl)                                                                                                                                                                                     |
| `/ontology/shacl`                                                      | Final/latest SHACL shapes                     | Forwards to final/latest `.shacl` file (GitHub)              | [https://w3id.org/health-ri/ontology/shacl](https://w3id.org/health-ri/ontology/shacl)                                                                                                                                                                                 |
| `/ontology/documentation`                                              | Final/latest HTML documentation               | Forwards to OntoUML human-readable documentation             | [https://w3id.org/health-ri/ontology/documentation](https://w3id.org/health-ri/ontology/documentation)                                                                                                                                                                 |
| `/ontology/specification`                                              | Final/latest HTML specification               | Forwards to gUFO human-readable documentation                | [https://w3id.org/health-ri/ontology/specification](https://w3id.org/health-ri/ontology/specification)                                                                                                                                                                 |
| `/ontology/json`                                                       | Final/latest JSON export of OntoUML           | Forwards to final/latest `.json` file (GitHub)               | [https://w3id.org/health-ri/ontology/json](https://w3id.org/health-ri/ontology/json)                                                                                                                                                                                   |
| `/ontology/vpp`                                                        | Final/latest OntoUML model (`.vpp`)           | Forwards to final/latest `.vpp` file (GitHub)                | [https://w3id.org/health-ri/ontology/vpp](https://w3id.org/health-ri/ontology/vpp)                                                                                                                                                                                     |
| `/ontology/vX.Y.Z/{format}`                                            | Versioned ontology release                    | Forwards to version-specific file/page                       | [https://w3id.org/health-ri/ontology/v0.6.0/ttl](https://w3id.org/health-ri/ontology/v0.6.0/ttl)                                                                                                                                                                       |
| `/semantic-interoperability/mappings`                                  | Final/latest SSSOM mappings (about URI)       | Forwards to TSV (browser) or TTL (RDF tools)                 | [https://w3id.org/health-ri/semantic-interoperability/mappings](https://w3id.org/health-ri/semantic-interoperability/mappings)                                                                                                                                         |
| `/semantic-interoperability/mappings/ttl`                              | Final/latest SSSOM mappings (TTL, explicit)   | Forwards to final/latest `.ttl` file (GitHub)                | [https://w3id.org/health-ri/semantic-interoperability/mappings/ttl](https://w3id.org/health-ri/semantic-interoperability/mappings/ttl)                                                                                                                                 |
| `/semantic-interoperability/mappings/tsv`                              | Final/latest SSSOM mappings (TSV, explicit)   | Forwards to final/latest `.tsv` file (GitHub)                | [https://w3id.org/health-ri/semantic-interoperability/mappings/tsv](https://w3id.org/health-ri/semantic-interoperability/mappings/tsv)                                                                                                                                 |
| `/mapping-vocabulary`                                                  | Mapping Vocabulary (about URI)                | Forwards to HTML spec (browser) or TTL (RDF tools)           | [https://w3id.org/health-ri/mapping-vocabulary](https://w3id.org/health-ri/mapping-vocabulary)                                                                                                                                                                         |
| `/mapping-vocabulary/ttl`                                              | Final/latest Mapping Vocabulary (TTL)         | Forwards to final/latest `.ttl` file (GitHub)                | [https://w3id.org/health-ri/mapping-vocabulary/ttl](https://w3id.org/health-ri/mapping-vocabulary/ttl)                                                                                                                                                                 |
| `/mapping-vocabulary/specification`                                    | Final/latest Mapping Vocabulary specification | Forwards to final/latest spec page                           | [https://w3id.org/health-ri/mapping-vocabulary/specification](https://w3id.org/health-ri/mapping-vocabulary/specification)                                                                                                                                             |
| `/mapping-vocabulary/vX.Y.Z`                                           | Versioned Mapping Vocabulary (about URI)      | Forwards to HTML spec (browser) or TTL (RDF tools)           | [https://w3id.org/health-ri/mapping-vocabulary/v1.0.0](https://w3id.org/health-ri/mapping-vocabulary/v1.0.0)                                                                                                                                                           |
| `/mapping-vocabulary/vX.Y.Z/specification`                             | Versioned Mapping Vocabulary specification    | Forwards to version-specific HTML spec                       | [https://w3id.org/health-ri/mapping-vocabulary/v1.0.0/specification](https://w3id.org/health-ri/mapping-vocabulary/v1.0.0/specification)                                                                                                                               |
