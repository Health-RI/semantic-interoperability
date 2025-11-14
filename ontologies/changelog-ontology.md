# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [1.1.1] - 2025-11-14

### Changed

- Updated UML note colors in the Visual Paradigm diagrams to align with the revised **Rules Policy** definitions:
  - Adjusted existing note color assignments to comply with the updated rule categories and definitions.
  - This is a **visual/editorial** update only and does **not** change the ontology’s logical content.

## [1.1.0] - 2025-11-12

### Changed

- Bumped ontology metadata:
  - `owl:versionInfo` **0.11.9 → 1.1.0**
  - `owl:versionIRI` **…/v0.11.9 → …/v1.1.0**
  - `dcterms:modified` **2025-10-29 → 2025-11-12**
  - `dcterms:conformsTo` artifacts updated to **…/v1.1.0/json** and **…/v1.1.0/vpp**.
- Reclassified **BirthRelatedLegislationRule**:
  - `rdf:type` **gufo:Kind → gufo:Category**
  - `rdfs:subClassOf` **gufo:IntrinsicMode → gufo:FunctionalComplex**
- Broadened the equivalence of **HumanCell**:
  - `owl:equivalentClass` now expresses **DiploidCell ⊔ HaploidCell ⊔ Polyploid** (previously **DiploidCell ⊔ HaploidCell**).
- Aligned administrative gender subproperty hierarchy (property specializations now inherit from the recognized-gender property):
  - `nonBinaryAdministrativeGenderInheresInPersonWithNonBinaryAdministrativeGender`: **subPropertyOf** `hasAdministrativeGender` → `administrativeGenderInheresInPersonWithRecognizedAdministrativeGender`
  - `femaleAdministrativeGenderInheresInPersonWithFemaleAdministrativeGender`: **subPropertyOf** `hasAdministrativeGender` → `administrativeGenderInheresInPersonWithRecognizedAdministrativeGender`
  - `maleAdministrativeGenderInheresInPersonWithMaleAdministrativeGender`: **subPropertyOf** `hasAdministrativeGender` → `administrativeGenderInheresInPersonWithRecognizedAdministrativeGender`
  - `personWithRecognizedLegalGenderInheresInLegalGender`: **subPropertyOf** `hasAdministrativeGender` → `administrativeGenderInheresInPersonWithRecognizedAdministrativeGender`
- Polished textual definitions (`rdfs:comment`) for **18** terms (no semantic change), including:
  - *Person, PhysicalDocument, DigitalDocument, Date, OffsetDateTime, Diagnosis, DiagnosedEntity, DiagnosingAgent, DiagnosticRelation, BirthNotification, KaryotypicalMale, KaryotypicalFemale, Chromosome, HealthcareDiagnosis, PsychologicalHealthCondition, NonHumanAnimal*, and others.

### Added

- Introduced class **Polyploid**:
  - `rdfs:label` “Polyploid”
  - `rdfs:subClassOf` **HumanCell**
  - Stereotyped as **gufo:SubKind** (declared as both `owl:Class` and `owl:NamedIndividual`).
- Introduced object property **hasAllosome**:
  - `rdfs:label` “has allosome”
  - `rdfs:domain` **Person**
  - `rdfs:range` **Allosome**
  - Stereotyped as **gufo:MaterialRelationshipType**.

## [0.11.9] - 2025-10-29

### Changed

- Completed the **UML Note Classification (color coding)** rollout:
  - Fixed remaining notes in Visual Paradigm diagrams that were not updated in the previous release.
  - Ensured all notes consistently follow the standardized categories (**SEMI**, **CNST**, **RATL**, **SCOP**, **TRAC**, **EXMP**, **TODO**) with the prescribed colors and formatting.

### Added

- Introduced **tagged values for versioning and validation control**:
  - Each package now includes tagged values for:
    - `introducedInVersion`
    - `lastChangedInVersion`
    - `lastPublishedInVersion`
    - `reviewedBy`
  - Enables precise lifecycle tracking and validation according to the *Ontology Lifecycle and Validation Policy*.

### Not serialized

