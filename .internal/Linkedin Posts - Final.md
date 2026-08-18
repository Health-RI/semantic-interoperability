# LinkedIn Posts

## POSTED

### Post 1: **Are you drowning in mappings and models?**

[Image]

Health data projects can involve FHIR profiles, the OMOP Common Data Model, openEHR archetypes and templates, and a mix of local schemas, tables, and mapping spreadsheets. Over time, each new project tends to add more transformations, more spreadsheets, and more custom bridges.

The **Health-RI Semantic Interoperability Initiative [1]** doesn't introduce yet another standard or data model. Instead, it makes the intended meanings behind existing ones explicit in a single, unifying upper-level ontology that acts as a *common semantic reference model*.

Rather than maintaining multiple pairwise mappings between standards, schemas, and data models, each concept is mapped once to this shared ontology. If system A and system B both align to this ontology, they can be confident they share the same interpretation of each concept and can therefore exchange each other's data with far less effort.

Browse the ontology and initiative overview, and reach out if you'd like to explore how this approach could clarify semantics in your health data project.

<!-- # HealthRI #SemanticInteroperability #ReferenceOntology #HealthDataStandards #HealthcareData #Interoperability #OntologyEngineering #FHIR #OMOP #openEHR -->

**References:**
[1] **Health-RI Semantic Interoperability:** https://w3id.org/health-ri/semantic-interoperability

## UNDER REVIEW

### Post 2: **Where Should Interoperability Start? High-Leverage Domains**

We cannot model everything. With limited time and resources, we must decide what to model and where to start — which concepts to align first to get the most impact from our efforts.
We move faster toward our interoperability goals when we focus on the high-leverage areas first: the concepts that many projects and standards share.

**The Health-RI Ontology [1]** prioritizes modeling areas around cross-cutting concepts (e.g., patient identity, sex & gender, diagnosis) where multiple standards intersect — so that reuse is immediate and implementation risk is lower.

Why this depth-over-breadth strategy works:

- **Early impact**: stabilize concepts most projects touch.
- **Clarity**: deep semantics prevent "label-only" misunderstandings.
- **Smoother upgrades**: well-defined cores reduce downstream breaking changes.

Help us prioritize what comes next: tell us which topic we should focus on to help you most by:

- Sharing your **top use case** (which domain blocks you today?).
- Proposing a small set of **core concepts** you need aligned now.
- Submitting them via our concept request form [2].

We'll then weigh demand, reuse potential, and dependencies when prioritizing what to model next.

<!-- # HealthRI #SemanticInteroperability #HealthData #Interoperability #OntologyEngineering #DataModeling -->

**References:**
[1] **Health-RI Semantic Interoperability Initiative**: <https://health-ri.github.io/semantic-interoperability/>
[2] **Initiative's concept request form**: <https://github.com/health-ri/semantic-interoperability/issues/new?template=concept-request.yml>

## TO BE SENT TO REVIEW

### Post 3: **Semantic Traceability: Keeping Meaning and Representation Aligned**

Is your data model specified using diagrams (like flowcharts or UML) and contains textual definitions? If so, can you really guarantee that everyone shares the same understanding of its concepts?
**Implementation shouldn't define meaning.** If your data model drifts from your conceptual model, your interoperability will fail in practice.

At the **Health-RI Semantic Interoperability Initiative [1]**, we start with OntoUML [2] to build a conceptual model that captures domain semantics for domain experts to validate. Then we encode the same concepts in OWL using gUFO [3] to create a computational ontology — so machines can process (and reason over) what experts agreed on, while keeping a traceable link between representations and meaning.

OntoUML is a highly expressive conceptual modeling language designed to capture rich domain distinctions precisely. Over its 20 years of use, it has demonstrated that ontologically well-founded models are more stable, reusable, and easier to align across projects and standards. gUFO is the OWL implementation that carries the same ontological commitments as OntoUML into computational ontologies, so reasoning and mappings stay connected to the original conceptualization.

**Why this separation between meaning and representation works:**

- **Clarity**: definitions are precise and not limited by computational requirements; OWL classes implement them.
- **Less drift**: the computational implementation explicitly traces back to the conceptual anchor, preserving semantic traceability along the stack.
- **Better reviews**: domain experts read diagrams; engineers and tools reason over OWL.

A tiny example of how this works can be seen here [4].
If you care about semantic interoperability, you need semantic traceability: start by making meaning explicit, then let your stacks implement it.

<!-- # HealthRI #SemanticTraceability #SemanticInteroperability #OntologyEngineering #ConceptualModeling #OntoUML #gUFO #OWL #KnowledgeRepresentation -->

**References:**
[1] **Health-RI Semantic Interoperability Initiative**: <https://w3id.org/health-ri/semantic-interoperability>
[2] **OntoUML**: <https://ontouml.org/>
[3] **gUFO**: <https://nemo-ufes.github.io/gufo/>
[4] **Example**: <https://health-ri.github.io/semantic-interoperability/method/mapping-strategy/#conceptualization-implementation-and-mapping>

