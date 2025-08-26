# Frequently Asked Questions (FAQ)

## Project Overview and Strategic Context

*Questions about the initiative’s purpose, strategic goals, expected impact, and broader context.*

!!! warning "Disclaimer"
    The answers in this section are part of an ongoing effort to address strategic questions about the initiative. They are based on initial interpretations and should be used with caution. All entries are marked as **drafts** and will be further refined and validated in collaboration with stakeholders.

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
    The development of the OntoUML conceptual model, its implementation as the gUFO OWL ontology, and the strategy for semantically aligning third-party ontologies using [Health-RI Mapping Vocabulary](../method/specification.html) properties are all concrete milestones achieved. Figures and examples in the documentation illustrate successful alignment strategies already in use.

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

    [Read more.](../method/)

??? question "How does this initiative relate to the FAIR principles?"
    It supports the 'I' in FAIR—Interoperability—by grounding vocabularies and schemas in shared ontologies and ontological commitments.
    [Learn more](../semantic-interoperability/)

??? question "What are the main components of the approach?"
    - OntoUML conceptual modeling
    - gUFO OWL-based computational ontologies
    - Schema-to-ontology mappings using tools like SSSOM

    [Read more.](../method)

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

??? question "What are OntoUML and gUFO, and why are they used?"
    OntoUML is a conceptual modeling language grounded in the foundational ontology named Unified Foundational Ontology (UFO). gUFO is its OWL counterpart, enabling computational use. Together, they ensure semantic precision and machine-actionable models.

    OntoUML operates at MDA's CIM layer to capture conceptual semantics, while gUFO provides a platform-independent OWL implementation at the PIM layer. This ensures a traceable and interoperable flow from conceptualization to deployment.

    [OntoUML overview](../ontouml-gufo/ontouml) • [gUFO details](../ontouml-gufo/gufo)

??? question "OntoUML and gUFO seem very complex. Isn’t that a barrier to adoption?"
    This is a common concern. Foundational ontologies like UFO are indeed complex—because they aim to capture real-world meaning with a high level of precision and avoid ambiguity across domains. Some complexity is simply inherent to the task: when we model the real-life elements, especially across institutions or sectors, we cannot always rely on overly simplistic representations.

    That said, this initiative does not require users to engage directly with UFO. Instead, we rely on OntoUML and gUFO to make that foundational theory accessible in practice. OntoUML provides intuitive modeling constructs grounded in UFO, while gUFO offers a lightweight OWL implementation suitable for real-world applications.

    This layered approach lets modelers benefit from UFO’s expressive power without being overwhelmed by its formal depth. The complexity is managed by the modeling framework and supported by tools like Visual Paradigm and the OntoUML plugin. In fact, these languages have already been applied successfully in domains like public health, law, and digital humanities—demonstrating that the approach is both practical and scalable.

??? question "How is the OntoUML model converted to OWL?"
    The OntoUML model is exported to OWL using the gUFO specification via plugin tooling. The resulting ontology retains the original semantics in a format suitable for Semantic Web technologies.
    [More info.](../ontouml-gufo/gufo)

??? question "What is the difference between OntoUML and gUFO?"
    OntoUML is a conceptual modeling language for humans; gUFO is its OWL-based computational counterpart used in Semantic Web technologies.
    [OntoUML](../ontouml-gufo/ontouml) • [gUFO](../ontouml-gufo/gufo)

## Mapping and Alignment Strategy

*Questions about how external concepts are aligned to the Health-RI reference model using dedicated mapping properties from the [Health-RI Mapping Vocabulary](../method/specification.html).*