- Tagged values and note color data are part of the `.vpp` (Visual Paradigm) model and are **not exported** to `.json` or `.ttl` artifacts.
  These remain **editor metadata** supporting governance and visual consistency.

## [0.11.8] - 2025-10-28

### Changed

- Applied the **UML Note Classification (color coding)** policy across the ontology diagrams in the Visual Paradigm model:
  - All notes now follow the standardized categories (**SEMI**, **CNST**, **RATL**, **SCOP**, **TRAC**, **EXMP**, **TODO**) with the prescribed colors and formatting.
  - This is a **visual/editorial** update only and does **not** change the ontology's logical content.

### Not serialized

- Note colors and formatting are editor metadata and are **not exported** to the `.json` or `.ttl` artifacts.
  They are visible only in the **`.vpp`** (OntoUML/Visual Paradigm) model.

## [0.11.7] - 2025-10-27

### Added

- Ontology metadata for release `0.11.7`:
  - `owl:versionIRI`, `owl:versionInfo`, `dcterms:modified`, and `dcterms:conformsTo` links to `v0.11.7/json` and `v0.11.7/vpp`.

- Documentation:
  - Additional `rdfs:comment` clarifications on `Date`, `Month`, and `OffsetDateTime` retained and cross-checked (field ranges, leap-year rules, offset semantics).

### Removed

- No classes were removed in this release.

## [0.11.6] - 2025-10-27

### Added

- Ontology metadata for release `0.11.6`:
  - `owl:versionIRI`, `owl:versionInfo`, `dcterms:modified`, and `dcterms:conformsTo` links to `v0.11.6/json` and `v0.11.6/vpp`.

- Temporal value model (refactor and extensions):
  - Introduced `OffsetDateTime` (as a `gufo:QualityValue`) with documented constraints for calendar fields, including explicit allowance of `second = 60` only to represent a leap second.
  - Introduced `Month` as an enumerated value type with individuals `January` … `December`.
  - New properties tied to the refactor:
    - `date` (object property; domain `OffsetDateTime`, range `Date`).
    - `utcOffsetMinutes` and `nanosecond` (data properties on `OffsetDateTime`).

- Documentation:
  - Rich `rdfs:comment` added for `OffsetDateTime` describing field ranges (year/month/day, leap-year rules, hour/minute/second, fractional second precision) and timezone offset format.

### Changed

- Temporal properties and ranges/domains aligned to the new model:
  - `start` / `end`: range changed from `Timestamp` to `OffsetDateTime`.
  - `hour`, `minute`, `second`: domain changed from `Timestamp` to `OffsetDateTime`.
  - `year`: domain changed from `Timestamp` to `Date`.
  - `month`: **now an object property** to `Month` (previously `xsd:int`).

- Diagnostic/sex-related formalizations:
  - Minor refinements to partitions/disjointness/equivalences across diagnostic outcomes (`Diagnosis` vs `NoDiagnosisOutcome`), karyotypical classes, and dimorphic characteristics; definitions tightened without changing intended semantics.

- Textual improvements:
  - Clarified wording in several `rdfs:comment` notes across diagnosing agents/persons, gender/sex facets, and health condition groupings for precision and consistency.

### Removed

- Legacy temporal artifacts deprecated by the refactor:
  - `day_1` and `month_1` (duplicate integer-valued properties on `Timestamp`).
  - The prior integer-valued `month` (`xsd:int`) property on `Timestamp` (fully replaced by the object property to `Month`).

## [0.11.5] - 2025-10-15

### Added

- Ontology metadata for release `0.11.5`:
  - `owl:versionIRI`, `owl:versionInfo`, `dcterms:modified`, and `dcterms:conformsTo` links to `v0.11.5/json` and `v0.11.5/vpp`.
- Diagnostic belief & assessment layer:
  - `Belief`, `DiagnosisSuspicion`, `DiagnosticAssessmentOutcome` (partition including `NoDiagnosisOutcome` and `Diagnosis`), `PositiveDiagnosisAssessment`, and `ConcludedDiagnosticRelation`.
  - `ProfessionalDiagnosingAgent` and `SelfDiagnosis` to capture professional vs. self-assessment contexts.
