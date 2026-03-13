# Method Overview

## Current Situation

<!-- TODO: Update this image, removing the "nodes" concept. -->

![Current Situation](./assets/images/Picture1.png)
*Figure 1. Fragmented cross-institutional schemas and pairwise mappings in the current situation.*

!!! note

    Figure 1 may contain legacy terminology (e.g., "nodes"). Interpret it as referring to data sources/schemas and their mappings.

Across the health and life sciences, data producers and consumers often need to publish and consume data across institutions and systems. However, for this data exchange to be meaningful and analytically reliable, the data must be interpreted consistently and correctly by all parties involved.[^1][^2] In practice, achieving this often relies on manual, case-by-case mappings across heterogeneous standards and local schemas, which is technically complex, time-consuming, and error-prone.[^3][^4]

!!! note

    In this page, "schema" is used broadly to include local database schemas as well as standard-level models (e.g., FHIR, OMOP, openEHR) and RDF/OWL artifacts used for exchange.

Addressing this challenge requires moving beyond structural or syntactic alignment. What is needed is semantic interoperability—a shared understanding of the meaning behind the data being exchanged.[^3][^4][^5] Otherwise, systems may appear to agree because they use the same terms or data structures, while still committing to different conceptualizations. Such a situation can lead to [*false agreement*](../semantic-interoperability/index.md).[^6][^7]

As illustrated in Figure 1, each institution maintains its own data schema and data repository, often resulting in fragmented data silos. These schemas often vary significantly in structure, terminology, and the standards or assumptions they follow.[^3][^4][^8][^9][^10] In practice, several challenges arise:

- Some schemas adhere to formal standards, while others are informally defined by the data authors themselves.[^4][^10]
- A single schema might be influenced by multiple standards, each introducing different terminologies or modeling assumptions.[^4][^8]
- Documentation is often incomplete or ambiguous, which leads to misunderstandings and misinterpretation when data is exchanged between institutions.[^4][^8]
- Mappings and transformations are often specified at the level of implementation artifacts (schemas and their structures), leaving underlying conceptualizations and meaning-level relations implicit.[^11][^7]
- Similar labels, codes, textual definitions, or even OWL axioms are not sufficient to guarantee shared meaning when ontological commitments remain implicit.[^6][^7]

This lack of clear, shared semantics introduces significant barriers to data integration and analysis. It increases the risk of misinterpretation, reduces confidence in the data, and ultimately limits reuse and impact.[^1][^3][^9]

!!! warning

    Shared labels, codes, or even similar OWL patterns do not guarantee shared meaning. Apparent agreement can hide genuine semantic misalignment ("false agreement"), so mappings must make their intended ontological commitments explicit and reviewable.[^12][^7]

To address these challenges and ensure semantic alignment across institutions and systems, we propose a new approach centered around a common semantic reference model: the Health-RI Ontology (HRIO).[^11][^12]

## Toward a Solution: Introducing a Common Semantic Reference Model

Rather than relying on isolated and potentially ambiguous schemas, we propose the creation of a common semantic reference model—the Health-RI Ontology, or simply HRIO—to serve as a shared semantic foundation across institutions and systems.[^11][^12]

HRIO is not intended to replace local schemas. Instead, it will serve as a semantic anchor: each schema will be expected to explicitly declare how its elements correspond to the concepts in HRIO, clarifying their intended meaning and enabling consistent interpretation.[^12][^11]

!!! note

    In practice, schemas do not need to be restructured or rewritten. Rather, they must be mapped to HRIO—declaring, for each concept, its corresponding concept (or the nature of its relation) in the shared ontology, using the Health-RI Mapping Vocabulary (HRIV) (cf. SKOS mapping relations for general vocabulary alignment).[^13]

!!! info

    The Common Reference Model is a semantic hub, not a replacement for local schemas. It supports reuse by letting multiple standards and local schemas align to one shared conceptualization rather than maintaining many pairwise mappings.

### Framing the Scope of HRIO

HRIO differs from ontologies whose primary goal is to prescribe a single, self-contained conceptualization of a narrowly delimited domain. Because HRIO functions as a common semantic reference model for semantic interoperability, its scope is defined primarily by the meanings that must be made explicit so that heterogeneous standards, local schemas, and related implementation artifacts can be interpreted in a shared and reviewable way.

