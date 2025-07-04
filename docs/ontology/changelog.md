# Changelog

All notable changes to this project are documented in this file.

This changelog follows the [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) format and reflects the **adapted semantic versioning** strategy defined in the repository's documentation:

**Version format**: `<major>.<minor>.<patch>`

- **Major** versions represent conceptual milestones or structural overhauls. These are the only versions that trigger formal **releases**, are considered **stable**, and receive a corresponding published specification webpage.
- **Minor** versions include additions, refinements, or reorganizations that preserve semantic compatibility.
- **Patch** versions provide small corrections or clarifications (e.g., label adjustments, comment improvements) that do not affect conceptual structure.

The repository uses a **fast versioning strategy**: new versions are made available in the `/ontology` folder as soon as possible, even if they present minor completeness or consistency issues. This ensures early access and traceability, while formal stability is guaranteed only for major versions.

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

## [0.5.2] - 2025-07-01

### Added

- New **Package**:

  - _Auxiliary_ package to hold supporting concepts.

- New **Classes**:

  - _Legal Gender_ (subkind of Administrative Gender)
  - _Gender Identity_ and its phases:
    - Male Gender Identity
    - Female Gender Identity
    - Non-binary Gender Identity
  - _Person with Recognized Legal Gender_
  - _Person with Recognized Administrative Gender_
  - _Administrative Gender Recognizer_ (role)
  - _Administrative Gender Recognition_ (relator)
  - _Administrative Gender_ (mode)
  - _Person Without Legal Gender_
  - _Person's Sex and Gender_ (category)

- **Generalizations** and **Generalization Sets**:

  - New hierarchies linking _Gender Identity_ phases to _Gender Identity_
  - Added generalizations connecting _Administrative Gender_ subkinds and roles
  - Introduced _gender identity types_ generalization set (complete, disjoint)

- **Relations**:

  - New characterization and mediation relations linking persons to their administrative, legal, and gender identity classifications.
  - Added properties with correct cardinalities to support these relations.

- **Diagram**:
  - _Administrative-Legal Gender_ diagram placeholder added.

### Changed

- Many **descriptions** were added to previously empty class definitions, improving semantic clarity:

  - For example, _Sex at Birth_, _Phenotypic Sex_, _Karyotypical Sex_, _Assigned Sex at Birth_, _Healthcare Professional_, _Birth Record_, _Legal Gender Recognition_, and many others now have clear, detailed descriptions.
  - These changes improve documentation for users and implementers.

- Various **names and stereotypes** were adjusted for consistency and correctness:

  - _Assigned Sex at Birth_ renamed to _Sex at Birth_, now a **subkind**.
  - _Legal Gender Recognition_ stereotype changed from **relator** to **subkind**.
  - _Legal Gender Certificate_ stereotype corrected from **subkind** to **kind**.
  - _Document_ stereotype adjusted from **kind** to **category**.

- **Removed**:

  - _Complementary_ package.
  - _Biological Sex Assignment_ classes and related mediation relations (including _Biological Sex Assigner_ and _Assignee_ roles).
  - _Legal Gender_, _Biological Sex_, and _Social Gender_ classes were removed and restructured.
  - Obsolete generalizations supporting these now-removed classes.

- **Refactored**:
  - ID values for many classes and properties were reorganized for consistency.
  - Cardinalities on properties were reviewed and corrected (e.g., from `0..1` to `1..*` where appropriate).

### Notes

This release reflects a **significant conceptual reorganization** of the ontology to:

- Clarify the distinction between biological, administrative, and self-identified dimensions of sex and gender.
- Better support legal and administrative use cases, including formal recognition processes.
- Improve semantic precision and documentation quality.

## [0.6.0] - 2025-07-02

### Added

- New classes to model administrative gender roles and designations:
  - _Person with Male Administrative Gender_
  - _Person with Female Administrative Gender_
  - _Person with Non-binary Administrative Gender_
  - _Male Administrative Gender_
  - _Female Administrative Gender_
  - _Non-binary Administrative Gender_
- New generalizations linking these classes to their respective superclasses.
- Two new generalization sets:
  - _person's administrative genders_ (incomplete, overlapping)
  - _administrative gender types_ (complete, disjoint)
- New characterization relations connecting persons to their administrative gender classifications.
- A new generalization set _administrative gender characterization types_ grouping characterization relations by gender type.

### Changed

- Updated various internal IDs for consistency.
- Corrected property cardinalities and read-only settings on characterization relations.
- Improved naming of certain properties, including renaming one to **"has administrative gender"** to clarify its role.
