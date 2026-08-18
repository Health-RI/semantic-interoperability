# Package Metadata (after v1.0.0)

**Status:** Introduced after **version 1.0.0** of the Health-RI Ontology.
Before v1.0.0 there were **no package-specific metadata**; only ontology-level metadata existed.

**Scope:** These fields apply to **UML Packages** (each logical package in the model). They are implemented as **tagged values on a package stereotype** and exported by CI to RDF for FAIR discovery and governance.

> **Note:** The **Title** and **Description** of a package are **not tagged values**. They must be filled using Visual Paradigm's **default "Name/Title" and "Description" fields** on the Package element. Do not duplicate these as tags.

---

## Design principles

* **Minimal maintenance:** Only a handful of fields, most of which are **CI-managed**.
* **No duplication:** Do **not** repeat ontology-level metadata (license, publisher, namespace, landing page).
* **Traceable to releases:** Version references point to the model version (e.g., `0.11.5`), because packages are not versioned independently.

---

## Tag set (per Package)

All tags live under the custom stereotype (e.g., `«HRI Package Metadata»`). The table specifies the **type**, **multiplicity**, **who sets it**, **when it changes**, and **example values**.

| Tag name                  | Type                      | Mult. | Set by          | When it changes                                              | Example                                 |            |                        |       |
| ------------------------- | ------------------------- | ----: | --------------- | ------------------------------------------------------------ | --------------------------------------- | ---------- | ---------------------- | ----- |
| `stage`                   | enum (`int                |   irv | erv             | pub`)                                                        | 1                                       | Maintainer | On workflow transition | `irv` |
| `introducedInVersion`     | string (model version)    |     1 | CI (first seen) | Only once (first release that includes this package)         | `0.10.2`                                |            |                        |       |
| `lastChangedInVersion`    | string (model version)    |  0..1 | CI              | When semantic changes occur to this package between releases | `0.11.5`                                |            |                        |       |
| `lastPublishedInVersion`  | string (model version)    |  0..1 | CI              | When this package reaches `pub` in a release                 | `0.11.5`                                |            |                        |       |
| `reviewedBy`              | list of IRIs (ORCID URIs) |  0..* | Reviewers/CI    | Each time the stage's review completes; overwrite per stage  | `https://orcid.org/0000-0003-2736-7817` |            |                        |       |
| `reviewedOn` *(optional)* | date (`YYYY-MM-DD`)       |  0..1 | CI              | When the stage's checklist passes                            | `2025-10-24`                            |            |                        |       |

**Exact meanings**

* **`stage`** – Current workflow state for the package.
* **`introducedInVersion`** – First model version in which this package appears. Immutable.
* **`lastChangedInVersion`** – Most recent model version where this package's semantics changed (classes, relations, constraints, or formal annotations). Ignore cosmetic layout/doc edits.
* **`lastPublishedInVersion`** – Most recent model version where this package reached `pub` (i.e., formally published).
* **`reviewedBy`** – ORCID URIs of reviewers.

---

## What stays in default VP fields (not tags)

* **Title** (Package name) — *Visual Paradigm's built-in "Name/Title".*
* **Description** — *Visual Paradigm's built-in "Description".*

  * Keep it concise (1–3 sentences) and scoped to **what this package adds** beyond the ontology-level description.

---

## RDF export (illustrative)

During the site build/release, CI emits a simple RDF representation for each package resource (example CURIEs shown):

```ttl
:Package/admin-legal-gender
  a hri:Package ;
  dct:title "Administrative & Legal Gender"@en ;          # from VP's default fields
  dct:description "Concepts and relations for ..."@en ;   # from VP's default fields
  hri:stage "irv" ;
  hri:introducedInVersion "0.10.2" ;
  hri:lastChangedInVersion "0.11.5" ;
  hri:lastPublishedInVersion "0.11.5" ;
  hri:validatedBy <https://orcid.org/0000-0003-2736-7817>,
                  <https://orcid.org/0000-0003-1451-4240> ;
  prov:wasValidatedAtTime "2025-10-24"^^xsd:date .
```

> We intentionally keep these as **custom `hri:*` properties** to avoid overloading generic predicates. Mapping to other vocabularies (e.g., `adms:status`, `dct:hasVersion`) can be added later if needed.

---

## Migration note (pre-1.0.0 models)

* For releases **before 1.0.0**, packages lack these tags. CI should **not fail** on missing metadata for historical versions.
