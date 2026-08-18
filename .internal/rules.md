# SHACL Validation Shapes and Rules

## Purpose & scope

This document specifies how Health-RI publishes and maintains a SHACL **shapes graph** that:

- validates data against the **gUFO-based OWL ontology** produced from the OntoUML model (A-box quality checks), and
- performs controlled **rule-driven inferences** to enrich data with safe, deterministic triples.

We deliberately separate **conceptual intent** written in OntoUML (human-readable notes on diagrams) from **machine-checkable behavior** (SHACL). The OntoUML notes remain the authoritative human description; the `.shacl` file is the executable counterpart and the single source of truth for validation and rule execution.

## Terminology (used here)

- **Validation shapes**: SHACL node/property shapes that use core/SHACL-SPARQL constraints to validate RDF data.
- **Rules**: SHACL rules as defined in SHACL Advanced Features (AF). We support `sh:TripleRule` (preferred) and `sh:SPARQLRule` (when needed).

> In older prose you may see "constraints" (→ *validation shapes*) and "derivation rules" (→ *rules*).

## Attachment strategy: OntoUML → gUFO → SHACL

1) **Authoring** happens in OntoUML (Visual Paradigm) with notes that name and describe each rule in plain language.
2) **OWL export** is generated against **gUFO** (the implementation ontology), producing the public **gUFO-based Health-RI OWL** (HRIO).
3) **SHACL shapes** are authored **over the OWL vocabulary** (IRIs in the released ontology), not over OntoUML internal identifiers.
4) The shapes graph references released class/property IRIs (`hrio:`*, `gufo:`*, etc.), ensuring the executable constraints and rules apply to the **published gUFO-based ontology**.

## File, namespaces, and metadata

**File**: one distribution file per ontology version, extension **`.shacl`** in Turtle syntax.

Recommended header (template):

```turtle
@prefix sh:   <http://www.w3.org/ns/shacl#> .
@prefix dash: <http://datashapes.org/dash#> .
@prefix dct:  <http://purl.org/dc/terms/> .
@prefix pav:  <http://purl.org/pav/> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix hrio: <https://w3id.org/health-ri/ontology#> .
@prefix gufo: <http://purl.org/nemo/gufo#> .
@prefix ex:   <https://w3id.org/health-ri/examples#> . # for illustrations only

[] a owl:Ontology ;
   dct:title "Health-RI Ontology — SHACL Shapes and Rules" ;
   pav:version "1.1.0" ;
   owl:versionIRI <https://w3id.org/health-ri/ontology/v1.1.0/shacl> ;
   dct:modified "2025-11-12" ;
   dct:conformsTo <https://www.w3.org/TR/shacl/> , <https://www.w3.org/TR/shacl-af/> ;
   dct:isPartOf  <https://w3id.org/health-ri/ontology/v1.1.0/ttl> .
```

### Namespace policy

- Use `hrio:` IRIs from the released ontology for all targets/paths.
- Reuse `gufo:` IRIs only when a shape/rule addresses gUFO-level contracts (e.g., generic relator/situation patterns).

## Mapping OntoUML notes to SHACL artifacts

**In the model (OntoUML):**

- Every rule that has an executable counterpart starts with the **CNST** tag and carries a **short Name** in parentheses, followed by the plain-language description, e.g. `CNST (OneActiveIdentifier): …`.
- The note is **anchored** to the governed element(s) (class, relation, or diagram-level scope).

**In the `.shacl` file:**

- Create one top-level resource per rule/shape with:
  - `rdfs:label` = the **Name** from the note.
  - `dct:description` = the note's **plain description** (verbatim or lightly edited).
  - `dct:identifier` = a stable **ID** (e.g., `HRIO-CNST-OneActiveIdentifier`).
  - `sh:message` = user-facing failure message (short imperative).
  - `sh:severity` = `sh:Violation` (default) or `sh:Warning` (when advisory).
- For a **validation** constraint, implement as `sh:NodeShape` (with nested `sh:property` where applicable).
- For a **rule**, attach `sh:rule` (prefer `sh:TripleRule`; fall back to `sh:SPARQLRule` when construct logic needs SPARQL).

