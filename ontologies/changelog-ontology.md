# Changelog

All notable changes to this project will be documented in this file. Entries are generated with automated support by comparing each ontology release against its immediate predecessor and summarizing the resulting changes.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [1.6.0] - 2026-02-10

### TL;DR

- Refactors the sex/gender model around a new **SexGender** backbone with explicit **Female / Male / NonBinarySexGender** and **Woman / Man / NonBinaryPerson** partitions.
- Replaces legacy sex-at-birth / phenotypic / karyotypic terms and bearer roles with new IRIs, updating dependent `owl:equivalentClass`, `rdfs:subClassOf`, and disjointness axioms.
- Updates release metadata to **1.6.0** and removes `skos:prefLabel` annotations for **242** terms (no semantic change, but may affect label-dependent consumers).

### Added

- Introduced a consolidated **SexGender** backbone (metamodelling via gUFO stereotypes: many terms are both `owl:Class` and `owl:NamedIndividual`):
  - **SexGender**: `rdf:type` `gufo:Category`; `rdfs:subClassOf` `gufo:Aspect`; `owl:equivalentClass` **Gender ⊔ Sex** and **Female ⊔ Male ⊔ NonBinarySexGender**.
  - **Female**, **Male**, **NonBinarySexGender**: `rdf:type` `gufo:Category`; `rdfs:subClassOf` **SexGender**; with `owl:equivalentClass` **FemaleGender ⊔ FemaleSex**, **MaleGender ⊔ MaleSex**, **NonBinaryGender ⊔ IndeterminateSex**.
  - **Woman**, **Man**, **NonBinaryPerson**: `rdf:type` `gufo:SubKind`; `rdfs:subClassOf` **Person**; with `owl:equivalentClass` **FemaleGenderPerson ⊔ FemaleSexPerson**, **MaleGenderPerson ⊔ MaleSexPerson**, **NonBinaryGenderPerson ⊔ IndeterminateSexPerson**.
- Added explicit sex-type specializations and person subkinds:
  - **FemaleSex**, **MaleSex**, **IndeterminateSex**: `rdf:type` `gufo:Category`; `rdfs:subClassOf` **Sex** (and **Female / Male / NonBinarySexGender** respectively).
  - **FemaleSexPerson**, **MaleSexPerson**, **IndeterminateSexPerson**: `rdf:type` `gufo:SubKind`; `rdfs:subClassOf` **Person** (aligned to **Woman / Man / NonBinaryPerson** respectively).
- Added explicit **sex-at-birth** taxonomy and bearer roles (metamodelling via gUFO stereotypes):
  - **SexAtBirthFemaleSex**, **SexAtBirthMaleSex**, **SexAtBirthIndeterminateSex**: `rdf:type` `gufo:SubKind`; `rdfs:subClassOf` **SexAtBirth** (+ aligned to corresponding **...Sex** and **Phenotypic...Sex**).
  - Bearer roles: **SexAtBirthAssignedPerson**, **SexAtBirthUnassignedPerson**, **SexAtBirthDeterminateSexPerson**, **SexAtBirthFemaleSexPerson**, **SexAtBirthMaleSexPerson**, **SexAtBirthIndeterminateSexPerson** (`rdf:type` `gufo:Role`).
- Added explicit **phenotypic sex** specializations and bearer role:
  - **PhenotypicFemaleSex**, **PhenotypicMaleSex**, **PhenotypicAmbiguousSex** (`rdf:type` `gufo:SubKind`).
  - **PhenotypicSexAssessedPerson** (`rdf:type` `gufo:Role`).
- Added explicit **karyotypic sex** specializations and person subkinds:
  - **KaryotypicSex**: `rdf:type` `gufo:Kind`; `rdfs:subClassOf` `gufo:IntrinsicMode` and **Sex**.
  - **KaryotypicFemaleSex**, **KaryotypicMaleSex** (`rdf:type` `gufo:SubKind`; `rdfs:subClassOf` **KaryotypicSex**).
  - **KaryotypicFemaleSexPerson**, **KaryotypicMaleSexPerson** (+ **RegularKaryotypical\*Person**, **VariantKaryotypical\*Person**) to represent karyotypic person partitions.
- Added **GenderModality** partition and supporting relationships:
  - **GenderModality**: `rdf:type` `gufo:Category`; `rdfs:subClassOf` **Gender**; `owl:equivalentClass` **Cisgender ⊔ Transgender**.
  - **Cisgender**, **Transgender**: `rdf:type` `gufo:Kind`; `rdfs:subClassOf` **GenderModality**.
  - **hasCause**, **hasCause_1** (`rdf:type` `gufo:MaterialRelationshipType`, `owl:ObjectProperty`): `rdfs:domain` **GenderModality**; `rdfs:range` **Sex** / **Gender**.
- Introduced **PreferredPronoun** (`rdf:type` `gufo:Kind`; `rdfs:subClassOf` `gufo:Quality`) to replace **PreferredGenderedPronoun** (see *Removed*).
- Introduced supporting modeling individuals:
  - **SexAxis**, **SexOutcome**, **GenderOutcome**, **SexGenderOutcome**, **SexGenderType**, **GenderContext** (`rdf:type` `owl:NamedIndividual`; `rdfs:subClassOf` **ConcreteIndividualType**).

### Changed

