# Frequently Asked Questions (FAQ)

## Project Overview and Strategic Context

*Questions about the initiative’s purpose, strategic goals, expected impact, and broader context.*

**Further reading:**

- [Overview of methods and approach](../method/)
- [FAIR & semantic interoperability context](../semantic-interoperability/)

!!! warning "Disclaimer"
    The answers in this section are part of an ongoing effort to address strategic questions about the initiative. They are based on initial interpretations and should be used with caution. All entries are marked as drafts and will be further refined and validated in collaboration with stakeholders.

??? question "What is the goal of Health-RI’s semantic interoperability initiative?"
    To enable meaningful data integration across health and life sciences institutions by aligning data semantically, not just structurally. This is achieved through the development and adoption of a common reference model that captures domain meaning explicitly.

??? question "What exactly are we trying to achieve with semantic interoperability?"
    We aim to align external and internal ontologies to a shared reference model, ensuring that semantic definitions are preserved across conceptual and computational layers. This is achieved through structured mappings (e.g., `hriv:hasExactMeaning`) from third-party concepts to Health-RI’s reference ontology (OntoUML) and its computational counterpart (gUFO).

??? question "Why is semantic interoperability important in healthcare and life sciences?"
    Because it ensures that data from diverse sources is interpreted consistently, reducing the risk of misinterpretation and improving reusability, reproducibility, and trust. It supports FAIR data practices and accelerates data-driven innovation.

??? question "What problem is this initiative addressing?"
    It addresses the issue of inconsistent data semantics across institutions, which leads to errors, false agreement, and limited reuse. Many systems use similar terms but with different meanings, or different terms for the same concept.