## Authoring conventions (validation shapes)

### Targets

- Prefer `sh:targetClass hrio:Class` for class-scoped constraints.
- Use `sh:targetSubjectsOf hrio:property` / `sh:targetObjectsOf` when the scope is "any subject/object using property P".
- For data-wide guards (rare), use a named target node set with SHACL-SPARQL `SELECT`.

### Property constraints

- Put property checks under a **class-scoped** `sh:NodeShape` via `sh:property` with `sh:path hrio:yourProperty`.
- Use `sh:minCount`, `sh:maxCount`, `sh:datatype`, `sh:class`, `sh:nodeKind`, `sh:in`, `sh:pattern`, `sh:uniqueLang`, etc.
- Message style: imperative, terse, single responsibility (one check → one message). Use `sh:order` to control display.

### Example (template)

```turtle
# CNST (OneActiveIdentifier)
hrio:OneActiveIdentifier
    a sh:NodeShape ;
    rdfs:label "OneActiveIdentifier" ;
    dct:description "Each X must have exactly one identifier whose status is Active." ;
    sh:targetClass hrio:X ;               # replace with the governed class IRI
    sh:severity sh:Violation ;
    sh:property [
        sh:path hrio:identifier ;         # replace with property IRI
        sh:minCount 1 ; sh:maxCount 1 ;
        sh:message "Provide exactly one identifier." ;
        sh:order 1
    ] ;
    sh:property [
        sh:path hrio:identifierStatus ;   # replace with property IRI
        sh:in ( hrio:Active ) ;
        sh:message "Identifier status must be Active." ;
        sh:order 2
    ] .
```

### Closed shapes (optional)

- Use `sh:closed true` and `sh:ignoredProperties` only for mature, well-bounded records.

## Authoring conventions (rules)

### When to use rules

- Deterministic, local inferences that (a) reduce boilerplate, or (b) materialize convenience classifications/links.
- Prefer **`sh:TripleRule`** for simple pattern → triple generation; prefer **`sh:SPARQLRule`** for complex constructs.

### Safety

- Rules **must not** assert T-box axioms; only A-box triples.
- Do not introduce contradictions with OWL reasoning; avoid generating inferred types that violate disjointness partitions.

### TripleRule example (template)

```turtle
# RULE (RecognizedAdminGenderRole)
hrio:RecognizedAdminGenderRole
    a sh:NodeShape ;
    rdfs:label "RecognizedAdminGenderRole" ;
    dct:description "If Y recognizes administrative gender for X, assert that X plays the role 'Person with Recognized Administrative Gender'." ;
    sh:targetSubjectsOf hrio:administrativeGenderRecognizedFor ;  # replace
    sh:rule [
        a sh:TripleRule ;
        sh:subject sh:this ;
        sh:predicate rdf:type ;
        sh:object hrio:PersonWithRecognizedAdministrativeGender     # replace
    ] .
```

### SPARQLRule example (template)

```turtle
# RULE (IsAdultByDate)
hrio:IsAdultByDate
    a sh:NodeShape ;
    rdfs:label "IsAdultByDate" ;
    dct:description "If birth date is known and age >= 18, assert type Adult." ;
    sh:targetClass hrio:Person ;
    sh:rule [
        a sh:SPARQLRule ;
        sh:construct """
          CONSTRUCT { $this a hrio:Adult . }
          WHERE {
            $this hrio:birthDate ?d .
            BIND(NOW() AS ?now)
            # Replace with your canonical age function/calculation
            FILTER ( YEAR(?now) - YEAR(?d) - IF (MONTH(?now)<MONTH(?d) || (MONTH(?now)=MONTH(?d) && DAY(?now)<DAY(?d)), 1, 0) >= 18 )
          }
        """
    ] .
```

## Severity & messaging