- Health condition origin refinements:
  - `AcquiredHealthCondition` and `CongenitalHealthCondition`, plus supporting `Condition`/`ConditionIndicator` scaffolding.
- Expanded commentary:
  - Rich `rdfs:comment` documentation added across agents, chromosomes/allosomes, diagnosis types, and person/role facets to clarify intended use and contrasts.

### Changed

- Clarified and consolidated definitions using `owl:equivalentClass` partitions (e.g., for `Allosome`, `DiagnosedEntity`, `DiagnosingAgent`, `HealthcareDiagnosis`, `HealthCondition`) without altering intended semantics.
- Textual improvements to multiple `rdfs:comment` notes for precision and consistency (e.g., administrative/legal gender recognition patterns, agent/document scopes).

### Removed

- No removals in this release; previous constructs are retained while documentation and partitions were refined.

## [0.11.3] - 2025-09-25

### Added

- Ontology metadata for release `0.11.3`:
  - `owl:versionIRI`, `owl:versionInfo`, `dcterms:modified`, and `dcterms:conformsTo` links to `v0.11.3/json` and `v0.11.3/vpp`.
- Administrative/Legal gender recognition model:
  - `AdministrativeGenderRecognizingOrganization` (role) with mediation to `AdministrativeGenderRecognition`.
  - `LegalGenderRecognizer` aligned as a subclass of `AdministrativeGenderRecognizingOrganization`.
  - `LegalGenderRecognitionDocument` (role mixin) mediating `LegalGenderRecognition` and specializing `AdministrativeGenderRecognitionDocument`.
  - New object properties: `createsOnBehalfOf` (agent → recognizing organization) and `parentOf` (person → person).
- Agent/document taxonomy:
  - `IndividualAgent` (category) introduced; `ArtificialAgent` and `Person` now refine under it.
  - `Document` now equivalent to `DigitalDocument ⊔ PhysicalDocument`; both classes added with Functional Complex grounding and updated comment.
- New/explicit `owl:equivalentClass` unions or partitions for:
  - `Allosome` (`AllosomeX ⊔ AllosomeY`), `DiagnosedEntity`, `DiagnosingAgent`,
    `DiagnosticAssessmentOutcome`, `HealthCondition`, `HealthcareDiagnosis` (three orthogonal partitions),
    `KnownOriginHealthCondition` (`Inherent ⊔ ExternallyCaused`),
    `PersonWithAssessedPhenotypicSex`, `PersonWithAssignedSexAtBirth`,
    `PersonWithRecognizedAdministrativeGender`, `PersonWithRecognizedLegalGender`,
    `Substantial`, `LivingPerson` (awareness and life-phase partitions), and `Person` (karyotype, sex-chromosome, life/death, and legal-gender facets).
- Additional `owl:AllDisjointClasses` axioms consistent with the above unions.

### Changed

- Broadened ranges:
  - `isBiologicalFatherOf` and `isBiologicalMotherOf` now range over `Person` (previously `Child`).
- Property alignment:
  - `legalGenderRecognitionMediatesLegalGenderRecognizer ⊑ recognizedBy` and
    `legalGenderRecognitionMediatesPersonWithRecognizedLegalGender ⊑ recognizes`
    (replacing prior subproperties under administrative-gender mediation).
- Person/agent hierarchy:
  - `Person` is now a subclass of `IndividualAgent`; `ArtificialAgent` refactored under `IndividualAgent` (instead of directly under Functional Complex).
  - `SelfAwarePerson` and `NonSelfAwarePerson` now specialize `LivingPerson` (previously under `Person`).
- Health condition partitions:
  - `EstablishedHealthCondition` explicitly partitioned by `Structural ⊔ NonStructural` and by `Traumatic ⊔ NonTraumatic` (clarified, preserving intent).
- Textual refinements:
  - Shortened/clarified `rdfs:comment` for `AdministrativeGender`.
- Consistency edits:
  - Normalized ordering of several `owl:unionOf` and `owl:AllDisjointClasses` lists (no semantic change intended).

### Removed

