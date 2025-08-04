# Semantic Mapping Strategy

!!! warning "Disclaimer"
    While efforts have been made to ensure accuracy, the material in this page is still under review and may contain inaccuracies or omissions. Users are advised to interpret and apply the content with caution.

## Model‑Driven Techniques: MDA, MDD, and MDE

The **[Model‑Driven Architecture (MDA)](http://www.omg.org/mda/)**, defined by the Object Management Group (OMG), is an architectural framework that structures system modeling into abstract layers—promoting interoperability, portability, and reuse by separating domain concerns from technical implementation [1,2].  

- **Model‑Driven Development (MDD)** denotes development processes guided by high‑level models; MDA is one such OMG‑conforming realization [2].  
- **Model‑Driven Engineering (MDE)** is an overarching paradigm including model creation, transformation, code generation, reverse-engineering, and lifecycle evolution [2].

OMG defines three main abstraction layers [1,2]:

- **Computation‑Independent Model (CIM)**: captures domain context and system requirements in business terms, without specifying implementation structure.  
- **Platform‑Independent Model (PIM)**: defines structural and behavioral aspects—such as classes and relationships—in a technology-agnostic way, without committing to any particular implementation platform.  
- **Platform‑Specific Model (PSM)**: refines the PIM with technology‑specific information (e.g. database schemas, APIs, frameworks) to enable implementation.

## CIM and PIM in Our Ontology Artifacts

Within our semantic interoperability framework:

- The **OntoUML ontology** sits at the CIM layer: it defines conceptual domain entities and relationships grounded in the Unified Foundational Ontology (UFO) [3].  
- The **gUFO representation** (OWL‑based lightweight implementation of UFO) resides at the PIM layer: it expresses those same concepts as an executable OWL 2 DL ontology, suitable for reasoning and integration with Semantic Web tools [3].

![Mapping from OntoUML at CIM to gUFO/OWL at PIM](./assets/images/mapping-cim-pim.png)  
*Figure 1: OntoUML at the CIM layer defines the semantics that are implemented in gUFO/OWL at the PIM layer.*

This visual clarifies that OntoUML provides the conceptual meaning, which the gUFO artifact operationalizes—while preserving semantic integrity across layers.

### Roles of the Artifacts

| Artifact   | Layer | Purpose                                                                  |
| ---------- | ----- | ------------------------------------------------------------------------ |
| OntoUML    | CIM   | Domain-level clarity, conceptual validation, communication among experts |
| gUFO (OWL) | PIM   | Machine-readable semantics, reasoning support, tool interoperability     |

Maintaining both artifacts ensures clear traceability from domain concepts (OntoUML / CIM) to executable ontology structures (gUFO / PIM) [3].

## Semantic Reference: Defining CIM-to-PIM Semantics

In the Health‑RI architecture, every class in the gUFO ontology (PIM) is implicitly semantically defined by its counterpart in OntoUML (CIM). For example, the class `health‑ri:Person` in gUFO borrows its semantics from the `Person` class in the OntoUML model. Because the CIM is not computational, this semantic linkage remains implicit and is **not formally encoded** [3].

## Aligning Third‑Party Ontologies via SKOS Mapping

Our common reference model provides authoritative semantics to external concept definitions. When another ontology defines `onto:Person`, we interpret it as intended to match our `health‑ri:Person`. To make this relationship explicit, we assert a **[`skos:exactMatch`](https://www.w3.org/TR/skos-reference/#mapping)** link from the third‑party concept to ours—signifying that the external concept carries the same meaning.

![Deriving OntoUML semantics via mapping to Health‑RI reference model](./assets/images/mapping-cim-pim2.png)  
*Figure 2: If an external ontology defines `External:Patient` which we map via `skos:exactMatch` to `health‑ri:Patient`—and `health‑ri:Patient` implements OntoUML `Patient`—then we can interpret `External:Patient` as conveying the same semantics as the `OntoUML Patient` concept, by transitivity of the mapping.*

### SKOS Mapping Properties for Cross‑Scheme Alignment

The [SKOS](https://www.w3.org/TR/skos-reference/) standard provides a set of mapping properties designed for expressing alignments between concepts in different concept schemes (e.g. external vocabularies and our Health‑RI ontology). The principal properties are: `skos:exactMatch`, `skos:closeMatch`, `skos:broadMatch`, `skos:narrowMatch`, and `skos:relatedMatch`.

#### Our Choice: `skos:exactMatch`

- While SKOS does not enforce logical equivalence in OWL terms, `skos:exactMatch` is intended to indicate that two concepts refer to the same real-world entity. We adopt `skos:exactMatch` to indicate that a third‑party concept was intended to denote the same meaning as our reference concept.
- This choice is based on practical considerations:
  - `exactMatch` is widely recognized and adopted within linked data and vocabulary alignment practices.
  - It interoperates effectively across ontology tools and mapping workflows.
- We do **not assume inferential closure** (e.g. transitive consequences beyond the explicit mapping), preserving precision in semantic assignments.

![Cross-ontology mapping using skos:exactMatch and rdfs:subClassOf](./assets/images/example-mapping.png)  
*Figure 3: External ontologies (e.g., HealthCare and Veterinary) map their local concepts to reference concepts in the Health-RI Ontology via `skos:exactMatch` (red). These reference concepts are also semantically structured via `rdfs:subClassOf` (brown), enabling consistent classification across domains.*

This figure illustrates how concepts such as `hc:Patient` and `vet:Patient` are mapped to `hri:HealthcarePatient` and `hri:VeterinaryPatient` respectively. These are in turn subsumed by higher-level concepts like `hri:Human` or `hri:NonHumanAnimal`, ultimately aligning under `hri:Animal`. This modeling strategy ensures that semantic alignments preserve domain distinctions while enabling unified interpretation under a shared reference ontology.

## Summary of Semantic Alignment Strategy

- **OntoUML (CIM)** defines the authoritative semantics for PIM artifacts.  
- **gUFO (PIM)** encodes those semantics in an executable OWL ontology.  
- **External concepts** are mapped to our reference via `skos:exactMatch`, indicating shared meaning.  
- This enables reasoning from external definitions back to OntoUML semantics—even when external artifacts don't know about OntoUML directly.

## References

[1] Object Management Group. *[MDA Guide rev. 2.0](https://www.omg.org/cgi-bin/doc?ormsc/14-06-01)*. OMG Document ormsc/14-06-01, 2014.  

[2] Brambilla, M., Cabot, J., Wimmer, M. *Model-Driven Software Engineering in Practice*. Morgan & Claypool, 2017.  

[3] Guizzardi, G. *On Ontology, Ontologies, Conceptualizations and the Reality of Categories*. Applied Ontology, 16(2), 2021.  
