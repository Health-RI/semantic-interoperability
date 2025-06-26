# Ontology Publishing

This repository follows a structured and transparent publishing approach to support traceability, stability, and reuse of the Health-RI Ontology and its artifacts.

## Versioning Policy

We use an **adapted semantic versioning** scheme to indicate the type and impact of changes:

**Format**: `<major>.<minor>.<patch>`

- **Major**: Conceptual milestones or structural overhauls.
- **Minor**: Any scoped modifications, including additions, refinements, or reorganizations that preserve semantic compatibility.
- **Patch**: Fixes or clarifications that stay within the established scope (e.g., label corrections, comment improvements).

While inspired by [Semantic Versioning](https://semver.org/), this adapted strategy is tailored for ontology and conceptual model management.

!!! note
    Only **major versions** will trigger a formal release and will have a corresponding published specification webpage (location to be defined). These releases are considered **stable versions**, and intended for broader reuse and citation.
    Minor and patch versions are published in the repository but will not have standalone specification pages.

!!! info
    We adopt a **fast versioning strategy**: files are made available in the `/ontology` folder as soon as possible, even when they may present smaller completion or consistency issues. This enables early access and collaboration, while stability is guaranteed only for major releases.

## Published Artifacts

For each ontology release, the following artifacts are published:

- **OntoUML conceptual model (Visual Paradigm)**
  File: `Health-RI Ontology-v<version>.vpp`
  Includes all OntoUML constructs and diagrams

- **OntoUML JSON export**
  File: `Health-RI Ontology-v<version>.json`
  Conforms to the [OntoUML Schema](https://w3id.org/ontouml/schema)

- **gUFO OWL ontology (Turtle)**
  File: `Health-RI Ontology-v<version>.ttl`
  OWL serialization that imports or reflects gUFO axioms

!!! note
    gUFO files are only generated for versions of the model that are **syntactically valid**.
    As a result, no `.ttl` file will be provided for versions that are still incomplete or under development.

!!! info
    The version numbers of the `.vpp`/`.json` (OntoUML) and `.ttl` (OWL/gUFO) files are managed independently. The `.ttl` file includes a `dcterms:conformsTo` metadata relation to indicate which OntoUML version it corresponds to.

    !!! example
        ```ttl
        <https://w3id.org/health-ri/ontology#> dcterms:conformsTo <https://w3id.org/health-ri/ontouml-v0.3.0> .
        ```


## Repository Structure

All current artifacts are made available in the `/ontology` folder:

```txt
ontology/
│
├── Health-RI Ontology-vX.Y.Z.vpp    # latest OntoUML model
├── Health-RI Ontology-vX.Y.Z.json   # latest OntoUML JSON export
├── Health-RI Ontology-vX.Y.Z.ttl    # latest OWL ontology
├── archive.rar                      # compressed file with all previous versions
└── changelog.md                     # human-readable log of changes
```

### Archive and Change History

- Only the **latest version** of each artifact is visible directly in the `ontology/` folder.
- **All previous versions** are archived in the `archive.rar` file for transparency and reproducibility.
- A **changelog file (`changelog.md`)** summarizes all version changes and links them to their respective files and semantic impact.
  - The changelog follows the [Keep a Changelog](https://keepachangelog.com/) format.
  - It is generated and maintained with the support of an AI-assisted tool to ensure consistency and clarity.

## Permanent Identifiers

To support stable references and long-term access, we provide permanent URLs (PermURLs) via [W3ID](https://w3id.org/):

- **Latest release**: <https://w3id.org/health-ri/ontology/latest>

- **All releases overview**: <https://w3id.org/health-ri/ontology/releases>

These PermURLs allow users and systems to always retrieve the most recent or complete list of released ontology versions, even if the actual files are hosted elsewhere (e.g., on GitHub).
