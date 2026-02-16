# Ontology Rules and SHACL Implementation

!!! warning "Disclaimer"

    While efforts have been made to ensure accuracy, the material in this page is still under review and may contain inaccuracies or omissions. Users are advised to interpret and apply the content with caution.

## Purpose & Scope

This document describes the rules of the Health-RI Ontology (HRIO) that, for each released version of HRIO, are implemented in SHACL. These ontology rules are of two types:

- Constraints, which validate data against the HRIO gUFO/OWL ontology produced from the HRIO OntoUML model (A-box quality checks), and
- derivation rules, which perform controlled rule-driven inferences to enrich data with safe, deterministic triples.

These rules are implemented in SHACL because the language is expressive for both constraint validation and rule-based derivation, and because the SHACL artifacts can be directly associated with the HRIO gUFO/OWL file.

We maintain a clear separation between:

- Conceptual intent in OntoUML (human-friendly constraints and rules, documented as notes), and
- Machine-checkable behavior in SHACL (executable shapes and rules over the RDF/OWL vocabulary).

OntoUML notes express the intended constraints and derivation rules. The corresponding `.shacl` file is the executable source of truth for their implementation for the matching ontology release.

The shapes graph is authored in Turtle and relies on SHACL Core and SHACL Advanced Features. Its contents evolve as the ontology grows. The conventions in this document describe how we implement these rules in SHACL for current and future ontology modules and domains.

## Attachment Strategy: HRIO OntoUML → gUFO → HRIO gUFO/OWL → SHACL

1. **Conceptual authoring in HRIO OntoUML (Visual Paradigm)**

    - Constraints and derivation rules are specified as notes attached to classes, relations, or diagrams.
    - Notes use tags such as `CNST (ShortName):` and `DRIV (ShortName):`, followed by a precise natural-language description.

1. **OWL export to HRIO gUFO/OWL**

    - The HRIO OntoUML model is exported to OWL as HRIO gUFO/OWL, following gUFO patterns for types, relators, roles, situations, etc.

1. **SHACL authoring over the released OWL vocabulary**

    - SHACL shapes and rules are authored only over IRIs present in the released HRIO gUFO/OWL files.
    - No SHACL artifact references internal OntoUML identifiers or unversioned/pre-release IRIs.

1. **Execution over published HRIO gUFO/OWL**

    - Shapes target IRIs in the released ontology namespace and reuse `gufo:` IRIs where relevant.
    - Validation and rule materialization operate on datasets aligned to HRIO gUFO/OWL.

### Policy

- We use the HRIO base IRI (`hrio:`) for ontology classes and properties.
- We use `gufo:` for gUFO classes and properties (e.g., relator and role patterns).
- We use `rdf:`, `rdfs:`, `owl:`, `xsd:`, and `sh:` in line with SHACL Core and SHACL-AF standards.

## Mapping OntoUML Notes to SHACL Artifacts

### In the OntoUML Model

Executable constraints (`CNST`) and derivation rules (`DRIV`) appear as textual notes anchored to classes or relations, as defined in [Ontology Note Classification and Visual Conventions](./ontology-notes-policy.md).

For each note with executable intent, we create one top-level `sh:NodeShape` with:

- `sh:name` – a short name matching the note's `(ShortName)`;
- `sh:description` – a natural-language paraphrase;
- one or more targets (`sh:targetClass`, `sh:targetSubjectsOf`, `sh:targetObjectsOf`).

Constraint rules are implemented as validation shapes, which may contain:

- SHACL-SPARQL queries via `sh:sparql`, or
- property constraints via `sh:property`.
    - `sh:severity` and `sh:message` typically appear inside the relevant property constraint.

Derivation rules are implemented as rule shapes, which include:

- a `sh:rule` element (`sh:TripleRule` or `sh:SPARQLRule`).
- No validation properties (`sh:severity`, `sh:message`) are used in rule-only shapes.

We may optionally add metadata such as:

- `rdfs:label` aligned with `sh:name`;
- `dct:identifier` for stable cross-system identifiers.

## Authoring Conventions: Constraints (Validation Shapes)

### Targets

In our SHACL shapes for constraints:

- We use `sh:targetClass` when constraints apply to instances of a class.
- We use `sh:targetSubjectsOf` / `sh:targetObjectsOf` when targeting occurrences of a property.
- For global or cross-class patterns, we use SHACL-SPARQL (`sh:sparql`).

### Property Constraints

For property-level validation:

- We define property-level validation inside `sh:property` blocks.
- We use `sh:path` to identify the validated property.
- We rely primarily on core SHACL constraints, including:
    - `sh:minCount`, `sh:maxCount`,
    - `sh:qualifiedMinCount`, `sh:qualifiedMaxCount`,
    - `sh:class`, `sh:datatype`, `sh:nodeKind`, `sh:in`, `sh:pattern`, etc.

Validation messages are concise and describe the issue from the focus node's perspective.

## Authoring Conventions: Derivation Rules

### When We Use Rules

In our SHACL artifacts, derivation rules provide deterministic, local inferences that:

- eliminate repetitive or boilerplate assertions implied by ontology semantics, and
- create derived relationships that simplify data access and querying.

Our guidelines are:

- We prefer `sh:TripleRule` for direct, pattern-based triple creation.
- We use `sh:SPARQLRule` for conditions involving joins, filters, or multi-step logic.
- Our derivation rules are idempotent, non-destructive, and compatible with ontology disjointness constraints.

## Practices We Follow and Avoid

### What We Do

In our SHACL shapes and rules, we:

- only use released HRIO and gUFO IRIs;
- keep each shape or rule single-purpose, with clear naming and description;
- prefer SHACL Core features and use SPARQL only where needed;
- design rules to be safe and aligned with the ontology's logical constraints.

### What We Avoid

We do not:

- express ontology (T-box) changes as SHACL rules;
- depend on the order of execution across shapes;
- materialize triples that violate disjointness or other logical axioms;
- reference editor-internal or pre-release IRIs.