In this sense, HRIO is not intended to reproduce every term, structure, or modeling decision found in external artifacts. Rather, it aims to provide a shared semantic foundation that captures the meanings most relevant for alignment across standards, schemas, and related artifacts. This is especially important in a domain as broad as health and life sciences, where the same label may be used with different intended meanings in different contexts. Accordingly, the use or reuse of mature external semantic resources should not be framed as an alternative to HRIO. When appropriate, such resources can be aligned to HRIO through mappings, allowing reuse of existing artifacts while preserving HRIO's role as the shared meaning-level reference model for interoperability. Other semantic artifacts may therefore remain valuable at the representation or implementation level without replacing HRIO's role in making meaning explicit and traceable.

For example, a term such as `Patient` may be used in one artifact to denote a person registered to receive care, in another to denote a person currently receiving care, and in another to denote a person with a history of care. If HRIO attempted to pre-model every possible interpretation of every reused label across the full domain, the reference model would quickly become unmanageably large and difficult to govern. For that reason, HRIO must be scoped incrementally and according to interoperability value.

Figure 2 summarizes the prioritization logic for candidate HRIO content.

```mermaid
flowchart LR
    S([Candidate concept])

    D1{Cross-artifact<br/>recurrence?}
    D2{Interoperability<br/>relevance?}
    D3{Meaning-level<br/>risk?}

    O1[[Deprioritize<br/>or exclude for now]]
    O2[[Defer unless<br/>strategically required]]
    O3[[Priority candidate<br/>for HRIO analysis]]
    O4[[Contextual candidate<br/>for HRIO analysis]]

    S --> D1
    D1 -- Yes --> D2
    D1 -- No --> O1

    D2 -- Yes --> D3
    D2 -- No --> O2

    D3 -- Yes --> O3
    D3 -- No --> O4

    classDef start fill:#ffffff,stroke:#1f1f1f,stroke-width:2px,color:#111111;
    classDef decision fill:#fafafa,stroke:#4a4a4a,stroke-width:1.5px,color:#111111;
    classDef outcome fill:#f7f7f7,stroke:#5b5b5b,stroke-width:1.5px,color:#111111;
    classDef selected fill:#f4f4f4,stroke:#222222,stroke-width:2px,color:#111111;

    class S start;
    class D1,D2,D3 decision;
    class O1,O2 outcome;
    class O3,O4 selected;
```

*Figure 2. Prioritization logic for candidate HRIO content.*

Apparent coverage should therefore be interpreted carefully. Broad coverage at the label level does not necessarily mean that the distinctions needed for semantic traceability, governance, and the avoidance of false agreement are already available at the meaning level.

!!! note

    The scope of HRIO is driven by meaning-level interoperability needs, not by the mere frequency of labels in external artifacts.

Priority should therefore be given to concepts that:

- occur across multiple influential standards or local schemas;
- are especially important for semantic interoperability and recurrent mapping work; and
- require conceptual clarification because their intended meaning varies across artifacts or is prone to false agreement.

At the current stage of the initiative, this prioritization can begin with standards such as FHIR, OMOP, and openEHR. For each prioritized concept, the modeling process begins by examining how the corresponding source expressions are used in those artifacts, including their definitions, usage context, and related terms. Based on this analysis, candidate content for HRIO can be classified using practical decision lists such as *must be*, *should be*, *can be*, and *should not be*. This helps distinguish what is essential to the reference model from what is optional, premature, or outside the current scope.

Figure 3 summarizes the analysis workflow and scope classification for candidate HRIO content.

```mermaid
%%{init: {"flowchart": {"wrappingWidth": 110}} }%%
flowchart LR
    S([Prioritized or<br/>contextual candidate])

    P1[Collect source<br/>expressions]
    P2[Examine<br/>definitions]
    P3[Examine usage context<br/>and related terms]
    P4[Assign<br/>scope class]

    subgraph C["Scope classes"]
        direction TB
        C1[[must be]]
        C2[[should be]]
        C3[[can be]]
        C4[[should not be]]
    end

    E([Scope justification<br/>recorded])

    S --> P1 --> P2 --> P3 --> P4
    P4 --> C1
    P4 --> C2
    P4 --> C3
    P4 --> C4

    C1 --> E
    C2 --> E
    C3 --> E
    C4 --> E

    classDef start fill:#ffffff,stroke:#1f1f1f,stroke-width:2px,color:#111111;
    classDef process fill:#fafafa,stroke:#4a4a4a,stroke-width:1.5px,color:#111111;
    classDef outcome fill:#f7f7f7,stroke:#5b5b5b,stroke-width:1.5px,color:#111111;

    class S,E start;
    class P1,P2,P3,P4 process;
    class C1,C2,C3,C4 outcome;
```