- `AdministrativeGenderRecognizer` (role) and related mediation restriction on `AdministrativeGenderRecognition` (superseded by recognizing organization pattern).
- `GenderRecognitionDocument` (kind) and its mediation restriction (replaced by `LegalGenderRecognitionDocument` role-mixin approach).
- Assertion `ArtificialAgent ⊑ gufo:FunctionalComplex` (replaced by alignment under `IndividualAgent`).

## [0.11.0] - 2025-09-11

### Added

- Ontology metadata for release `0.11.0`:
  - `owl:versionIRI`, `owl:versionInfo`, and `dcterms:modified`.
  - `dcterms:conformsTo` links to `v0.11.0/json` and `v0.11.0/vpp`.
- Prefix for gUFO: `ns1: <http://purl.org/nemo/gufo#>`.
- Time and date value model:
  - Classes: `Timestamp`, `Date`.
  - Datatype properties on `Timestamp`: `year`, `month_1`, `day_1`, `hour`, `minute`, `second`, `subsecond`, `timezone`.
  - Datatype properties on `Date`: `year_1`, `month`, `day`.
- Birth / death / kinship model:
  - Classes and roles: `PersonsBirth`, `PersonsDeath`, `PersonsDeathCause`, `PersonsDeathCauseType`, `ParentChildRelation`, `Offspring`, `BiologicalFather`, `BiologicalMother`, `DeadPerson`, `LivingPerson`, `Child`, `Adolescent`, `Adult`.
  - Object properties: `start`, `end`, `dateOfBirth`, `isBiologicalFatherOf`, `isBiologicalMotherOf`.
  - Qualified cardinality restrictions connecting persons, roles, relators, and events (e.g., `wasCreatedIn`, `wasTerminatedIn`, `mediates`, `manifestedIn`).
- New/explicit `owl:equivalentClass` unions for:
  - `Person`, `LivingPerson`, `AdministrativeGender`, `HealthcareDiagnosis`, `HumanCell`,
    `CellularEntity`, `CellularEntityDiagnosis`, `DiagnosedEntity`, `DiagnosingAgent`,
    `ExternallyCausedHealthCondition`, `NonInjuryHealthCondition`, `NonStructuralHealthCondition`,
    `PersonWithAssessedPhenotypicSex`, `PersonWithRecognizedAdministrativeGender`,
    `PersonWithRecognizedLegalGender`, `PersonWithRegularSexChromosome`, `PersonWithVariantSexChromosome`,
    `SexualDimorphicCharacteristic`, `VisualSexCharacteristic`, `Substantial`, `Animal`.
- Additional `owl:AllDisjointClasses` axioms aligning with the above unions.

### Changed

- Diagnostic modeling refactor (gUFO-aligned):
  - `DiagnosticMethod` reclassified from `gufo:Category`/`gufo:FunctionalComplex` to `ns1:Kind` and `ns1:ExtrinsicMode`, with a qualified restriction to `DiagnosticRelation` via `ns1:inheresIn`.
  - `DiagnosticRelation` now uses the inverse qualified restriction of `ns1:inheresIn` (replacing earlier `gufo:mediates` pattern).
- Normalized ordering of several `owl:unionOf` and `owl:AllDisjointClasses` lists for consistency (no semantic change intended).

### Removed

- Previous `DiagnosticMethod` axioms based on `gufo:Category`, `gufo:FunctionalComplex`, and `gufo:mediates`.
- Prior `DiagnosticRelation` restriction using `gufo:mediates`.

## [0.10.1] - 2025-09-10

### Added

- Multiple new ontology constructs introduced, including:
  - Additional health condition types and refinements of diagnostic categories
  - New generalization sets expanding classification coverage
  - Supplemental relations between diagnostic entities and health conditions

### Removed

- Deprecated constructs and outdated classification elements that overlapped with the new health condition and diagnostic modules.

### Changed

- Adjusted internal identifiers (`id` fields) to maintain serialization consistency after the additions and removals.
- Updated generalization structures to align with the refined health condition taxonomy.

## [0.9.2] - 2025-09-02

### Added

