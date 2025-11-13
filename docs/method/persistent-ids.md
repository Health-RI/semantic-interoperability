# Persistent Identifiers (PIDs)

This page lists the **persistent, stable, and dereferenceable identifiers (PIDs)** established by the Health-RI Semantic Interoperability Initiative. These URIs support semantic interoperability, long-term accessibility, and alignment with FAIR principles.

## Initiative-Wide Identifier

### URI: `https://w3id.org/health-ri/semantic-interoperability`

This URI refers to the Semantic Interoperability Initiative as a whole. It provides persistent access to the initiative's public-facing resources and is suitable for citing the initiative in publications, websites, and metadata records.

## Ontology Identifier

### URI: `https://w3id.org/health-ri/ontology`

This is the **main identifier for the Health-RI Ontology**, which always resolves to the ontology's most recent version.

### Identifiers for the **Latest Ontology Version**

These URIs point to the **most recent release** of the Health-RI Ontology and related documentation formats.

| PID                       | Description                                  |
| ------------------------- | -------------------------------------------- |
| `/ontology/ttl`           | OWL ontology in Turtle format                |
| `/ontology/specification` | HTML rendering of the ontology specification |
| `/ontology/documentation` | Markdown documentation (raw version)         |
| `/ontology/json`          | OntoUML model exported as JSON               |
| `/ontology/vpp`           | OntoUML model file in Visual Paradigm format |
| `/ontology/shacl`         | SHACL constraint and derivation rules        |

Each of these URIs redirects to the latest available version of the resource.

!!! tip
    You can use either `/doc` or `/documentation`, and `/spec` or `/specification` — both forms are valid and equivalent.

!!! note
    Our SHACL file uses the `.shacl` extension and Turtle serialization.

### Identifiers for **Versioned Ontology Releases**

To support traceability and reproducibility, each ontology release is also available via **version-specific URIs**. Each versioned release of the Health-RI Ontology is identified by its own dedicated URI in the format **`https://w3id.org/health-ri/ontology/vX.Y.Z`**. This URI is used as the `owl:versionIRI` in the ontology metadata.

#### Format

`https://w3id.org/health-ri/ontology/vX.Y.Z/{format}`

Where:

- `X.Y.Z` is the semantic version (e.g., `2.0.0`)
- `{format}` is one of:
    - `ttl` — OWL ontology (Turtle)
    - `vpp` — OntoUML model (Visual Paradigm)
    - `json` — OntoUML model (JSON)
    - `shacl` — SHACL constraint and derivation rules (Turtle)
    - `documentation` — Markdown documentation
    - `specification` — HTML specification

!!! tip
    You can also use the version URI without a `{format}` (e.g., `/v0.6.0`) to directly access the `.ttl` file.

#### Examples

- `https://w3id.org/health-ri/ontology/v0.6.0/ttl`
  → Ontology in Turtle format for version 0.6.0

- `https://w3id.org/health-ri/ontology/v0.6.0/vpp`
  → Visual Paradigm project file for version 0.6.0

- `https://w3id.org/health-ri/ontology/v0.9.1/documentation`
  → Markdown documentation for version 0.9.1

- `https://w3id.org/health-ri/ontology/v0.6.0/specification`
  → HTML specification for version 0.6.0

- `https://w3id.org/health-ri/ontology/v0.11.9/shacl`
  → SHACL shapes for version 0.11.9

## SSSOM Mappings PIDs

The following PIDs provide **stable access to the latest SSSOM mapping set** produced by the initiative, in both Turtle (TTL) and TSV formats.

### Latest Mappings

- **URI (default/TTL):**
  `https://w3id.org/health-ri/semantic-interoperability/mappings`
  *(also available explicitly as `/mappings/ttl`)*

- **URI (TSV):**
  `https://w3id.org/health-ri/semantic-interoperability/mappings/tsv`

These PIDs redirect to the canonical files in the Health-RI GitHub repository (branch `main`), ensuring that citations remain stable while the underlying files can be updated as needed.

#### Examples

- `https://w3id.org/health-ri/semantic-interoperability/mappings`
  → Latest SSSOM mappings in Turtle (`.ttl`)

- `https://w3id.org/health-ri/semantic-interoperability/mappings/tsv`
  → Latest SSSOM mappings in TSV (`.tsv`)

## Mapping Vocabulary PIDs

The **Health-RI Mapping Vocabulary** defines terms used in our mapping work. The PIDs below provide stable access to the latest vocabulary and to versioned snapshots.

### Latest Vocabulary

- **URI (TTL):**
  `https://w3id.org/health-ri/mapping-vocabulary`
  *(also available explicitly as `/mapping-vocabulary/ttl`)*

- **URI (HTML specification):**
  `https://w3id.org/health-ri/mapping-vocabulary/specification`
  *(alias: `/mapping-vocabulary/spec`)*

!!! tip
    Both `/spec` and `/specification` are valid and equivalent for the vocabulary specification.

#### Examples

- `https://w3id.org/health-ri/mapping-vocabulary`
  → Latest vocabulary in Turtle (`.ttl`)

- `https://w3id.org/health-ri/mapping-vocabulary/spec`
  → Latest HTML specification

### Versioned Vocabulary

Versioned PIDs follow semantic versioning and resolve to immutable artifacts for that release.

- **URI (TTL):**
  `https://w3id.org/health-ri/mapping-vocabulary/vX.Y.Z`
  *(also available explicitly as `/vX.Y.Z/ttl`)*

