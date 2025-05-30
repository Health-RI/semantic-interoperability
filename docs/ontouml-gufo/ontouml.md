# OntoUML

<p align="left"><img src="../../assets/images/ontouml-logo.png" width="500" alt="OntoUML Logo"></p>

**OntoUML** is an ontologically well-founded language designed for ontology-driven conceptual modeling. It extends the Unified Modeling Language (UML) by incorporating the ontological distinctions provided by the Unified Foundational Ontology (UFO). Through UML’s profiling mechanism, OntoUML defines a collection of class and association stereotypes that reflect the ontological distinctions present in UFO. It also establishes semantically motivated syntactical constraints to ensure that every syntactically correct model represents a sound UFO-based ontology.

OntoUML introduced a methodological commitment to ontological analysis, helping modelers make conceptually sound modeling decisions. By aligning UML notation with foundational ontology, OntoUML became a practical and rigorous approach to ontology-driven conceptual modeling **<a href="#ref1">[1]</a>**.

Originally developed to make the use of foundational ontology in modeling more accessible and operational, OntoUML plays a central role in applying UFO in practice. The language was engineered to support the creation of high-quality domain models by explicitly encoding ontological distinctions in modeling constructs, enabling a principled approach to identifying and correcting conceptual modeling errors early in the development process **<a href="#ref2">[2]</a>**.

Over time, OntoUML evolved beyond a simple UML profile: it became a community-supported ecosystem with formal semantics and tool support. Its precision and ontological grounding have made it especially valuable in complex domains such as healthcare, defense, digital forensics, and enterprise modeling, where ambiguity and conceptual inconsistency can have significant consequences **<a href="#ref2">[2]</a>**.

## Origins

