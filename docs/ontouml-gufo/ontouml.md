# OntoUML

<p align="left"><img src="../../assets/images/ontouml-logo.png" width="500" alt="OntoUML Logo"></p>

**OntoUML** is an ontologically well-founded language designed for ontology-driven conceptual modeling. It extends the Unified Modeling Language (UML) by incorporating the ontological distinctions provided by the Unified Foundational Ontology (UFO). Through UML’s profiling mechanism, OntoUML defines a collection of class and association stereotypes that reflect the ontological distinctions present in UFO. It also establishes semantically motivated syntactical constraints to ensure that every syntactically correct model represents a sound UFO-based ontology.

OntoUML introduced a methodological commitment to ontological analysis, helping modelers make conceptually sound modeling decisions. By aligning UML notation with foundational ontology, OntoUML became a practical and rigorous approach to ontology-driven conceptual modeling **<a href="#ref1">[1]</a>**.

Originally developed to make the use of foundational ontology in modeling more accessible and operational, OntoUML plays a central role in applying UFO in practice. The language was engineered to support the creation of high-quality domain models by explicitly encoding ontological distinctions in modeling constructs, enabling a principled approach to identifying and correcting conceptual modeling errors early in the development process **<a href="#ref2">[2]</a>**.

Over time, OntoUML evolved beyond a simple UML profile: it became a community-supported ecosystem with formal semantics and tool support. Its precision and ontological grounding have made it especially valuable in complex domains such as healthcare, defense, digital forensics, and enterprise modeling, where ambiguity and conceptual inconsistency can have significant consequences **<a href="#ref2">[2]</a>**.

## Origins