### Post 4: **How to Define Your Ontology Terms (and why mapping to HRIO matters)**

A black screen with green text

AI-generated content may be incorrect.
If you can't say exactly what a term means, you can't safely reuse it across projects. For semantic interoperability, "what does this term mean?" must have a precise, inspectable answer.

The **Health-RI Ontology (HRIO)** provides that shared meaning layer: a gUFO-based OWL ontology with rich scope notes and a conceptual reference model for health and life sciences.

**What you can rely on:**

- A **reference ontology** (`hrio:`) with well-documented concepts for core domains (e.g. conditions, sex & gender, diagnostics).
- A **mapping vocabulary** (`hriv:`) designed for aligning local terms to HRIO meanings, either embedded in your ontology or via non-invasive SSSOM mappings.
- A published **SSSOM mapping set** showing concrete examples of local terms aligned to `hrio:` using `hriv:` properties.

**How to adopt (quick start):**

1) **Pick** a local term that needs clearer semantics.
   Choose a column header, code, or class in your ontology where people routinely ask "what does this actually mean?".
2) **Select** the closest HRIO meaning.
   Find the `hrio:` class that best represents the intended meaning of your term using the online specification browser.
3) **Attach** a meaning-level relation.

- Use `hriv:hasExactMeaning` when your term is meant to exactly denote that HRIO meaning.
- Use `hriv:hasBroaderMeaningThan` or `hriv:hasNarrowerMeaningThan` when your term is more generic or more specific than the HRIO class.

Declare this as an RDF triple (in your ontology or in a SSSOM mapping file) so consumers can see, query, and reason over the link.
Once you add these links, each local term clearly points to a specific HRIO concept. Others now can see exactly what you mean, without you having to redesign your whole model.

**Call to action:**
In your next ontology or data model, pick one ambiguous local term and link it to HRIO using an `hriv:` relation. Treat that as your semantic "unit test": if others can understand and reuse the term after its relation with HRIO, you're on the right track. Share any gaps or missing concepts you encounter so they can be considered for future HRIO and mapping updates.

<!-- # HealthRI #SemanticInteroperability #OntologyEngineering #ReferenceOntology #Semantics #SemanticMapping #HRIO #SSSOM #HealthData #SemanticWeb -->

**References:**

- Health-RI Semantic Interoperability Initiative — Overview: <https://w3id.org/health-ri/semantic-interoperability>
- Health-RI Ontology — Specification: <https://health-ri.github.io/semantic-interoperability/ontology/specification-ontology.html>
- Health-RI Mapping Vocabulary — Specification: <https://health-ri.github.io/semantic-interoperability/method/specification-vocabulary.html>

## IN PROGRESS - Add image and send to review

### Post 5: **Not just a match: using the Health-RI Mapping Vocabulary to make meaning explicit**

Most mappings say *"these terms match"*. For semantic interoperability, that's not enough — you need to say **what kind of match** and **what you intend them to mean**.

SKOS mapping properties (`skos:exactMatch`, `skos:broadMatch`, `skos:narrowMatch`) are great for aligning concept schemes, but they're intentionally lightweight: they don't distinguish definitional links from approximations, nor do they tie mappings explicitly back to your conceptual model. For example, `skos:exactMatch` only says that two concepts are sufficiently similar that they can be used interchangeably in many contexts; it does not explain what underlying meaning each concept is supposed to represent.

That's why we use the **Health-RI Mapping Vocabulary (`hriv`) [1]**, developed within the **Health-RI Semantic Interoperability Initiative [2]**: a meaning-level mapping layer that connects local expressions (e.g., column headers, codes, ontology terms) in your models to well-founded, precisely defined reference meanings in the Health-RI Ontology (`hrio:`) [3], which always acts as the mapping target. In other words, `hriv:` mappings are always stated from your model to `hrio:` (never the other way around), making explicit the representation–meaning link for your concepts.

With three principal relations:

- `hriv:hasExactMeaning` — your term is **fully equivalent in meaning** to the chosen `hrio:` concept (its semantics are defined by that meaning, without asserting `owl:equivalentClass`).
- `hriv:hasBroaderMeaningThan` — your term has a **broader meaning** than the `hrio:` concept (it includes that concept and possibly more).
- `hriv:hasNarrowerMeaningThan` — your term has a **narrower meaning** than the `hrio:` concept (it captures a more specific notion).

This lets us:

- Keep **meaning and representation traceable** from OntoUML through OWL to external models.
- **Preserve local schemas** while making each term's intended meaning explicit.
- Automatically **entail SKOS mappings** (via `rdfs:subPropertyOf`), so tools still see `skos:exactMatch`, `skos:narrowMatch`, and `skos:broadMatch` where expected.

Tiny example:

- If an external ontology defines `ont:Human` with the same intended meaning as `hrio:Person`, you can assert: `ont:Human hriv:hasExactMeaning hrio:Person .`
- If an external ontology defines `ont:Animal` for both humans and non-human animals, you use: `ont:Animal hriv:hasBroaderMeaningThan hrio:Person .`

In both cases, the mapping is explicit about **how** meanings relate, and a reasoner can derive the corresponding SKOS mapping automatically.

**Call to action:**
Pick one ambiguous term in your model, find the closest `hrio:` concept, and assert the minimal `hriv:` relation (`hasExactMeaning`, `hasBroaderMeaningThan`, or `hasNarrowerMeaningThan`) that reflects your intent. Share a tricky term pair in the comments and we'll suggest how you could align it using `hriv:`.

<!-- # HealthRI #HealthRIMappingVocabulary #SemanticInteroperability #SemanticTraceability #OntologyEngineering #SemanticMapping #HRIO #HRIV #SKOS #SSSOM -->

**References:**

[1] **Health-RI Mapping Vocabulary**: <https://health-ri.github.io/semantic-interoperability/method/specification-vocabulary.html>
[2] **Health-RI Semantic Interoperability Initiative**: <https://w3id.org/health-ri/semantic-interoperability>
[3] **Health-RI Ontology (HRIO)**: <https://health-ri.github.io/semantic-interoperability/ontology/documentation/>

### Post 6: **Pairwise Mappings Don't Scale — From O(N²) to O(N) with a Semantic Hub**

Most projects still solve the *same* mapping problem over and over. Every time you adopt a new standard, you shouldn't have to rebuild all your mappings from scratch.

Suppose you have **N** standards S₁ … Sₙ. The usual approach is to define pairwise mappings between every pair of standards: {S₁ ↔ S₂, S₁ ↔ S₃, …, Sᵢ ↔ Sⱼ, …, Sₙ₋₁ ↔ Sₙ}

That can grow to **N × (N − 1) / 2** mappings — quadratic complexity. If you already have N standards and add one more, the new standard introduces **up to N additional alignments** to define, test, and maintain.

Adopting the semantic backbone provided by the **Health-RI Semantic Interoperability Initiative [1]**, you switch to a *hub-and-spoke* semantic model. Conceptually:

- For each standard Sᵢ, you define a mapping function *mᵢ: Sᵢ → HRIO*, where HRIO is the **Health-RI Ontology [2]**, and you express those mappings using mapping properties from the **Health-RI Mapping Vocabulary [3]**.
- When terms from Sᵢ and Sⱼ map to the same `hrio:` concept *c*, they are semantically aligned via *c* without a direct Sᵢ ↔ Sⱼ mapping row.

Instead of maintaining up to **N × (N − 1) / 2** pairwise mappings, you maintain **N mappings into a shared meaning space**. **Complexity drops from O(N²) to O(N)**, and each new standard requires only one additional mapping set (its own Sᵢ → HRIO mapping).

If you care about long-term interoperability across many standards, you want a **semantic hub**, not an ever-growing web of pairwise patches.

**Call to action:**
Make a quick inventory: how many standards do you use today, and how many pairwise mappings are you maintaining? How much effort has gone into designing, validating, and maintaining those mappings? Would replacing them with a single semantic hub and one mapping set per standard help you? If so, let us know via the contribution forms on our site: <https://health-ri.github.io/semantic-interoperability/contributing/>

<!-- # HealthRI #SemanticInteroperability #OntologyEngineering #HealthDataStandards #SemanticHub #HRIO #HRIV #SSSOM -->

**References:**

[1] **Health-RI Semantic Interoperability Initiative**: <https://w3id.org/health-ri/semantic-interoperability>
[2] **Health-RI Ontology (HRIO)**: <https://health-ri.github.io/semantic-interoperability/ontology/documentation/>
[3] **Health-RI Mapping Vocabulary**: <https://health-ri.github.io/semantic-interoperability/method/specification-vocabulary.html>

### Post X: **Call for Community Review: Sex and Gender Ontology**

<!-- ADD IMAGE -->

Semantic interoperability is not just a technical challenge—it shapes how data is interpreted when moving between hospitals and registries, with direct consequences for people's lives.

If we want this data to be reusable and trustworthy, we need a common semantic solution that people can understand and rely on. Within the **Health-RI Semantic Interoperability Initiative**, we are developing our ontology for the community and with its involvement. In that spirit, we invite you to critically assess the ontology's Sex and Gender package so it can become a trusted collective asset.

**Contributing is simple:** look at the model and its documentation and tell us what seems unclear, incorrect, missing, or misleading. Whether you are a sex and gender expert or an ontologist, **any contribution is welcome**.

All instructions for participating in this external review are available at:
https://health-ri.github.io/semantic-interoperability/contributing/call-for-community-review/#open-calls

We look forward to your feedback.

<!-- #HealthRI #SexAndGender #SemanticInteroperability #Ontology #HealthData #OpenScience -->