??? question "How are mappings from local schemas to the reference model created?"
    If schemas are OWL/RDF-based, mappings can be embedded directly using standard RDF properties. Otherwise, external mappings are created using [SSSOM](https://mapping-commons.github.io/sssom/).

    Mappings follow the [Health-RI Mapping Vocabulary](../method/specification.html) and can be asserted using:

    - [`hriv:hasExactMeaning`](../method/specification.html#hasExactMeaning) for perfect semantic alignment (only one allowed),
    - [`hriv:hasBroaderMeaningThan`](../method/specification.html#hasExactMeaning) or [`hriv:hasNarrowerMeaningThan`](../method/specification.html#hasExactMeaning) when the match is approximate.

    These mappings support semantic alignment without requiring modification to the original schema and are managed either by Health-RI (non-invasively in SSSOM) or by partners (embedded in their own RDF models).

    [Full explanation](../method/mapping-strategy)

??? question "What is `hriv:hasExactMeaning`, and how is it different from `owl:equivalentClass` or `skos:exactMatch`?"
    `hriv:hasExactMeaning` (equivalent to `semiotics:expresses`) is used to state that an external concept carries the same intended meaning as a concept in the Health-RI reference model. It expresses a strong semantic alignment in terms of **shared meaning**, but it does not imply logical equivalence.

    - Unlike `owl:equivalentClass`, it does not entail formal logical equivalence and therefore avoids unintended reasoning consequences when integrating ontologies with different logical foundations.
    - Unlike `skos:exactMatch`, which is often used for linking concepts across vocabularies in a looser, less formally grounded way, `hriv:hasExactMeaning` is tied to an explicit semantic grounding in a reference ontology. This makes it more precise for interoperability scenarios where meaning—not logical entailment—is the key requirement.

    In summary, `hriv:hasExactMeaning` is intended for strong semantic alignment without the risks of logical overcommitment (`owl:equivalentClass`) or the potential ambiguity of generic lexical alignment (`skos:exactMatch`).

??? question "Why is there a rule that only one `hriv:hasExactMeaning` is allowed per concept?"
    To avoid semantic ambiguity. Allowing multiple `hriv:hasExactMeaning` assertions for the same concept would imply conflicting definitions and hinder consistent interpretation. Each external concept must match only one Health-RI concept with perfect equivalence.

??? question "What should I do if no exact match exists between my concept and the Health-RI ontology?"
    If your concept is broader or narrower than any existing reference concept, use `hriv:hasBroaderMeaningThan` or `hriv:hasNarrowerMeaningThan` accordingly. These mappings allow approximate alignment. You are also encouraged to contact the Health-RI team to propose additions to the reference model to enable more precise mappings in the future ([read more.](../contributing)).

??? question "Can new concepts be added to the Health-RI ontology to improve mapping precision?"
    Yes. When `hriv:hasExactMeaning` cannot be used due to missing concepts, we encourage you to contact the Health-RI modeling team ([read more.](../contributing)).

    If justified, new intermediate concepts may be added to the reference ontology. This helps replace approximate mappings (`hriv:hasBroaderMeaningThan`, `hriv:hasNarrowerMeaningThan`) with exact ones and ensures better semantic precision for reasoning, integration, and long-term alignment.

    [See example](../method/mapping-strategy)

??? question "Who can create or host the semantic mappings?"
    Mappings can be authored by:

    - **Health-RI** (non-invasive, published in SSSOM format), for public or external ontologies;
    - **External partners**, by embedding `hriv:hasExactMeaning*` statements directly in their ontology files, especially when they control the editorial process of the external artifact.

??? question "Can I request new reference concepts if needed for mapping?"
    Yes. If you find that no suitable concept exists in the Health-RI ontology to match yours, you can propose new reference concepts. These requests are welcome and reviewed by the modeling team. If accepted, new concepts may be added to enable stronger mappings in the future.

??? question "Who creates and maintains the semantic mappings to the Health-RI ontology?"
    Mappings can be created and maintained by:

    - The **Health-RI team**, which curates non-invasive mappings using the [SSSOM](https://w3id.org/sssom/) format. These mappings are published externally and do not alter the original third-party ontologies.
    - **External partners**, who can embed mappings directly in their own ontology files using [Health-RI Mapping Vocabulary](../method/specification.html) properties (e.g., `hriv:hasExactMeaning`).

    [Read more.](../method/mapping-strategy)

## SSSOM Mapping Set

??? question "Is the Health-RI SSSOM Mapping Set manually curated or automatically generated?"
    It is **manually curated** by the Health-RI mapping team with input from external collaborators.

??? question "Where can I download the SSSOM Mapping Set, and in which formats?"
    Use the stable URIs:

    - `https://github.com/Health-RI/semantic-interoperability/mappings` → TTL
    - `https://github.com/Health-RI/semantic-interoperability/mappings/ttl` → TTL
    - `https://github.com/Health-RI/semantic-interoperability/mappings/tsv` → TSV.

??? question "How is the mapping set versioned?"
    The mapping set uses date-based versions (YYYY-MM-DD) tied to the publication date, with at most one release per day.

??? question "Can a published mapping be deleted? How are corrections handled?"
    Published mappings **cannot be removed**. To revise an entry, create a new record that uses `replaces` to supersede the old one; the system will automatically add the corresponding `isReplacedBy` link to the replaced record at publication time.

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
    Yes. Most mappings are positive, where you state that two concepts are related. But sometimes you may want to explicitly say that a mapping should **not** hold. For that, use the field `predicate_modifier` with the value `Not`. If your mapping is positive, just leave this field empty.

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

??? question "What are the supported ways to contribute a new mapping row?"
    There are two options:

    1) **Issue form (preferred)** — submit the SSSOM mapping issue form for a single row.
    2) **Excel template** — fill in the `mappings` sheet (rows) and the `prefix` sheet (CURIE bindings) in the [provided XLSX](https://raw.githubusercontent.com/Health-RI/semantic-interoperability/refs/heads/main/resources/mappings_template.xlsx), then attach it to a new issue.
    In the template, headers for mandatory fields are black, and optional ones are green. Both methods are curator-reviewed and integrated into the official mapping set.

??? question "What should I check before submitting a mapping?"
    Use the submission checklist:

    - All mandatory contributor fields are present and correctly formatted.
    - Optional values (if any) use valid identifiers (e.g., ORCID, resolvable URIs, SEMAPV terms).
    - If you pin a version, ensure `object_source` is a specific version URI (not a generic one).

## Ontology Lifecycle and Publishing

*Questions about how the ontology is released, versioned, and maintained over time.*

??? question "Where can I find the latest version of the Health-RI ontology?"
    All published versions are available in the `/ontologies/` folder. The most recent major release is always accessible via: <https://w3id.org/health-ri/ontology>

    [More on versioning](../method/publications)

??? question "What is the difference between major, minor, and patch versions in your versioning policy?"
    We follow an adapted semantic versioning scheme: `<major>.<minor>.<patch>`.
    - **Major** versions mark conceptual milestones or structural overhauls and are considered stable and citable.
    - **Minor** versions include scoped improvements that preserve semantic compatibility.
    - **Patch** versions address fixes or clarifications without modifying the established scope.
    Only major versions trigger a formal release and a published specification.

    [Read more.](../method/publications)

??? question "What does the 'latest' folder contain and how is it maintained?"
    The `ontologies/latest/` folder and the [ontology's PID](https://w3id.org/health-ri/ontology) always resolves to the most recent available release.
    They provides stable access to the most recent files without needing to specify a version number.
    Each new release automatically updates the `latest/` folder and the file related to the ontology's PID to target the latest content.

??? question "How do I cite or refer to the Health-RI initiative and its artifacts?"
    You can use the following persistent identifiers (PIDs) to cite the initiative and its semantic artifacts:

    - **Initiative-wide identifier**: `https://w3id.org/health-ri/semantic-interoperability`
    - **Health-RI Ontology**: `https://w3id.org/health-ri/ontology`
    - **Health-RI SSOM Mapping Set**: `https://w3id.org/health-ri/semantic-interoperability/mappings`
    - **Health-RI Mapping Vocabulary**: `https://w3id.org/health-ri/mapping-vocabulary`

    These PIDs are stable, dereferenceable, and aligned with FAIR principles. They are suitable for use in citations, publications, and metadata records.

    [Read more.](../method/permanent-ids)

??? question "What types of files are published with each ontology version?"
    Each ontology version includes the following artifacts:

    - `.vpp`: OntoUML conceptual model (Visual Paradigm project)
    - `.json`: OntoUML export compliant with the OntoUML Schema
    - `.ttl`: OWL ontology (based on gUFO) — only for syntactically valid models
    - `.md`: Human-readable documentation (Markdown)
    - `.html`: Human-readable specification (HTML)
    - `.png`: Diagram images (only in the `latest/` folder)

    These are published under both `ontologies/latest/` (most recent version) and `ontologies/versioned/` (versioned archive).
    [More details here.](../method/publications)

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

    [Details here.](../method/permanent-ids)

??? question "What’s the difference between the latest and versioned ontology URIs?"
    - The **latest URI** (`https://w3id.org/health-ri/ontology`) always points to the most recent stable release. Its content may change over time as new versions are published.
    - A **versioned URI** (e.g., `https://w3id.org/health-ri/ontology/v2.0.0`) points to a specific, immutable release. Its content will never change, ensuring long-term consistency.

    Use the **versioned URI** when immutability is essential — for example, in scientific publications, formal mappings, or regulatory documentation. This guarantees that your references always point to the same version of the ontology.

    Use the **latest URI** when you want to stay aligned with the most up-to-date ontology version and future improvements.

    [More info](../method/permanent-ids)

??? question "Which URI should I use in my mapping: the latest or a versioned one?"
    Use the **latest URI** (e.g., `https://w3id.org/health-ri/ontology#HealthcarePatient`) when:

    - You want to always point to the most up-to-date definition.
    - Your use case allows future updates without breaking dependencies.

    Use the **versioned URI** (e.g., `https://w3id.org/health-ri/ontology/v2.0.0#HealthcarePatient`) when:

    - You need traceability and reproducibility (e.g., publications, data provenance).
    - You want to avoid semantic drift caused by future updates.

    [Best practices.](../method/permanent-ids)

??? question "What is the publishing strategy for ontology releases?"
    A fast versioning strategy is adopted, where only major versions are considered stable and published with full documentation. Minor/patch versions are published for collaboration and traceability.
    [More info.](../method/publications)

??? question "How are the OntoUML and gUFO ontologies and the produced semantic mappings maintained over time?"
    Ontologies and semantic mappings are maintained in version-controlled repositories and released through a structured publishing pipeline. Each release is assigned a permanent, citable URL, with both a persistent identifier (PURL) and a timestamped version. Ontologies are published in multiple formats (e.g., RDF/Turtle, JSON) and validated prior to release. This process ensures transparency, long-term accessibility, and semantic stability across versions.
    [Read more.](../method/publications)

??? question "Who is responsible for maintaining the ontology and its associated mappings?"
    The Health-RI team is responsible for maintaining the core ontologies and mappings produced within the initiative. This work is carried out in close collaboration with external partners who contribute ideas, suggestions, and mappings. Contributions are reviewed and integrated through a structured, version-controlled process.
    [Read more.](../contributing)

??? question "How will the new solutions be maintained and supported? (TBD)"
    TBD.

??? question "How will the solution be tested and accepted? (TBD)"
    TBD.

??? question "Where can I find an overview of all persistent identifiers provided by the initiative?"
    The initiative maintains a consolidated table of all PIDs, covering the ontology, mapping set, and mapping vocabulary.  
    This table describes the behavior of each PID (e.g., redirects, format-specific access) and provides examples.  

    [See the full overview.](../method/permanent-ids)

### Community Contributions and Feedback

*Questions about how users can provide input, report issues, or contribute to the ontology and mappings.*

??? question "Can external parties contribute to the modeling or mapping process?"
    Yes. External contributions are welcome and encouraged.

    Community members can submit suggestions, error reports, or collaboration proposals directly via our [GitHub Issue Forms](https://github.com/health-ri/semantic-interoperability/issues/new/choose).

    Available contribution types include:

    - Reporting errors or inconsistencies in the OntoUML/gUFO models
    - Proposing new ontology concepts
    - Suggesting improvements to documentation or mappings
    - Proposing example use cases or general feedback

    For details, visit the [Contributing page.](../contributing/).

??? question "How can I contribute to the Health-RI Semantic Interoperability Initiative?"
    You can contribute by submitting structured feedback using one of our GitHub Issue Forms. We currently support the following contribution types:

    - **Report an error** in the OntoUML or gUFO-based ontology
    - **Request a new concept** to be added to the reference model
    - **Submit other input** such as documentation improvements, mapping suggestions, or collaboration proposals

    Start here: [Contribute via GitHub](https://github.com/health-ri/semantic-interoperability/issues/new/choose)
    Or visit our [Contributing page](../contributing/) for more guidance.

??? question "Do I need to check the ontology version before submitting a contribution?"
    Yes, we ask contributors to indicate which version of the ontology or artifact they reviewed before submitting a request — especially when reporting issues or suggesting new concepts.

    This helps us avoid duplicates, understand the context of your feedback, and keep the review process efficient.

    You’ll find a field for this information in the contribution forms.

??? question "Where can I find more information on how to submit feedback?"
    See our [Contributing page](../contributing/), which outlines how to submit structured input, what types of feedback are accepted, and how your suggestions will be reviewed.

    All community input is tracked as GitHub Issues and reviewed by the modeling and coordination teams.
