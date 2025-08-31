# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

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

## [0.7.0] - 2025-07-30

### Changed

- Reassigned internal OntoUML element identifiers to improve structural consistency and tooling traceability:
  - Multiple `id` values for classes, generalizations, and relations were systematically rotated or swapped.
  - These changes have no impact on the logical content or semantics of the ontology but support improved internal alignment.

### Removed

- Class: `Organization` (previously defined as a `kind`) was removed from the ontology.
  - It included a description as a structured group with roles, responsibilities, and formal authority.
  - If still needed, its usage should be reintroduced in future updates or considered as part of an external reference ontology.

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

## [0.9.1] - 2025-07-30

### Changed

- Updated internal identifiers (`id` fields) for multiple classes, relations, and generalizations to improve consistency in serialization and downstream processing. These changes do not affect the logical structure or semantics of the ontology.

### Fixed

- Corrected typographic artifacts in textual descriptions for sex and gender constructs that previously used escaped HTML-like formatting (`**<<mode>>**`, `**<<phase>>**`, etc.). These are now consistently rendered.
- Minor cleanup in markdown-style syntax within descriptions, ensuring accurate rendering in downstream documentation tools.

