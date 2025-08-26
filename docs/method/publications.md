# Initiative Publications

This repository implements a structured, transparent publishing process for both the Health-RI Ontology and its SSSOM mapping sets, ensuring all artifacts are traceable, stable, and reusable, and supporting FAIR-aligned interoperability.

## Publishing the Ontology

Before diving into specific files and artifacts, we first outline how ontology versions are tracked and the policy guiding version numbering.

### Versioning Policy

We use an **adapted semantic versioning** scheme to indicate the type and impact of changes:

**Format**: `<major>.<minor>.<patch>`

- **Major**: Conceptual milestones or structural overhauls.
- **Minor**: Any scoped modifications, including additions, refinements, or reorganizations that preserve semantic compatibility.
- **Patch**: Fixes or clarifications that stay within the established scope (e.g., label corrections, comment improvements).

While inspired by [Semantic Versioning](https://semver.org/), this adapted strategy is tailored for ontology and conceptual model management.

!!! note
    Only **major versions** will trigger a formal release and will have a corresponding published specification webpage. These releases are considered **stable versions**, and intended for broader reuse and citation.

!!! info
    We adopt a **fast versioning strategy**: files are made available in the `/ontology` folder as soon as possible, even when they may present smaller completion or consistency issues. This enables early access and collaboration, while stability is guaranteed only for major releases.

### Published Artifacts

For each ontology release, the following artifacts are published — always in both `ontologies/latest/` and `ontologies/versioned/` folders.

- **OntoUML conceptual model (Visual Paradigm)**
  Includes all OntoUML constructs and diagrams.
  - [`ontologies/latest/health-ri-ontology.vpp`](https://w3id.org/health-ri/ontology/vpp)
  - `ontologies/versioned/health-ri-ontology-v<version>.vpp`

- **OntoUML JSON export**
  Conforms to the [OntoUML Schema](https://w3id.org/ontouml/schema).
  - [`ontologies/latest/health-ri-ontology.json`](https://w3id.org/health-ri/ontology/json)
  - `ontologies/versioned/health-ri-ontology-v<version>.json`

- **gUFO OWL ontology (Turtle)**
  OWL serialization that imports or reflects gUFO axioms.
  - [`ontologies/latest/health-ri-ontology.ttl`](https://w3id.org/health-ri/ontology/ttl)
  - `ontologies/versioned/health-ri-ontology-v<version>.ttl`

- **Markdown documentation**
  - [`ontologies/latest/documentations/documentation.md`](https://w3id.org/health-ri/ontology/documentation)
  - `ontologies/versioned/documentations/documentation-v<version>.md`

- **HTML specification**
  - [`ontologies/latest/documentations/specification.html`](https://w3id.org/health-ri/ontology/specification)
  - `ontologies/versioned/documentations/specification-v<version>.html`

!!! note
    gUFO files are only generated for versions of the model that are **syntactically valid**.
    As a result, no `.ttl` file will be provided for versions that are still incomplete or under development.

!!! info
    The version numbers of the `.vpp`/`.json` (OntoUML) and `.ttl` (OWL/gUFO) files are managed independently. The `.ttl` file includes a `dcterms:conformsTo` metadata relation to indicate which OntoUML version it corresponds to.

    `<https://w3id.org/health-ri/ontology#> dcterms:conformsTo <https://w3id.org/health-ri/ontouml-v0.3.0> .`

### Repository Structure

All current artifacts are made available in the `/ontologies` folder:

```
ontologies/
│
├── latest/
│   ├── health-ri-ontology.vpp
│   ├── health-ri-ontology.json
│   ├── health-ri-ontology.ttl
│   ├── documentations/
│   │   ├── documentation.md
│   │   └── specification.html
│   └── images/
│       └── *.png   # Exported PNG images of all diagrams
│
├── versioned/
│   ├── health-ri-ontology-vX.Y.Z.json
│   ├── health-ri-ontology-vX.Y.Z.vpp
│   ├── health-ri-ontology-vX.Y.Z.ttl
│   └── documentations/
│       ├── documentation-vX.Y.Z.md
│       └── specification-vX.Y.Z.html
│
├── changelog.md
└── ...
```

!!! tip "What does 'latest' mean?"
    The `latest/` folder always mirrors the contents of the highest published version. This provides stable, convenient access to the most recent files without needing to specify a version number.

!!! note "Where are the images of the diagrams?"
    The `images/` folder — containing exported PNG versions of all OntoUML diagrams — is only provided under the `latest/` folder.  
    These images are always generated from the most recent `.vpp` file and are not versioned individually.

### Archive and Change History

- Only the **latest version** of each artifact is visible directly in the `ontologies/latest/` folder.
- **All previous versions** are organized in the `ontologies/versioned/` directory for transparency and reproducibility.
- A **changelog file (`changelog.md`)** summarizes all version changes and links them to their respective files and semantic impact.
  - The changelog follows the [Keep a Changelog](https://keepachangelog.com/) format.
  - It is generated and maintained with the support of an AI-assisted tool to ensure consistency and clarity.

!!! tip "Looking for PID details?"
    The full description of all Permanent Identifiers (PIDs) — including format-specific URIs for each version — is documented separately. Access the complete description at: [Permanent Identifiers](permanent-ids.md).

## Publishing SSSOM Mappings

This section describes the publication process for our **SSSOM mapping sets** (cross-ontology alignments), which follow a different versioning strategy than the ontology artifacts described above.

The SSSOM mapping set uses date-based versions in the format `YYYY-MM-DD` (at most one version per day).  
Published mappings are **append-only**: existing rows are not deleted. To correct or supersede a row, add a new one using the `replaces` field to reference the previous record.

- **SSSOM Mapping Set (TSV & TTL)**  
  Curated cross-ontology alignments published as a tabular SSSOM set and as RDF/Turtle.
  - `https://github.com/Health-RI/semantic-interoperability/mappings` — redirects to the **TTL** version  
  - `https://github.com/Health-RI/semantic-interoperability/mappings/ttl` — **TTL** version  
  - `https://github.com/Health-RI/semantic-interoperability/mappings/tsv` — **TSV** version  
  - Human-readable table: `docs/ontology/mappings.md`