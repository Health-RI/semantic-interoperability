<p align="left"><img src="assets/images/health-ri-logo-blue.png" width="750" alt="Health-RI Logo"></p>

# Health-RI Semantic Interoperability Initiative

!!! warning "Initiative status: discontinued"

    The Health-RI Semantic Interoperability Initiative was formally paused on **May 1, 2026** and has since been **discontinued**.

    No further development, curation, community review, or release activity is planned under this initiative. Existing documentation, released artifacts, persistent identifiers, and repository materials remain available as archival resources for reference, reuse, and citation. They are not actively maintained, and known limitations may remain unresolved.

    See [Initiative Status](status.md) for details.

!!! tip "Watch: applied use cases for semantic interoperability"

    Watch a short video showing how similar labels and values in health datasets may represent different meanings, and how HRIO and the Health-RI SSSOM mapping set can support more precise, traceable, and defensible data reuse decisions.

    [Watch the video on YouTube](https://youtu.be/xHN8Xmxqv4w)

<!-- !!! open-call "OPEN CALL: validate the HRIO Sex and Gender Ontology"

    We are running an external community review of the **Sex and Gender** package in HRIO.
    Please help us validate the model and documentation.

    <div class="button-grid button-grid--grid2" style="--btn-fixed: 360px; --btn-max: 360px" markdown>

    [Open: Sex and Gender review page](external-review/sex-and-gender/){ .md-button .md-button--primary }

    [Call for Contribution Overview](contributing/call-for-community-review/){ .md-button .md-button--primary }

    </div> -->

The health domain is shaped by many standards and models that guide the design of databases and the implementation of systems. They are applied in diverse contexts, from hospital records to research infrastructures. To enable effective data reuse, the data within these systems often needs to be exchanged, compared, and integrated. In other words, the data must be interoperable (fulfilling the "I" in FAIR).

In practice, interoperability often breaks because **meaning stays implicit**. Similar labels, codes, or even similar OWL patterns can hide genuine semantic misalignment ("false agreement")—and those mismatches usually surface later as brittle integrations, silent errors, and hard-to-reproduce results.

## What we do differently: semantic traceability

The Health-RI Semantic Interoperability Initiative developed a model-driven, ontology-based framework designed to enable **semantic traceability**: keeping meaning and representation aligned across the stack.

We developed the **Health-RI Ontology (HRIO)** as a common semantic reference model:

- **HRIO OntoUML (CIM)**: a conceptual model for experts to validate (meaning-first).
- **HRIO gUFO/OWL (PIM)**: a computational OWL implementation of the same meanings (machine-processable).
- **Health-RI Mapping Vocabulary (HRIV)**: a meaning-level mapping layer that links external terms to HRIO meanings with explicit intent.

This makes it possible to trace semantics **from external artifacts → mapped HRIO meanings → conceptual reference definitions**, and also in the reverse direction.

## Map once, reuse everywhere (a semantic hub)

Most interoperability programs end up maintaining many pairwise mappings across standards and local schemas. The approach developed by the initiative replaces that scaling trap with a semantic hub:

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

During active development, we treated semantic artifacts like production assets:

- **Role separation** (Mapper ≠ Reviewer; Curator publishes)
- **Validation before release** (promotion gates)
- **Append-only history** where mappings are **superseded** (never overwritten), with `replaces` lineage
- **Stable, citable PIDs (w3id)** and **version IRIs / dated releases** to support reproducibility

## Quick start (10 minutes)

!!! tip "AI Assistants (GPT)"

    Two ChatGPT assistants created during the initiative remain linked as archival aids.

    <div class="button-grid button-grid--grid2" markdown>

    [Open: Semantic Interoperability Guide](https://chatgpt.com/g/g-6992c8eb8780819185f0922ac33d79ce-health-ri-semantic-interoperability-guide){ .md-button .md-button--primary .gpt-button }

    [Open: HRIO Mapping Assistant](https://chatgpt.com/g/g-6990a7e348c4819190ef2de88503ff5e-hrio-mapping-assistant){ .md-button .md-button--primary .gpt-button }

    </div>

    - Use the **Guide** for questions about the initiative, artifacts, releases, and PIDs.
    - Use the **Mapping Assistant** to draft a candidate **HRIV meaning mapping** from your term to **HRIO** (one predicate + confidence + evidence snippets).

    *These tools are not actively maintained. Always validate results against the archived documentation. Their outputs are not reviewed, curated, or published by this discontinued initiative.*

**1) Pick** one ambiguous local term (column header, code, or ontology class).

**2) Select** the closest HRIO meaning (browse the ontology specification/documentation).

**3) Attach** a meaning-level relation (your semantic "unit test"):