The development of OntoUML is rooted in the work of [Giancarlo Guizzardi](https://www.giancarloguizzardi.com/), particularly his Ph.D. thesis titled [*Ontological Foundations for Structural Conceptual Models*](https://research.utwente.nl/files/6042428/thesis_Guizzardi.pdf) **<a href="#ref3">[3]</a>**. Although the term “OntoUML” was not used in that work, the conceptual basis for the language—its ontological foundations, modeling distinctions, and methodological approach—was thoroughly developed there. Similarly, the ontology that would later be known as the **Unified Foundational Ontology (UFO)** was introduced in substance, though not yet by name.

The formal naming and definition of UFO as a unified foundational ontology appeared in a set of contemporaneous publications by Guizzardi and Wagner **<a href="#ref4">[4]</a>****<a href="#ref5">[5]</a>****<a href="#ref6">[6]</a>**. These works extended the ideas from the thesis and applied them to domains such as agent concepts and business modeling, positioning UFO as a comprehensive foundation for conceptual modeling.

OntoUML was conceived as a lightweight UML profile grounded in this ontological foundation, designed to bridge the gap between formal ontology and practical modeling. It provides semantically rich modeling constructs through stereotypes and well-defined constraints that reflect ontological distinctions—such as types, roles, phases, and relators. This ensures that OntoUML models are logically consistent and ontologically expressive, enhancing semantic precision and interoperability.

## Documentation and Standardization Efforts

Unlike some modeling languages that provide a centralized and formal specification, OntoUML does not have a single, unified source of documentation. Instead, its evolution is driven by academic research, with improvements and extensions typically introduced through peer-reviewed publications.

This decentralized development model can pose challenges for newcomers, making the language harder to study and adopt compared to alternatives that offer consolidated reference materials.

There are, however, two major online resources that offer learning materials for OntoUML:

- The official OntoUML portal: [https://ontouml.org/](https://ontouml.org/)  
  > While this is the main site, much of its content is outdated and has not been maintained in recent years.

- The documentation project at Read the Docs: [https://ontouml.readthedocs.io/en/latest/](https://ontouml.readthedocs.io/en/latest/)  
  > This version is more comprehensive and somewhat more recent, but it still contains outdated content and should be read with caution.

Despite their limitations, these resources remain valuable for learning the language. However, users should remain aware of their partial and outdated nature and supplement them with insights from more recent academic publications.

## Additional Learning Resources

Professor [Giancarlo Guizzardi](https://www.giancarloguizzardi.com/), the original creator of OntoUML and the Unified Foundational Ontology (UFO), offers a wide array of high-quality educational materials freely accessible through his personal website. These resources are invaluable for those interested in learning about ontologies, foundational ontology, and the practical use of OntoUML.

- **[Recorded Talks and Keynotes](https://www.giancarloguizzardi.com/recorded-talks)** — Presentations and invited lectures on ontologies, conceptual modeling, and foundational theories.
- **[Courses and Tutorials](https://www.giancarloguizzardi.com/courses)** — Graduate-level lectures, structured modules, and instructional materials on ontology-driven conceptual modeling and OntoUML.
- **[Research and Publications](https://www.giancarloguizzardi.com/research)** — A comprehensive collection of peer-reviewed papers, book chapters, and conference proceedings that define and advance the OntoUML language and UFO theory.

Together, these materials provide both theoretical grounding and practical guidance, making them highly valuable for students, researchers, and professionals working with conceptual models.

## Adoption and Influence

Since its inception, OntoUML has been adopted by various academic, corporate, and governmental institutions worldwide for developing conceptual models across diverse domains. The foundational theories underlying OntoUML have also influenced other conceptual modeling languages, such as ORM 2.0.

Several research groups have contributed to the development and dissemination of OntoUML, including:

- The [Semantics, Cybersecurity & Services (SCS)](https://www.utwente.nl/en/eemcs/scs/) group at the University of Twente, the Netherlands  
- The [Ontology & Conceptual Modeling Research Group (NEMO)](https://nemo.inf.ufes.br/en/) at the Federal University of Espírito Santo, Brazil  
- The [KRDB Research Centre for Knowledge-based Artificial Intelligence](https://www.inf.unibz.it/krdb/) at the Free University of Bozen-Bolzano, Italy  
- The [Center for Conceptual Modelling and Implementation (CCMi)](https://ccmi.fit.cvut.cz/en/) at the Faculty of Information Technology, Czechia

## Supporting Tools and Developments

The official development of OntoUML tools is hosted on GitHub at [https://github.com/OntoUML](https://github.com/OntoUML). These projects are primarily academic efforts, maintained by researchers and contributors from the OntoUML community.

- **[ontouml-js](https://w3id.org/ontouml/js)**: A JavaScript library for creating, manipulating, and serializing OntoUML models into JSON format compliant with the ontouml-schema.
- **[ontouml-json2graph](https://w3id.org/ontouml/json2graph)**: Transforms OntoUML JSON models into graph representations aligned with the OntoUML Vocabulary, facilitating visualization and semantic analysis.
- **[ontouml-metamodel](https://w3id.org/ontouml/metamodel)**: Provides an implementation-independent metamodel of OntoUML, covering both abstract and concrete syntaxes, serving as a reference for various OntoUML tools.
- **[ontouml-models](https://w3id.org/ontouml-models/git)**: A collaborative, structured, and open-source catalog of OntoUML and UFO ontology models, supporting empirical research and model sharing.
  > A detailed description of the catalog is provided in the [OntoUML/UFO Catalog page](./ontouml-ufo-catalog.md).
- **[ontouml-models-lib](https://w3id.org/ontouml/models-lib)**: A Python library designed to access and manage OntoUML models from the OntoUML/UFO Catalog, simplifying software development tasks.
- **[ontouml-models-tools](https://w3id.org/ontouml/models-tools)**: A set of tools for processing and validating OntoUML models, including functionalities for data quality verification and model analysis.
- **[ontouml-models-vocabulary](https://w3id.org/ontouml/models-vocabulary)**: Defines vocabularies to annotate and interlink models within the OntoUML/UFO Catalog, enhancing semantic interoperability.
- **[ontouml-schema](https://w3id.org/ontouml/schema)**: Provides a JSON Schema representation for OntoUML models, enabling validation and exchange of models in a standardized format.
- **[ontouml-server](https://w3id.org/ontouml/server)**: A server-side application offering services for OntoUML model management, including storage, conversion, and validation functionalities.
- **[ontouml-vocabulary](https://w3id.org/ontouml/vocabulary)**: An OWL vocabulary that formalizes the OntoUML metamodel, supporting the serialization and exchange of OntoUML models as linked data.
- **[ontouml-vocabulary-lib](https://w3id.org/ontouml/vocabulary-lib)**: A Python library facilitating the manipulation of OntoUML vocabulary concepts within RDFLib graphs, bridging OntoUML and Semantic Web technologies.
- **[ontouml-vp-plugin](https://w3id.org/ontouml/vp-plugin)**: A plugin for Visual Paradigm that integrates OntoUML modeling capabilities, allowing users to create and manage OntoUML models within the Visual Paradigm environment.

These tools enhance the usability and applicability of OntoUML across various modeling workflows, supporting both academic exploration and industrial adoption.

## References

<a id="ref1"></a>
- **[1]** Guizzardi, G., Wagner, G., Falbo, R. A., Guizzardi, R. S. S., & Almeida, J. P. A. (2015). *OntoUML: A well-founded profile for UML-based conceptual modeling*. Applied Ontology, 10(3–4), 259–291. <https://doi.org/10.3233/AO-150157>

<a id="ref2"></a>
- **[2]** Guizzardi, G., Wagner, G., Almeida, J. P. A., Guizzardi, R. S. S., & Sales, T. P. (2022). *The Unified Foundational Ontology (UFO): Supercharging modeling with foundational ontologies*. Applied Ontology, 17(1), 1–44. <https://doi.org/10.3233/AO-210256>

<a id="ref3"></a>
- **[3]** Guizzardi, G. (2005). *Ontological foundations for structural conceptual models* [Doctoral dissertation, University of Twente]. Telematica Instituut / CTIT. [**[Access]**](https://research.utwente.nl/en/publications/ontological-foundations-for-structural-conceptual-models/) [**[Download]**](https://research.utwente.nl/files/6042428/thesis_Guizzardi.pdf)

<a id="ref4"></a>
- **[4]** Guizzardi, G., & Wagner, G. (2004). *On the ontological foundations of agent concepts*. In Proceedings of the 6th International Bi-Conference Workshop on Agent-Oriented Information Systems (AOIS), held in conjunction with CAiSE 2004, Riga, Latvia.

<a id="ref5"></a>
- **[5]** Guizzardi, G., & Wagner, G. (2005a). *Some applications of a unified foundational ontology in business modeling*. In T. Bui & A. G. Tjoa (Eds.), Ontologies and business systems analysis. IDEA Group Publishing.

<a id="ref6"></a>
- **[6]** Guizzardi, G., & Wagner, G. (2005b). *Towards ontological foundations for agent modeling concepts using UFO*. In V. Dignum, M. Dastani, B. Dunin-Kȩplicz, & R. Meyer (Eds.), Agent-Oriented Information Systems II (pp. xx–xx). Lecture Notes in Artificial Intelligence (Vol. 3508). Springer. <https://doi.org/10.1007/11538394_6>
