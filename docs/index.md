<p align="left"><img src="assets/images/health-ri-logo-blue.png" width="750" alt="Health-RI Logo"></p>

# Health-RI Semantic Interoperability Initiative

The health domain is shaped by many standards and models that guide the design of databases and the implementation of systems. They are applied in diverse contexts, from hospital records to research infrastructures. To enable effective data reuse, the data within these systems often needs to be exchanged, compared, and integrated. In other words, the data must be interoperable (fulfilling the "I" in FAIR).

But achieving this is technically complex, time-consuming, and prone to errors when relying on case-by-case mappings between standards. In the past, several initiatives have sought to address this challenge, and while they brought valuable contributions, some unintentionally added to the creation of a "standard #15," resulting in another model in an already crowded landscape.

<p align="center"><img src="assets/images/xkcd-standards.png" width="500" alt="XKCD Comic #927 - Standards"><br>
<em>Source: <a href="https://xkcd.com/927/">xkcd.com/927</a></em></p>

Important efforts such as FHIR, OpenEHR, SNOMED CT, OMOP, and convergence initiatives between them remain crucial endeavors for interoperability, and our work builds directly on them while taking a distinct perspective.

The Health-RI Semantic Interoperability Initiative addresses this challenge by developing a unifying upper-level ontology that defines the precise meaning of key concepts already present in widely used standards such as FHIR, OMOP, and OpenEHR. This ontology serves as a shared reference point, allowing existing standards to map their concepts to it. Through this mapping, the intended meanings become clear and explicit to anyone who needs to interoperate across systems.

We do not intend to replace the standards and models already in use, into which research groups and institutions have invested significant effort and resources. Instead, our approach replaces the need for multiple pairwise mappings between those standards with a single, reusable mapping to our ontology.

This makes the Health-RI Semantic Interoperability Initiative non-intrusive: the ontology complements existing efforts and provides the semantic backbone that supports their interoperability. We know this is complex and ambitious work, but once a mapping is created it can be applied consistently across different projects and contexts. By relying on solid theoretical foundations and state-of-the-art technologies, and by working together as a community, we are confident that we can turn this work into a practical means for achieving semantic interoperability.

At this early stage, as we continue to explore alternatives and collaborations, we are already receiving valuable support and feedback from academics and professionals across Health-RI and the broader health data community. Their perspectives are helping us shape the work and ensure it stays aligned with ongoing national and international efforts toward interoperability.

We invite you to explore the resources we are making available — including our [**ontology**](ontology/index.md), [**mapping vocabulary**](method/specification-vocabulary.html), and [**mapping sets**](method/mapping-set.md) — all of which are openly published and continuously improved.

We also welcome direct engagement, whether through sharing feedback, proposing new mappings, or discussing use cases and potential applications with us.

After all, semantic interoperability can only be achieved **through the community**: initiatives earn trust only when they are built openly and collaboratively. Together, we can ensure this effort translates into real, lasting improvements in how health data is shared and reused.

---

## About Health-RI

[Health-RI](https://www.health-ri.nl) is a national initiative in the Netherlands dedicated to building an integrated infrastructure for health and life-sciences data. By improving data sharing, reuse, and accessibility, Health-RI aims to empower researchers, clinicians, and policymakers to accelerate data-driven healthcare innovation.

Semantic interoperability plays a foundational role in this mission by ensuring that data from diverse sources can be aligned and understood consistently — not just technically, but conceptually.

---

## What’s on this site

This site documents how Health-RI achieves semantic interoperability across health and life-sciences data: our concepts, modeling foundations (OntoUML & gUFO), the method and mapping vocabulary we use, and the published ontology deliverables (specs, docs, changelog).

- **Semantic Interoperability**: [Overview](semantic-interoperability/index.md)
- **OntoUML & gUFO**: [Overview](ontouml-gufo/index.md) · [OntoUML](ontouml-gufo/ontouml.md) · [OntoUML Stereotypes](ontouml-gufo/ontouml-stereotypes.md) · [OntoUML/UFO Catalog](ontouml-gufo/ontouml-ufo-catalog.md) · [Creating OntoUML Models](ontouml-gufo/creating-ontouml-models.md) · [gUFO](ontouml-gufo/gufo.md)
- **Method**: [Overview](method/index.md) · [Introduction](method/introduction.md) · [Mapping Strategy](method/mapping-strategy.md) · [Mapping Vocabulary Specification](method/specification-vocabulary.html) · [SSSOM Mapping Set](method/mapping-set.md) · [Publications](method/publications.md) · [Persistent Identifiers](method/persistent-ids.md)
- **Deliverables**: [Overview](ontology/index.md) · [Ontology Documentation](ontology/documentation.md) · [Ontology Specification](ontology/specification-ontology.html) · [Ontology Changelog](ontology/changelog-ontology.md)
- **Help & Contributions**: [FAQ](faq.md) · [Contributing](contributing.md)

---

## Who this is for

Data stewards, modelers, and engineers who need stable, shared meaning across systems — using a common reference model (OntoUML → gUFO) and mappings that align external ontologies to it.

---

## License

**Semantic Artifacts & Documentation**: All ontologies, vocabularies, mapping files, documentation, templates, and other semantic artifacts are licensed under the [**Creative Commons Attribution 4.0 International (CC BY 4.0)**](https://creativecommons.org/licenses/by/4.0/) license.

**Auxiliary Code**: Any code scripts or auxiliary utilities are licensed under the [**MIT License**](https://spdx.org/licenses/MIT.html).
