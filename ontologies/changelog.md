# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),  
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