- Expanded the allowed `restrictedTo` values for several constructs:
  - Beyond `functional-complex`, now explicitly includes `collective`, `quantity`, `relator`, `intrinsic-mode`, `extrinsic-mode`, and `quality`.
- Introduced `restrictedTo` constraints to clarify permissible ontological kinds.

### Changed

- Updated `isExtensional` values from `null` to explicit `false` for improved clarity in multiple classes.
- Adjusted internal identifiers (`id` fields) for consistency across classes, relations, and generalizations.

### Fixed

- Corrected the stereotypes of three classes, changing them from `role` to `subkind` to better reflect their ontological nature.

## [0.9.1] - 2025-07-30

### Changed

- Updated internal identifiers (`id` fields) for multiple classes, relations, and generalizations to improve consistency in serialization and downstream processing. These changes do not affect the logical structure or semantics of the ontology.

### Fixed

- Corrected typographic artifacts in textual descriptions for sex and gender constructs that previously used escaped HTML-like formatting (`**<<mode>>**`, `**<<phase>>**`, etc.). These are now consistently rendered.
- Minor cleanup in markdown-style syntax within descriptions, ensuring accurate rendering in downstream documentation tools.

## [0.9.0] - 2025-07-30

### Added

- New textual descriptions were added to key sections of the ontology and diagrams, improving documentation and understandability:
  - Ontology-level description of sex and gender, distinguishing intrinsic and extrinsic modes and their role in formal assessment or self-identification.
  - Detailed diagram descriptions for:
    - **Sex at Birth**, **Karyotypical Sex**, **Phenotypic Sex**
    - **Legal Gender**, **Administrative Gender**, **Gender Identity**
    - Integrated overview diagram of all sex and gender modes
    - Biological **Sex** as a conceptual umbrella

### Changed

- Swapped internal identifiers of several classes and generalizations to align with structural or tooling needs. These include:
  - Various class IDs for `Person`, `Gender`, `Health Condition`, and diagnostic modules
  - Generalization and generalization set IDs (e.g., in "healthcare diagnosis types by use", "by focus", etc.)
- These identifier changes do not affect the semantic content of the model but improve consistency and traceability in tooling pipelines.

### Fixed

- Improved alignment and phrasing in existing class descriptions for **Gender** and **Sex**, especially in the documentation layer.

## [0.8.0] - 2025-07-30

### Added

- Introduced a new diagnostic module with comprehensive modeling of diagnostic types and roles, including:
  - `Healthcare Diagnosis`, `Clinical Diagnosis`, `Laboratory Diagnosis`, `Radiological Diagnosis`, `Administrative Coding Diagnosis`, `Epidemiological Diagnosis`, `Surveillance Diagnosis`, `Research Diagnosis`
  - Diagnosis roles such as `Diagnosed Biological Part`, `Diagnosed Specimen`, `Diagnosed Group`, and `Diagnosed Cellular Entity`
  - `Conclusive Diagnostic Assessment`, `Concluded Diagnostic Relation`, and other related constructs
- New taxonomy and generalization sets for diagnosis classification, including:
  - `healthcare diagnosis types by source`, `healthcare diagnosis types by focus`, `healthcare diagnosis types by use`, `types of diagnosed entities`, and `cellular entity diagnosis types`
- Introduced `Self-diagnosis`, `External Diagnosis`, and `Diagnosis Suspicion` as distinct classes
- New diagnostic relation: characterization between diagnosis suspicion and assessed condition
- Expanded health condition classification with:
  - `Traumatic Health Condition`, `Non-traumatic Health Condition`, `Risk-based Health Condition`, `Exposure-based Health Condition`, `Inherent Health Condition`, and `Injury`
- Introduced `Cellular Entity` and its states: `Living Cellular Entity`, `Dead Cellular Entity`
- New generalization sets for animal types, trauma-based health condition types, and cellular entity states

### Changed

- Replaced `Animal`, `Non-Human Animal`, `Living Animal`, and `Dead Animal` with an updated and more expressive `Cellular Entity` taxonomy
- Revised several stereotypes:
  - Changed various `subkind` and unnamed classes to proper `category`, `roleMixin`, or `phaseMixin` stereotypes
  - Updated `Health Condition` classes to clarify their nature (e.g., intrinsic vs extrinsic modes)