- **ontology** (`https://w3id.org/health-ri/ontology`)
  - `owl:versionInfo` **"1.5.0" → "1.6.0"**; `owl:versionIRI` **…/v1.5.0 → …/v1.6.0**.
  - `dcterms:modified` **2026-02-04 → 2026-02-10**.
  - `dcterms:conformsTo` links updated to **…/v1.6.0/json** and **…/v1.6.0/vpp**.
  - Added `dcterms:contributor` annotations.
- Consolidated core sex/gender hierarchy and typing:
  - **Sex**, **Gender**: `rdfs:subClassOf` **`gufo:Aspect` + `gufo:ExtrinsicMode` → SexGender**.
  - **Sex**: added `owl:equivalentClass` **FemaleSex ⊔ IndeterminateSex ⊔ MaleSex**.
  - **FemaleGender**, **MaleGender**, **NonBinaryGender**: added `rdfs:subClassOf` **Female / Male / NonBinarySexGender**.
  - **FemaleGenderPerson**, **MaleGenderPerson**, **NonBinaryGenderPerson**: added `rdfs:subClassOf` **Woman / Man / NonBinaryPerson**.
  - **SelfDesignatedGender**: added `rdfs:subClassOf` **Gender**.
- Refactored sex-at-birth and phenotypic-sex bearers and partitions:
  - **SexAtBirth**:
    - `owl:equivalentClass` **FemaleSexAtBirth ⊔ IndeterminateSexAtBirth ⊔ MaleSexAtBirth → SexAtBirthFemaleSex ⊔ SexAtBirthIndeterminateSex ⊔ SexAtBirthMaleSex**.
    - `rdfs:subClassOf` constraint `gufo:inheresIn` **≥ 1** **PersonWithAssignedSexAtBirth → SexAtBirthAssignedPerson**.
  - **SexAtBirthAssignment**: `rdfs:subClassOf` constraint `gufo:mediates` **≥ 1** **PersonWithAssignedSexAtBirth → SexAtBirthAssignedPerson**.
  - **PhenotypicSex**:
    - Added `owl:equivalentClass` **PhenotypicAmbiguousSex ⊔ PhenotypicFemaleSex ⊔ PhenotypicMaleSex**.
    - `rdfs:subClassOf` constraint `gufo:inheresIn` **≥ 1** **PersonWithAssessedPhenotypicSex → PhenotypicSexAssessedPerson**.
  - **PhenotypicSexAssessment**: `rdfs:subClassOf` constraint `gufo:mediates` **≥ 1** **PersonWithAssessedPhenotypicSex → PhenotypicSexAssessedPerson**.
  - **CisgenderPerson**, **TransgenderPerson**:
    - Updated bearer links **PersonWithAssignedSexAtBirth → SexAtBirthAssignedPerson**.
    - Added `rdfs:subClassOf` restriction `owl:onProperty [ owl:inverseOf gufo:inheresIn ]` `owl:someValuesFrom` **Cisgender / Transgender**.
  - **FemaleCisgenderPerson**, **MaleCisgenderPerson**, **SelfIdentifiedCisgender\***, **ExternallyAttributedCisgender\***:
    - Updated `rdfs:subClassOf` **PersonWithFemaleSexAtBirth / PersonWithMaleSexAtBirth → SexAtBirthFemaleSexPerson / SexAtBirthMaleSexPerson**.
- Refactored **Person** equivalences, constraints, and karyotypic naming:
  - **Person**:
    - `owl:equivalentClass` **PersonWithAssignedSexAtBirth ⊔ PersonWithUnassignedSexAtBirth → SexAtBirthAssignedPerson ⊔ SexAtBirthUnassignedPerson**.
    - `owl:equivalentClass` **KaryotypicalFemale ⊔ KaryotypicalMale → KaryotypicFemaleSexPerson ⊔ KaryotypicMaleSexPerson**.
    - `owl:equivalentClass` **LegalGenderRecognizedPerson ⊔ LegalGenderUnassignedPerson → LegallyRecognizedGenderPerson ⊔ LegallyUnassignedGenderPerson**.
    - `owl:equivalentClass` **FemaleBiologicalPerson ⊔ IndeterminateBiologicalPerson ⊔ MaleBiologicalPerson → FemaleSexPerson ⊔ IndeterminateSexPerson ⊔ MaleSexPerson**.
    - Added `owl:equivalentClass` **Man ⊔ NonBinaryPerson ⊔ Woman**.
    - `rdfs:subClassOf` constraint `gufo:inheresIn` **≥ 1** **KaryotypicalSex → KaryotypicSex**.
    - Added `rdfs:subClassOf` restriction `owl:onProperty [ owl:inverseOf gufo:inheresIn ]` `owl:someValuesFrom` **SexGender**.
  - **PersonWithRegularSexChromosome**:
    - `owl:equivalentClass` **RegularKaryotypicalFemale ⊔ RegularKaryotypicalMale → RegularKaryotypicalFemalePerson ⊔ RegularKaryotypicalMalePerson**.
- Updated biological parent specializations:
  - **BiologicalMother**: `rdfs:subClassOf` **FemaleBiologicalPerson → FemaleSexPerson**.
  - **BiologicalFather**: `rdfs:subClassOf` **MaleBiologicalPerson → MaleSexPerson**.
