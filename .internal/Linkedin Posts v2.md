# Health-RI Semantic Interoperability – General

## Post 5: The 5-Step CI/CD for Semantic Models (Whiteboard to Production)

**Make the method repeatable.** Just like software, semantic models need an auditable, governed workflow to move from an idea on a whiteboard to a production asset.

Here is our 5-step process:

1) **Model** in OntoUML (CIM); capture definitions and scope notes.
2) **Validate** with stakeholders.
3) **Encode** in OWL via **gUFO** (PIM); add annotations.
4) **Align** externals using the mapping vocabulary (`hasExactMeaning` / broader / narrower) and publish rows in **SSSOM**.
5) **Pin** versions: ontology **version IRI** + mapping **release date**; ship via stable **w3id PIDs**.

Outcomes:

- **Faster onboarding** (diagram → class one-to-one).
- **Audit-ready** (version IRIs, dated releases).
- **More reuse** (shared SSSOM rows instead of bespoke glue).

**Call to action:** Add "pin version IRI + release date" to CI/CD; align one concept family and publish 3–5 SSSOM rows.

**References:**

- *Semantic Mapping Strategy (workflow & alignment).* Accessed Nov 6, 2025. <https://health-ri.github.io/semantic-interoperability/method/mapping-strategy/>
- *Initiative Publications — Release & versioning policy.* Accessed Nov 6, 2025. <https://health-ri.github.io/semantic-interoperability/method/publications/>

## Post 7: **Map Once, Reuse Everywhere — The Health-RI SSSOM Mapping Set**

Many teams have lived this: a new or updated dataset or standard arrives and you're back in a spreadsheet, remapping the *same* concepts again—first mapping between A and B, then mapping C to both A and B; when a new version of C shows up (C₂), you repeat the exercise and create two more mappings (C₂–A and C₂–B), each with its own rules... With this kind of maintenance burden, why not map everything once into a shared set you can reuse?

The **Health-RI SSSOM Mapping Set [1]** is our curated mapping set and main way of sharing mappings with the community. We create and maintain mappings from widely used health standards to the Health-RI Ontology (HRIO) [2] and publish them for reuse. The mapping set is not the ontology itself: HRIO provides the shared meanings, while the mapping set is the collection of relations between standard-specific terms and those HRIO concepts. Map each external scheme **once** to HRIO—by asserting `hriv:` relations as axioms in models you control, and via the shared SSSOM Mapping Set where you cannot edit the source—and reuse those mappings wherever you need cross-standard interoperability.

The SSSOM Mapping Set:

- **Imposes a 1×N topology**
  Instead of pairwise mappings between every standard, we maintain a SSSOM Mapping Set where each external ontology, terminology, or schema contributes its mappings into HRIO. The same mapping rows can then be reused across multiple projects, domains, and standards that rely on those terms.

- **Works explicitly at the meaning level**
  Rows use the **Health-RI Mapping Vocabulary (`hriv:`) [3]** to relate your local terms to `hrio:` concepts. This makes your *intended meaning* explicit, instead of merely stating *"these look similar"*.

- **Remains auditable over time**
  Each mapping row has a persistent identifier and may be superseded via `replaces`. Releases are **dated**, so you can always reconstruct which mappings were in force at a given point in time.

**To contribute to the SSSOM Mapping Set,** you can:

- If you **maintain or can edit** an ontology or schema, add `hriv:` mappings directly as axioms there and, if you want them included in the SSSOM Mapping Set, submit the corresponding rows via:
  - The GitHub issue form for a single vetted row, or
  - The Excel template for batches, including labels, identifiers, and provenance.

- If you **cannot edit** the source model, contribute directly to the SSSOM Mapping Set by sending vetted mappings to us using:
  - A single vetted row via the GitHub issue form, or
  - Batches via the Excel template, including labels, identifiers, and provenance.

**To consume the SSSOM Mapping Set:**

- Download the mappings from the stable `w3id` PIDs for the SSSOM Mapping Set: `https://w3id.org/health-ri/semantic-interoperability/mappings` (TTL) or `https://w3id.org/health-ri/semantic-interoperability/mappings/tsv` (TSV).
- Record which **mapping release** (file and date) you used, so your integrations remain reproducible.
- When updating, follow each row's `replaces` lineage to see what changed and stay aligned with newer versions.
- Use the SSSOM TSV directly in your pipelines, or load the published TTL/RDF/OWL version into your triple store or ontology tooling and let `hriv:` relations flow through your processes.

**Call to action:**
For your next integration, pick one standard you already implement and select **one ambiguous term** (a column header, code, or ontology class). Map it once to HRIO through the SSSOM Mapping Set. That single row can immediately connect your term to every other standard aligned with the same HRIO meaning.