- Improved modeling coherence for diagnostic processes, replacing older concepts like `Antemortem Diagnosis` and `Postmortem Diagnosis` with more granular and categorized alternatives

### Removed

- Removed the entire `Animal` classification block including:
  - `Animal`, `Non-Human Animal`, `Living Animal`, `Dead Animal`
  - Their generalizations and generalization sets (e.g., `animal types`, `animal living state`)

## [0.7.0] - 2025-07-30

### Changed

- Reassigned internal OntoUML element identifiers to improve structural consistency and tooling traceability:
  - Multiple `id` values for classes, generalizations, and relations were systematically rotated or swapped.
  - These changes have no impact on the logical content or semantics of the ontology but support improved internal alignment.

### Removed

- Class: `Organization` (previously defined as a `kind`) was removed from the ontology.
  - It included a description as a structured group with roles, responsibilities, and formal authority.
  - If still needed, its usage should be reintroduced in future updates or considered as part of an external reference ontology.

## [0.6.0] - 2025-07-30

### Added

- Introduced new classes to represent administrative gender assignments:
  - `Person with Male Administrative Gender`
  - `Person with Female Administrative Gender`
  - `Person with Non-binary Administrative Gender`
  - `Male Administrative Gender`, `Female Administrative Gender`, and `Non-binary Administrative Gender`
- Added new generalizations and generalization sets:
  - Generalizations linking `Person with Administrative Gender` roles to `Person`
  - Generalizations linking administrative gender phases to the `Administrative Gender` category
  - Generalization sets:
    - `person's administrative genders` (complete, not disjoint)
    - `administrative gender types` (complete, disjoint)
    - `administrative gender characterization types` (complete, disjoint)
- Introduced three new `characterization` relations:
  - Each links one of the `Person with X Administrative Gender` roles with the corresponding `X Administrative Gender` phase
- Added names to several previously unnamed relations, such as `"has administrative gender"`

### Changed

- Swapped internal OntoUML element IDs to improve structural clarity and align with internal conventions. These changes affect class and generalization identifiers but not their semantic content.
- Improved the clarity of modeling administrative gender recognition as separate from legal or self-identified gender representations.
- Reorganized the ontology structure to accommodate the new administrative gender module while preserving backward compatibility.

### Fixed

- Corrected some inconsistencies in generalization references and alignment of identifiers for relations and generalizations across the administrative gender module.

## [0.5.2] - 2025-06-30

### Added

- Added detailed descriptions for multiple classes in the ontology, replacing previously null values to improve clarity and documentation quality.

### Changed

- Updated descriptions for:
  - Roles, relators, and categories related to sex and gender assignments and recognitions (e.g., Person with Assigned Sex at Birth, Legal Gender Recognizer, Administrative Gender Recognizer).
  - Core biological concepts such as Chromosome, Allosome, Human Cell, Karyotypical Sex, Phenotypic Sex, and Sex at Birth.
  - Traits and characteristic categories for sexual and visual dimorphic features.
  - High-level categories like Sex and Gender, including Legal, Administrative, and Identity forms.
  - General concepts including Person, Organization, Government, and Document.
- Improved consistency and clarity across all descriptions to support better understanding in administrative, legal, medical, and ontological contexts.

## [0.5.1] - 2025-06-30

### Added

- Class: `Sex` was introduced to the model.

### Removed

- Package: `Complementary`
- Classes: `Biological Sex Assigner`, `Biological Sex Assignee`, and `Biological Sex Assignment`
- Classes: `Social Gender` and `Administrative Gender`

### Changed

- Renamed `Phenotypic Sex Assignment` to `Phenotypic Sex Assessment`.
- Renamed `Phenotypic Sex Assigner` to `Phenotypic Sex Assessor`.
- Renamed `Phenotypic Sex Assignee` to `Person with Assessed Phenotypic Sex`.

## [0.4.0] - 2025-06-25

### Added

