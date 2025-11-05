# OntoUML/UFO Catalog

<p align="left"><img src="https://user-images.githubusercontent.com/8641647/223740939-1abcd2af-e954-4d19-b087-56f1be4417c3.png" width="500" alt="OntoUML/UFO Catalog Logo"></p>

The **OntoUML/UFO Catalog** is a structured, community-driven repository of real-world models represented using the OntoUML language and grounded in the Unified Foundational Ontology (UFO). It was developed to support empirical research, educational activities, and tool development in ontology-driven conceptual modeling.

This catalog provides a curated collection of models across diverse domains—such as law, healthcare, logistics, and cybersecurity—each described with rich metadata detailing its origin, modeling objective, language, domain, and other relevant aspects. By offering standardized, machine-readable formats and persistent identifiers, the catalog promotes reuse, discoverability, and long-term accessibility of high-quality conceptual models.

## Access and Structure

The catalog is openly maintained on GitHub at [w3id.org/ontouml/models](https://w3id.org/ontouml/models). Models are provided in multiple formats, including:

- **`.json`**: JSON serialization compliant with the [OntoUML Schema](https://w3id.org/ontouml/schema)
- **`.ttl`**: RDF/Turtle files using the [OntoUML Vocabulary](https://w3id.org/ontouml/vocabulary)
- **`.vpp`**: Original diagrams in Visual Paradigm format

!!! tip
    If your goal is to use OntoUML with Semantic Web technologies, prefer the `.ttl` files. For diagram visualization and editing, use the `.vpp` files in Visual Paradigm.

Each model is organized in its own folder and includes a set of standardized metadata files (`metadata.ttl`, `metadata-json.ttl`, `metadata-vpp.ttl`, etc.). The catalog as a whole is described by a root `catalog.ttl` file and validated using SHACL shapes provided under the `/shapes` directory.

### Directory Structure Overview

```
/ontouml-models
├── catalog.ttl
├── /models
│   └── /[model-id]/
│       ├── ontology.json
│       ├── ontology.ttl
│       ├── ontology.vpp
│       ├── metadata.ttl
│       ├── metadata-json.ttl
│       ├── metadata-vpp.ttl
│       ├── /original-diagrams/
│       └── /new-diagrams/
├── /shapes
    ├── Catalog-shape.ttl
    ├── Dataset-shape.ttl
    ├── Distribution-shape.ttl
    ├── Resource-shape.ttl
    └── SemanticArtefact-shape.ttl
```

A public **dashboard** is available at [w3id.org/ontouml-models/dashboard](https://w3id.org/ontouml-models/dashboard), offering visualizations of the catalog's contents. Users can explore metadata distributions by year, domain, modeling task, and stereotype usage. As of now, the catalog comprises over **190 datasets**, with more than **13.000 classes**, **9.000 relations**, and **hundreds of thousands of RDF triples**.

## Catalog's Persistent URLs

- FDP Catalog page: https://w3id.org/ontouml-models
- GitHub repository: https://w3id.org/ontouml-models/git
- Dashboard: https://w3id.org/ontouml-models/dashboard
- Catalog's latest release: https://w3id.org/ontouml-models/release

## References

The OntoUML/UFO Catalog has been formally described in the following peer-reviewed publication:

> Prince Sales, T., Barcelos, P. P. F., Fonseca, C. M., Souza, I. V., Romanenko, E., Bernabé, C. H., Bonino da Silva Santos, L. O., Fumagalli, M., Kritz, J., Almeida, J. P. A., & Guizzardi, G. (2023). A FAIR catalog of ontology-driven conceptual models. Data & Knowledge Engineering, 147, 102210. [https://doi.org/10.1016/j.datak.2023.102210](https://doi.org/10.1016/j.datak.2023.102210). Permanent URL: https://w3id.org/ontouml-models/.

This article presents the rationale, structure, and empirical coverage of the catalog and is recommended for citation when using the catalog in research.