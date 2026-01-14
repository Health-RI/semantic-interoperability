# Health-RI Semantic Interoperability Initiative

[![Project DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.16949640.svg)](https://doi.org/10.5281/zenodo.16949640)
[![Project Status – Active](https://www.repostatus.org/badges/latest/active.svg)](https://www.repostatus.org/#active)
![GitHub last commit](https://img.shields.io/github/last-commit/Health-RI/semantic-interoperability)
![GitHub Created At](https://img.shields.io/github/created-at/Health-RI/semantic-interoperability)
![GitHub Release](https://img.shields.io/github/v/release/Health-RI/semantic-interoperability)
![GitHub Release Date](https://img.shields.io/github/release-date/Health-RI/semantic-interoperability)
![GitHub commits since latest release](https://img.shields.io/github/commits-since/Health-RI/semantic-interoperability/latest)
![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/health-ri/semantic-interoperability/deploy.yml)
[![Documentation](https://img.shields.io/badge/Docs-Specification-blue.svg)](https://health-ri.github.io/semantic-interoperability/)

<!-- Ontology latest release -->
<!-- [![Ontology Version](https://img.shields.io/github/v/release/Health-RI/semantic-interoperability?filter=ontology-v*&sort=semver)](https://github.com/Health-RI/semantic-interoperability/releases?q=tag%3Aontology-) [![License: CC-BY-4.0](https://img.shields.io/badge/License-CC--BY--4.0-blue.svg)](https://creativecommons.org/licenses/by/4.0/)
-->

This repository hosts the source files for the [Health-RI Semantic Interoperability Initiative documentation site](https://health-ri.github.io/semantic-interoperability/), which presents our approach to enabling semantic interoperability in health and life sciences.

Visit the documentation at: **<https://health-ri.github.io/semantic-interoperability/>**

## Releases

| Deliverable                      | Latest Release                                                                                                                                                                                                               | All Releases                                                                                                                                                                                            | License                                                                                                                          |
| -------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| **Health-RI Ontology**           | TBA                                                                                                                                                                                                                          | TBA                                                                                                                                                                                                     | [![License: CC-BY-4.0](https://img.shields.io/badge/License-CC--BY--4.0-blue.svg)](https://creativecommons.org/licenses/by/4.0/) |
| **Health-RI SSSOM Mapping Set**  | [![Mapping Set Version](https://img.shields.io/github/v/release/Health-RI/semantic-interoperability?filter=mappings-v*&sort=date)](https://github.com/Health-RI/semantic-interoperability/releases/tag/mappings-v2025-09-08) | [![All Mappings Releases](https://img.shields.io/badge/All%20Mappings%20Releases-913800)](https://github.com/Health-RI/semantic-interoperability/releases?q=mapping+NOT+vocabulary&expanded=true)       | [![License: CC-BY-4.0](https://img.shields.io/badge/License-CC--BY--4.0-blue.svg)](https://creativecommons.org/licenses/by/4.0/) |
| **Health-RI Mapping Vocabulary** | [![Vocabulary Version](https://img.shields.io/github/v/release/Health-RI/semantic-interoperability?filter=vocabulary-v*&sort=semver)](https://github.com/Health-RI/semantic-interoperability/releases/tag/vocabulary-v1.1.0) | [![All Vocabulary Releases](https://img.shields.io/badge/All%20Vocabulary%20Releases-913800)](https://github.com/Health-RI/semantic-interoperability/releases?q=vocabulary+NOT+documents&expanded=true) | [![License: CC-BY-4.0](https://img.shields.io/badge/License-CC--BY--4.0-blue.svg)](https://creativecommons.org/licenses/by/4.0/) |
| **Documents**                    | [![Latest Document](https://img.shields.io/github/v/release/Health-RI/semantic-interoperability?filter=documents-*&sort=date)](https://github.com/Health-RI/semantic-interoperability/releases/tag/documents-2026-01-13)     | [![All Document Releases](https://img.shields.io/badge/All%20Document%20Releases-913800)](https://github.com/Health-RI/semantic-interoperability/releases?q=documents&expanded=true)                    | [![License: CC-BY-4.0](https://img.shields.io/badge/License-CC--BY--4.0-blue.svg)](https://creativecommons.org/licenses/by/4.0/) |

## Repository structure

This repository is organized around the MkDocs documentation site and the semantic artifacts it publishes (ontology, mappings, and vocabulary).

```text
.
├─ docs/         # MkDocs website source (pages + shared assets)
├─ ontologies/   # Health-RI Ontology artifacts (latest + versioned)
├─ mappings/     # Health-RI mapping set exports
├─ vocabulary/   # Health-RI Mapping Vocabulary artifacts (latest + versioned)
├─ scripts/      # Utility scripts for generation/conversion/maintenance
├─ resources/    # Templates, prompts, QR codes, etc.
├─ documents/    # Manuscripts and other supporting documents
├─ site/         # Built documentation site output (generated)
├─ mkdocs.yml    # MkDocs configuration
├─ CITATION.cff   # Citation metadata
└─ LICENSE-*.md   # Licensing for artifacts and code
```

## License

**Semantic Artifacts & Documentation:** All ontologies, vocabularies, mapping files, documentation, templates, and other semantic artifacts in this repository (e.g., `ontologies/`, `mappings/`, `vocabulary/`, and related subfolders) are licensed under the [**Creative Commons Attribution 4.0 International (CC BY 4.0)**](https://creativecommons.org/licenses/by/4.0/) license.

**Auxiliary Code:** Any code scripts or auxiliary utilities (e.g., in `/scripts/`) are licensed under the [**MIT License**](https://spdx.org/licenses/MIT.html).
