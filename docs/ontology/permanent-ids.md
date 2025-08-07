# Permanent Identifiers (PIDs)

This page lists the **persistent, stable, and dereferenceable identifiers (PIDs)** established by the Health-RI Semantic Interoperability Initiative. These URIs support semantic interoperability, long-term accessibility, and alignment with FAIR principles.

## Initiative-Wide Identifier: `/semantic-interoperability`

### URI

`https://w3id.org/health-ri/semantic-interoperability`

This URI refers to the Semantic Interoperability Initiative as a whole. It provides persistent access to the initiative’s public-facing resources and is suitable for citing the initiative in publications, websites, and metadata records.

## Ontology Identifier: `/ontology`

### URI

`https://w3id.org/health-ri/ontology`

This is the **main identifier for the Health-RI Ontology**. It supports HTTP content negotiation to serve either machine-readable ontology files (e.g., Turtle) or human-readable documentation (HTML specification).

### Identifiers for the **Latest Ontology Version**

These URIs point to the **most recent release** of the Health-RI Ontology and related documentation formats.

| PID                       | Description                                  |
| ------------------------- | -------------------------------------------- |
| `/ontology/ttl`           | OWL ontology in Turtle format                |
| `/ontology/specification` | HTML rendering of the ontology specification |
| `/ontology/documentation` | Markdown documentation (raw version)         |
| `/ontology/json`          | OntoUML model exported as JSON               |
| `/ontology/vpp`           | OntoUML model file in Visual Paradigm format |

Each of these URIs redirects to the latest available version of the resource.

### Identifiers for **Versioned Ontology Releases**

To support traceability and reproducibility, each ontology release is also available via **version-specific URIs**.

#### Format

`https://w3id.org/health-ri/ontology/vX.Y.Z/{format}`

Where:

- `X.Y.Z` is the semantic version (e.g., `2.0.0`)
- `{format}` is one of:
  - `ttl` — OWL ontology (Turtle)
  - `vpp` — OntoUML model (Visual Paradigm)
  - `json` — OntoUML model (JSON)
  - `documentation` — Markdown documentation
  - `specification` — HTML specification

#### Examples

- `https://w3id.org/health-ri/ontology/v0.6.0/ttl`
  → Ontology in Turtle format for version 0.6.0

- `https://w3id.org/health-ri/ontology/v0.6.0/vpp`
  → Visual Paradigm project file for version 0.6.0

- `https://w3id.org/health-ri/ontology/v0.9.1/documentation`
  → Markdown documentation for version 0.9.1

- `https://w3id.org/health-ri/ontology/v0.6.0/specification`
  → HTML specification for version 0.6.0

## Overview of Persistent Identifiers

| PID                              | Description                      | Behavior                          | Example                                                    |
| -------------------------------- | -------------------------------- | --------------------------------- | ---------------------------------------------------------- |
| `/ontology`                      | Ontology root                    | Content negotiation (RDF or HTML) | `https://w3id.org/health-ri/ontology`                      |
| `/ontology/ttl`                  | Latest ontology in Turtle format | Redirects to raw `.ttl` file      | `https://w3id.org/health-ri/ontology/ttl`                  |
| `/ontology/specification`        | Latest HTML specification        | Human-readable documentation      | `https://w3id.org/health-ri/ontology/specification`        |
| `/ontology/documentation`        | Markdown documentation           | Redirects to `.md`                | `https://w3id.org/health-ri/ontology/documentation`        |
| `/ontology/json`                 | Latest JSON export of OntoUML    | Redirects to `.json`              | `https://w3id.org/health-ri/ontology/json`                 |
| `/ontology/vpp`                  | Latest OntoUML model (`.vpp`)    | Redirects to Visual Paradigm file | `https://w3id.org/health-ri/ontology/vpp`                  |
| `/ontology/vX.Y.Z/{format}`      | Versioned ontology release       | Format-specific persistent access | `https://w3id.org/health-ri/ontology/v0.6.0/ttl`           |
| `/semantic-interoperability`     | Project-level identifier         | Redirects to documentation site   | `https://w3id.org/health-ri/semantic-interoperability`     |
| `/semantic-interoperability/git` | Source code and data repository  | Redirects to GitHub               | `https://w3id.org/health-ri/semantic-interoperability/git` |
