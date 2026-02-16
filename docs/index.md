<p align="left"><img src="assets/images/health-ri-logo-blue.png" width="750" alt="Health-RI Logo"></p>

# Health-RI Semantic Interoperability Initiative

The health domain is shaped by many standards and models that guide the design of databases and the implementation of systems. They are applied in diverse contexts, from hospital records to research infrastructures. To enable effective data reuse, the data within these systems often needs to be exchanged, compared, and integrated. In other words, the data must be interoperable (fulfilling the "I" in FAIR).

In practice, interoperability often breaks because **meaning stays implicit**. Similar labels, codes, or even similar OWL patterns can hide genuine semantic misalignment ("false agreement")—and those mismatches usually surface later as brittle integrations, silent errors, and hard-to-reproduce results.

## What we do differently: semantic traceability

The Health-RI Semantic Interoperability Initiative is a model-driven, ontology-based framework designed to enable **semantic traceability**: keeping meaning and representation aligned across the stack.

We develop the **Health-RI Ontology (HRIO)** as a common semantic reference model:

- **HRIO OntoUML (CIM)**: a conceptual model for experts to validate (meaning-first).
- **HRIO gUFO/OWL (PIM)**: a computational OWL implementation of the same meanings (machine-processable).
- **Health-RI Mapping Vocabulary (HRIV)**: a meaning-level mapping layer that links external terms to HRIO meanings with explicit intent.

This makes it possible to trace semantics **from external artifacts → mapped HRIO meanings → conceptual reference definitions**, and also in the reverse direction.

## Map once, reuse everywhere (a semantic hub)

Most interoperability programs end up maintaining many pairwise mappings across standards and local schemas. Our approach replaces that scaling trap with a semantic hub:

- Each external standard, schema, or ontology maps **once** to HRIO.
- When two external terms map to the same HRIO meaning, their intended semantics become comparable through the shared reference model—without needing a bespoke pairwise mapping for every combination.

<p align="center"><img src="assets/images/xkcd-standards.png" width="500" alt="XKCD Comic #927 - Standards"><br>
<em>Source: <a href="https://xkcd.com/927/">xkcd.com/927</a></em></p>

## A concrete example: avoiding "same label, different meaning"

Two standards may both use the label "Man", while embedding different conceptualizations (e.g., a karyotype-based reading versus a gender-based reading). Treating them as interchangeable creates false agreement.

With HRIO + HRIV:

- each external term is linked to the specific HRIO meaning it intends,
- and cross-standard interpretations are derived from those explicit meaning-level commitments (not from labels alone).

## Trust by design: auditable semantic assets

We treat semantic artifacts like production assets:

- **Role separation** (Mapper ≠ Reviewer; Curator publishes)
- **Validation before release** (promotion gates)
- **Append-only history** where mappings are **superseded** (never overwritten), with `replaces` lineage
- **Stable, citable PIDs (w3id)** and **version IRIs / dated releases** to support reproducibility

## Quick start (10 minutes)

!!! tip "AI Assistants (GPT)"
    Two optional ChatGPT assistants can help you navigate the initiative and draft mappings.

    <div class="button-gridb" markdown>
    [Open: Semantic Interoperability Guide](https://chatgpt.com/g/g-6992c8eb8780819185f0922ac33d79ce-health-ri-semantic-interoperability-guide){ .md-button .md-button--primary .gpt-button }
    [Open: HRIO Mapping Assistant](https://chatgpt.com/g/g-6990a7e348c4819190ef2de88503ff5e-hrio-mapping-assistant){ .md-button .md-button--primary .gpt-button }
    </div>

    - Use the **Guide** for questions about the initiative, artifacts, releases, and PIDs.
    - Use the **Mapping Assistant** to draft a candidate **HRIV meaning mapping** from your term to **HRIO** (one predicate + confidence + evidence snippets).

    *These tools are drafting aids. Always validate results against the documentation and follow the mapping governance rules before publishing or submitting contributions.*

**1) Pick** one ambiguous local term (column header, code, or ontology class).
   
**2) Select** the closest HRIO meaning (browse the ontology specification/documentation).
   
**3) Attach** a meaning-level relation (your semantic "unit test"):
   - `hriv:hasExactMeaning` (intended meaning is fully equivalent)
   - `hriv:hasBroaderMeaningThan` / `hriv:hasNarrowerMeaningThan` (meaning is broader/narrower)

