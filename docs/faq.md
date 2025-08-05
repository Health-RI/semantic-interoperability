# Frequently Asked Questions (FAQ)

!!! warning
    This page's content is still under review and may contain inaccuracies or omissions. Users are advised to interpret and apply the content with caution.

## Project Overview and Strategic Context

*Questions about the initiative’s purpose, strategic goals, expected impact, and broader context.*

??? question "What is the goal of Health-RI’s semantic interoperability initiative?"
    To enable meaningful data integration across health and life sciences institutions by aligning data semantically, not just structurally. This is achieved through the development and adoption of a common reference model that captures domain meaning explicitly.

??? question "What exactly are we trying to achieve with semantic interoperability?"
    We aim to align external and internal ontologies to a shared reference model, ensuring that semantic definitions are preserved across conceptual and computational layers. This is achieved through structured mappings (e.g., `skos:exactMatch`) from third-party concepts to Health-RI’s authoritative conceptual model (OntoUML) and its computational counterpart (gUFO).

??? question "Why is semantic interoperability important in healthcare and life sciences?"
    Because it ensures that data from diverse sources is interpreted consistently, reducing the risk of misinterpretation and improving reusability, reproducibility, and trust. It supports FAIR data practices and accelerates data-driven innovation.

??? question "What problem is this initiative addressing?"
    It addresses the issue of inconsistent data semantics across institutions, which leads to errors, false agreement, and limited reuse. Many systems use similar terms but with different meanings, or different terms for the same concept.

??? question "What does success look like for this project?"
    Success means having a robust reference model (OntoUML) and executable OWL artifacts (gUFO) in place, with external ontologies semantically aligned through precise mappings. It also includes supporting community contributions, replacing approximate mappings (e.g., `skos:narrowMatch`) with exact ones where possible, and continuously refining the model to bridge semantic gaps.

??? question "Who will benefit from or use the developed solutions?"
    Researchers, clinicians, developers, and data stewards who need to align datasets from different systems and institutions while preserving domain meaning.

??? question "Are there any external collaborators or partner organizations? (TBD)"
    TBD.

??? question "What is the current situation regarding data interoperability in the Netherlands? (TBD)"
    TBD.

??? question "How do current systems or processes work without semantic alignment?"
    Without semantic alignment, systems may use the same term for different concepts or different terms for the same concept, causing ambiguity and inconsistency.

??? question "What are some examples of current successes or progress?"
    The development of the OntoUML conceptual model, its implementation as the gUFO OWL ontology, and the strategy for semantically aligning third-party ontologies using SKOS mapping are all concrete milestones achieved. Figures and examples in the documentation illustrate successful alignment strategies already in use.

??? question "What challenges are currently being faced?"
    One challenge is when no exact match exists between external concepts and the reference ontology. This requires approximate mappings and motivates the need to expand the Health-RI ontology to bridge gaps. Another challenge is managing transitivity and ambiguity in mappings (e.g., limiting to a single `skos:exactMatch` per concept).

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

    [Read more](../method/)

??? question "How does this initiative relate to the FAIR principles?"
    It supports the 'I' in FAIR—Interoperability—by grounding vocabularies and schemas in shared ontologies and ontological commitments.
    [Learn more](../semantic-interoperability/)