- Updated recognized-gender constraints to target new bearer role IRIs:
  - **AdministrativeGender**: `rdfs:subClassOf` constraint `gufo:inheresIn` **≥ 1** **AdministrativeGenderRecognizedPerson → AdministrativelyRecognizedGenderPerson**.
  - **AdministrativeGenderRecognition**: `rdfs:subClassOf` constraint `gufo:mediates` **≥ 1** **AdministrativeGenderRecognizedPerson → AdministrativelyRecognizedGenderPerson**.
  - **LegalGender**: `rdfs:subClassOf` constraint `owl:onProperty [ owl:inverseOf gufo:inheresIn ]` **some** **LegalGenderRecognizedPerson → LegallyRecognizedGenderPerson**.
  - **LegalGenderRecognition**: `rdfs:subClassOf` constraint `gufo:mediates` **≥ 1** **LegalGenderRecognizedPerson → LegallyRecognizedGenderPerson**.
- Updated disjointness axioms (`owl:AllDisjointClasses`) to reflect the refactor:
  - Replaced **FemaleSexAtBirth / IndeterminateSexAtBirth / MaleSexAtBirth** with disjointness over **SexAtBirthFemaleSex / SexAtBirthIndeterminateSex / SexAtBirthMaleSex**.
  - Replaced **FemaleBiologicalPerson / IndeterminateBiologicalPerson / MaleBiologicalPerson** with disjointness over **FemaleSexPerson / IndeterminateSexPerson / MaleSexPerson**.
  - Replaced **KaryotypicalFemale / KaryotypicalMale** with disjointness over **KaryotypicFemaleSexPerson / KaryotypicMaleSexPerson** (and added disjointness over **KaryotypicFemaleSex / KaryotypicMaleSex**).
  - Added disjointness over **Gender / Sex**, and over **Cisgender / Transgender**.
- Updated helper subproperty hierarchies (structural alignments via `rdfs:subPropertyOf`):
  - `femaleGenderInheresInFemaleGenderPerson`, `maleGenderInheresInMaleGenderPerson`, `nonBinaryGenderInheresInNonBinaryGenderPerson`: `rdfs:subPropertyOf` **person → person_1** (and added specializations to **woman / man / nonBinaryPerson** where applicable).
  - `selfAwarePerson`, `selfIdentifiedGenderInheresInSelfAwarePerson`, `externallyGenderAttributedPersonInheresInExternallyAttributedGender`: `rdfs:subPropertyOf` **person → person_1**.
- **value**: `rdfs:domain` **PreferredGenderedPronoun → PreferredPronoun**.
- Documentation:
  - Removed `skos:prefLabel` annotations for **242** terms.
  - Removed `skos:altLabel` annotations for **7** terms, including: *Diagnosis, HealthCondition, PhenotypicSex, SelfIdentifiedGender*.
  - Editorial-only (no semantic change):
    - Normalized `rdfs:comment` whitespace/line endings for **31** terms, including: *AdministrativeGenderRecognitionDocument, Belief, ArtificialAgent, Chromosome, Date*, and others.

### Removed

- Removed legacy sex-at-birth / phenotypic / karyotypic IRIs superseded by the refactor:
  - **PersonWithAssignedSexAtBirth**, **PersonWithUnassignedSexAtBirth**, **PersonWithDeterminateSexAtBirth**, **PersonWithFemaleSexAtBirth**, **PersonWithMaleSexAtBirth**, **PersonWithIndeterminateSexAtBirth**.
  - **FemaleSexAtBirth**, **MaleSexAtBirth**, **IndeterminateSexAtBirth**.
  - **PersonWithAssessedPhenotypicSex**, **FemalePhenotypicPerson**, **MalePhenotypicPerson**, **AmbiguousPhenotypicPerson**.
  - **KaryotypicalSex**, **KaryotypicalFemale**, **KaryotypicalMale**, **RegularKaryotypicalFemale**, **RegularKaryotypicalMale**, **VariantKaryotypicalFemale**, **VariantKaryotypicalMale**.
  - **FemaleBiologicalPerson**, **MaleBiologicalPerson**, **IndeterminateBiologicalPerson**.
- Removed legacy recognized-gender bearer role IRIs superseded by the updated constraints:
  - **AdministrativeGenderRecognizedPerson**, **LegalGenderRecognizedPerson**, **LegalGenderUnassignedPerson**.
- Removed **PreferredGenderedPronoun** (replaced by **PreferredPronoun**).
- Removed supporting blank-node `owl:unionOf` / `owl:AllDisjointClasses` class expressions superseded by the updated axioms (see *Changed*).

## [1.5.0] - 2026-02-04

### TL;DR

- Introduces **PersonWithDeterminateSexAtBirth** and adds cisgender specializations (**FemaleCisgenderPerson**, **MaleCisgenderPerson**).
- Refines sex-at-birth / cis-trans alignment via updated `owl:equivalentClass` axioms and added `rdfs:subClassOf` links.
- Updates ontology release metadata to **1.5.0** and normalizes `rdfs:comment` line endings (CRLF → LF) for **46** terms (no semantic change).

### Added

- Introduced cisgender specializations (metamodelling via gUFO stereotypes: terms are both `owl:Class` and `owl:NamedIndividual`):
  - **FemaleCisgenderPerson**: `rdf:type` `gufo:Role`; `rdfs:subClassOf` **CisgenderPerson**, **FemaleGenderPerson**, **PersonWithFemaleSexAtBirth**.
  - **MaleCisgenderPerson**: `rdf:type` `gufo:Role`; `rdfs:subClassOf` **CisgenderPerson**, **MaleGenderPerson**, **PersonWithMaleSexAtBirth**.
