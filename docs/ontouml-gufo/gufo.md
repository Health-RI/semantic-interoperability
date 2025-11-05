# gentle UFO (gUFO)

The 'gentle Unified Foundational Ontology', or simply **gUFO**, is a simplified and lightweight version of the Unified Foundational Ontology (UFO). It was designed to make ontology-driven conceptual modeling more accessible and practical for real-world applications, while preserving the formal rigor of its parent ontology.

## What is gUFO?

gUFO provides a set of foundational building blocks—such as `Object`, `Event`, `Quality`, and `Situation`—that help structure knowledge in a clear and shared way. These concepts are intended to be reused across different domains, helping organizations align their understanding of data and concepts.

Put simply, gUFO is a toolkit for creating consistent and precise representations of meaning.

## Why was gUFO created?

UFO is rich and comprehensive, but its complexity can be a barrier for practical adoption. To address this, gUFO was introduced in 2019 as a lightweight version of UFO. It focuses on usability, compatibility with existing tools, and ease of adoption for systems that need formal grounding without the burden of full ontological complexity.

The goal was to support knowledge graph creation, semantic data integration, and model interoperability in a more approachable way <a href="#ref2">[2]</a>.

## Where is gUFO used?

gUFO has found applications in various fields:

- **Semantic interoperability** across organizations and systems
- **Knowledge graphs** for structured web data and enterprise data integration
- **Ontology engineering** and conceptual modeling in research and industry
- **Linked data** and Semantic Web technologies
- **Education**, as a stepping stone to foundational ontologies

Its use has been documented in both academic and applied settings across domains such as public health, digital humanities, software engineering, and e-government <a href="#ref5">[5]</a>.

## When was gUFO developed?

gUFO was released in 2019 by João Paulo A. Almeida, Giancarlo Guizzardi, Tiago Prince Sales, and Ricardo A. Falbo. It is built on more than a decade of research on UFO and its application in ontology-driven conceptual modeling <a href="#ref1">[1]</a>.

## How does gUFO work?

gUFO is implemented in OWL 2 DL, which means it can be used with standard ontology tools and reasoners. Its key features include:

- **Reusable core categories** grounded in formal ontology
- **Interoperability** with tools and linked data ecosystems
- **Simplified structure** focused on structural (not behavioral) aspects
- **Extendibility**, allowing users to specialize concepts for their domains

This balance between formality and simplicity makes gUFO ideal for organizations aiming to adopt semantic technologies without starting from scratch.


## How to Create a gUFO Ontology

There are two main ways to create a gUFO-compliant ontology, depending on the user's familiarity with ontology modeling tools and the desired level of formality or tool support.

### 1. Direct Authoring in OWL

The most flexible approach is to create the ontology directly using an OWL 2 DL editor such as:

- [**Protégé**](https://protege.stanford.edu) – A free, open-source ontology editor widely used in academic and industry settings
- [**TopBraid Composer**](https://www.topquadrant.com/products/topbraid-composer/) – A professional-grade editor with advanced RDF and SPARQL support
- [**WebVOWL Editor**](http://vowl.visualdataweb.org/webvowl-editor/) – A lightweight, web-based tool for visual ontology creation

You can import the official gUFO ontology from:

- **OWL file**: [https://purl.org/nemo/gufo](https://purl.org/nemo/gufo)
- **Documentation site**: [https://nemo-ufes.github.io/gufo/](https://nemo-ufes.github.io/gufo/)

After importing gUFO into your tool, you can begin defining your own classes and properties as specializations of gUFO's foundational categories, such as `gufo:Object`, `gufo:Event`, `gufo:Quality`, or `gufo:Situation`.

This approach gives full control over ontology structure and serialization, and is ideal for applications requiring fine-grained reasoning or integration with existing linked data.

### 2. Modeling in OntoUML and Direct Export to gUFO

An alternative and user-friendly approach to creating a gUFO ontology is to first model it conceptually in OntoUML and then export it directly to a gUFO-compliant OWL ontology using the [**ontouml-vp-plugin**](https://w3id.org/ontouml/vp-plugin) in Visual Paradigm.

#### Steps:

1. **Create the OntoUML model** using Visual Paradigm with the OntoUML plugin.
   - The plugin supports OntoUML stereotypes such as `«kind»`, `«role»`, `«relator»`, and offers a dedicated palette for ontology-driven modeling.
2. **Export directly to gUFO**:
   - From the top menu, select **`Export → Export to gUFO`**.
   - In the dialog that appears, configure the export parameters:
     - Set the **Base IRI**
     - Choose the **output format** (e.g., Turtle)
     - Optionally enable URI customization, property creation behavior, and pre-analysis
   - Select which model elements to include and click **Export**.

This process will generate an OWL ontology in the selected format, conforming to the [gUFO specification](https://nemo-ufes.github.io/gufo/).

### Summary

| Approach                 | Tooling                   | Output Format    | Best For                                           |
| ------------------------ | ------------------------- | ---------------- | -------------------------------------------------- |
| Direct OWL authoring     | Protégé, TopBraid, etc.   | OWL 2 / RDF      | Ontologists, Semantic Web experts                  |
| OntoUML + transformation | Visual Paradigm + plugins | OWL 2 (via gUFO) | Conceptual modelers, teams using UFO-based methods |

Both approaches are valid and produce gUFO-compliant ontologies. The choice depends on the modeling style and technical familiarity of the user.

## References

<a id="ref1"></a>
**[1]** Guizzardi, G. (2005). *Ontological foundations for structural conceptual models.* [PhD Thesis - Research UT, graduation UT, University of Twente]. Telematica Instituut / CTIT. [**[Access]**](https://research.utwente.nl/en/publications/ontological-foundations-for-structural-conceptual-models/) [**[Download]**](https://research.utwente.nl/files/6042428/thesis_Guizzardi.pdf)

<a id="ref2"></a>
**[2]** Almeida, J. P. A., Guizzardi, G., Sales, T. P., & Falbo, R. A. (2019). *gUFO: A Lightweight Implementation of the Unified Foundational Ontology (UFO).* [**[Access]**](https://nemo-ufes.github.io/gufo/)

<a id="ref3"></a>
**[3]** Guizzardi, G., Wagner, G., Falbo, R. A., Guizzardi, R. S. S., & Almeida, J. P. A. (2013). *Towards Ontological Foundations for the Conceptual Modeling of Events.* In *Conceptual Modeling – ER 2013* (pp. 327–341). Springer. [**[DOI]**](https://doi.org/10.1007/978-3-642-41924-9_27)

<a id="ref4"></a>
**[4]** Sales, T. P., Guizzardi, G., Almeida, J. P. A., & Benevides, A. B. (2023). *Ontology-Driven Conceptual Modeling with gUFO.* In *Frontiers in Artificial Intelligence and Applications*, 394, 331–336. [**[Access]**](https://ebooks.iospress.nl/pdf/doi/10.3233/FAIA231122)

<a id="ref5"></a>
**[5]** Guizzardi, G. (2020). *Contributions to Ontology-Driven Conceptual Modeling Theory*. [Doctoral Habilitation Thesis, Free University of Bozen-Bolzano]. [**[Download]**](https://bia.unibz.it/esploro/outputs/doctoral/Contributions-to-Ontology-Driven-Conceptual-Modeling-Theory/991006425097401241?repId=12284268390001241)