- `hriv:hasExactMeaning` (intended meaning is fully equivalent)
- `hriv:hasBroaderMeaningThan` / `hriv:hasNarrowerMeaningThan` (meaning is broader/narrower)

**4) Document and validate it** in your own workflow. The initiative's contribution, review, curation, and release workflows are closed.

## Community and collaboration

During its active phase, the initiative received valuable support and feedback from academics and professionals across Health-RI and the broader health data community. Their perspectives helped shape the work and align it with national and international efforts toward interoperability.

The resources produced by the initiative remain openly available — including the [**ontology**](deliverables/index.md), [**mapping vocabulary**](method/specification-vocabulary.html), and [**mapping sets**](method/mapping-schema.md) — for reference, reuse, and citation. For the conceptual rationale and the initiative-level definition of semantic traceability, see our [academic paper](https://raw.githubusercontent.com/Health-RI/semantic-interoperability/main/documents/preprints/enabling-semantic-traceability-in-health-data-v1.1.0.pdf).

The contribution and community-review pages are retained as historical documentation of the processes used during the initiative. New submissions are not reviewed, curated, or integrated into project releases.

______________________________________________________________________

## About Health-RI

[Health-RI](https://www.health-ri.nl) is a national initiative in the Netherlands dedicated to building an integrated infrastructure for health and life-sciences data. By improving data sharing, reuse, and accessibility, Health-RI aims to empower researchers, clinicians, and policymakers to accelerate data-driven healthcare innovation.

Semantic interoperability plays a foundational role in this mission by ensuring that data from diverse sources can be aligned and understood consistently — not just technically, but conceptually.

______________________________________________________________________

## What's on this site

This site documents how the Health-RI Semantic Interoperability Initiative approached semantic interoperability across health and life-sciences data: its concepts, modeling foundations (OntoUML & gUFO), method and mapping vocabulary, and published ontology deliverables (specs, docs, changelog).

- **Initiative Status**: [Discontinuation and archival status](status.md)
- **Semantic Interoperability**: [Overview](semantic-interoperability/index.md)
- **OntoUML & gUFO**: [Overview](ontouml-gufo/index.md) · [OntoUML](ontouml-gufo/ontouml.md) · [OntoUML Stereotypes](ontouml-gufo/ontouml-stereotypes.md) · [OntoUML/UFO Catalog](ontouml-gufo/ontouml-ufo-catalog.md) · [Creating OntoUML Models](ontouml-gufo/creating-ontouml-models.md) · [gUFO](ontouml-gufo/gufo.md)
- **Method**: [Overview](method/index.md) · [Introduction](method/introduction.md) · [Mapping Strategy](method/mapping-strategy.md) · [Mapping Vocabulary Specification](method/specification-vocabulary.html) · [SSSOM Mapping Set](method/mapping-schema.md) · [Mapping Governance](method/mapping-governance.md) · [Ontology Versioning](method/ontology-versioning.md) · [Ontology Validation](method/ontology-validation.md) · [Publications](method/publications.md) · [Persistent Identifiers](method/persistent-ids.md)
- **Deliverables**: [Overview](deliverables/index.md) · [Ontology Documentation](deliverables/documentation.md) · [Ontology Specification](deliverables/specification-ontology.html) · [Ontology Changelog](deliverables/changelog-ontology.md)
- **Help & Archived Contributions**: [FAQ](faq.md) · [Contribution Process](./contributing/overview.md) · [Calls for Community Review](./contributing/call-for-community-review.md) · [Contribution Channels](./contributing/contribution-channels.md)

______________________________________________________________________

## Who this is for

Data stewards, modelers, and engineers who need stable, shared meaning across systems — using a common reference model (OntoUML → gUFO) and mappings that align external ontologies, terminologies, and schemas to it.

______________________________________________________________________

## License

**Semantic Artifacts & Documentation**: All ontologies, vocabularies, mapping files, documentation, templates, and other semantic artifacts are licensed under the [**Creative Commons Attribution 4.0 International (CC BY 4.0)**](https://creativecommons.org/licenses/by/4.0/) license.

**Auxiliary Code**: Any code scripts or auxiliary utilities are licensed under the [**MIT License**](https://spdx.org/licenses/MIT.html).
