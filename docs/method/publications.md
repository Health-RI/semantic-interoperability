# Initiative Publications

This repository documents the structured publishing process used for both the Health-RI Ontology and its SSSOM mapping sets, ensuring released artifacts are traceable, stable, and reusable, and supporting FAIR-aligned interoperability.

!!! note "Operational status: discontinued"

    The Health-RI Semantic Interoperability Initiative has been **discontinued**. The procedures described on this page are retained as historical policy and are no longer executed as an active development or release workflow. No further releases are planned under this initiative. See [Initiative Status](../status.md).

## Publishing the Ontology

Before diving into specific files and artifacts, we first outline how ontology versions were tracked and the policy that guided version numbering.

### Versioning Policy

Please refer to the [Ontology Versioning Policy](./ontology-versioning.md) page for full details.

### Published Artifacts

For each ontology release, the following artifacts were published — always in both `ontologies/latest/` and `ontologies/versioned/` folders.

- **OntoUML conceptual model (Visual Paradigm)**: Includes all OntoUML constructs and diagrams.

    - [`ontologies/latest/health-ri-ontology.vpp`](https://w3id.org/health-ri/ontology/vpp)
    - `ontologies/versioned/health-ri-ontology-v<version>.vpp`

- **OntoUML JSON export**: Conforms to the [OntoUML Schema](https://w3id.org/ontouml/schema).

    - [`ontologies/latest/health-ri-ontology.json`](https://w3id.org/health-ri/ontology/json)
    - `ontologies/versioned/health-ri-ontology-v<version>.json`

- **gUFO OWL ontology (Turtle)**: OWL serialization that imports or reflects gUFO axioms.

    - [`ontologies/latest/health-ri-ontology.ttl`](https://w3id.org/health-ri/ontology/ttl)
    - `ontologies/versioned/health-ri-ontology-v<version>.ttl`

- **SHACL validation shapes and derivation rules (Turtle)**: SHACL Core and SHACL Advanced Features graph that validates HRIO-aligned instance data and materializes safe, ontology-compatible triples.

    - [`ontologies/latest/health-ri-ontology.shacl`](https://w3id.org/health-ri/ontology/shacl)
    - `ontologies/versioned/health-ri-ontology-v<version>.shacl` (via `https://w3id.org/health-ri/ontology/v<version>/shacl`)

- **Markdown documentation**: Textual documentation of the OntoUML ontology.

    - [`ontologies/latest/documentations/documentation.md`](https://w3id.org/health-ri/ontology/documentation)
    - `ontologies/versioned/documentations/documentation-v<version>.md`

- **HTML specification**: Documentation of the gUFO ontology.

    - [`ontologies/latest/documentations/specification.html`](https://w3id.org/health-ri/ontology/specification)
    - `ontologies/versioned/documentations/specification-v<version>.html`

!!! note

    Derived gUFO artifacts (`.ttl`, `.shacl`, and the HTML specification) were generated only for releases where the OntoUML model was syntactically valid and the transformation pipeline completed successfully. If a release could not produce these derived files, they could be absent from `ontologies/versioned/`, and the corresponding "latest" PID (e.g., `/ontology/ttl`) continued to resolve to the most recent available derived artifact.

!!! info

    All published artifacts use the HRIO release version identifier (`X.Y.Z`) defined in the Ontology Versioning Policy. When an OWL (`.ttl`) artifact is present, it includes a `dcterms:conformsTo` relation to indicate the OntoUML artifact version it was generated from.

    `<https://w3id.org/health-ri/ontology#> dcterms:conformsTo <https://w3id.org/health-ri/ontology/vX.Y.Z/json> .`

### Repository Structure

Published ontology artifacts are available in the `/ontologies` folder:

```text
ontologies/
│
├── latest/
│   ├── health-ri-ontology.vpp
│   ├── health-ri-ontology.json
│   ├── health-ri-ontology.ttl
│   ├── health-ri-ontology.shacl
│   ├── documentations/
│   │   ├── documentation.md
│   │   └── specification.html
│   └── images/
│       └── *.png   # Exported PNG images of all OntoUML diagrams
│
├── versioned/
│   ├── health-ri-ontology-vX.Y.Z.json
│   ├── health-ri-ontology-vX.Y.Z.vpp
│   ├── health-ri-ontology-vX.Y.Z.ttl
│   ├── health-ri-ontology-vX.Y.Z.shacl
│   └── documentations/
│       ├── documentation-vX.Y.Z.md
│       └── specification-vX.Y.Z.html
│
├── changelog-ontology.md
└── ...
```

!!! tip "What does 'latest' mean after discontinuation?"

    The `latest/` folder mirrors the contents of the highest published version. Because the initiative has been discontinued, it should now be understood as the **final available published version**, not as an artifact expected to advance.

!!! note "Where are the images of the diagrams?"

    The `images/` folder — containing exported PNG versions of all OntoUML diagrams — is only provided under the `latest/` folder.
    These images were generated from the most recent published `.vpp` file and were not versioned individually.

### Archive and Change History

- Only the **final/latest version** of each artifact is visible directly in the `ontologies/latest/` folder.
- **All previous versions** are organized in the `ontologies/versioned/` directory for transparency and reproducibility.
- A **changelog file (`changelog-ontology.md`)** summarizes all version changes and links them to their respective files and semantic impact.
    - The changelog follows the [Keep a Changelog](https://keepachangelog.com/) format.
    - It was drafted with AI support as an editorial aid. Entries were intended to be reviewed and aligned with the released artifacts, but they may still contain inaccuracies or lag behind model changes in a given snapshot.
    - The prompts used to draft AI-supported changelog content are available in `resources/prompts/`.

!!! tip "Looking for PID details?"

    The full description of all Persistent Identifiers (PIDs) — including format-specific URIs for each version — is documented separately. Access the complete description at: [Persistent Identifiers](persistent-ids.md).

## Publishing SSSOM Mappings

This section describes the publication process used for our **SSSOM mapping sets** (meaning mappings), which followed a different versioning strategy than the ontology artifacts described above.

The SSSOM mapping set used date-based versions in the format `YYYY-MM-DD` (at most one version per day).
Published mappings are **append-only**: existing rows are not deleted. To correct or supersede a row, a new one was added using the `replaces` field to reference the previous record.

- **SSSOM Mapping Set (TSV & TTL)**:
    Curated meaning mappings published as a tabular SSSOM set and as RDF/Turtle.
    - `https://w3id.org/health-ri/semantic-interoperability/mappings` — redirects to the **TTL** version
    - `https://w3id.org/health-ri/semantic-interoperability/mappings/ttl` — **TTL** version
    - `https://w3id.org/health-ri/semantic-interoperability/mappings/tsv` — **TSV** version

!!! tip

    A human-readable version of the final published mappings [can be accessed in this link](https://health-ri.github.io/semantic-interoperability/deliverables/mappings/).

!!! note

    Both serializations of the final SSSOM Mapping Set — **TSV** and **TTL** — are stored in the `/mappings` folder of this repository.
    The redirect links above provide stable access to these files, while the folder itself contains the recorded versions.
