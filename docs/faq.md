# Frequently Asked Questions (FAQ)

!!! warning
    This page's content is still under review and may contain inaccuracies or omissions. Users are advised to interpret and apply the content with caution.

## Project Overview and Strategic Context

??? question "What is the goal of Health-RI’s semantic interoperability initiative?"
    To enable meaningful data integration across health and life sciences institutions by aligning data semantically, not just structurally. This is achieved through the development and adoption of a common reference model that captures domain meaning explicitly.

??? question "What exactly are we trying to achieve with semantic interoperability? (TBD)"
    TBD.

??? question "Why is semantic interoperability important in healthcare and life sciences?"
    Because it ensures that data from diverse sources is interpreted consistently, reducing the risk of misinterpretation and improving reusability, reproducibility, and trust. It supports FAIR data practices and accelerates data-driven innovation.

??? question "What problem is this initiative addressing?"
    It addresses the issue of inconsistent data semantics across institutions, which leads to errors, false agreement, and limited reuse. Many systems use similar terms but with different meanings, or different terms for the same concept.

??? question "What does success look like for this project? (TBD)"
    TBD.

??? question "Who will benefit from or use the developed solutions?"
    Researchers, clinicians, developers, and data stewards who need to align datasets from different systems and institutions while preserving domain meaning.

??? question "Are there any external collaborators or partner organizations? (TBD)"
    TBD.

??? question "What is the current situation regarding data interoperability in the Netherlands? (TBD)"
    TBD.

??? question "How do current systems or processes work without semantic alignment? (TBD)"
    TBD.

??? question "What are some examples of current successes or progress? (TBD)"
    TBD.

??? question "What challenges are currently being faced? (TBD)"
    TBD.

??? question "What risks and limitations should be considered? (TBD)"
    TBD.

??? question "What assumptions are being made during development? (TBD)"
    TBD.

??? question "What changes are expected in the future? (TBD)"
    TBD.

??? question "How might the future process or system improve data use across institutions? (TBD)"
    TBD.

??? question "What changes will users experience? (TBD)"
    TBD.

??? question "What is the common reference model and why is it needed?"
    It’s a conceptual model created using OntoUML to serve as a semantic anchor for all participating data schemas. Instead of replacing local schemas, it provides a shared foundation for mapping and aligning meaning.
    [Read more](../method/)

??? question "How does this initiative relate to the FAIR principles?"
    It supports the 'I' in FAIR—Interoperability—by grounding vocabularies and schemas in shared ontologies and ontological commitments.
    [Learn more](../semantic-interoperability/)

??? question "What are the main components of the approach?"
    - OntoUML conceptual modeling
    - gUFO OWL-based computational ontologies
    - Schema-to-ontology mappings using tools like SSSOM
    [Read more](../method/#toward-a-solution-introducing-a-common-reference-model)

??? question "What are OntoUML and gUFO, and why are they used?"
    OntoUML is a conceptual modeling language grounded in formal ontology (UFO). gUFO is its OWL counterpart, enabling computational use. Together, they ensure semantic precision and machine-actionable models.
    [OntoUML overview](../ontouml-gufo/ontouml/) • [gUFO details](../ontouml-gufo/gufo/)

## Technical Implementation and Adoption

??? question "How is the OntoUML model converted to OWL?"
    The OntoUML model is exported to OWL using the gUFO specification via plugin tooling. The resulting ontology retains the original semantics in a format suitable for Semantic Web technologies.
    [More info](../ontouml-gufo/gufo/)

??? question "What is the difference between OntoUML and gUFO?"
    OntoUML is a conceptual modeling language for humans; gUFO is its OWL-based computational counterpart used in Semantic Web technologies.
    [OntoUML](../ontouml-gufo/ontouml/) • [gUFO](../ontouml-gufo/gufo/)

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

??? question "How are mappings from local schemas to the reference model created?"
    If schemas are OWL/RDF-based, mappings can be embedded directly using standard RDF properties. Otherwise, external mappings are created using [SSSOM](https://mapping-commons.github.io/sssom/).
    [Full explanation](../method/#mapping-schemas-to-the-gufo-ontology)

??? question "How will the new solutions be maintained and supported? (TBD)"
    TBD.

??? question "How will the solution be tested and accepted? (TBD)"
    TBD.

??? question "Can external parties contribute to the modeling or mapping process?"
    Yes. Collaboration is encouraged through feedback, schema alignment, and domain expert engagement. Please contact the coordination team if you would like to be involved.