- Introduced **PersonWithDeterminateSexAtBirth** (metamodelling as `gufo:Role`):
  - `rdfs:subClassOf` **PersonWithAssignedSexAtBirth**; `owl:equivalentClass` **PersonWithFemaleSexAtBirth ⊔ PersonWithMaleSexAtBirth**.

### Changed

- **ontology** (`https://w3id.org/health-ri/ontology`)
  - `owl:versionInfo` **"1.4.0" → "1.5.0"**; `owl:versionIRI` **…/v1.4.0 → …/v1.5.0**.
  - `dcterms:modified` **2026-02-03 → 2026-02-04**.
  - `dcterms:conformsTo` links updated to **…/v1.5.0/json** and **…/v1.5.0/vpp**.
- Refined sex-at-birth / cis-trans role definitions:
  - **PersonWithAssignedSexAtBirth**:
    - `owl:equivalentClass` **PersonWithFemaleSexAtBirth ⊔ PersonWithIndeterminateSexAtBirth ⊔ PersonWithMaleSexAtBirth → PersonWithFemaleSexAtBirth ⊔ PersonWithMaleSexAtBirth**.
    - Added `owl:equivalentClass` **CisgenderPerson ⊔ PersonWithIndeterminateSexAtBirth ⊔ TransgenderPerson**.
  - **PersonWithFemaleSexAtBirth**, **PersonWithMaleSexAtBirth**: added `rdfs:subClassOf` **PersonWithDeterminateSexAtBirth**.
  - **CisgenderPerson**: added `rdfs:subClassOf` **PersonWithAssignedSexAtBirth**; added `owl:equivalentClass` **FemaleCisgenderPerson ⊔ MaleCisgenderPerson**.
  - **TransgenderPerson**: added `rdfs:subClassOf` **PersonWithAssignedSexAtBirth** and **PersonWithDeterminateSexAtBirth**.
  - **Person**: removed `owl:equivalentClass` **CisgenderPerson ⊔ TransgenderPerson**.
- Documentation:
  - Added `rdfs:comment` definition text for **FemaleSexAtBirth**, **MaleSexAtBirth**, **IndeterminateSexAtBirth**, **FemininePresentingPerson**, **MasculinePresentingPerson**, **NonBinaryPresentingPerson**.
- Editorial-only (no semantic change):
  - Normalized `rdfs:comment` line endings (CRLF → LF) for **46** terms, including:
    - *Person, Diagnosis, HealthcareDiagnosis, Chromosome, Date, OffsetDateTime, AdministrativeGender, ExternallyAttributedGender*, and others.

### Removed

- Removed supporting blank-node `owl:unionOf` class expressions superseded by the updated `owl:equivalentClass` axioms (see *Changed*).
- No public named classes or properties (non-blank-node IRIs) were removed in this release.

## [1.4.0] - 2026-02-03

### TL;DR

- Extends the **gender** model with an explicit **GenderExpression** layer and corresponding *presenting-person* phases.
- Refactors recognized **legal/administrative** gender bearer patterns to new role IRIs and updates dependent constraints and helper subproperty hierarchies.
- Updates ontology release metadata: `owl:versionInfo` **1.3.0 → 1.4.0**, `owl:versionIRI`, `dcterms:modified`, and `dcterms:conformsTo`.

### Added - Introduced a self-designated gender layer and expression taxonomy (metamodelling via gUFO stereotypes: terms are both `owl:Class` and `owl:NamedIndividual`)

- **SelfDesignatedGender**: `rdf:type` `gufo:Category`; `rdfs:subClassOf` `gufo:IntrinsicMode`; `owl:equivalentClass` **GenderExpression ⊔ SelfIdentifiedGender**.
- **GenderExpression**: `rdf:type` `gufo:Kind`; `rdfs:subClassOf` **Gender** and **SelfDesignatedGender**; `rdfs:subClassOf` constraint `gufo:inheresIn` **≥ 1** **SelfAwarePerson**; `owl:equivalentClass` **FeminineGenderExpression ⊔ MasculineGenderExpression ⊔ NonBinaryGenderExpression**.
- **FeminineGenderExpression**, **MasculineGenderExpression**, **NonBinaryGenderExpression**: `rdf:type` `gufo:Phase`; `rdfs:subClassOf` **GenderExpression** and the corresponding **FemaleGender / MaleGender / NonBinaryGender**; `rdfs:subClassOf` constraint `gufo:inheresIn` **≥ 1** **FemininePresentingPerson / MasculinePresentingPerson / NonBinaryPresentingPerson**.
- **FemininePresentingPerson**, **MasculinePresentingPerson**, **NonBinaryPresentingPerson**: `rdf:type` `gufo:Phase`; `rdfs:subClassOf` the corresponding **FemaleGenderPerson / MaleGenderPerson / NonBinaryGenderPerson**; `rdfs:subClassOf` restriction `owl:onProperty [ owl:inverseOf gufo:inheresIn ]` `owl:qualifiedCardinality 1` **FeminineGenderExpression / MasculineGenderExpression / NonBinaryGenderExpression**.
- Introduced **PreferredGenderedPronoun**: `rdf:type` `gufo:Kind`; `rdfs:subClassOf` `gufo:Quality`; with datatype property **value** (`rdf:type` `owl:DatatypeProperty`; `rdfs:subPropertyOf` `gufo:hasQualityValue`; `rdfs:domain` **PreferredGenderedPronoun**; `rdfs:range` `xsd:string`).
- Introduced new recognized-gender bearer role IRIs (metamodelling as `gufo:Role`):  
  - **AdministrativeGenderRecognizedPerson**: `rdfs:subClassOf` **Person** and **ExternallyGenderAttributedPerson**; `rdfs:subClassOf` restrictions `owl:onProperty [ owl:inverseOf gufo:inheresIn ]` **some** **AdministrativeGender** and `owl:onProperty [ owl:inverseOf gufo:mediates ]` **some** **AdministrativeGenderRecognition**.  
  - **LegalGenderRecognizedPerson**: `rdfs:subClassOf` **AdministrativeGenderRecognizedPerson**; `rdfs:subClassOf` restriction `gufo:inheresIn` **≥ 1** **LegalGender** and `owl:onProperty [ owl:inverseOf gufo:mediates ]` **some** **LegalGenderRecognition**.  
  - **LegalGenderUnassignedPerson**: `rdfs:subClassOf` **Person**.

