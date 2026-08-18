# Frequently Asked Questions (FAQ)

## Project Overview and Strategic Context

*Questions about the initiative's purpose, strategic goals, expected impact, and broader context.*

**Further reading:**

- [Overview of methods and approach](method/index.md)
- [FAIR & semantic interoperability context](semantic-interoperability/index.md)

!!! warning "Disclaimer"

    This FAQ is retained as archival project documentation. Several entries were drafts or work in progress when the initiative was discontinued and may contain interpretations that were not further refined or validated with stakeholders. Use them with appropriate caution.

!!! warning "Transparency (AI-assisted drafting)"

    Parts of this FAQ were drafted with AI-assisted editing support and reviewed by Health-RI team members during the active initiative. No further project review is planned after discontinuation.

??? question "What is the current status of the Health-RI Semantic Interoperability Initiative?"

    The initiative was formally paused on **May 1, 2026** and has since been **discontinued**.

    No further development, curation, community review, or release activity is planned under this initiative. Existing documentation, released artifacts, persistent identifiers, and repository materials remain available as archival resources for reference, reuse, and citation, but they are not actively maintained.

    This does not invalidate previously released artifacts. For reproducible references, use versioned persistent identifiers where available. See [Initiative Status](status.md).

??? question "Is there an assistant that can help me navigate this initiative and its artifacts?"

    The initiative created an Assistant (GPT) that explains the initiative in plain terms and points to relevant pages and stable identifiers (w3id PIDs). If it remains accessible, treat it as an archived, non-maintained navigation aid.

    [Open the Assistant (GPT)](https://chatgpt.com/g/g-6992c8eb8780819185f0922ac33d79ce-health-ri-semantic-interoperability-guide){ .md-button .md-button--primary }

    Typical questions it can answer:

    - What is the Health-RI Semantic Interoperability Initiative?
    - Give me a quick tour of the project's main artifacts.
    - Where can I find the final official HRIO release?
    - Explain HRIO in plain terms and how I should use it.
    - Explain HRIV (Mapping Vocabulary) and what it's for.
    - How do I cite the final official ontology release?
    - What's the difference between the ontology TTL and the SHACL shapes?
    - How do persistent identifiers (w3id) work in this project?
    - I have a term/IRI—help me interpret it and find its definition.
    - How are mappings represented in this initiative?

    Notes:

    - Treat the linked docs and PIDs as the authoritative archival reference.
    - Avoid pasting sensitive or unpublished content into the assistant.
    - Assistant outputs are not reviewed, curated, or published by an active Health-RI Semantic Interoperability Initiative workflow.

??? question "What is the goal of Health-RI's semantic interoperability initiative?"

    To enable meaningful data integration across health and life sciences institutions by aligning data semantically, not just structurally. This is achieved through the development and adoption of a common reference model that captures domain meaning explicitly.

??? question "What exactly are we trying to achieve with semantic interoperability?"

    We aim to align source expressions from heterogeneous artifacts—such as standards, local schemas, ontologies, and related implementation artifacts—to a shared reference model, so that their intended meanings can be interpreted consistently across conceptual and computational layers.

    This is achieved through structured meaning mappings (e.g., `hriv:hasExactMeaning`, `hriv:hasBroaderMeaningThan`, `hriv:hasNarrowerMeaningThan`) from source expressions to the Health-RI Ontology (HRIO), which is specified in OntoUML and implemented as a gUFO-based OWL ontology (HRIO gUFO/OWL).

??? question "Why is semantic interoperability important in healthcare and life sciences?"

    Because it ensures that data from diverse sources is interpreted consistently, reducing the risk of misinterpretation and improving reusability, reproducibility, and trust. It supports FAIR data practices and accelerates data-driven innovation.

??? question "What problem is this initiative addressing?"

    It addresses the issue of inconsistent data semantics across institutions, which leads to errors, false agreement, and limited reuse. Many systems use similar terms but with different meanings, or different terms for the same concept. Rather than assuming agreement based on labels, definitions, codes, or OWL axioms, the initiative requires that mapped concepts be traced back to a shared, well-defined conceptualization.

??? question "Is there a standardized way to define common reference models? Are we using standardized methods, languages, or tools?"

    There is currently no global standard for defining and implementing semantic reference models. However, the approach adopted by this initiative—based on ontology-driven conceptual modeling and explicit ontological commitments—is recognized in the literature as a viable path to achieve semantic interoperability (see [Guizzardi (2020)](https://doi.org/10.1162/dint_a_00033)).

    We apply well-established methods and languages that have been successfully used in a variety of domains and are widely recognized for their effectiveness (see [Guizzardi et al. (2022)](https://journals.sagepub.com/doi/abs/10.3233/AO-210256)). These include:

    - OntoUML for conceptual modeling (reference model)
    - OWL and RDF for computational representation and publishing (gUFO-based OWL implementation)
    - SSSOM mapping sets for sharing meaning mappings (when mappings are maintained as separate artifacts)
    - Persistent identifiers, alignment with FAIR principles

    Other approaches may offer faster implementation or simpler integration but often fail to ensure semantic consistency over time. By contrast, our approach prioritizes long-term semantic precision and interoperability.

??? question "What does success look like for this project?"

    Success means having a robust common semantic reference model (HRIO OntoUML) and its computational implementation (HRIO gUFO/OWL) in place, with high-priority source expressions from important standards, schemas, ontologies, and related implementation artifacts aligned to HRIO meanings through reviewed mappings.

    During active development, this also included supporting community contributions, treating broader/narrower mappings as useful indicators of semantic mismatch, and refining the model over time so that exact-meaning mappings (`hriv:hasExactMeaning`) could be used whenever genuinely justified.

??? question "Who will benefit from or use the developed solutions?"

    Researchers, clinicians, developers, and data stewards who need to align datasets from different systems and institutions while preserving domain meaning.

??? question "Are there any external collaborators or partner organizations?"

    Yes. The initiative's work was carried out with Health-RI's external collaborators, including Leiden University Medical Center (LUMC) and Amsterdam University Medical Center (Amsterdam UMC).

??? question "What is the current situation regarding data interoperability in the Netherlands? (TBD)"

    Not completed before discontinuation.

??? question "How do current systems or processes work without semantic alignment?"

    Without semantic alignment, systems may use the same term for different concepts or different terms for the same concept, causing ambiguity and inconsistency.

??? question "What are some examples of current successes or progress?"

    The development of the HRIO OntoUML conceptual model, its implementation as the gUFO-based OWL ontology, and the strategy for semantically aligning source expressions from heterogeneous artifacts using [Health-RI Mapping Vocabulary](method/specification-vocabulary.html) properties are all concrete milestones already achieved.

??? question "What challenges and unresolved limitations were identified?"

    A recurring challenge is that no exact-meaning alignment is sometimes justified between a source expression and the reference ontology. In such cases, broader/narrower meaning mappings are not failures; they are useful ways to make semantic mismatch explicit and may indicate areas where HRIO could have been refined further.

    A further challenge concerns scoping the reference model in a domain as broad as health and life sciences. HRIO cannot model every possible interpretation of every reused label, so coverage must be prioritized according to interoperability value, recurrence across important artifacts, and the risk of false agreement.

    Consistent interpretation across tooling also remains important. HRIV mappings can be aligned to SKOS mapping relations for interoperability and discovery, but SKOS-level entailments (e.g., transitivity of `skos:exactMatch`) must not be used to change the intended interpretation of an HRIV mapping. This makes the documented curation rules and governance important when assessing or reusing the released mappings.

??? question "What risks and limitations should be considered?"

    The current documentation illustrates intended benefits but does not present an empirical evaluation of mapping-effort reduction, error reduction, or user comprehension gains.

    Adoption may also increase initial effort in the short term, since new standards and local schemas still require curated meaning mappings. In addition, mappings must be maintained per source artifact and release, and reviewed when source or HRIO definitions evolve. Continued use of the approach outside this discontinued initiative therefore requires adopters to provide their own governance and maintenance processes.

??? question "What assumptions were made during development?"

    The approach relies on explicit semantic assumptions linking layers and artifacts. In particular:

    - The HRIO gUFO/OWL ontology is treated as an implementation of the HRIO OntoUML reference model, preserving the same intended meanings across conceptual and computational layers.
    - External artifacts are treated as indirectly representing HRIO meanings via their HRIV links to HRIO concepts; this "indirect representation" is derived from implementation and mapping assumptions rather than encoded as an OWL relation.

    In the OWL implementation, mapping assertions are expressed as object-property assertions between individuals denoting expressions and meanings (with OWL 2 DL punning when OWL class IRIs are used). As a result, HRIV mappings should not be interpreted as OWL class axioms.

??? question "What changes are expected in the future?"

    No further development, curation, community review, or release activity is planned under the discontinued Health-RI Semantic Interoperability Initiative. The published artifacts remain available as archival resources. Any future work based on them would be outside this initiative and would require separate governance and maintenance arrangements.

??? question "How might the future process or system improve data use across institutions? (TBD)"

    Not completed before discontinuation.

??? question "What changes will users experience? (TBD)"

    Not completed before discontinuation.

??? question "What is the common reference model and why is it needed?"

    It is a conceptual model created using OntoUML to serve as a shared semantic reference for standards, local schemas, ontologies, and related implementation artifacts. Rather than replacing local schemas or mirroring external artifacts one by one, it acts as a semantic hub that makes relevant meanings explicit and supports reviewed mappings across heterogeneous sources.

    OntoUML defines the domain-level semantics, while gUFO implements those concepts in OWL. This layered architecture supports semantic traceability from the conceptual model to machine-processable artifacts.

??? question "Does HRIO aim to model everything in health and life sciences?"

    No. HRIO is not intended to model every possible term, label, or modeling choice found across the full health and life sciences domain.

    Instead, HRIO is scoped incrementally as a common semantic reference model for interoperability. Its purpose is to make the meanings most relevant for alignment across important standards, local schemas, ontologies, and related implementation artifacts explicit and reviewable. Coverage should therefore be driven by interoperability value, conceptual necessity, and evidence of actual use, rather than by the mere existence or frequency of labels in external artifacts.

??? question "How is candidate HRIO content prioritized?"

    Candidate HRIO content should be prioritized according to interoperability value. Priority is highest for meanings that recur across influential standards, schemas, or related artifacts, are important for recurrent mapping work, and are especially prone to semantic ambiguity or false agreement.

    In practice, this means HRIO should focus first on concepts whose meanings need to be made explicit so that heterogeneous artifacts can be interpreted and aligned in a shared and reviewable way. Not every local distinction or artifact-specific label should be incorporated into the reference model.

??? question "How does this initiative relate to the FAIR principles?"

    It supports the 'I' in FAIR—Interoperability—by grounding vocabularies and schemas in shared ontologies and ontological commitments (see [FAIR & semantic interoperability](semantic-interoperability/index.md)).

??? question "What are the main components of the approach?"

    - [OntoUML](ontouml-gufo/ontouml.md) conceptual modeling for HRIO
    - [gUFO](ontouml-gufo/gufo.md) as the OWL-based computational implementation of HRIO
    - HRIV meaning mappings from source expressions to HRIO meanings
    - SSSOM mapping sets and embedded mappings for managing semantic alignments
    - Persistent identifiers and publication artifacts for stable access and traceability

??? question "Why do we need the semantic interoperability initiative if standards like HL7, OMOP, or DCAT-AP already exist? Isn't this duplicating existing efforts?"

    This initiative complements existing standards like HL7, OMOP, and DCAT by focusing on semantic precision, ontological clarity, and interoperability at the conceptual level. While HL7 and OMOP define syntactic and structural specifications for health data, this initiative addresses foundational semantics to align and reason over data models meaningfully. It:

    - Provides foundational ontological grounding that is missing in most standards.
    - Enables alignment across heterogeneous schemas and institutions through a shared conceptual backbone.
    - Supports model-driven engineering (MDE) practices to enable consistent transformations and mappings.

??? question "What is the relationship between this initiative and existing health data standards such as OMOP, HL7, or DCAT-AP?"

    This initiative does not aim to create a new standard or to replace existing standards, schemas, or ontologies. Instead, it recognizes that artifacts such as OMOP, HL7 standards such as FHIR, openEHR, and DCAT-AP serve different purposes and contain different kinds of content, including exchange structures, information models, terminologies, and other implementation-level artifacts.

    The goal is to support semantic interoperability across such heterogeneous artifacts by aligning relevant source expressions to shared HRIO meanings. In this way, HRIO functions as a common semantic reference model: it does not replace those artifacts, but provides a shared meaning-level foundation that helps make their intended semantics explicit, comparable, and mappable in a reviewable way.

??? question "Why did Health-RI decide to build a new ontology instead of reusing existing ones from the biomedical and life sciences domains (like those in OBO Foundry)? (TBD)"

    Not completed before discontinuation.

??? question "How does HRIO relate to external ontologies and semantic resources?"

    HRIO is not intended to replace mature external ontologies or other semantic resources. Instead, it serves as the common meaning-level reference model used to support semantic interoperability across heterogeneous artifacts.

    When appropriate, external ontologies and related semantic resources can be reused and aligned to HRIO through mappings. In this way, existing resources may remain valuable at the representation or implementation level without replacing HRIO's role in making shared meanings explicit, comparable, and traceable.

??? question "Given that many life sciences ontologies adopt the Basic Formal Ontology (BFO), what motivated the use of UFO rather than BFO as the foundation for this initiative's ontology? (TBD)"

    Not completed before discontinuation.

## Modeling Approach: OntoUML and gUFO

*Questions about the internal modeling framework, layers, and implementation choices.*

**Further reading:**

- [OntoUML overview](ontouml-gufo/ontouml.md)
- [gUFO details](ontouml-gufo/gufo.md)

??? question "What are OntoUML and gUFO, and why are they used?"

    OntoUML is a conceptual modeling language grounded in the foundational ontology named Unified Foundational Ontology (UFO). gUFO is its OWL counterpart, enabling computational use. Together, they ensure semantic precision and machine-actionable models.

    OntoUML operates at MDA's CIM layer to capture conceptual semantics, while gUFO provides a platform-independent OWL implementation at the PIM layer. This ensures a traceable and interoperable flow from conceptualization to deployment.

??? question "What is semantic traceability in this initiative?"

    Semantic traceability is the ability to preserve and inspect how intended meaning is carried across the different layers of the initiative's approach, from the conceptual reference model to its computational implementation and related mapping artifacts.

    In practice, this means that HRIO OntoUML provides the conceptual representation of the intended meanings, while HRIO gUFO/OWL provides the corresponding computational implementation. Mappings from source expressions to HRIO then make it possible to trace how meanings in external artifacts relate to the shared reference model in a controlled and reviewable way.

??? question "OntoUML and gUFO seem very complex. Isn't that a barrier to adoption?"

    This is a common concern. Foundational ontologies like UFO are indeed complex—because they aim to capture real-world meaning with a high level of precision and avoid ambiguity across domains. Some complexity is simply inherent to the task: when we model the real-life elements, especially across institutions or sectors, we cannot always rely on overly simplistic representations.

    That said, this initiative does not require users to engage directly with UFO. Instead, we rely on OntoUML and gUFO to make that foundational theory accessible in practice. OntoUML provides intuitive modeling constructs grounded in UFO, while gUFO offers a lightweight OWL implementation suitable for real-world applications.

    This layered approach lets modelers benefit from UFO's expressive power without being overwhelmed by its formal depth. The complexity is managed by the modeling framework and supported by tools like Visual Paradigm and the OntoUML plugin. In fact, these languages have already been applied successfully in domains like public health, law, and digital humanities—demonstrating that the approach is both practical and scalable.

??? question "How is the OntoUML model converted to OWL?"

    The OntoUML model is exported to OWL using the [gUFO specification](ontouml-gufo/gufo.md) via plugin tooling. The resulting ontology retains the original semantics in a format suitable for Semantic Web technologies.

??? question "What is the difference between OntoUML and gUFO?"

    OntoUML is a conceptual modeling language for humans; gUFO is its OWL-based computational counterpart used in Semantic Web technologies.

## Mapping and Alignment Strategy

*Questions about how external concepts are aligned to the Health-RI reference model using dedicated mapping properties from the Health-RI Mapping Vocabulary.*

**Further reading:**

- [Health-RI Mapping Vocabulary](method/specification-vocabulary.html)
- [Mapping strategy guide](method/mapping-strategy.md)
- [Archived contribution process](contributing/overview.md)

!!! tip "HRIO Mapping Assistant (GPT)"

    Need help drafting a meaning mapping from a schema term (or text concept) to HRIO?

    [Open HRIO Mapping Assistant](https://chatgpt.com/g/g-6990a7e348c4819190ef2de88503ff5e-hrio-mapping-assistant){ .md-button .md-button--primary }

    It proposes exactly **one** HRIV predicate (`hriv:hasExactMeaning` / `hriv:hasBroaderMeaningThan` / `hriv:hasNarrowerMeaningThan`), a **confidence %**, and **evidence snippets** (so you can justify and review the mapping).

    *Archived drafting aid only: always confirm against HRIO docs. There is no active Health-RI review, curation, or release workflow for assistant outputs.*

??? question "How are mappings from source artifacts to the reference model created?"

    Mappings are expressed using the Health-RI Mapping Vocabulary (HRIV) predicates (i.e., HRIV-defined subproperties of `hriv:meaningMappingRelation`).

    In practice, the mapping target is an HRIO meaning, while the source may be a source expression drawn from a standard, local schema, ontology, or related implementation artifact.

    There are two complementary approaches:

    - If a source artifact is outside Health-RI's editorial control, mappings are typically maintained non-invasively in a separate mapping artifact (e.g., a SSSOM mapping set).
    - If a source artifact is under the editorial control of its authors/maintainers (and governance permits), HRIV mapping assertions may be embedded directly in the artifact itself.

    **Historical policy:** mappings produced under the initiative could only target HRIO concepts in packages that were at least at the `erv` (external review) stage. Mapping to concepts in packages at the `int` (internal) or `irv` (internal review) stage was not permitted.

    Mappings can be asserted using:

    - [`hriv:hasExactMeaning`](method/specification-vocabulary.html#hasExactMeaning) when an exact-meaning alignment is justified,
    - [`hriv:hasBroaderMeaningThan`](method/specification-vocabulary.html#hasBroaderMeaningThan) or [`hriv:hasNarrowerMeaningThan`](method/specification-vocabulary.html#hasNarrowerMeaningThan) when exact alignment is not justified, to make the remaining mismatch explicit.

    These mappings support semantic alignment without requiring replacement of source artifacts.

??? question "What is `hriv:hasExactMeaning`, and how is it different from `owl:equivalentClass` or `skos:exactMatch`?"

    `hriv:hasExactMeaning` (a specialized subproperty of `semiotics:expresses`) is used to state that an external concept carries the same intended meaning as a concept in the Health-RI reference model—i.e., the expression's semantics are precisely determined by that meaning. It expresses a strong meaning mapping, but it does not imply logical equivalence.

    - Unlike `owl:equivalentClass`, it does not entail formal logical equivalence and therefore avoids unintended reasoning consequences when integrating ontologies with different logical foundations.
    - Unlike `skos:exactMatch`, which is often used for linking concepts across vocabularies in a looser, less formally grounded way, `hriv:hasExactMeaning` is tied to an explicit semantic grounding in a reference ontology.

    In the OWL implementation, HRIV mapping assertions are not OWL class axioms: they are expressed as object-property assertions between individuals denoting expressions and meanings (with OWL 2 DL punning when class IRIs are used). Therefore, they do not imply `owl:equivalentClass`, `owl:sameAs`, or `rdfs:subClassOf` entailments between the mapped classes. For compatibility with SKOS tooling, corresponding SKOS mapping assertions can be derived, but the HRIV predicate remains the authoritative carrier of the intended meaning.

??? question "Do HRIV mappings imply OWL entailments between external classes (e.g., equivalence or subsumption)?"

    No. HRIV mappings are not OWL class axioms between external classes. They link external concepts to HRIO meanings (and, in OWL 2 DL implementations, rely on punning when class IRIs are used as individuals).

    Once external concepts are linked to HRIO meanings, their relationship can be assessed by inspecting (and querying/reasoning over) HRIO. Any derived cross-standard relationship should be interpreted as a mapping-level assessment grounded in HRIO, not as an OWL DL class-level entailment between the external classes.

??? question "How does HRIV relate to SKOS mapping relations?"

    HRIV mapping relations are aligned via `rdfs:subPropertyOf` to corresponding SKOS mapping relations so Health-RI mappings can participate in SKOS-based tooling and workflows.

    However, the HRIV predicates remain the authoritative carriers of the intended (definitional) semantics: any entailed SKOS mapping assertions should be treated as a derived "SKOS view" for interoperability and discovery, and SKOS-level entailments (e.g., transitivity of `skos:exactMatch`) must not be used to change the intended interpretation of an HRIV mapping.

??? question "Why is there a rule that only one `hriv:hasExactMeaning` is allowed per concept?"

    To avoid semantic ambiguity during curation and downstream interpretation, and to keep exact-meaning mappings function-like. With respect to `hriv:hasExactMeaning`, each source expression may have at most one exact HRIO target.

    This makes exact-meaning mapping behave like a partial many-to-one function: some source expressions may have no exact target yet, while multiple source expressions may share the same HRIO meaning.

    Practically, this is best treated as a curation/validation policy for Health-RI mapping artifacts (rather than an OWL logical constraint): HRIV's use is designed around controlled, consistently interpretable mapping assertions.

??? question "How do I choose between `hriv:hasBroaderMeaningThan` and `hriv:hasNarrowerMeaningThan`?"

    Use `hriv:hasBroaderMeaningThan` when your expression is broader in scope than the HRIO target (it includes the HRIO concept but is not limited to it). Use `hriv:hasNarrowerMeaningThan` when your expression is narrower in scope than the HRIO target (it is limited to a subset of what the HRIO concept covers).

    Examples:

    - Broader-than: "Adult patient" mapped to "Pregnant adult patient" (the expression covers more than the target).
    - Narrower-than: "Left femur fracture" mapped to "Femur fracture" (the expression covers less than the target).

??? question "Is there a tool to help me draft mappings to HRIO?"

    The initiative created the [**HRIO Mapping Assistant (GPT)**](https://chatgpt.com/g/g-6990a7e348c4819190ef2de88503ff5e-hrio-mapping-assistant).

    If it remains accessible, it can help map a domain concept to HRIO by proposing **one** HRIV predicate and a candidate HRIO target, plus a confidence estimate and supporting evidence snippets.

    *Treat the output as an archived draft: always verify the target meaning in HRIO. Assistant outputs do not enter an active Health-RI review, curation, or release workflow.*

??? question "What should I do if no exact match exists between my concept and the Health-RI ontology?"

    If no exact HRIO target is justified, use `hriv:hasBroaderMeaningThan` or `hriv:hasNarrowerMeaningThan` to make the remaining semantic mismatch explicit. These approximate mappings are not failures; they document what can already be aligned and what still differs semantically.

    If you reuse the approach after discontinuation, model refinements or additional concepts must be governed and maintained outside this initiative.

??? question "Can new concepts be added to the Health-RI ontology to improve mapping precision?"

    No new concepts are planned under the discontinued Health-RI Semantic Interoperability Initiative. The published HRIO remains available as an archival artifact.

    When reusing the approach independently, a missing meaning may still justify extending or adapting a reference model, but such work would be outside this initiative and would require separate governance, identifiers, validation, and maintenance.

??? question "Who creates and maintains the semantic mappings to the Health-RI ontology?"

    Mappings were created and maintained by:

    - The Health-RI team, which curated non-invasive mappings using the [SSSOM](https://w3id.org/sssom/) format for public or external ontologies. These mappings remain published externally and do not alter the original third-party ontologies.
    - External partners, who could embed mappings directly in their own ontology files using Health-RI Mapping Vocabulary properties (e.g., `hriv:hasExactMeaning`), especially when they controlled the editorial process of the external artifact.

    The Health-RI initiative no longer maintains or curates these mappings after discontinuation.

## SSSOM Mapping Set

??? question "Is the Health-RI SSSOM Mapping Set manually curated or automatically generated?"

    The released mapping set was manually curated by the Health-RI mapping team with input from external collaborators.

??? question "Where can I download the SSSOM Mapping Set, and in which formats?"

    Use the stable URIs:

    - `https://w3id.org/health-ri/semantic-interoperability/mappings` → TTL
    - `https://w3id.org/health-ri/semantic-interoperability/mappings/ttl` → TTL
    - `https://w3id.org/health-ri/semantic-interoperability/mappings/tsv` → TSV.

??? question "How is the mapping set versioned?"

    The mapping set used date-based versions (YYYY-MM-DD) tied to the publication date, with at most one release per day. The final published release remains available through the documented PIDs.

??? question "Can a published mapping be deleted? How are corrections handled?"

    Under the initiative's publication policy, published mappings were not removed. Revisions were represented by a new record using `replaces` to supersede the old one. Because the initiative is discontinued, known issues in the final mapping set may remain unresolved.

??? question "Which SSSOM fields are mandatory, optional, or system-assigned?"

    Under the initiative's historical workflow, fields were divided by responsibility:

    - Contributor (mandatory) — provided in submissions (e.g., `subject_id`, `predicate_id`, `object_id`, `mapping_justification`, `author_id`, `mapping_date`)
    - Contributor (optional) — added when available
    - Curator — added or verified by Health-RI curators
    - System (Fixed) — constant, not changed
    - System (Generated) — assigned at publication time

??? question "What fields were required when contributing a mapping?"

    At minimum, contributors provided all mandatory fields:
    `subject_id`, `predicate_id`, `object_id`, `mapping_justification`, `author_id`, and `mapping_date`.

    Optional fields could be added when available. System-assigned and curator fields were handled during the review and publication process.

    For the complete specification, see the Mapping Set Schema Reference page.

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

- [Archived contribution process](contributing/overview.md)

!!! warning "Contribution process closed"

    The initiative has been **discontinued**. Contribution channels are retained only as historical documentation; new submissions are not reviewed, curated, or scheduled for release.

??? question "What were the supported ways to contribute a new mapping row?"

    There were two options:

    1. Issue form (preferred) — contributors submitted one SSSOM mapping row per issue.
    2. Excel template — contributors filled in the `mappings` sheet (rows) and the `prefix` sheet (CURIE bindings), then attached the completed XLSX to a GitHub issue.

    These routes are no longer active project intake channels.

??? question "What should contributors have checked before submitting a mapping?"

    The submission checklist required:

    - all mandatory contributor fields to be present and correctly formatted;
    - optional values to use valid identifiers (e.g., ORCID, resolvable URIs, SEMAPV terms); and
    - when pinning a version, `object_source` to be a specific version URI rather than a generic one.

??? question "Can external parties contribute to the modeling or mapping process?"

    During active development, external parties contributed through GitHub Issue forms, community review, and collaboration with the project team. The initiative is now discontinued, so those project contribution workflows are closed.

??? question "How can I contribute to the Health-RI Semantic Interoperability Initiative?"

    The initiative has been discontinued and no longer accepts contributions for review, curation, or integration into project releases. The [contribution pages](contributing/overview.md) remain available as historical documentation.

??? question "Do I need to check the ontology version before submitting a contribution?"

    During active development, contributors were asked to indicate which version of the ontology or artifact they reviewed before submitting a request, especially when reporting issues or suggesting new concepts. This helped establish the context of each submission.

??? question "Where can I find more information on how feedback was submitted?"

    See the archived [Contributing page](contributing/overview.md), which documents the contribution process used during the initiative.

## Ontology Lifecycle and Publishing

*Questions about how the ontology was released, versioned, and maintained over time.*

**Further reading:**

- [Publications & operations](method/publications.md)
- [Ontology versioning](./method/ontology-versioning.md)
- [Validation & stage gates](./method/ontology-validation.md)
- [Persistent identifiers (PIDs)](method/persistent-ids.md)

!!! note "Operational status: discontinued"

    This section documents the initiative's ontology lifecycle, versioning, review, and publication approach. The initiative has been **discontinued**, and these procedures are retained as historical policy rather than an active development or release workflow.

??? question "What are the ontology lifecycle stages (`int`, `irv`, `erv`, `pub`)?"

    - `int` — internal work (drafting, labeling, layout).
    - `irv` — internal review by team members not involved in modeling.
    - `erv` — external review with invited community input.
    - `pub` — published.

    A package's stage described its validation status. GitHub Release creation was related but separate: a GitHub Release could be created when a package entered `erv`, when a package already in `erv` or `pub` was updated, or when a package advanced from `erv` to `pub`.

??? question "Who validated at each stage?"

    - `irv`: independent internal reviewers (not the authors).
    - `erv`: domain and modeling specialists (community call invited participation).

??? question "How long did reviews take?"

    During active development, the target was one sprint for internal and one sprint for external review; either could extend to two depending on scope/availability.

??? question "How was the community involved in external review?"

    During active development, a Call for Community Review was issued when a package entered `erv`; feedback was collected during the external-review sprint.

??? question "What triggered a stage reversion (e.g., `pub → int`) and what happened then?"

    During active development, critical defects or major scope changes could revert a package to `int`; the package then re-passed the stage gates before moving forward again.

??? question "Where can I find the final version of the Health-RI ontology?"

    All published versions are available in the `/ontologies/` folder. The final/latest published release remains accessible via: <https://w3id.org/health-ri/ontology>

??? question "How does versioning work for the ontology (X.Y.Z)?"

    Format: `X.Y.Z` with strict priority `X > Y > Z`. Only one component increments per ontology update; lower components reset.

    Meanings:

    - X — package index: add/remove a package → `X++`; then `Y = 0`, `Z = 0`.
    - Y — stage/semantic: any package stage transition or semantic modeling change → `Y++`; then `Z = 0`.
    - Z — non-semantic: labels/typos, diagram/layout, links/docs, and other non-semantic corrections → `Z++`.

    Rules: no skipping numbers; exactly one single-step bump per ontology update.

    Important: ontology version assignment is separate from GitHub Release creation. GitHub Releases use an already assigned ontology version, but they do not determine whether `X`, `Y`, or `Z` changes.

    Scope: applies to the ontology artifacts versioned together as HRIO; the mapping set and mapping vocabulary are versioned separately.

??? question "What does the 'latest' folder contain after discontinuation?"

    The `ontologies/latest/` folder and the ontology PID resolve to the final available published release. They provide stable access without requiring a version number, but they are not expected to advance under this discontinued initiative.

??? question "How do I cite or refer to the Health-RI initiative and its artifacts?"

    You can use the following Persistent Identifiers (PIDs) to cite the initiative and its semantic artifacts:

    - Initiative-wide identifier: `https://w3id.org/health-ri/semantic-interoperability`
    - Health-RI Ontology: `https://w3id.org/health-ri/ontology`
    - Health-RI SSOM Mapping Set: `https://w3id.org/health-ri/semantic-interoperability/mappings`
    - Health-RI Mapping Vocabulary: `https://w3id.org/health-ri/mapping-vocabulary`

    These PIDs are stable, dereferenceable, and aligned with FAIR principles. They are suitable for use in citations, publications, and metadata records. For reproducibility, prefer versioned PIDs where available.

??? question "What types of files are published with each ontology version?"

    Each published ontology version includes the following artifacts where available:

    - `.vpp`: OntoUML conceptual model (Visual Paradigm project)
    - `.json`: OntoUML export compliant with the OntoUML Schema
    - `.ttl`: OWL ontology (based on gUFO) — only for syntactically valid models
    - `.md`: Human-readable documentation (Markdown)
    - `.html`: Human-readable specification (HTML)
    - `.png`: Diagram images (only in the `latest/` folder)

    These are published under both `ontologies/latest/` (final/latest version) and `ontologies/versioned/` (versioned archive).

??? question "Where can I find the exported images of the ontology diagrams?"

    Exported PNG images of OntoUML diagrams are available in the `ontologies/latest/images/` folder. They correspond to the final/latest published `.vpp` file and were not maintained for previous versions.

??? question "Why is there sometimes no OWL (.ttl) file available for a version?"

    The `.ttl` file (gUFO-compliant OWL ontology) was generated only when the OntoUML model was syntactically valid. Incomplete or draft versions could therefore lack a `.ttl` file.

??? question "Can the latest version of the OWL (.ttl) file correspond to a different version than the latest version of the OntoUML (.json/.vpp) model?"

    Yes. The `.ttl` file was only published for releases where the OntoUML model was syntactically valid and the transformation pipeline completed successfully.
    If the final HRIO release does not include a `.ttl`, the `/ontology/ttl` PID continues to resolve to the latest available `.ttl`, which may correspond to an earlier HRIO version.
    When present, the OWL file includes a `dcterms:conformsTo` triple linking it to the OntoUML artifact version it was derived from.

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

??? question "What's the difference between the latest and versioned ontology URIs?"

    - The latest URI (`https://w3id.org/health-ri/ontology`) resolves to the final available published release under this initiative. It is not expected to advance after discontinuation.
    - A versioned URI (e.g., `https://w3id.org/health-ri/ontology/v2.0.0`) points to a specific, immutable release. Its content will not change, ensuring long-term consistency.

    Use a versioned URI when immutability and reproducibility are important, for example in scientific publications, formal mappings, or regulatory documentation.

??? question "What was the publishing strategy for ontology releases?"

    Ontology versioning and GitHub Release creation were related but distinct.

    The ontology version (`X.Y.Z`) was assigned according to the ontology versioning rules. A GitHub Release was created only when at least one domain package entered `erv`, when a package already in `erv` or `pub` was updated, or when a package advanced from `erv` to `pub`. Changes limited to packages that remained only in `int` or `irv` did not require a GitHub Release.

    When a GitHub Release was created, it used the ontology version already assigned to that repository state; it did not determine the version number itself.

    Publication and dissemination activities associated with a GitHub Release could include:

    - a tagged GitHub Release with release notes and relevant packaged artifacts;
    - an archived snapshot with a DOI, where applicable;
    - artifacts exposed through w3id PIDs and repository folders for latest and versioned access; and
    - catalog and discoverability updates, where applicable.

??? question "How were the OntoUML and gUFO ontologies and the produced semantic mappings maintained over time?"

    During active development, the ontology artifacts were maintained in version-controlled repositories through a structured ontology versioning and publication process. For any given ontology version, the ontology artifacts released as part of HRIO share the same `X.Y.Z` identifier and remain aligned to the same underlying HRIO OntoUML model.

    GitHub Release creation was operationally separate from ontology version assignment. When the conditions for a GitHub Release were met, the repository publication used the ontology version already assigned under the `X`/`Y`/`Z` rules; it did not determine the version number itself.

    The ontology was published in multiple formats and exposed through stable, citable persistent identifiers (PIDs). Validation and publication checks were applied as appropriate before release so that the published artifacts remain transparent, accessible, and semantically traceable across versions.

    Semantic mappings produced within the initiative were also maintained in version-controlled repositories and published in stable forms, but they followed their own versioning and publication rules rather than the ontology's `X.Y.Z` version identifier.

    After discontinuation, these released resources remain archival and are no longer actively maintained by the initiative.

??? question "Will HRIO be modularized into separate ontology modules?"

    No further modularization is planned under the discontinued initiative. The released ontology artifacts retain the coordinated HRIO structure and versioning used at the time of publication.

??? question "Who is responsible for maintaining the ontology and its associated mappings?"

    The Health-RI team was responsible for the core ontologies and mappings produced within the initiative. The initiative has now been discontinued, so active maintenance, review, curation, and integration are no longer planned.

??? question "How were the solutions maintained and supported?"

    The ontology was maintained through version-controlled ontology updates, staged validation, publication-stage operations, and issue-based feedback.

    After a package reached `pub`, the Publication Stage Operations Checklist continued to apply while the package remained in `pub`. GitHub Releases were not limited to `pub`: they could also be created when a package entered `erv`, when a package already in `erv` or `pub` was updated, or when a package advanced from `erv` to `pub`.

    Publication-stage operations could include:

    - Release and preservation: create or update the GitHub Release as required, preserve the released state, and record the DOI-backed archive where applicable.
    - Catalog and discoverability: update the OntoUML/UFO Catalog, upload the package report to the repository where applicable, and announce publication-related updates and follow-ups.
    - Academic publication (optional): consider a peer-reviewed venue and, when accepted, add the formal citation and publisher DOI to the documentation and release materials.

    These operational support activities ended with discontinuation. Existing released resources remain available as archival materials.

??? question "What happened right after a package was published (`pub`)?"

    When a package advanced from `erv` to `pub`, it became formally published. While remaining in `pub`, publication-stage operations were completed or updated as appropriate.

    These could include:

    - creating or updating the GitHub Release for the relevant ontology version, where required;
    - preserving the released state (e.g., DOI-backed archive);
    - updating catalogs and other discoverability channels; and
    - posting publication-related announcements and follow-ups.

    Note: GitHub Release activity was not exclusive to `pub`; it could also occur earlier when a package entered `erv` or when packages already in `erv` or `pub` were updated.

??? question "How was the ontology tested and accepted?"

    Acceptance was tied to passing the stage gate checklists:

    - `int → irv` gate (author self-check + modeling/diagram/metadata readiness).
        Entry into `irv` happened only after all Internal Stage Gate items passed.
    - `irv → erv` gate (independent internal review).
        Reviewers executed the Internal Review Stage Gate; evidence was recorded in the review issue.
    - `erv → pub` outcome (independent external review).
        When the package passed external review, the modeler recorded `<erv → pub>`; then the Publication Stage Operations Checklist was executed while remaining in `pub`.

    Timelines: during active development, internal and external reviews were planned as sprint activities; the target was one sprint, optionally extended to two depending on scope and availability.
    Substantive defects or scope changes at any stage could revert the package to `int` for rework; advancement then followed the same gates again.

??? question "Where can I find an overview of all persistent identifiers provided by the initiative?"

    The initiative documentation contains a consolidated table of PIDs covering the ontology, mapping set, and mapping vocabulary. See [Persistent Identifiers](method/persistent-ids.md).

??? question "How do persistent identifiers (w3id) work in this project?"

    Persistent identifiers (PIDs) are used throughout the initiative to provide stable, dereferenceable URIs that link to project resources (e.g., OntoUML models, documentation). These PIDs resolve via content negotiation, meaning they can return different formats (e.g., HTML, Markdown, or Turtle) based on how the link is accessed. The system selects the best format automatically or, in some cases, forwards you to the initiative's GitHub repository or documentation site.

    After discontinuation, unversioned or `latest` PIDs resolve to the final available published artifacts and are not expected to advance under this initiative. Versioned PIDs remain the preferred references for reproducibility.