- **URI (HTML specification):**
  `https://w3id.org/health-ri/mapping-vocabulary/vX.Y.Z/specification`
  *(alias: `/vX.Y.Z/spec`)*

#### Examples

- `https://w3id.org/health-ri/mapping-vocabulary/v1.0.0`
  → Vocabulary in Turtle for version `v1.0.0`

- `https://w3id.org/health-ri/mapping-vocabulary/v1.0.0/spec`
  → HTML specification for version `v1.0.0`

## Overview of Persistent Identifiers

| PID                                        | Description                                  | Behavior                                | Example                                                                                                                                  |
| ------------------------------------------ | -------------------------------------------- | --------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| `/semantic-interoperability`               | Project-level identifier                     | Redirects to documentation site         | [https://w3id.org/health-ri/semantic-interoperability](https://w3id.org/health-ri/semantic-interoperability)                             |
| `/semantic-interoperability/git`           | Source code and data repository              | Redirects to GitHub                     | [https://w3id.org/health-ri/semantic-interoperability/git](https://w3id.org/health-ri/semantic-interoperability/git)                     |
| `/ontology`                                | Ontology root                                | Redirects to raw `.ttl` file            | [https://w3id.org/health-ri/ontology](https://w3id.org/health-ri/ontology)                                                               |
| `/ontology/ttl`                            | Latest ontology in Turtle format             | Redirects to raw `.ttl` file            | [https://w3id.org/health-ri/ontology/ttl](https://w3id.org/health-ri/ontology/ttl)                                                       |
| `/ontology/shacl`                          | Latest SHACL shapes                          | Redirects to latest `.shacl`            | [https://w3id.org/health-ri/ontology/shacl](https://w3id.org/health-ri/ontology/shacl)                                                   |
| `/ontology/specification`                  | Latest HTML specification                    | Human-readable documentation            | [https://w3id.org/health-ri/ontology/specification](https://w3id.org/health-ri/ontology/specification)                                   |
| `/ontology/documentation`                  | Markdown documentation                       | Redirects to `.md`                      | [https://w3id.org/health-ri/ontology/documentation](https://w3id.org/health-ri/ontology/documentation)                                   |
| `/ontology/json`                           | Latest JSON export of OntoUML                | Redirects to `.json`                    | [https://w3id.org/health-ri/ontology/json](https://w3id.org/health-ri/ontology/json)                                                     |
| `/ontology/vpp`                            | Latest OntoUML model (`.vpp`)                | Redirects to Visual Paradigm file       | [https://w3id.org/health-ri/ontology/vpp](https://w3id.org/health-ri/ontology/vpp)                                                       |
| `/ontology/vX.Y.Z/{format}`                | Versioned ontology release                   | Format-specific persistent access       | [https://w3id.org/health-ri/ontology/v0.6.0/ttl](https://w3id.org/health-ri/ontology/v0.6.0/ttl)                                         |
| `/ontology/vX.Y.Z/shacl`                   | Versioned SHACL shapes                       | Redirects to `.shacl` for that version  | [https://w3id.org/health-ri/ontology/v0.11.9/shacl](https://w3id.org/health-ri/ontology/v0.11.9/shacl)                                   |
| `/semantic-interoperability/mappings`      | Latest SSSOM mappings (TTL)                  | Redirects to latest `.ttl`              | [https://w3id.org/health-ri/semantic-interoperability/mappings](https://w3id.org/health-ri/semantic-interoperability/mappings)           |
| `/semantic-interoperability/mappings/ttl`  | Latest SSSOM mappings (TTL, explicit)        | Redirects to latest `.ttl`              | [https://w3id.org/health-ri/semantic-interoperability/mappings/ttl](https://w3id.org/health-ri/semantic-interoperability/mappings/ttl)   |
| `/semantic-interoperability/mappings/tsv`  | Latest SSSOM mappings (TSV)                  | Redirects to latest `.tsv`              | [https://w3id.org/health-ri/semantic-interoperability/mappings/tsv](https://w3id.org/health-ri/semantic-interoperability/mappings/tsv)   |
| `/mapping-vocabulary`                      | Latest Mapping Vocabulary (TTL)              | Redirects to latest `.ttl`              | [https://w3id.org/health-ri/mapping-vocabulary](https://w3id.org/health-ri/mapping-vocabulary)                                           |
| `/mapping-vocabulary/ttl`                  | Latest Mapping Vocabulary (TTL, explicit)    | Redirects to latest `.ttl`              | [https://w3id.org/health-ri/mapping-vocabulary/ttl](https://w3id.org/health-ri/mapping-vocabulary/ttl)                                   |
| `/mapping-vocabulary/specification`        | Latest Mapping Vocabulary HTML specification | Redirects to latest spec page           | [https://w3id.org/health-ri/mapping-vocabulary/specification](https://w3id.org/health-ri/mapping-vocabulary/specification)               |
| `/mapping-vocabulary/vX.Y.Z`               | Versioned Mapping Vocabulary (TTL)           | Redirects to version-specific `.ttl`    | [https://w3id.org/health-ri/mapping-vocabulary/v1.0.0](https://w3id.org/health-ri/mapping-vocabulary/v1.0.0)                             |
| `/mapping-vocabulary/vX.Y.Z/specification` | Versioned Mapping Vocabulary specification   | Redirects to version-specific HTML spec | [https://w3id.org/health-ri/mapping-vocabulary/v1.0.0/specification](https://w3id.org/health-ri/mapping-vocabulary/v1.0.0/specification) |