The development of OntoUML is rooted in the work of Giancarlo Guizzardi, particularly his Ph.D. thesis titled [*Ontological Foundations for Structural Conceptual Models*](https://research.utwente.nl/files/6042428/thesis_Guizzardi.pdf) **<a href="#ref3">[3]</a>**. Although the term “OntoUML” was not used in that work, the conceptual basis for the language—its ontological foundations, modeling distinctions, and methodological approach—was thoroughly developed there. Similarly, the ontology that would later be known as the **Unified Foundational Ontology (UFO)** was introduced in substance, though not yet by name.

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

## Adoption and Influence

Since its inception, OntoUML has been adopted by various academic, corporate, and governmental institutions worldwide for developing conceptual models across diverse domains. The foundational theories underlying OntoUML have also influenced other conceptual modeling languages, such as ORM 2.0.

Several research groups have contributed to the development and dissemination of OntoUML, including:

- The [Semantics, Cybersecurity & Services (SCS)](https://www.utwente.nl/en/eemcs/scs/) group at the University of Twente, the Netherlands  
- The [Ontology & Conceptual Modeling Research Group (NEMO)](https://nemo.inf.ufes.br/en/) at the Federal University of Espírito Santo, Brazil  
- The [KRDB Research Centre for Knowledge-based Artificial Intelligence](https://www.inf.unibz.it/krdb/) at the Free University of Bozen-Bolzano, Italy  
- The [Center for Conceptual Modelling and Implementation (CCMi)](https://ccmi.fit.cvut.cz/en/) at the Faculty of Information Technology, Czechia

## Supporting Tools and Developments

The official development of OntoUML tools is hosted on GitHub at [https://github.com/OntoUML](https://github.com/OntoUML). These projects are primarily academic efforts, maintained by researchers and contributors from the OntoUML community.

- **[ontouml-js](https://github.com/OntoUML/ontouml-js)**: A JavaScript library for creating, manipulating, and serializing OntoUML models into JSON format compliant with the ontouml-schema.
- **[ontouml-json2graph](https://github.com/OntoUML/ontouml-json2graph)**: Transforms OntoUML JSON models into graph representations aligned with the OntoUML Vocabulary, facilitating visualization and semantic analysis.
- **[ontouml-metamodel](https://github.com/OntoUML/ontouml-metamodel)**: Provides an implementation-independent metamodel of OntoUML, covering both abstract and concrete syntaxes, serving as a reference for various OntoUML tools.
- **[ontouml-models](https://github.com/OntoUML/ontouml-models)**: A collaborative, structured, and open-source catalog of OntoUML and UFO ontology models, supporting empirical research and model sharing.
- **[ontouml-models-lib](https://github.com/OntoUML/ontouml-models-lib)**: A Python library designed to access and manage OntoUML models from the OntoUML/UFO Catalog, simplifying software development tasks.
- **[ontouml-models-tools](https://github.com/OntoUML/ontouml-models-tools)**: A set of tools for processing and validating OntoUML models, including functionalities for data quality verification and model analysis.
- **[ontouml-models-vocabulary](https://github.com/OntoUML/ontouml-models-vocabulary)**: Defines vocabularies to annotate and interlink models within the OntoUML/UFO Catalog, enhancing semantic interoperability.
- **[ontouml-schema](https://github.com/OntoUML/ontouml-schema)**: Provides a JSON Schema representation for OntoUML models, enabling validation and exchange of models in a standardized format.
- **[ontouml-server](https://github.com/OntoUML/ontouml-server)**: A server-side application offering services for OntoUML model management, including storage, conversion, and validation functionalities.
- **[ontouml-vocabulary](https://github.com/OntoUML/ontouml-vocabulary)**: An OWL vocabulary that formalizes the OntoUML metamodel, supporting the serialization and exchange of OntoUML models as linked data.
- **[ontouml-vocabulary-lib](https://github.com/OntoUML/ontouml-vocabulary-lib)**: A Python library facilitating the manipulation of OntoUML vocabulary concepts within RDFLib graphs, bridging OntoUML and Semantic Web technologies.
- **[ontouml-vp-plugin](https://github.com/OntoUML/ontouml-vp-plugin)**: A plugin for Visual Paradigm that integrates OntoUML modeling capabilities, allowing users to create and manage OntoUML models within the Visual Paradigm environment.

These tools enhance the usability and applicability of OntoUML across various modeling workflows, supporting both academic exploration and industrial adoption.

### OntoUML/UFO Catalog

The OntoUML/UFO Catalog is a structured, community-driven repository of real-world OntoUML models, developed with the goal of supporting research, education, and tool development in conceptual modeling. It provides a curated collection of ontologies from various domains—ranging from law and healthcare to logistics and cybersecurity—all represented using OntoUML and grounded in the Unified Foundational Ontology (UFO). Each model is accompanied by metadata that documents its origin, purpose, and scope, facilitating discoverability and reuse.

Designed as an open and extensible initiative, the catalog is maintained on GitHub ([OntoUML Models Repository](https://github.com/OntoUML/ontouml-models)) and promotes collaborative contributions from the broader community. It has proven to be an essential resource for empirical studies and validation of modeling tools and techniques. A peer-reviewed study has also systematically documented the catalog’s structure, evolution, and coverage, highlighting its value for both researchers and practitioners **<a href="#ref7">[7]</a>**.

## References

<a id="ref1"></a> 
- **[1]** Guizzardi, G., Wagner, G., Falbo, R. A., Guizzardi, R. S. S., & Almeida, J. P. A. (2015). *OntoUML: A well-founded profile for UML-based conceptual modeling*. Applied Ontology, 10(3–4), 259–291. https://doi.org/10.3233/AO-150157

<a id="ref2"></a>
- **[2]** Guizzardi, G., Wagner, G., Almeida, J. P. A., Guizzardi, R. S. S., & Sales, T. P. (2022). *The Unified Foundational Ontology (UFO): Supercharging modeling with foundational ontologies*. Applied Ontology, 17(1), 1–44. https://doi.org/10.3233/AO-210256

<a id="ref3"></a>
- **[3]** Guizzardi, G. (2005). *Ontological foundations for structural conceptual models* [Doctoral dissertation, University of Twente]. Telematica Instituut / CTIT. [**[Access]**](https://research.utwente.nl/en/publications/ontological-foundations-for-structural-conceptual-models/) [**[Download]**](https://research.utwente.nl/files/6042428/thesis_Guizzardi.pdf)

<a id="ref4"></a>
- **[4]** Guizzardi, G., & Wagner, G. (2004). *On the ontological foundations of agent concepts*. In Proceedings of the 6th International Bi-Conference Workshop on Agent-Oriented Information Systems (AOIS), held in conjunction with CAiSE 2004, Riga, Latvia.

<a id="ref5"></a>
- **[5]** Guizzardi, G., & Wagner, G. (2005a). *Some applications of a unified foundational ontology in business modeling*. In T. Bui & A. G. Tjoa (Eds.), Ontologies and business systems analysis. IDEA Group Publishing.

<a id="ref6"></a>
- **[6]** Guizzardi, G., & Wagner, G. (2005b). *Towards ontological foundations for agent modeling concepts using UFO*. In V. Dignum, M. Dastani, B. Dunin-Kȩplicz, & R. Meyer (Eds.), Agent-Oriented Information Systems II (pp. xx–xx). Lecture Notes in Artificial Intelligence (Vol. 3508). Springer. https://doi.org/10.1007/11538394_6

<a id="ref7"></a>
- **[7]** Sales, T. P., Guizzardi, G., Almeida, J. P. A., & Guizzardi, R. S. S. (2023). *The OntoUML/UFO Catalog: A structured repository of real-world ontologies for conceptual modeling research*. Journal of Systems and Software, 201, 111645. https://doi.org/10.1016/j.jss.2023.111645
