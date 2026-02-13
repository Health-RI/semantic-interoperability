# News & Updates

## 2026-02-13

- **Index** — Changed: Reworked the homepage to emphasize semantic traceability, the semantic-hub mapping approach, and a 10-minute quick start.
- **Method Overview** — Changed: Expanded the method overview with clearer definitions, rationale, and references for HRIO/HRIV-based semantic traceability.
- **Frequently Asked Questions (FAQ)** — Changed: Added detailed guidance on HRIO/HRIV meaning mappings, including interpretation caveats (SKOS/OWL) and adoption considerations.
- **Mapping Strategy** — Changed: Clarified CIM/PIM layering for HRIO artifacts, updating the figure caption and adding an artifact-by-layer comparison table.
- **The Health-RI SSSOM Mapping Set Schema** — Modified: Added semantic-traceability context, expanded field guidance, and clarified that HRIV predicates are meaning-level links (not OWL equivalence/subsumption).
- **Mapping Governance** — Modified: Strengthened curation and review guidance with warnings against false agreement, clearer evidence expectations, and notes on mapping stability versus HRIO maturity.
- **Ontology Validation** — Modified: Updated review checklists with opt-out acknowledgement guidance and transparency notes for AI-assisted drafting of documentation text.
- **Ontology Rules** — Modified: Clarified how SHACL constraints and derivation rules attach to HRIO artifacts, including an updated OntoUML→gUFO/OWL→SHACL workflow.
- **Ontology Versioning** — Changed: Aligned terminology and artifact lists under HRIO, clarifying that all release artifacts share one version identifier.
- **Persistent IDs** — Changed: Expanded guidance on citing versioned PIDs versus using “latest” PIDs for browsing, and clarified HRIO namespace identifiers.
- **Publications** — Changed: Clarified when derived OWL/SHACL/spec artifacts are published and how “latest” PIDs behave when derived artifacts are unavailable.
- **Deliverables Overview** — Modified: Updated the deliverables summary to explicitly describe HRIO, HRIV, the SSSOM mapping set, and the changelog.
- **Contribution Channels** — Fixed: Refreshed contribution guidance with HRIO terminology, links to mapping governance, and normalized SSSOM issue-form links.
- **Calls for Community Review** — Modified: Clarified the external review process for HRIO domains, including default acknowledgement with opt-out and a current “no open calls” status note.

## 2026-02-11

- **[Health Ri Ontology](https://w3id.org/health-ri/ontology)** — Added: Published v1.6.0 release artifacts (Turtle, JSON, SHACL, Visual Paradigm) and refreshed sex/gender diagrams and SKOS labels for improved display.

## 2026-02-04

- **[Health-RI Ontology](https://w3id.org/health-ri/ontology)** — Added: Published v1.5.0 release artifacts (Turtle, JSON, Visual Paradigm) and refreshed gender/sex diagrams, adding cisgender/transgender and sex-at-birth type visualizations.

## 2026-02-03

- **[Health-RI Ontology](https://w3id.org/health-ri/ontology)** — Modified: Updated to v1.4.0, adding gender expression and preferred pronoun concepts and refining administrative and legal gender recognition terminology.

## 2026-02-02

- **[Health-RI Ontology](https://w3id.org/health-ri/ontology)** — Added: Published ontology release 1.3.0, refactoring gender modeling (externally-attributed vs self-identified) and adding cisgender/transgender modality concepts, plus SocialAgent taxonomy updates and refreshed metadata.

## 2025-12-08

- [**Contributing to the Health-RI Semantic Interoperability Effort**](./contributing/overview.md) — Renamed: provides an overview of contribution options, separating community review calls from general channels and linking to the main submission forms.
- [**Contribution Channels**](./contributing/contribution-channels.md) — Created: focuses the page on ongoing contribution options outside time-bound review calls, with clarified sections and button-based links to structured issue forms.
- [**Calls for Community Review**](./contributing/call-for-community-review.md) — Created: describes the external community review process for ontology domains, including participation options and how open and closed calls are listed.

## 2025-11-19

- **Ontology validation checklists** — Modified: Added warnings and clarifications to ontology validation checklists, relaxing pending items and aligning terminology with OWL/gUFO exports and diagram notation.

## 2025-11-14

- [**Ontology Rules and SHACL Implementation**](./method/ontology-rules.md) — Created: Introduced a dedicated overview of ontology constraint and derivation rules and their implementation using SHACL.
- [**Ontology Notes Policy**](./method/ontology-notes-policy.md) — Changed: Updated the notes policy with the new DRIV rule category and adjusted note colors to align with the ontology rules.
- Changed: Several pages received minor updates to show their relation to the newly created ontology rules page.

## 2025-11-05

- [**Governance, Lifecycle, and Validation of the Health-RI SSSOM Mapping Set**](./method/mapping-governance.md) — Created: defines roles, two-person rule, lifecycle gates, and validation policy for the SSSOM Mapping Set.
- [**The Health-RI SSSOM Mapping Set Schema**](./method/mapping-schema.md) — Renamed and expanded: added a comprehensive field table and browsing guidance, and aligned versioning to append-only.
- [**Ontology Versioning Old**](./method/ontology-versioning-old.md) — Renamed and clarified: explicitly applies to pre-v1.0.0 releases.
- [**Mappings**](./ontology/mappings.md) — Changed: added a scope note and linked to the Mapping Set schema.

## 2025-11-03

- [**News & Updates**](news.md) — Created: added a date-based, page-first changelog page and linked it in navigation.
- [**SSSOM Mapping Set**](./method/mapping-schema.md) — Changed: improved readability; added guidance on permanent URIs, append-only versioning using `replaces`, and BCP 47 language-tagged strings; introduced a submission-checklist URI validator; defined allowed `predicate_id` values; switched examples to HTTPS; and removed the default `object_source`.
- [**Mapping Strategy**](./method/mapping-strategy.md) — Changed: Clarified caption and examples, updated broader/narrower mappings (ghc Patient to Healthcare/Veterinary), and corrected the prefix to `hriv`.
- [**SSSOM Mappings Template**](https://raw.githubusercontent.com/Health-RI/semantic-interoperability/refs/heads/main/resources/mappings_template.xlsx) — Changed: added basic input validation and displayed contextual information when boxes are selected.