*Figure 3. Analysis workflow and scope classification for candidate HRIO content.*

!!! note "Internal scoping process"

    Health-RI applies an internal scoping process to prioritize candidate HRIO content and to guide scope-classification decisions. This process is important for maintaining conceptual rigor, consistency, and governance. However, its full internal content, working materials, and decision records are not published on this page.

Accordingly, HRIO should cover the meanings and distinctions that are necessary to support reliable alignment across important standards and local schemas. It should also include the related concepts needed to define, contextualize, and differentiate those target meanings in an ontologically well-founded way. However, HRIO should not aim to mirror external artifacts one by one, nor to introduce distinctions solely because they are possible in principle. Coverage should be justified by interoperability relevance, conceptual necessity, and evidence of actual use.

The scope of HRIO is also expected to evolve over time. Insights from mapping activities, expert review, and external validation may reveal semantic gaps in the reference model. When this happens, the ontology may be extended with additional concepts or refinements, provided that these additions improve semantic traceability and support better alignment across artifacts. Likewise, contributions received during the lifecycle may justify extensions or revisions when they expose genuine interoperability needs and are accepted through the appropriate review process.

!!! note "Current maintainability approach and future modularization"

    As HRIO grows, stronger modularization techniques may become necessary to keep the ontology maintainable, governable, and reusable over time. In a more mature setup, domain-oriented modules could be packaged more explicitly, with clearer ownership boundaries and more fine-grained maintenance practices.

    At present, however, this is not yet the adopted approach. The current governance already distinguishes domain packages and tracks their lifecycle independently, but ontology artifacts are still released under a shared HRIO version identifier and maintained as parts of one coordinated release process.

    Given the current size of the ontology and available capacity, the practical strategy is to preserve coherence and maintainability through disciplined scoping, consistent modeling decisions, and a shared release line. In this sense, stronger modularization should be understood as a future improvement rather than a current requirement.

From a mapping perspective, the long-term goal is that relevant source expressions in prioritized standards, schemas, and related artifacts can be linked to HRIO meanings via `hriv:hasExactMeaning` whenever their intended semantics are fully and precisely defined by a specific HRIO concept. When this is not yet possible, `hriv:hasBroaderMeaningThan` and `hriv:hasNarrowerMeaningThan` should be used to make the remaining semantic mismatch explicit. These non-exact mappings are not failures; they are useful indicators that the reference model may later need refinement. Over time, such cases should be reviewed so that approximate alignments can be replaced with exact ones whenever justified by improved modeling.

!!! info "Why `hriv:hasExactMeaning` behaves like a partial function"

    If we consider only `hriv:hasExactMeaning`, the mapping behaves like a partial many-to-one function from source expressions to HRIO meanings. It is *function-like* because each source expression may have at most one exact HRIO target. It is *partial* because some source expressions may have no exact target yet. It is *many-to-one* because multiple source expressions from different standards or schemas may share the same HRIO meaning.

    This characterization applies only to `hriv:hasExactMeaning`. In contrast, `hriv:hasBroaderMeaningThan` and `hriv:hasNarrowerMeaningThan` may relate a single source expression to multiple HRIO meanings when semantic overlap is partial or distributed, but only where the broader/narrower relation is justified by definitions and scope.

### Expressing HRIO as a Semantic Reference Model

To be effective, HRIO must be expressed in a highly expressive modeling language—one capable of making ontological commitments explicit and capturing rich semantic distinctions.[^14][^15]

These requirements call for the use of ontologically well-founded modeling languages, which are grounded in formal ontology and support the precise representation of complex domains. Among them, [OntoUML](../ontouml-gufo/ontouml.md) stands out as a leading and widely adopted approach, offering both theoretical rigor and practical tooling.[^14][^15]

Figure 4 illustrates the roles and technologies involved in our approach to enabling semantic interoperability. At the top, the conceptual HRIO reference model is represented using OntoUML (HRIO OntoUML), providing a clear and ontologically well-founded view of the meaning of concepts. While this model supports human understanding, it is not directly usable in computational artifacts.