<!-- #HealthRI #SemanticInteroperability #SSSOM #SemanticMapping #HRIO #HRIV #HealthData #SemanticWeb -->

**References:**

[1] **Health-RI SSSOM Mapping Set**: https://health-ri.github.io/semantic-interoperability/ontology/mappings/
[2] **Health-RI Ontology (HRIO)**: https://health-ri.github.io/semantic-interoperability/ontology/specification-ontology.html
[3] **Health-RI Mapping Vocabulary**: https://health-ri.github.io/semantic-interoperability/method/specification-vocabulary.html

## Post 8: Trust by Design — Rules, Releases, and the `replaces` Chain

**Untraceable data pipelines are fragile pipelines.** Trust in semantic data doesn't just happen; it's built via **governance** that is visible and verifiable.

Health-RI enforces **role separation** (Mapper ≠ Reviewer; Curator publishes), **promotion gates** (validation before release), and an **append-only** history where mapping rows are **superseded**, never overwritten.

What this guarantees:

- **Reproducibility** — every release is **dated**; ontology has a **version IRI**; pipelines can be pinned.
- **Auditability** — each row tracks author/reviewer **provenance**; you can trace a row's **`replaces`** lineage.
- **Stability** — **w3id PIDs** keep links durable as artifacts evolve.

Operational tip:
Record both the **ontology version IRI** and the **mapping release date** in your ETL runs and reports.

**Call to action:** Pin your next job to a specific **version IRI + release date**, and verify the row's `replaces` chain before promotion.

**References:**

- *Mapping Governance, Lifecycle & Validation.* Accessed Nov 6, 2025. <https://health-ri.github.io/semantic-interoperability/method/mapping-governance/>
- *Initiative Publications — Release & versioning policy.* Accessed Nov 6, 2025. <https://health-ri.github.io/semantic-interoperability/method/publications/>
- *Persistent Identifiers (w3id) — Policy & Endpoints.* Accessed Nov 6, 2025. <https://health-ri.github.io/semantic-interoperability/method/persistent-ids/>

## Post 9: Iterate in Public — Culture & How to Contribute (Issue Form / XLSX)

**Shortcuts create false agreement later.** We do the hard work **now** and iterate in the open: propose, review, **supersede**—never edit in place. Semantic interoperability is a **team sport**; durable meaning emerges from **open participation**.

Mappings ship as a well-researched **first draft**, then improve via review and **supersession**—never by editing in place.

Two contribution paths:

- **Issue form** — a single SSSOM row (fast lane).
- **XLSX template** — batch rows with CURIE prefixes (bulk lane).

Minimum you provide:

- **Labels with language tags** (e.g., `Patient@en`, `Patiënt@nl`)
- **Provenance** (author + reviewer, ideally with ORCIDs)
- **Rationale** for non-obvious alignments

Process:
Mapper submits → Reviewer approves/rejects → Curator validates → Released with date; prior row marked as **replaced**.

**Call to action:** Submit one **"nail-the-meaning"** example via the **Mapping** issue form (a single row is fine); we'll review and publish it in the next dated release.

**References:**

- *SSSOM Mapping Set — Schema & Contribution routes.* Accessed Nov 6, 2025. <https://health-ri.github.io/semantic-interoperability/method/mapping-schema/>
- *Mapping Governance, Lifecycle & Validation.* Accessed Nov 6, 2025. <https://health-ri.github.io/semantic-interoperability/method/mapping-governance/>

## Post 10: FAIR is Broken Without PIDs. Here's How We Fix It

**Stable, resolvable identifiers are the quiet infrastructure behind interoperability.** If your link breaks, your data isn't Findable or Accessible anymore.

Health-RI publishes **persistent identifiers (w3id)** for the initiative, the ontology, and mapping artifacts—so people and machines always land on the **current, citable** resource.

What you get: frictionless links for specs, Turtle/TSV downloads, and documentation that won't rot as URLs change. That's Findable/Accessible in FAIR, operationalized.

Impact: consistent citations in papers and portals; stable APIs for pipelines; fewer broken integrations during upgrades.

**Call to action:** Bookmark the PID page and wire these URIs into your catalogs, ETL, and scripts; if you need additional resolvers, open an issue.

**References:**

[8] *Persistent Identifiers (w3id) — Policy & Endpoints*, accessed 6 Nov 2025. <https://health-ri.github.io/semantic-interoperability/method/persistent-ids/>
[9] *Initiative Publications — Release & versioning policy*, accessed 6 Nov 2025. <https://health-ri.github.io/semantic-interoperability/method/publications/>