??? question "What are the main components of the approach?"
    - OntoUML conceptual modeling
    - gUFO OWL-based computational ontologies
    - Schema-to-ontology mappings using tools like SSSOM
    [Read more](../method/#toward-a-solution-introducing-a-common-reference-model)

## Modeling Approach: OntoUML and gUFO

*Questions about the internal modeling framework, layers, and implementation choices.*

??? question "What are OntoUML and gUFO, and why are they used?"
    OntoUML is a conceptual modeling language grounded in formal ontology (UFO). gUFO is its OWL counterpart, enabling computational use. Together, they ensure semantic precision and machine-actionable models.

    OntoUML operates at MDA's CIM layer to capture conceptual semantics, while gUFO provides a platform-independent OWL implementation at the PIM layer. This ensures a traceable and interoperable flow from conceptualization to deployment.

    [OntoUML overview](../ontouml-gufo/ontouml/) • [gUFO details](../ontouml-gufo/gufo/)

??? question "How is the OntoUML model converted to OWL?"
    The OntoUML model is exported to OWL using the gUFO specification via plugin tooling. The resulting ontology retains the original semantics in a format suitable for Semantic Web technologies.
    [More info](../ontouml-gufo/gufo/)

??? question "What is the difference between OntoUML and gUFO?"
    OntoUML is a conceptual modeling language for humans; gUFO is its OWL-based computational counterpart used in Semantic Web technologies.
    [OntoUML](../ontouml-gufo/ontouml/) • [gUFO](../ontouml-gufo/gufo/)

## Mapping and Alignment Strategy

*Questions about how external concepts are aligned to the Health-RI reference model using SKOS and related mapping techniques.*

??? question "How are mappings from local schemas to the reference model created?"
    If schemas are OWL/RDF-based, mappings can be embedded directly using standard RDF properties. Otherwise, external mappings are created using [SSSOM](https://mapping-commons.github.io/sssom/).

    Mappings follow SKOS standards and can be asserted using:
    - `skos:exactMatch` for perfect semantic alignment (only one allowed),
    - `skos:broadMatch` or `skos:narrowMatch` when the match is approximate.

    These mappings support semantic alignment without requiring modification to the original schema and are managed either by Health-RI (non-invasively in SSSOM) or by partners (embedded in their own RDF models).

    [Full explanation](../method/#mapping-schemas-to-the-gufo-ontology)

??? question "What is `skos:exactMatch`, and how is it different from `owl:equivalentClass`?"
    `skos:exactMatch` indicates strong semantic similarity between two concepts across different ontologies, but it does not imply logical equivalence. Unlike `owl:equivalentClass`, it avoids unintended reasoning consequences and is safer for linking ontologies with different logical foundations.

??? question "Why is there a rule that only one `skos:exactMatch` is allowed per concept?"
    To avoid semantic ambiguity. Allowing multiple `skos:exactMatch` assertions for the same concept would imply conflicting definitions and hinder consistent interpretation. Each external concept must match only one Health-RI concept with perfect equivalence.

??? question "What should I do if no exact match exists between my concept and the Health-RI ontology?"
    If your concept is broader or narrower than any existing reference concept, use `skos:broadMatch` or `skos:narrowMatch` accordingly. These mappings allow approximate alignment. You are also encouraged to contact the Health-RI team to propose additions to the reference model to enable more precise mappings in the future.

??? question "Who can create or host the semantic mappings?"
    Mappings can be authored by:
    - **Health-RI** (non-invasive, published in SSSOM format), for public or external ontologies;
    - **External partners**, by embedding `skos:*Match` statements directly in their ontology files, especially when they control the editorial process of the external artifact.

??? question "Can I request new reference concepts if needed for mapping?"
    Yes. If you find that no suitable concept exists in the Health-RI ontology to match yours, you can propose new reference concepts. These requests are welcome and reviewed by the modeling team. If accepted, new concepts may be added to enable stronger mappings in the future.

## Ontology Lifecycle and Publishing

*Questions about how the ontology is released, versioned, and maintained over time.*

??? question "Where can I find the latest version of the Health-RI ontology?"
    All published versions are available in the `/ontologies/` folder. The most recent major release is always accessible via:
    <https://w3id.org/health-ri/ontology/latest>
    [More on versioning](../ontology/publishing/#versioning-policy)

??? question "What artifacts are published with each ontology release?"
    Each release includes:
    - OntoUML `.vpp` and `.json` files
    - OWL `.ttl` file
    - Diagram images
    - A versioned changelog and archive
    [Details here](../ontology/publishing/#published-artifacts)

??? question "What is the publishing strategy for ontology releases?"
    A fast versioning strategy is adopted, where only major versions are considered stable and published with full documentation. Minor/patch versions are published for collaboration and traceability.
    [More info](../ontology/publishing/#versioning-policy)

??? question "How will the new solutions be maintained and supported? (TBD)"
    TBD.

??? question "How will the solution be tested and accepted? (TBD)"
    TBD.

## Community Contributions and Feedback

*Questions about how users can provide input, report issues, or contribute to the ontology and mappings.*

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