![Common Reference Model](./assets/images/common-reference-model.png)
*Figure 4. HRIO as a common semantic reference model, from conceptual representation to computational implementation and mappings.*

To enable computational use, the HRIO OntoUML model is transformed into a corresponding gUFO-based OWL implementation (HRIO gUFO/OWL), based on [gUFO](../ontouml-gufo/gufo.md), a lightweight ontology in OWL aligned with the Unified Foundational Ontology (UFO).[^15][^16]

Figure 5 summarizes *semantic traceability* in the approach, connecting (i) the semiotic view (referent, conceptualization, representation) with (ii) the Model-Driven Architecture (MDA) view. It highlights the relationship between the conceptual model (HRIO OntoUML, CIM) and its computational ontology implementation (HRIO gUFO/OWL, PIM), helping preserve meaning across layers.[^17][^18][^19] For the initiative-level conceptual rationale and worked example, see the academic paper.[^20]

<!-- TODO: Add this new image. -->

![Semantic traceability architecture (Semiotic + MDA views)](./assets/images/semantic-traceability.png)
*Figure 5. Semantic traceability across semiotic and MDA views, linking HRIO OntoUML (CIM) to HRIO gUFO/OWL (PIM).*

Once the computational ontology is available, computational artifacts—such as schemas, web ontologies, or others used for information exchange—can be mapped to HRIO gUFO/OWL using the Health-RI Mapping Vocabulary (HRIV). These mappings may be created by Health-RI (see [mappings](../deliverables/mappings.md)) or by the owners of the aligned artifacts.[^11][^21]

!!! info "Why OntoUML?"

    OntoUML is used for HRIO OntoUML because it is grounded in the Unified Foundational Ontology (UFO) and supports explicit ontological commitments. This helps:

    - make modeling commitments discussable, reviewable, and comparable across artifacts;
    - support conceptual clarification and meaning negotiation with domain experts (when terminology alone is not reliable);
    - preserve intended semantics when transforming the conceptual model into HRIO gUFO/OWL.

    For more information, access: [OntoUML](../ontouml-gufo/ontouml.md).

## Division of Responsibilities: Modeling and Mapping Teams

![Modeling and Mapping Teams](./assets/images/Picture2.png)
*Figure 6. Division of responsibilities and feedback loop between the ontology modeling and ontology mapping teams.*

To operationalize the approach based on a common semantic reference model (HRIO), Health-RI will structure the effort around two complementary teams:

- The Ontology Modeling Team
- The Ontology Mapping Team

These teams will work in parallel to accelerate delivery while maintaining a clear division of responsibilities.

!!! tip

    Treat mappings as versioned artifacts: they must be reviewed when either the source schema/standard or the reference model evolves. Capturing rationale for each mapping decision reduces rework and reviewer disagreement.

### Ontology Modeling Team

The Modeling Team is responsible for developing the HRIO reference model (HRIO OntoUML) using OntoUML. Team members are expected to:

- Model domain knowledge using OntoUML with a high degree of accuracy and precision.
- Analyze and interpret technical materials, such as standards, protocols, and domain documentation.
- Engage with domain specialists to gather the necessary insights for accurate modeling.

The team's objective is to produce a semantically rich and ontologically well-founded model that captures the essential structure and meaning of the domain.

### Ontology Mapping Team

The Mapping Team is responsible for aligning concepts from external standards and local schemas (and related implementation artifacts such as RDF/OWL ontologies, codes, and schema elements) to HRIO. In the approach, these external artifacts contribute the *source expressions* being mapped, while HRIO concepts play the role of the target meanings. This involves:

