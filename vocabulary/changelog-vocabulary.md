# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to the [versioning policies available in this link.](https://health-ri.github.io/semantic-interoperability/method/publications/).

## [1.1.0] - 2025-08-31
### Added
- Introduced **`hriv:meaningMappingRelation`** as an abstract, closed superproperty for all meaning-level mappings.
  - Declared as a `subPropertyOf skos:relatedMatch`.
  - Must not be asserted directly.
- Added **alignment with SKOS mapping relations**:
  - `hriv:hasExactMeaning` → `skos:exactMatch`
  - `hriv:hasBroaderMeaningThan` → `skos:narrowMatch`
  - `hriv:hasNarrowerMeaningThan` → `skos:broadMatch`
- New **vocabulary-level comment** describing the *hybrid semantic strategy* (intentional grounding via semiotics + pragmatic set-theoretic alignment).

### Changed
- Refined `rdfs:comment` usage for mapping properties (`hasExactMeaning`, `hasBroaderMeaningThan`, `hasNarrowerMeaningThan`) to:
  - Separate long descriptions into multiple `rdfs:comment` statements.
  - Clarify the distinction from OWL constructs (`owl:equivalentClass`) and SKOS mappings.
  - Explicitly state the pragmatic SKOS alignment interpretation.

### Metadata
- Updated ontology version to **1.1.0**.
- Added `dcterms:modified "2025-08-31"^^xsd:date`.
- Updated `owl:versionIRI` to `.../v1.1.0`.
- Added `dcat:hasCurrentVersion`, `dcat:previousVersion`, and `dcat:hasVersion` links for version tracking.
- Expanded `owl:versionInfo` to include a descriptive version note.

## [1.0.0] - 2025-08-25
### Added
- Initial release of the Health-RI Mapping Vocabulary.
- Introduced core mapping properties:
  - `hriv:hasExactMeaning`
  - `hriv:hasBroaderMeaningThan`
  - `hriv:hasNarrowerMeaningThan`
- Established alignment strategy for expressing exact, broader, and narrower meaning links across artifacts.