- Default `sh:severity` is **`sh:Violation`**. Use **`sh:Warning`** for advisory checks (e.g., completeness hints).
- `sh:message` is short, specific, and refers to **this** node ("Provide at least one …", "Value must be an IRI …").
- Add `dct:identifier` and optionally `dash:sourceConstraint` for cross-tool diagnostics.

## Module structure and ordering

Group shapes by package/scope to mirror OntoUML packages:

- Section comment: `### [Package Name] — Validation`
- Section comment: `### [Package Name] — Rules`

Use monotonically increasing `sh:order` within a node shape to control reporting order. Avoid interdependent shapes (no assumed execution order across node shapes).

## Minimal "how to run" (pySHACL)

```bash
# Validate (A-box) against HRIO shapes
python -m pyshACL -s health-ri-ontology.v1.1.0.shacl -m -i rdfs \
  -df turtle -sf turtle \
  -d your-data.ttl

# Materialize rules into a new graph (if your runner supports SHACL-AF rules)
python -m pyshACL -s health-ri-ontology.v1.1.0.shacl -r -m -i rdfs \
  -df turtle -sf turtle \
  -d your-data.ttl -o enriched-data.ttl
```

> Use the same **namespace IRIs** as in the released OWL; do not point shapes at pre-release or editor-internal IRIs.

## Worked "template" patterns

### Cardinality on relator participation

```turtle
# CNST (ExactlyOneParticipation)
hrio:ExactlyOneParticipation
  a sh:NodeShape ;
  rdfs:label "ExactlyOneParticipation" ;
  dct:description "Each X must participate in exactly one Y." ;
  sh:targetClass hrio:X ;
  sh:property [
    sh:path hrio:participatesIn ;  # replace with your relation
    sh:minCount 1 ; sh:maxCount 1 ;
    sh:message "Participate in exactly one Y."
  ] .
```

### Taxonomy disjointness (advisory check at data level)

```turtle
# CNST (MutuallyExclusiveLifeStages) — advisory
hrio:MutuallyExclusiveLifeStages
  a sh:NodeShape ;
  rdfs:label "MutuallyExclusiveLifeStages" ;
  sh:targetClass hrio:Person ;
  sh:severity sh:Violation ;
  sh:sparql [
    sh:message "A person cannot be both Child and Adult."
  ; sh:select """
      SELECT $this WHERE {
        $this a hrio:Child , hrio:Adult .
      }
    """ ] .
```

### Rule that materializes a convenience link

```turtle
# RULE (LinkToRecognitionDocument)
hrio:LinkToRecognitionDocument
  a sh:NodeShape ;
  rdfs:label "LinkToRecognitionDocument" ;
  dct:description "From recognition event E to its document D; assert E hrio:hasDocument D." ;
  sh:targetClass hrio:AdministrativeGenderRecognition ;  # replace
  sh:rule [
    a sh:SPARQLRule ;
    sh:construct """
      CONSTRUCT { $this hrio:hasDocument ?doc . }
      WHERE {
        $this hrio:recognizedBy ?agent .
        ?doc a hrio:AdministrativeGenderRecognitionDocument ;
             hrio:recordsRecognition $this .
      }
    """
  ] .
```

## Traceability

- Keep a **1:1 mapping** between OntoUML note names and SHACL resource labels.
- Record the mapping once per release in the changelog entry that introduces/changes the rule.
- Use `dct:identifier` as the stable cross-system key.

## Do's and Don'ts

### Do

- Target the **released** HRIO/gUFO IRIs.
- Prefer `sh:TripleRule` for maintainability.
- Keep each shape/rule single-purpose with a clear message.

### Don't

- Encode T-box (schema) changes as rules.
- Depend on execution order across node shapes.
- Hide breaking semantic changes under a Z bump.

## Distribution summary (v1.1.0)

- Shapes & rules file: **`health-ri-ontology.v1.1.0.shacl`**
- Version IRI: `…/v1.1.0/shacl`
- Targets: `hrio:` IRIs from `…/v1.1.0/ttl`; occasional `gufo:` patterns where appropriate
- PIDs: `/ontology/shacl` (latest), `/ontology/v1.1.0/shacl` (versioned)