### Changed - Release metadata updated on the ontology IRI

- **ontology** (`https://w3id.org/health-ri/ontology`)
  - `owl:versionInfo` **"1.3.0" → "1.4.0"**; `owl:versionIRI` **…/v1.3.0 → …/v1.4.0**.
  - `dcterms:modified` **2026-02-02 → 2026-02-03**.
  - `dcterms:conformsTo` links updated to **…/v1.4.0/json** and **…/v1.4.0/vpp**.

- Reworked **Gender** and related disjointness to include **GenderExpression**:
  - **Gender**: added `owl:equivalentClass` **ExternallyAttributedGender ⊔ GenderExpression ⊔ SelfIdentifiedGender**; updated `rdfs:comment` (definition text).
  - Updated disjointness axioms (`owl:AllDisjointClasses`): replaced **ExternallyAttributedGender / SelfIdentifiedGender** with disjointness over **ExternallyAttributedGender / GenderExpression / SelfIdentifiedGender** (and added explicit **GenderExpression / SelfIdentifiedGender** disjointness).

- Updated gender partitions to incorporate the new expression layer (and removed administrative/legal unions at the gender level):
  - **MaleGender**: `owl:equivalentClass` **AdministrativeMaleGender ⊔ LegalMaleGender** removed; **ExternallyAttributedMaleGender ⊔ SelfIdentifiedMaleGender → ExternallyAttributedMaleGender ⊔ MasculineGenderExpression ⊔ SelfIdentifiedMaleGender**.
  - **FemaleGender**: `owl:equivalentClass` **AdministrativeFemaleGender ⊔ LegalFemaleGender** removed; **ExternallyAttributedFemaleGender ⊔ SelfIdentifiedFemaleGender → ExternallyAttributedFemaleGender ⊔ FeminineGenderExpression ⊔ SelfIdentifiedFemaleGender**.
  - **NonBinaryGender**: `owl:equivalentClass` **AdministrativeNonBinaryGender ⊔ LegalNonBinaryGender** removed; **ExternallyAttributedNonBinaryGender ⊔ SelfIdentifiedNonBinaryGender → ExternallyAttributedNonBinaryGender ⊔ NonBinaryGenderExpression ⊔ SelfIdentifiedNonBinaryGender**.

- Updated bearer-phase unions to include presenting-person phases:
  - **MaleGenderPerson**: `owl:equivalentClass` **ExternallyAttributedMaleGenderPerson ⊔ SelfIdentifiedMaleGenderPerson → ExternallyAttributedMaleGenderPerson ⊔ MasculinePresentingPerson ⊔ SelfIdentifiedMaleGenderPerson**.
  - **FemaleGenderPerson**: `owl:equivalentClass` **ExternallyAttributedFemaleGenderPerson ⊔ SelfIdentifiedFemaleGenderPerson → ExternallyAttributedFemaleGenderPerson ⊔ FemininePresentingPerson ⊔ SelfIdentifiedFemaleGenderPerson**.
  - **NonBinaryGenderPerson**: `owl:equivalentClass` **ExternallyAttributedNonBinaryGenderPerson ⊔ SelfIdentifiedNonBinaryGenderPerson → ExternallyAttributedNonBinaryGenderPerson ⊔ NonBinaryPresentingPerson ⊔ SelfIdentifiedNonBinaryGenderPerson**.

- Refactored self-designation hierarchy and constraints:
  - **SelfIdentifiedGender**: `rdfs:subClassOf` **gufo:IntrinsicMode → SelfDesignatedGender**; updated `rdfs:comment`.
  - **SelfAwarePerson**: added `rdfs:subClassOf` restriction `owl:onProperty [ owl:inverseOf gufo:inheresIn ]` `owl:qualifiedCardinality 1` **GenderExpression**.

- Refactored recognized-gender constraints to target the new recognized-person role IRIs:
  - **AdministrativeGender**: `rdfs:subClassOf` constraint `gufo:inheresIn` **≥ 1** **PersonWithRecognizedAdministrativeGender → AdministrativeGenderRecognizedPerson**; updated `rdfs:comment`.
  - **AdministrativeGenderRecognition**: `rdfs:subClassOf` constraint `gufo:mediates` **≥ 1** **PersonWithRecognizedAdministrativeGender → AdministrativeGenderRecognizedPerson**; updated `rdfs:comment`.
  - **LegalGender**: `rdfs:subClassOf` constraint `owl:onProperty [ owl:inverseOf gufo:inheresIn ]` **some** **PersonWithRecognizedLegalGender → LegalGenderRecognizedPerson**; updated `rdfs:comment`.
  - **LegalGenderRecognition**: `rdfs:subClassOf` constraint `gufo:mediates` **≥ 1** **PersonWithRecognizedLegalGender → LegalGenderRecognizedPerson**; updated `rdfs:comment`.
  - **Person**: `owl:equivalentClass` **PersonWithRecognizedLegalGender ⊔ PersonWithUnassignedLegalGender → LegalGenderRecognizedPerson ⊔ LegalGenderUnassignedPerson**; updated `rdfs:comment`.