- Interpreting and understanding OntoUML models.
- Analyzing data schemas in various formats, with an emphasis on Semantic Web technologies.
- Applying best practices in concept mapping using appropriate tools and techniques.
- Utilizing the [Simple Standard for Sharing Ontological Mappings (SSSOM)](https://mapping-commons.github.io/sssom/) to document mappings in a consistent and reusable way.[^21]
- Collaborating closely with artifact owners and maintainers (e.g., standard communities, ontology/schema maintainers, and domain experts) to capture the intended meaning of concepts and schema elements.

!!! tip "Drafting mappings with the HRIO Mapping Assistant (GPT)"

    When you need help selecting a candidate HRIO target and choosing exactly one HRIV predicate, you can use the [HRIO Mapping Assistant](https://chatgpt.com/g/g-6990a7e348c4819190ef2de88503ff5e-hrio-mapping-assistant)\*\* as a drafting aid.

    *Always capture evidence in the mapping record and follow the review rules described in Mapping Governance before publishing or contributing mappings.*

Depending on editorial control, mappings may be maintained non-invasively in a separate mapping set (e.g., SSSOM) or embedded directly in the source artifact when governance permits.

This team plays a critical role in ensuring that concepts from standards, schemas, and related artifacts are semantically aligned with the reference model, enabling shared understanding and more reliable reuse across systems and integration settings.

### Domain Guidance and Coordination

While domain knowledge is essential, it does not need to reside within the modeling or mapping teams. Instead, a third coordinating group will provide:

- Access to domain experts and technical documentation.
- Guidance throughout the modeling and mapping processes.
- Logistical and institutional support to ensure smooth collaboration between stakeholders.

This group ensures that the teams are supported with the necessary context and resources to perform their tasks effectively.

### Collaborative Iteration and Feedback

As shown in Figure 6, the Modeling and Mapping Teams operate in a collaborative feedback loop.

- The Ontology Modeling Team develops the conceptual model.
- The Ontology Mapping Team uses this model to map source expressions from external artifacts to HRIO.
- Insights gained during the mapping process are fed back to the modeling team.

This feedback may include:

- Missing concepts that need to be added to the reference model.
- Redundant or unused elements that can be removed or revised.
- Ambiguities or inconsistencies that require clarification.

This iterative cycle improves both the quality of the reference model and the precision of the mappings. Over time, it leads to a stronger, more coherent semantic framework for Health-RI and others facing similar interoperability challenges.

## Translating OntoUML to OWL via gUFO

While OntoUML provides the expressiveness and ontological rigor needed to build HRIO OntoUML, it is designed primarily for conceptual modeling. Its focus is on producing models that support human understanding, learning, communication, and informed decision-making. As such, OntoUML models are not directly suited for computational use in Semantic Web applications or automated reasoning tasks.[^14][^15]

To bridge this gap, the OntoUML model must be transformed into a computational representation. This is achieved by converting the OntoUML reference model (HRIO OntoUML) into a gUFO-based OWL implementation (HRIO gUFO/OWL) using [gUFO (gentle UFO)](../ontouml-gufo/gufo.md)—a lightweight, computationally accessible ontology derived from UFO, the foundational ontology on which OntoUML is based.[^15][^16]

gUFO is implemented in the Web Ontology Language (OWL), a widely used standard for representing ontologies on the Semantic Web. This makes it compatible with existing RDF-based technologies and allows:[^16]

!!! note

    OntoUML is optimized for making ontological distinctions explicit for human understanding and review, while gUFO/OWL enables computational use. Keeping both layers preserves meaning while remaining technically tractable.

- The OntoUML-based reference model to be used computationally within semantic infrastructures.
- Semantic mappings from local RDF-based schemas to be aligned directly with the OWL representation of the model.

By converting HRIO OntoUML into HRIO gUFO/OWL, we ensure that the semantics captured during conceptual modeling are retained, while also enabling their technical integration into semantic web systems and interoperability workflows.[^16]

## References

[^1]: Wilkinson, M. D., et al. (2016). The FAIR Guiding Principles for scientific data management and stewardship. *Scientific Data, 3*(1), 160018. https://doi.org/10.1038/sdata.2016.18

[^2]: Piera-Jiménez, J., Leslie, H., Dunscombe, R., & Pontes, C. (2024). Interoperability in the context of integrated care. In V. Amelung, V. Stein, E. Suter, N. Goodwin, R. Balicer, & A.-S. Beese (Eds.), *Handbook of Integrated Care* (pp. 1–22). Springer Nature Switzerland. https://doi.org/10.1007/978-3-031-25376-8_101-1

[^3]: Yadav, R., Murria, S., & Sharma, A. (2021). A research review on semantic interoperability issues in electronic health record systems in medical healthcare. In *IoT-Based Data Analytics for the Healthcare Industry* (pp. 123–138). Elsevier. https://doi.org/10.1016/B978-0-12-821472-5.00009-0

[^4]: De Mello, B. H., et al. (2022). Semantic interoperability in health records standards: A systematic literature review. *Health Technol, 12*(2), 255–272. https://doi.org/10.1007/s12553-022-00639-w

[^5]: Palojoki, S., & Vuokko, R. (2023, April 26). Semantic interoperability of EHRs: Review of approaches for enhancing the goals of European Health Data Space. *Preprint*. https://doi.org/10.20944/preprints202304.0957.v1

[^6]: Guarino, N. (Ed.). (1998). *Formal Ontology in Information Systems: Proceedings of the 1st International Conference (Trento, Italy, June 6–8, 1998)*. IOS Press.

[^7]: Guizzardi, G., & Guarino, N. (2024). Explanation, semantics, and ontology. *Data & Knowledge Engineering, 153*, 102325. https://doi.org/10.1016/j.datak.2024.102325

[^8]: Capuano, N., Foggia, P., Greco, L., & Ritrovato, P. (2022). A Linked Data application for harmonizing heterogeneous biomedical information. *Applied Sciences, 12*(18), 9317. https://doi.org/10.3390/app12189317

[^9]: Mithiri, R. K. (2025). A semantic interoperability framework for cross-institutional integration of heterogeneous electronic health records. *International Journal of Engineering Technology Research & Development, 6*(3), 25–31.

[^10]: Saberi, M. A., Mcheick, H., & Adda, M. (2025). From data silos to health records without borders: A systematic survey on patient-centered data interoperability. *Information, 16*(2), 106. https://doi.org/10.3390/info16020106

[^11]: Ekaputra, F. J., Sabou, M., Serral, E., Kiesling, E., & Biffl, S. (2017). Ontology-based data integration in multi-disciplinary engineering environments: A review. *Open Journal of Information Systems (OJIS), 4*(1), 1–26.

[^12]: Guizzardi, G. (2020). Ontology, ontologies and the "I" of FAIR. *Data Intelligence, 2*(1–2), 181–191. https://doi.org/10.1162/dint_a_00040

[^13]: Miles, A., & Bechhofer, S. (2009, August 18). *SKOS Simple Knowledge Organization System Reference* (W3C Recommendation REC-skos-reference-20090818). World Wide Web Consortium. https://www.w3.org/TR/skos-reference/

[^14]: Guizzardi, G. (2005). *Ontological foundations for structural conceptual models* (Doctoral dissertation, University of Twente).

[^15]: Guizzardi, G., Botti Benevides, A., Fonseca, C. M., Porello, D., Almeida, J. P. A., & Prince Sales, T. (2022). UFO: Unified Foundational Ontology. *Applied Ontology, 17*(1), 167–210. https://doi.org/10.3233/AO-210256

[^16]: Almeida, J. P. A., Guizzardi, G., Sales, T. P., & Falbo, R. A. (2019). *gUFO: A lightweight implementation of the Unified Foundational Ontology (UFO)*. http://purl.org/nemo/doc/gufo

[^17]: Ogden, C. K., & Richards, I. A. (1923). *The meaning of meaning: A study of the influence of language upon thought and of the science of symbolism*. Kegan Paul, Trench, Trubner & Co.

[^18]: Gangemi, A. (2007). *Semiotics Ontology Design Pattern*. http://www.ontologydesignpatterns.org/cp/owl/semiotics.owl

[^19]: Miller, J., & Mukerji, J. (2003). *MDA Guide Version 1.0.1* (OMG/03-06-01). Object Management Group. http://www.omg.org/cgi-bin/doc?omg/03-06-01.pdf

[^20]: Barcelos, P. P. F., van Ulzen, N., Groeneveld, R., Konrad, A., Khalid, Q., Zhang, S., Trompert, A., & Vos, J. (n.d.). *Enabling Semantic Traceability in Health Data: The Health-RI Semantic Interoperability Initiative* (manuscript approved at SWAT4HCLS 2026, v1.1.1). [Download link.](https://raw.githubusercontent.com/Health-RI/semantic-interoperability/main/documents/preprints/enabling-semantic-traceability-in-health-data-v1.1.0.pdf)

[^21]: Zhang, S., Cornet, R., & Benis, N. (2024). Cross-Standard Health Data Harmonization using Semantics of Data Elements. *Scientific Data, 11*(1), 1407. https://doi.org/10.1038/s41597-024-04168-1