**4) Share it** with the community (one row is fine): contribute via the routes described in the contributing pages.

## Community and collaboration

At this early stage, as we continue to explore alternatives and collaborations, we are already receiving valuable support and feedback from academics and professionals across Health-RI and the broader health data community. Their perspectives are helping us shape the work and ensure it stays aligned with ongoing national and international efforts toward interoperability.

We invite you to explore the resources we are making available — including our [**ontology**](ontology/index.md), [**mapping vocabulary**](method/specification-vocabulary.html), and [**mapping sets**](method/mapping-schema.md) — all of which are openly published and continuously improved. For the conceptual rationale and the initiative-level definition of semantic traceability, see our [academic paper](https://raw.githubusercontent.com/Health-RI/semantic-interoperability/main/documents/preprints/enabling-semantic-traceability-in-health-data-v1.1.0.pdf).

We also welcome direct engagement—see [Contributing](contributing/overview.md), including time-bound [Calls for Community Review](contributing/call-for-community-review.md), and the ongoing [Contribution Channels](contributing/contribution-channels.md).

After all, semantic interoperability can only be achieved **through the community**: initiatives earn trust only when they are built openly and collaboratively. Together, we can ensure this effort translates into real, lasting improvements in how health data is shared and reused.

---

## About Health-RI

[Health-RI](https://www.health-ri.nl) is a national initiative in the Netherlands dedicated to building an integrated infrastructure for health and life-sciences data. By improving data sharing, reuse, and accessibility, Health-RI aims to empower researchers, clinicians, and policymakers to accelerate data-driven healthcare innovation.

Semantic interoperability plays a foundational role in this mission by ensuring that data from diverse sources can be aligned and understood consistently — not just technically, but conceptually.

---

## What's on this site

This site documents how Health-RI achieves semantic interoperability across health and life-sciences data: our concepts, modeling foundations (OntoUML & gUFO), the method and mapping vocabulary we use, and the published ontology deliverables (specs, docs, changelog).

- **Semantic Interoperability**: [Overview](semantic-interoperability/index.md)
- **OntoUML & gUFO**: [Overview](ontouml-gufo/index.md) · [OntoUML](ontouml-gufo/ontouml.md) · [OntoUML Stereotypes](ontouml-gufo/ontouml-stereotypes.md) · [OntoUML/UFO Catalog](ontouml-gufo/ontouml-ufo-catalog.md) · [Creating OntoUML Models](ontouml-gufo/creating-ontouml-models.md) · [gUFO](ontouml-gufo/gufo.md)
- **Method**: [Overview](method/index.md) · [Introduction](method/introduction.md) · [Mapping Strategy](method/mapping-strategy.md) · [Mapping Vocabulary Specification](method/specification-vocabulary.html) · [SSSOM Mapping Set](method/mapping-schema.md) · [Mapping Governance](method/mapping-governance.md) · [Ontology Versioning](method/ontology-versioning.md) · [Ontology Validation](method/ontology-validation.md) · [Publications](method/publications.md) · [Persistent Identifiers](method/persistent-ids.md)
- **Deliverables**: [Overview](ontology/index.md) · [Ontology Documentation](ontology/documentation.md) · [Ontology Specification](ontology/specification-ontology.html) · [Ontology Changelog](ontology/changelog-ontology.md)
- **Help & Contributions**: [FAQ](faq.md) · [Contributing](./contributing/overview.md) · [Calls for Community Review](./contributing/call-for-community-review.md) · [Contribution Channels](./contributing/contribution-channels.md)

---

## Who this is for

Data stewards, modelers, and engineers who need stable, shared meaning across systems — using a common reference model (OntoUML → gUFO) and mappings that align external ontologies, terminologies, and schemas to it.

---

## License

**Semantic Artifacts & Documentation**: All ontologies, vocabularies, mapping files, documentation, templates, and other semantic artifacts are licensed under the [**Creative Commons Attribution 4.0 International (CC BY 4.0)**](https://creativecommons.org/licenses/by/4.0/) license.

**Auxiliary Code**: Any code scripts or auxiliary utilities are licensed under the [**MIT License**](https://spdx.org/licenses/MIT.html).