??? question "Is there a standardized way to define common reference models? Are we using standardized methods, languages, or tools?"
    There is currently no global standard for defining and implementing semantic reference models. However, the approach adopted by this initiative—based on ontology-driven conceptual modeling and explicit ontological commitments—is recognized in the literature as the only viable path to achieve real semantic interoperability (see [Guizzardi (2020)](https://doi.org/10.1162/dint_a_00033)).

    We apply well-established methods and languages that have been successfully used in a variety of domains and are widely recognized for their effectiveness (see [Guizzardi et al. (2022)](https://journals.sagepub.com/doi/abs/10.3233/AO-210256)). These include:

    - OntoUML for conceptual modeling
    - OWL and RDF for computational representation and publishing
    - SSSOM Mappings for declaring resources semantics
    - Persistent identifiers, alignment with FAIR principles

    Other approaches may offer faster implementation or simpler integration but often fail to ensure semantic consistency over time. By contrast, our approach prioritizes long-term semantic precision and interoperability.

??? question "What does success look like for this project?"
    Success means having a robust reference model (OntoUML) and executable OWL artifacts (gUFO) in place, with external ontologies semantically aligned through precise mappings. It also includes supporting community contributions, replacing approximate mappings (e.g., `hriv:hasExactMeaning`) with exact ones where possible, and continuously refining the model to bridge semantic gaps.

??? question "Who will benefit from or use the developed solutions?"
    Researchers, clinicians, developers, and data stewards who need to align datasets from different systems and institutions while preserving domain meaning.

??? question "Are there any external collaborators or partner organizations? (TBD)"
    TBD.

??? question "What is the current situation regarding data interoperability in the Netherlands? (TBD)"
    TBD.

??? question "How do current systems or processes work without semantic alignment?"
    Without semantic alignment, systems may use the same term for different concepts or different terms for the same concept, causing ambiguity and inconsistency.

??? question "What are some examples of current successes or progress?"
    The development of the OntoUML conceptual model, its implementation as the gUFO OWL ontology, and the strategy for semantically aligning third-party ontologies using [Health-RI Mapping Vocabulary](../method/specification-vocabulary.html) properties are all concrete milestones achieved. Figures and examples in the documentation illustrate successful alignment strategies already in use.

??? question "What challenges are currently being faced?"
    One challenge is when no exact match exists between external concepts and the reference ontology. This requires approximate mappings and motivates the need to expand the Health-RI ontology to bridge gaps. Another challenge is managing transitivity and ambiguity in mappings (e.g., limiting to a single `hriv:hasExactMeaning` per concept).

??? question "What risks and limitations should be considered? (TBD)"
    TBD.

??? question "What assumptions are being made during development? (TBD)"
    TBD.

??? question "What changes are expected in the future?"
    Future work includes refining the ontology by introducing intermediate concepts to replace approximate mappings with exact ones, enhancing semantic precision and reasoning capabilities.

??? question "How might the future process or system improve data use across institutions? (TBD)"
    TBD.

??? question "What changes will users experience? (TBD)"
    TBD.

??? question "What is the common reference model and why is it needed?"
    It’s a conceptual model created using OntoUML to serve as a semantic anchor for all participating data schemas. Instead of replacing local schemas, it provides a shared foundation for mapping and aligning meaning.

    OntoUML defines the domain-level semantics, while gUFO implements those concepts in OWL. This layered architecture ensures that semantic meaning is preserved from human-level models to machine-readable artifacts.

??? question "How does this initiative relate to the FAIR principles?"
    It supports the 'I' in FAIR—Interoperability—by grounding vocabularies and schemas in shared ontologies and ontological commitments (see [FAIR & semantic interoperability](../semantic-interoperability/)).

??? question "What are the main components of the approach?"
    - [OntoUML](../ontouml-gufo/ontouml) conceptual modeling
    - [gUFO](../ontouml-gufo/gufo) OWL-based computational ontologies
    - Schema-to-ontology mappings using tools like [SSSOM](https://mapping-commons.github.io/sssom/)

??? question "Why do we need the semantic interoperability initiative if standards like HL7, OMOP, or DCAT-AP already exist? Isn’t this duplicating existing efforts?"
    This initiative complements existing standards like HL7, OMOP, and DCAT by focusing on semantic precision, ontological clarity, and interoperability at the conceptual level. While HL7 and OMOP define syntactic and structural specifications for health data, this initiative addresses foundational semantics to align and reason over data models meaningfully. It:

    - Provides foundational ontological grounding that is missing in most standards.
    - Enables alignment across heterogeneous schemas and institutions through a shared conceptual backbone.
    - Supports model-driven engineering (MDE) practices to enable consistent transformations and mappings.

??? question "What is the relationship between this initiative and existing health data standards such as OMOP, HL7, or DCAT-AP?"
    This initiative does not aim to create a new standard. Instead, it recognizes that existing standards such as OMOP, HL7, and DCAT-AP each serve different purposes and contain distinct types of content—ranging from data exchange formats to terminologies and domain-specific data models.

    The goal is to harmonize the underlying concepts from these standards, as well as other models and artifacts, by aligning them with a shared semantic reference ontology. This ontology provides a common conceptual foundation that enables consistent interpretation and integration of diverse representations. The reference ontology acts as a semantic anchor, supporting interoperability across heterogeneous data sources, standards, and systems.

??? question "Why did Health-RI decide to build a new ontology instead of reusing existing ones from the biomedical and life sciences domains (like those in OBO Foundry)? (TBD)"
    TBD.

??? question "Does the Health-RI initiative reuse any existing biomedical or life sciences ontologies? Are external ontologies integrated or referenced within the Health-RI ontology? (TBD)"
    TBD.

??? question "Given that many life sciences ontologies adopt the Basic Formal Ontology (BFO), what motivated the use of UFO rather than BFO as the foundation for this initiative’s ontology? (TBD)"
    TBD.

## Modeling Approach: OntoUML and gUFO

*Questions about the internal modeling framework, layers, and implementation choices.*

**Further reading:**

- [OntoUML overview](../ontouml-gufo/ontouml)
- [gUFO details](../ontouml-gufo/gufo)

??? question "What are OntoUML and gUFO, and why are they used?"
    OntoUML is a conceptual modeling language grounded in the foundational ontology named Unified Foundational Ontology (UFO). gUFO is its OWL counterpart, enabling computational use. Together, they ensure semantic precision and machine-actionable models.

    OntoUML operates at MDA's CIM layer to capture conceptual semantics, while gUFO provides a platform-independent OWL implementation at the PIM layer. This ensures a traceable and interoperable flow from conceptualization to deployment.

??? question "OntoUML and gUFO seem very complex. Isn’t that a barrier to adoption?"
    This is a common concern. Foundational ontologies like UFO are indeed complex—because they aim to capture real-world meaning with a high level of precision and avoid ambiguity across domains. Some complexity is simply inherent to the task: when we model the real-life elements, especially across institutions or sectors, we cannot always rely on overly simplistic representations.

    That said, this initiative does not require users to engage directly with UFO. Instead, we rely on OntoUML and gUFO to make that foundational theory accessible in practice. OntoUML provides intuitive modeling constructs grounded in UFO, while gUFO offers a lightweight OWL implementation suitable for real-world applications.

    This layered approach lets modelers benefit from UFO’s expressive power without being overwhelmed by its formal depth. The complexity is managed by the modeling framework and supported by tools like Visual Paradigm and the OntoUML plugin. In fact, these languages have already been applied successfully in domains like public health, law, and digital humanities—demonstrating that the approach is both practical and scalable.

??? question "How is the OntoUML model converted to OWL?"
    The OntoUML model is exported to OWL using the [gUFO specification](../ontouml-gufo/gufo) via plugin tooling. The resulting ontology retains the original semantics in a format suitable for Semantic Web technologies.

??? question "What is the difference between OntoUML and gUFO?"
    OntoUML is a conceptual modeling language for humans; gUFO is its OWL-based computational counterpart used in Semantic Web technologies.

## Mapping and Alignment Strategy

*Questions about how external concepts are aligned to the Health-RI reference model using dedicated mapping properties from the Health-RI Mapping Vocabulary.*

Further reading:

- [Health-RI Mapping Vocabulary](../method/specification-vocabulary.html)
- [Mapping strategy guide](../method/mapping-strategy)
- [How to contribute concepts/mappings](../contributing/)

??? question "How are mappings from local schemas to the reference model created?"
    If schemas are OWL/RDF-based, mappings can be embedded directly using standard RDF properties. Otherwise, external mappings are created using [SSSOM](https://mapping-commons.github.io/sssom/).

    Mappings follow the [Health-RI Mapping Vocabulary](../method/specification-vocabulary.html) and can be asserted using:

    - [`hriv:hasExactMeaning`](../method/specification-vocabulary.html#hasExactMeaning) for perfect semantic alignment (only one allowed),
    - [`hriv:hasBroaderMeaningThan`](../method/specification-vocabulary.html#hasBroaderMeaningThan) or [`hriv:hasNarrowerMeaningThan`](../method/specification-vocabulary.html#hasNarrowerMeaningThan) when the match is approximate.

    These mappings support semantic alignment without requiring modification to the original schema and are managed either by Health-RI (non-invasively in SSSOM) or by partners (embedded in their own RDF models).

??? question "What is `hriv:hasExactMeaning`, and how is it different from `owl:equivalentClass` or `skos:exactMatch`?"
    `hriv:hasExactMeaning` (equivalent to `semiotics:expresses`) is used to state that an external concept carries the same intended meaning as a concept in the Health-RI reference model. It expresses a strong semantic alignment in terms of shared meaning, but it does not imply logical equivalence.

    - Unlike `owl:equivalentClass`, it does not entail formal logical equivalence and therefore avoids unintended reasoning consequences when integrating ontologies with different logical foundations.
    - Unlike `skos:exactMatch`, which is often used for linking concepts across vocabularies in a looser, less formally grounded way, `hriv:hasExactMeaning` is tied to an explicit semantic grounding in a reference ontology. This makes it more precise for interoperability scenarios where meaning—not logical entailment—is the key requirement.

    In summary, `hriv:hasExactMeaning` is intended for strong semantic alignment without the risks of logical overcommitment (`owl:equivalentClass`) or the potential ambiguity of generic lexical alignment (`skos:exactMatch`).

??? question "Why is there a rule that only one `hriv:hasExactMeaning` is allowed per concept?"
    To avoid semantic ambiguity. Allowing multiple `hriv:hasExactMeaning` assertions for the same concept would imply conflicting definitions and hinder consistent interpretation. Each external concept must match only one Health-RI concept with perfect equivalence.

??? question "What should I do if no exact match exists between my concept and the Health-RI ontology?"
    If your concept is broader or narrower than any existing reference concept, use `hriv:hasBroaderMeaningThan` or `hriv:hasNarrowerMeaningThan` accordingly. These mappings allow approximate alignment. You are also encouraged to contact the Health-RI team to propose additions to the reference model to enable more precise mappings in the future.

??? question "Can new concepts be added to the Health-RI ontology to improve mapping precision?"
    Yes. When `hriv:hasExactMeaning` cannot be used due to missing concepts, we encourage you to contact the Health-RI modeling team.

    If justified, new intermediate concepts may be added to the reference ontology. This helps replace approximate mappings (`hriv:hasBroaderMeaningThan`, `hriv:hasNarrowerMeaningThan`) with exact ones and ensures better semantic precision for reasoning, integration, and long-term alignment. Requests are welcome and reviewed by the Health-RI modeling team; if accepted, new concepts may be added to enable stronger future mappings.

??? question "Who creates and maintains the semantic mappings to the Health-RI ontology?"
    Mappings can be created and maintained by:

    - The Health-RI team, which curates non-invasive mappings using the [SSSOM](https://w3id.org/sssom/) format, for public or external ontologies. These mappings are published externally and do not alter the original third-party ontologies.
    - External partners, who can embed mappings directly in their own ontology files using Health-RI Mapping Vocabulary properties (e.g., `hriv:hasExactMeaning`), especially when they control the editorial process of the external artifact.

## SSSOM Mapping Set

??? question "Is the Health-RI SSSOM Mapping Set manually curated or automatically generated?"
    It is manually curated by the Health-RI mapping team with input from external collaborators.

??? question "Where can I download the SSSOM Mapping Set, and in which formats?"
    Use the stable URIs:

    - `https://w3id.org/health-ri/semantic-interoperability/mappings` → TTL
    - `https://w3id.org/health-ri/semantic-interoperability/mappings/ttl` → TTL
    - `https://w3id.org/health-ri/semantic-interoperability/mappings/tsv` → TSV.

??? question "How is the mapping set versioned?"
    The mapping set uses date-based versions (YYYY-MM-DD) tied to the publication date, with at most one release per day.

??? question "Can a published mapping be deleted? How are corrections handled?"
    Published mappings cannot be removed. To revise an entry, create a new record that uses `replaces` to supersede the old one.

??? question "Which SSSOM fields are mandatory, optional, or system-assigned?"
    Fields are divided by responsibility:

    - Contributor (mandatory) — must be provided in PRs (e.g., `subject_id`, `predicate_id`, `object_id`, `mapping_justification`, `author_id`, `mapping_date`)
    - Contributor (optional) — can be added if available
    - Curator — added or verified by Health-RI curators
    - System (Fixed) — constant, cannot be changed
    - System (Generated) — assigned at publication time

??? question "What fields should I provide when contributing a mapping?"
    At minimum, contributors must provide all mandatory fields:
    `subject_id`, `predicate_id`, `object_id`, `mapping_justification`, `author_id`, and `mapping_date`.

    Optional fields can be added if available (for example, comments or additional provenance). System-assigned and curator fields will be handled during the review and publication process.

    For the complete specification of all fields and their roles, see the Mapping Set Schema Reference page.

??? question "Besides creating positive assertions, can I also create negative ones?"
    Yes. Most mappings are positive, where you state that two concepts are related. But sometimes you may want to explicitly say that a mapping should not hold. For that, use the field `predicate_modifier` with the value `Not`. If your mapping is positive, just leave this field empty.

    **Examples**

    - Positive mapping: "fhir:Patient has its semantics defined by hrio:Patient"
      `subject_id = fhir:Patient`
      `predicate_id = hriv:hasExactMeaning`
      `object_id = hrio:Patient`
      `predicate_modifier =` (empty)

    - Negative mapping: "vet:Patient DOES NOT have its semantics defined by hrio:Patient"
      `subject_id = vet:Patient`
      `predicate_id = hriv:hasExactMeaning`
      `object_id = hrio:Patient`
      `predicate_modifier = Not`

## Community Contributions and Feedback

**Further reading:**

- [Contributing page](../contributing/)
- [GitHub Issue Forms](https://github.com/health-ri/semantic-interoperability/issues/new/choose)
- [Mappings template (XLSX)](https://raw.githubusercontent.com/Health-RI/semantic-interoperability/refs/heads/main/resources/mappings_template.xlsx)

??? question "What are the supported ways to contribute a new mapping row?"
    There are two options:

    1) Issue form (preferred) — submit the SSSOM mapping issue form for a single row.
    2) Excel template — fill in the `mappings` sheet (rows) and the `prefix` sheet (CURIE bindings) in the provided XLSX, then attach it to a new issue.
    In the template, headers for mandatory fields are black, and optional ones are green. Both methods are curator-reviewed and integrated into the official mapping set.

??? question "What should I check before submitting a mapping?"
    Use the submission checklist:

    - All mandatory contributor fields are present and correctly formatted.
    - Optional values (if any) use valid identifiers (e.g., ORCID, resolvable URIs, SEMAPV terms).
    - If you pin a version, ensure `object_source` is a specific version URI (not a generic one).

??? question "Can external parties contribute to the modeling or mapping process?"
    Yes. External contributions are welcome and encouraged.

    Community members can submit suggestions, error reports, or collaboration proposals directly via our [GitHub Issue Forms](https://github.com/health-ri/semantic-interoperability/issues/new/choose).

    Available contribution types include:

    - Reporting errors or inconsistencies in the OntoUML/gUFO models
    - Proposing new ontology concepts
    - Suggesting improvements to documentation or mappings
    - Proposing example use cases or general feedback

    For details, visit the [Contributing page](../contributing/).

??? question "How can I contribute to the Health-RI Semantic Interoperability Initiative?"
    You can contribute by submitting structured feedback using one of our [GitHub Issue Forms](https://github.com/health-ri/semantic-interoperability/issues/new/choose). We currently support the following contribution types:

    - Report an error in the OntoUML or gUFO-based ontology
    - Request a new concept to be added to the reference model
    - Submit other input such as documentation improvements, mapping suggestions, or collaboration proposals

    Start here: [Contribute via GitHub](https://github.com/health-ri/semantic-interoperability/issues/new/choose). Or visit our [Contributing page](../contributing/) for more guidance.

??? question "Do I need to check the ontology version before submitting a contribution?"
    Yes, we ask contributors to indicate which version of the ontology or artifact they reviewed before submitting a request — especially when reporting issues or suggesting new concepts.

    This helps us avoid duplicates, understand the context of your feedback, and keep the review process efficient.

    You’ll find a field for this information in the contribution forms.

??? question "Where can I find more information on how to submit feedback?"
    See our [Contributing page](../contributing/), which outlines how to submit structured input, what types of feedback are accepted, and how your suggestions will be reviewed.

    All community input is tracked as GitHub Issues and reviewed by the modeling and coordination teams.

## Ontology Lifecycle and Publishing

*Questions about how the ontology is released, versioned, and maintained over time.*

**Further reading:**

- [Publications & operations](../method/publications)
- [Ontology versioning](./method/versioning-ontology.md)
- [Validation & stage gates](./method/validation-ontology.md)
- [Persistent identifiers (PIDs)](../method/persistent-ids)

??? question "What are the ontology lifecycle stages (`int`, `irv`, `erv`, `pub`)?"
    - `int` — internal work (drafting, labeling, layout).
    - `irv` — internal review by team members not involved in modeling.
    - `erv` — external review with invited community input.
    - `pub` — published; release operations (e.g., GitHub Release, DOI) are executed while remaining in `pub`.

??? question "Who validates at each stage?"
    - `irv`: independent internal reviewers (not the authors).
    - `erv`: domain and modeling specialists (community call invites participation).

??? question "How long do reviews take?"
    Target one sprint for internal and one sprint for external review; either may extend to two depending on scope/availability.

??? question "How is the community involved in external review?"
    A Call for Community Review is issued when a package enters `erv`; feedback is collected during the external-review sprint.

??? question "What triggers a stage reversion (e.g., `pub → int`) and what happens then?"
    Critical defects or major scope changes can revert to `int`; the package then re-passes the stage gates before moving forward again.

??? question "Where can I find the latest version of the Health-RI ontology?"
    All published versions are available in the `/ontologies/` folder. The most recent release is always accessible via: <https://w3id.org/health-ri/ontology>

??? question "How does versioning work for the ontology (X.Y.Z)?"
    Format: `X.Y.Z` with strict priority X > Y > Z — only one component increments per release; lower components reset.

    Meanings:
    - X — package index: add/remove a package → X++; then `Y = 0`, `Z = 0`.
    - Y — stage/semantic: any stage change (`int ↔ irv ↔ erv ↔ pub`) or semantic modeling change → Y++; then `Z = 0`.
    - Z — non-semantic: labels/typos, diagram/layout, links/docs → Z++.

    Rules: No skipping numbers; exactly one single-step bump per release.
    Scope: Applies to the ontology; the mapping set and mapping vocabulary are versioned separately.

??? question "What does the 'latest' folder contain and how is it maintained?"
    The `ontologies/latest/` folder and the ontology's PID always resolves to the most recent available release.
    They provide stable access to the most recent files without needing to specify a version number.
    Each new release automatically updates the `latest/` folder and the file related to the ontology's PID to target the latest content.

??? question "How do I cite or refer to the Health-RI initiative and its artifacts?"
    You can use the following Persistent Identifiers (PIDs) to cite the initiative and its semantic artifacts:

    - Initiative-wide identifier: `https://w3id.org/health-ri/semantic-interoperability`
    - Health-RI Ontology: `https://w3id.org/health-ri/ontology`
    - Health-RI SSOM Mapping Set: `https://w3id.org/health-ri/semantic-interoperability/mappings`
    - Health-RI Mapping Vocabulary: `https://w3id.org/health-ri/mapping-vocabulary`

    These PIDs are stable, dereferenceable, and aligned with FAIR principles. They are suitable for use in citations, publications, and metadata records.

??? question "What types of files are published with each ontology version?"
    Each ontology version includes the following artifacts:

    - `.vpp`: OntoUML conceptual model (Visual Paradigm project)
    - `.json`: OntoUML export compliant with the OntoUML Schema
    - `.ttl`: OWL ontology (based on gUFO) — only for syntactically valid models
    - `.md`: Human-readable documentation (Markdown)
    - `.html`: Human-readable specification (HTML)
    - `.png`: Diagram images (only in the `latest/` folder)

    These are published under both `ontologies/latest/` (most recent version) and `ontologies/versioned/` (versioned archive).

??? question "Where can I find the exported images of the ontology diagrams?"
    Exported PNG images of all OntoUML diagrams are available in the `ontologies/latest/images/` folder.
    These images are always generated from the latest `.vpp` file and are not maintained for previous versions.

??? question "Why is there sometimes no OWL (.ttl) file available for a version?"
    The `.ttl` file (gUFO-compliant OWL ontology) is only generated when the OntoUML model is syntactically valid.
    Incomplete or draft versions may not include a `.ttl` file until model consistency is ensured.

??? question "Can the latest version of the OWL (.ttl) file correspond to a different version than the latest version of the OntoUML (.json/.vpp) model?"
    Yes. The `.ttl` versioning is managed independently and may lag behind the `.vpp` or `.json` files.
    The OWL file includes a `dcterms:conformsTo` triple that explicitly links it to the OntoUML version it was derived from.

??? question "How can I access a specific version of the Health-RI ontology?"
    Use the versioned PID format: `https://w3id.org/health-ri/ontology/vX.Y.Z/{format}`

    Replace `X.Y.Z` with the version number (e.g., `v0.6.0`) and `{format}` with one of:

    - `ttl`: OWL ontology in Turtle format
    - `vpp`: OntoUML model in Visual Paradigm format
    - `json`: OntoUML model in JSON format
    - `specification`: Human-readable specification (HTML)
    - `documentation`: Human-readable documentation (Markdown)

    **Examples:**
    - `https://w3id.org/health-ri/ontology/v0.6.0/ttl` — Ontology in Turtle for version 0.6.0
    - `https://w3id.org/health-ri/ontology/v0.6.0/specification` — HTML specification for version 0.6.0

??? question "What’s the difference between the latest and versioned ontology URIs?"
    - The latest URI (`https://w3id.org/health-ri/ontology`) always points to the most recent stable release. Its content may change over time as new versions are published.
    - A versioned URI (e.g., `https://w3id.org/health-ri/ontology/v2.0.0`) points to a specific, immutable release. Its content will never change, ensuring long-term consistency.

    Use the versioned URI when immutability is essential — for example, in scientific publications, formal mappings, or regulatory documentation. This guarantees that your references always point to the same version of the ontology.

    Use the latest URI when you want to stay aligned with the most up-to-date ontology version and future improvements.

??? question "What is the publishing strategy for ontology releases?"
    What we publish (per release):
    - A tagged GitHub Release with packaged artifacts (Technical Report PDF, exported figures) and detailed notes.
    - An archived snapshot on Zenodo with a minted DOI (referenced from the Release notes).
    - Artifacts exposed under w3id PIDs and repository folders:
        - Latest: `https://w3id.org/health-ri/ontology` and `ontologies/latest/` (most recent release).
        - Versioned: `https://w3id.org/health-ri/ontology/vX.Y.Z/...` and `ontologies/versioned/` (immutable per release).
    - Catalog and discoverability records: OntoUML/UFO Catalog entry/update; Technical Report on ResearchGate; announcements on LinkedIn.

    Where to get the files:
    - GitHub Release page (exact packaged artifacts and notes).
    - Zenodo record (DOI) for a preserved, citable snapshot.
    - w3id PIDs and repository folders for “latest” and “versioned” access; images (`.png`) live under `ontologies/latest/`.

??? question "How are the OntoUML and gUFO ontologies and the produced semantic mappings maintained over time?"
    Ontologies and semantic mappings are maintained in version-controlled repositories and released through a structured publishing pipeline. Each release is assigned a permanent, citable URL, with both a Persistent Identifier (PI). Ontologies are published in multiple formats (e.g., RDF/Turtle, JSON) and validated prior to release. This process ensures transparency, long-term accessibility, and semantic stability across versions.

??? question "Who is responsible for maintaining the ontology and its associated mappings?"
    The Health-RI team is responsible for maintaining the core ontologies and mappings produced within the initiative. This work is carried out in close collaboration with external partners who contribute ideas, suggestions, and mappings. Contributions are reviewed and integrated through a structured, version-controlled process.

??? question "How will the new solutions be maintained and supported?"
    After a package reaches `pub`, we run the Publication Stage Operations Checklist while remaining in `pub`:

    - Release and preservation: publish a GitHub Release (tag, notes) including the package report (PDF) and figures; trigger Zenodo and record the DOI.
    - Catalog and discoverability: update the OntoUML/UFO Catalog; upload the report to ResearchGate; announce publication and follow-ups (e.g., DOI/catalog) on LinkedIn.
    - Academic publication (optional): consider a peer-reviewed venue; when accepted, add the formal citation and publisher DOI to the docs and Release.

    Ongoing support and feedback: GitHub Issues remain open as a standing channel; substantive issues can lead to a stage reversion for corrective work.
    Scope: This operational checklist is specific to the ontology.

??? question "What happens right after a package is published (`pub`)?"
    While remaining in `pub`, we:
    - Publish a GitHub Release (tag, notes, packaged artifacts) and mint a Zenodo DOI.
    - Update the OntoUML/UFO Catalog and upload the Technical Report to ResearchGate.
    - Post announcements and follow-ups (e.g., DOI/catalog) on LinkedIn.
    Feedback continues via GitHub Issues; substantive issues may trigger a reversion to `int`.

??? question "How will the ontology be tested and accepted?"
    Acceptance is tied to passing the stage gate checklists:

    - `int → irv` gate (author self-check + modeling/diagram/metadata readiness).
      Entry into `irv` happens only after all Internal Stage Gate items pass.
    - `irv → erv` gate (independent internal review).
      Reviewers execute the Internal Review Stage Gate; evidence is recorded in the review issue.
    - `erv → pub` outcome (independent external review).
      When the package passes external review, the modeler records `<erv → pub>`; then the Publication Stage Operations Checklist is executed while remaining in `pub`.

    Timelines: internal and external reviews are planned as sprint activities; the target is one sprint, optionally extended to two depending on scope and availability.
    Note: Substantive defects or scope changes at any stage can revert the package to `int` for rework; advancement then follows the same gates again.

??? question "Where can I find an overview of all persistent identifiers provided by the initiative?"
    The initiative maintains a consolidated table of all PIDs, covering the ontology, mapping set, and mapping vocabulary.
    This table describes the behavior of each PID (e.g., redirects, format-specific access) and provides examples.