- New class: `Person with Assigned Legal Gender or Sex at Birth`
  - Serves as a common superclass for `Person with Legal Gender` and `Person with Assigned Sex at Birth`
- New generalization set: `assigned legal gender or sex at birth` (complete, disjoint), including:
  - `Person with Assigned Legal Gender or Sex at Birth`
  - `Person with Legal Gender`
  - `Person with Assigned Sex at Birth`
- New mediation relations:
  - Between `Birth Notification` and `Person with Assigned Legal Gender or Sex at Birth`
  - Between `Birth Certificate` and `Person with Assigned Legal Gender or Sex at Birth`

### Changed

- Generalization structure revised to include new superclass for persons with assigned statuses
- Layout adjustments in diagrams to reflect new hierarchical relationships

## [0.3.0] - 2025-06-24

### Added

- New class: `Person with Unassigned Legal Gender or Sex at Birth`
  - Introduced as a superclass for both unassigned sex and unassigned legal gender persons.
- New generalization set: `legal gender or sex at birth` (complete, disjoint), covering:
  - `Person with Unassigned Legal Gender or Sex at Birth`
  - `Person with Unassigned Legal Gender`
  - `Person with Unassigned Sex at Birth`
- Mediation relations:
  - Between `Birth Notification` and `Person with Unassigned Legal Gender or Sex at Birth`
  - Between `Birth Certificate` and `Person with Unassigned Legal Gender or Sex at Birth`

### Changed

- Updated generalization structures to reflect the new shared superclass for unassigned status.
- Adjusted diagram layout to accommodate new shared superclass and its associated relations.

## [0.2.0] - 2025-06-23

### Added

- New package: `Legal Gender Model` including:
  - `Person with Unassigned Legal Gender`
  - `Person with Legal Gender`, with subtypes:
    - `Person with Male Legal Gender`
    - `Person with Female Legal Gender`
    - `Person with Other Legal Gender`
  - `Legal Gender Assignment`, `Government`, and `Birth Certificate`
- Generalization set: `legal gender` (complete, disjoint) under `Person with Legal Gender`
- Mediation relations:
  - Between `Legal Gender Assignment` and its participants (`Government` and `Person`)
- Material relation: `formalizes` between `Birth Certificate` and `Legal Gender Assignment`
- ComponentOf relations:
  - `Birth Certificate` composed of `Legal Gender Assignment`
- Dependency from the new `Legal Gender Model` package to the `Gender` package

### Changed

- Ontology version IRI updated to reflect new release
- Improvements in naming conventions and organization of existing generalization sets for clarity and consistency

### Fixed

- Minor alignment issues in model layout (diagrams were not affected)

## [0.1.0] - 2025-06-20

### Added

- Initial version of the Health-RI Ontology model.
- Two main packages: `Gender` and `Biology`, each with detailed OntoUML constructs.
- Core classes under `Gender`:
  - `Person with Unassigned Sex at Birth`
  - `Person with Assigned Sex at Birth`, including its specializations:
    - `Person with Male Sex at Birth`
    - `Person with Female Sex at Birth`
    - `Person with Indeterminate Sex at Birth`
  - `Sex at Birth Assignment`, `Healthcare Professional`, `Birth Notification`, and `Birth-related Legislation Rule`
- Core classes under `Biology`:
  - `Person`, `Human Cell`, `Chromosome`, `Allosome`, `Gamete`, `Diploid Cell`, `Haploid Cell`
  - Allosomal variants (`Allosome X`, `Allosome Y`) and karyotypical profiles:
    - `Regular Karyotypical Male`, `Regular Karyotypical Female`
    - `Variant Karyotypical Male`, `Variant Karyotypical Female`
    - `Karyotypically Indeterminate Person`
- Use of OntoUML stereotypes including `kind`, `subkind`, `role`, `relator`, `mode`, and relations such as `mediation` and `componentOf`.
- Several generalizations and complete disjoint generalization sets:
  - `sex at birth`, `karyotypical sex`, `variant karyotypic sex`, `regular karyotypical sex`, `allosome type`, and others.
- Two diagrams: `Sex at Birth` and `Chromosomes`, illustrating core structural aspects of the model.