- Added helper property specializations (structural alignments via `rdfs:subPropertyOf`):
  - `femininePresentingPerson`: `rdfs:subPropertyOf` `femaleGenderInheresInFemaleGenderPerson`.
  - `masculinePresentingPerson`: `rdfs:subPropertyOf` `maleGenderInheresInMaleGenderPerson`.
  - `nonBinaryPresentingPerson`: `rdfs:subPropertyOf` `nonBinaryGenderInheresInNonBinaryGenderPerson`.
  - `selfAwarePerson`: `rdfs:subPropertyOf` `person`.
  - `administrativeGenderInheresInAdministrativeGenderRecognizedPerson`: `rdfs:subPropertyOf` `externallyGenderAttributedPersonInheresInExternallyAttributedGender`.
  - `legalGenderRecognizedPersonInheresInLegalGender`: `rdfs:subPropertyOf` `administrativeGenderInheresInAdministrativeGenderRecognizedPerson`.

- Editorial-only (no semantic change):
  - Polished textual definitions (`rdfs:comment`) for **45** terms (no semantic change), including:
    - *Diagnosis, HealthcareDiagnosis, Chromosome, Date, OffsetDateTime, PhysicalDocument, DigitalDocument, BirthNotification, SocialAgent, ArtificialAgent, ExternallyGenderAttributedPerson*, and others.

### Removed - Removed legacy recognized-gender bearer patterns superseded by the refactor

- Removed legacy recognized-gender bearer role IRIs:
  - **PersonWithRecognizedAdministrativeGender**, **PersonWithRecognizedLegalGender**, **PersonWithUnassignedLegalGender**.
- Removed legacy recognized-gender inherence helper subproperties:
  - **administrativeGenderInheresInPersonWithRecognizedAdministrativeGender**, **personWithRecognizedLegalGenderInheresInLegalGender**.

## [1.3.0] - 2026-02-02

### TL;DR

- Refactors the **gender** model to distinguish **externally-attributed** vs **self-identified** gender, and adds explicit **legal/administrative** specializations with updated constraints.
- Refactors the **agent** taxonomy via **SocialAgent**, updates related disjointness axioms, and de-parents **ArtificialAgent** from **Agent**.
- Updates ontology release metadata: `owl:versionInfo` **1.2.1 → 1.3.0**, `owl:versionIRI`, `dcterms:modified`, and `dcterms:conformsTo`.

### Added

- Introduced a gender attribution pattern (metamodelling via gUFO stereotypes: many terms are both `owl:Class` and `owl:NamedIndividual`):
  - **GenderAttribution**: `rdfs:subClassOf` `gufo:Relator`; `gufo:mediates` **some** **GenderAttributor**; `gufo:mediates` **≥ 1** **ExternallyAttributedGender** and **≥ 1** **ExternallyGenderAttributedPerson**.
  - **GenderAttributor**: `rdf:type` `gufo:RoleMixin`; `rdfs:subClassOf` **Agent**; `gufo:mediates` **≥ 1** **GenderAttribution**.
- Added new gender layers and specializations:
  - **ExternallyAttributedGender** and **SelfIdentifiedGender** (+ Female/Male/NonBinary specializations and corresponding bearer phases).
  - **Administrative\*** and **Legal\*** gender specializations (gender + bearer phases).
  - **CisgenderPerson** / **TransgenderPerson** (and externally-attributed / self-identified cis/trans specializations).
- Added sex-at-birth subkinds:
  - **FemaleSexAtBirth**, **MaleSexAtBirth**, **IndeterminateSexAtBirth**.
- Introduced **SocialAgent**:
  - `rdf:type` `gufo:Category`; `owl:equivalentClass` **IndividualAgent ⊔ Organization**.
- Added helper property specializations (structural alignments via `rdfs:subPropertyOf`), including:
  - **recognizedBy** (`rdfs:subPropertyOf` `hasAttributor`), **recognizesGender** (`rdfs:subPropertyOf` `attributesGender`), plus **recognizesGender_1** and **recognizes_1**.
  - Gender / sex-at-birth inherence helper subproperties (e.g., **selfIdentifiedGenderInheresInSelfAwarePerson**, **sexAtBirthInheresInPersonWithAssignedSexAtBirth**, and related “personWith\*” subproperties).

### Changed

- Release metadata updated on the ontology IRI <https://w3id.org/health-ri/ontology>:
  - `owl:versionInfo` **"1.2.1" → "1.3.0"**; `owl:versionIRI` **…/v1.2.1 → …/v1.3.0**.
  - `dcterms:modified` **2025-12-15 → 2026-02-02**.
  - `dcterms:conformsTo` links updated to **…/v1.3.0/json** and **…/v1.3.0/vpp**.
- Reworked **Gender**:
  - Added `owl:equivalentClass` **FemaleGender ⊔ MaleGender ⊔ NonBinaryGender**.
  - Added `rdfs:subClassOf` constraint: `gufo:inheresIn` **≥ 1** **Person**.
  - Updated `rdfs:comment` (definition text).
- Reworked **AdministrativeGender**:
  - `rdf:type` **gufo:Kind → gufo:SubKind**.
  - `rdfs:subClassOf` **gufo:ExtrinsicMode** and **Gender** → **ExternallyAttributedGender**.
  - Added `rdfs:subClassOf` restriction: `owl:onProperty [ owl:inverseOf gufo:mediates ]` `owl:qualifiedCardinality 1` **AdministrativeGenderRecognition**.
  - Updated `owl:equivalentClass` **FemaleAdministrativeGender ⊔ MaleAdministrativeGender ⊔ NonBinaryAdministrativeGender → AdministrativeFemaleGender ⊔ AdministrativeMaleGender ⊔ AdministrativeNonBinaryGender**.
- Reworked **AdministrativeGenderRecognition**:
  - `rdf:type` **gufo:Kind → gufo:SubKind**.
  - `rdfs:subClassOf` **gufo:Relator → GenderAttribution**.
  - Constraints refactored:
    - Added `gufo:mediates` **≥ 1** **AdministrativeGender**.
    - Changed document constraint: `gufo:mediates` **≥ 1** **AdministrativeGenderRecognitionDocument → some** **AdministrativeGenderRecognitionDocument**.
    - Strengthened person constraint: `gufo:mediates` **some → ≥ 1** **PersonWithRecognizedAdministrativeGender**.
- Reworked **LegalGender**:
  - Added `owl:equivalentClass` **LegalFemaleGender ⊔ LegalMaleGender ⊔ LegalNonBinaryGender**.
  - Added `rdfs:subClassOf` restriction: `owl:onProperty [ owl:inverseOf gufo:mediates ]` `owl:qualifiedCardinality 1` **LegalGenderRecognition**.
- Updated **LegalGenderRecognition**:
  - Added `rdfs:subClassOf` restriction: `gufo:mediates` **≥ 1** **LegalGender**.
- Refactored bearer-role patterns:
  - **PersonWithRecognizedAdministrativeGender**:
    - Removed `owl:equivalentClass` union over **PersonWithFemaleAdministrativeGender / PersonWithMaleAdministrativeGender / PersonWithNonBinaryAdministrativeGender**.
    - Added `rdfs:subClassOf` **ExternallyGenderAttributedPerson**.
    - Updated `rdfs:comment` (definition text).
  - **PersonWithRecognizedLegalGender**:
    - Removed `owl:equivalentClass` union over **LegalFemalePerson / LegalMalePerson / LegalNonBinaryPerson**.
    - Updated `rdfs:comment` (definition text).
- Reworked **SelfAwarePerson**:
  - Added `rdfs:subClassOf` **Person**.
  - Replaced gender constraint: `owl:onProperty [ owl:inverseOf gufo:inheresIn ]` `owl:qualifiedCardinality 1`
    - **GenderIdentity → SelfIdentifiedGender**.
  - Added `owl:equivalentClass` **CisgenderPerson ⊔ TransgenderPerson**.
- Tightened and aligned **Person** and sex-at-birth modeling:
  - **Person**: added `owl:equivalentClass` **FemaleGenderPerson ⊔ MaleGenderPerson ⊔ NonBinaryGenderPerson** and **CisgenderPerson ⊔ TransgenderPerson**; added `rdfs:subClassOf` `owl:onProperty [ owl:inverseOf gufo:inheresIn ]` **some** **Gender**.
  - **SexAtBirth**: added `owl:equivalentClass` **FemaleSexAtBirth ⊔ IndeterminateSexAtBirth ⊔ MaleSexAtBirth**.
  - **PersonWithAssignedSexAtBirth**: added `rdfs:subClassOf` **PersonWithAssessedPhenotypicSex**.
  - **PersonWithFemaleSexAtBirth / PersonWithMaleSexAtBirth / PersonWithIndeterminateSexAtBirth**: added `owl:qualifiedCardinality 1` constraints (via `owl:onProperty [ owl:inverseOf gufo:inheresIn ]`) on the corresponding **\*SexAtBirth**.
- Agent taxonomy refactor:
  - **Agent**: added `owl:equivalentClass` **Animal ⊔ SocialAgent**.
  - **Organization** and **IndividualAgent**: `rdfs:subClassOf` **gufo:FunctionalComplex** and **Agent** → **SocialAgent** (via new intermediate taxonomy term).
  - **ArtificialAgent**: removed `rdfs:subClassOf` **Agent** (comment formatting also updated).
  - Updated disjointness axioms (`owl:AllDisjointClasses`):
    - Removed: **Animal / ArtificialAgent / Organization**.
    - Added: **IndividualAgent / Organization**.
- Disjointness and serialization adjustments relevant to gender and cells:
  - Replaced disjointness: **AdministrativeGender / GenderIdentity** → **ExternallyAttributedGender / SelfIdentifiedGender** (`owl:AllDisjointClasses`).
  - Added `owl:AllDisjointClasses` over **FemaleSexAtBirth / IndeterminateSexAtBirth / MaleSexAtBirth**.
  - **HumanCell**: `owl:equivalentClass` union reserialized (operands unchanged: **DiploidCell ⊔ HaploidCell ⊔ Polyploid**); removed the `owl:AllDisjointClasses` axiom over **DiploidCell / HaploidCell / Polyploid** present in the old serialization (verify if disjointness is asserted elsewhere).

- Editorial-only (no semantic change):
  - Normalized newline formatting in `rdfs:comment` for **20** entities (e.g., **Diagnosis**, **HealthcareDiagnosis**, **Chromosome**, **Date**, **OffsetDateTime**, **NonHumanAnimal**, and document terms).

### Removed

- Removed legacy gender identity taxonomy:
  - **GenderIdentity**, **FemaleGenderIdentity**, **MaleGenderIdentity**, **NonBinaryGenderIdentity**.
- Removed legacy administrative/legal bearer patterns superseded by the refactor:
  - **FemaleAdministrativeGender**, **MaleAdministrativeGender**, **NonBinaryAdministrativeGender**.
  - **PersonWithFemaleAdministrativeGender**, **PersonWithMaleAdministrativeGender**, **PersonWithNonBinaryAdministrativeGender**.
  - **LegalFemalePerson**, **LegalMalePerson**, **LegalNonBinaryPerson**.
- Removed legacy administrative gender inherence subproperties:
  - **femaleAdministrativeGenderInheresInPersonWithFemaleAdministrativeGender**, **maleAdministrativeGenderInheresInPersonWithMaleAdministrativeGender**, **nonBinaryAdministrativeGenderInheresInPersonWithNonBinaryAdministrativeGender**.

## [1.2.1] - 2025-12-15

### Changed

Class `Healthcare Professional` moved from package `Sex and Gender` to package `Person`.

## [1.2.0] - 2025-11-19

### Added

- **femaleTypicalDimorphicCharacteristicIsComponentOfFemaleBiologicalPerson**,  
  **maleTypicalDimorphicCharacteristicIsComponentOfMaleBiologicalPerson**,  
  **indeterminateDimorphicCharacteristicIsComponentOfIndeterminateBiologicalPerson**  
  - Added `rdfs:subPropertyOf` assertions to `sexualDimorphicCharacteristicIsComponentOfPerson`, introducing more specific dimorphic characteristic–person component relations.

- **femaleTypicalVisualSexCharacteristicIsComponentOfFemalePhenotypicPerson**,  
  **maleTypicalVisualSexCharacteristicIsComponentOfMalePhenotypicPerson**,  
  **indeterminateVisualSexCharacteristicIsComponentOfAmbiguousPhenotypicPerson**  
  - Added `rdfs:subPropertyOf` assertions to `personIsComponentOfVisualSexCharacteristic`, specializing visual sex characteristic–person component relations.

### Changed

- **ontology** (`https://w3id.org/health-ri/ontology`)  
  - Updated `owl:versionInfo` **`1.1.1` → `1.2.0`**.  
  - Updated `owl:versionIRI` **`…/v1.1.1` → `…/v1.2.0`**.  
  - Updated `dcterms:modified` **`2025-11-14` → `2025-11-19`**.  
  - Updated `dcterms:conformsTo` JSON and VPP links **`…/ontology/v1.1.1/{json,vpp}` → `…/ontology/v1.2.0/{json,vpp}`**.

- **SexAtBirthAssignment** – strengthened participation constraint  
  - `rdfs:subClassOf` previously pointed to an `owl:Restriction` with `owl:someValuesFrom` **SexAtBirthAssigner** on `owl:onProperty gufo:mediates`.  
  - Now `rdfs:subClassOf` points to an `owl:Restriction` using:
    - `owl:onClass` **SexAtBirthAssigner**,  
    - `owl:minQualifiedCardinality "1"^^xsd:nonNegativeInteger`,  
    - `owl:onProperty gufo:mediates`.  
  - Effect: changes the constraint from an existential restriction (∃ mediated **SexAtBirthAssigner**) to a qualified minimum cardinality restriction (≥ 1 mediated **SexAtBirthAssigner**).

- **PersonWithAssignedSexAtBirth** – strengthened assignment cardinality  
  - `rdfs:subClassOf` previously pointed to an `owl:Restriction` with:
    - `owl:someValuesFrom` **SexAtBirthAssignment**,  
    - `owl:onProperty` an anonymous property with `owl:inverseOf gufo:mediates`.  
  - Now `rdfs:subClassOf` points to an `owl:Restriction` using:
    - `owl:onClass` **SexAtBirthAssignment**,  
    - `owl:qualifiedCardinality "1"^^xsd:nonNegativeInteger`,  
    - `owl:onProperty` an anonymous property defined by `owl:inverseOf gufo:mediates`.  
  - Effect: changes the constraint from an existential restriction (∃ inverse-of-`gufo:mediates` **SexAtBirthAssignment**) to a qualified exact cardinality restriction (= 1 such assignment per person).  
  - The anonymous property node with `owl:inverseOf gufo:mediates` is effectively renamed at blank-node level; intended semantics remain the same (inverse of `gufo:mediates`).

### Removed

- Removed two `owl:Restriction` axioms based on `owl:someValuesFrom`:
  - The restriction on **SexAtBirthAssignment** using `owl:someValuesFrom` **SexAtBirthAssigner** on `owl:onProperty gufo:mediates`.  
  - The restriction on **PersonWithAssignedSexAtBirth** using `owl:someValuesFrom` **SexAtBirthAssignment** on an anonymous property (`owl:inverseOf gufo:mediates`).  
- Removed the supporting anonymous property node that previously encoded `owl:inverseOf gufo:mediates` for the old restriction; this is replaced by a new blank node with the same `owl:inverseOf` assertion in the updated pattern (see *Changed*).  
- No public named classes or properties (non-blank-node IRIs) were removed in this release.

### Not serialized

- None identified beyond the OWL-level changes summarized above; all observed changes are present in the serialized ontology.

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
