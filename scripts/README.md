# Scripts

This folder contains utility scripts used across the Health-RI Semantic Interoperability repository—mainly for documentation generation, version housekeeping, ontology release prep, and mapping conversions.

<!-- omit from toc -->
## Table of Contents

- [Dependencies (Python)](#dependencies-python)
- [Python scripts](#python-scripts)
  - [`docgen-ontouml.py` — OntoUML JSON → Markdown docs](#docgen-ontoumlpy--ontouml-json--markdown-docs)
  - [`docgen-pylode.py` — TTL → HTML specification (PyLODE), with post-processing](#docgen-pylodepy--ttl--html-specification-pylode-with-post-processing)
  - [`pylode-html-generate.py` — TTL → raw HTML specification (PyLODE)](#pylode-html-generatepy--ttl--raw-html-specification-pylode)
  - [`pylode-html-postprocess.py` — Post-process PyLODE HTML (Health-RI tweaks + optional RDF-driven enhancements)](#pylode-html-postprocesspy--post-process-pylode-html-health-ri-tweaks--optional-rdf-driven-enhancements)
  - [`insert-metadata.py` — Merge release metadata into the latest ontology TTL](#insert-metadatapy--merge-release-metadata-into-the-latest-ontology-ttl)
  - [`owl-postprocess.py` — Post-process ontology TTL using the paired OntoUML JSON export](#owl-postprocesspy--post-process-ontology-ttl-using-the-paired-ontouml-json-export)
  - [`make-diff-ttl.py` — RDF diff graphs between two versions](#make-diff-ttlpy--rdf-diff-graphs-between-two-versions)
  - [`diff-ttl.py` — Convenience wrapper: metadata insertion + diff for last two versions](#diff-ttlpy--convenience-wrapper-metadata-insertion--diff-for-last-two-versions)
  - [`move-latest.py` — Populate `ontologies/latest/` from versioned artifacts](#move-latestpy--populate-ontologieslatest-from-versioned-artifacts)
  - [`sssom-tsv2ttl.py` — Health-RI SSSOM TSV → TTL converter (tailored)](#sssom-tsv2ttlpy--health-ri-sssom-tsv--ttl-converter-tailored)
  - [`clean-unwanted-files.py` — Delete temporary/lock/backup artifacts across the repo](#clean-unwanted-filespy--delete-temporarylockbackup-artifacts-across-the-repo)
- [Batch scripts (Windows)](#batch-scripts-windows)
  - [`make-diff-json.bat` — Unified diff between two OntoUML JSON exports (with noise reduction)](#make-diff-jsonbat--unified-diff-between-two-ontouml-json-exports-with-noise-reduction)
  - [`prepare-image.bat` — Batch-process images for consistent presentation](#prepare-imagebat--batch-process-images-for-consistent-presentation)
  - [`run-clean-unwanted-files.bat` — Interactive wrapper for repo cleanup](#run-clean-unwanted-filesbat--interactive-wrapper-for-repo-cleanup)
  - [`run-merge-metadata.bat` — Wrapper for TTL metadata merge](#run-merge-metadatabat--wrapper-for-ttl-metadata-merge)
- [Workflow / CI integration](#workflow--ci-integration)
  - [Pipeline (high level)](#pipeline-high-level)
  - [Keeping `scripts/requirements-deploy.txt` correct](#keeping-scriptsrequirements-deploytxt-correct)

## Dependencies (Python)

Two requirements files are provided:

- `requirements-deploy.txt`: dependencies used by the documentation deploy workflow (`deploy.yml`).
- `requirements-scripts.txt`: superset needed to run all scripts in this folder locally.

Install for local script runs:

`pip install -r scripts/requirements-scripts.txt`

Some batch scripts also require external tools (e.g., `jq`, `git`/`diff`, ImageMagick).

## Python scripts

### `docgen-ontouml.py` — OntoUML JSON → Markdown docs

Generates Markdown documentation from the latest versioned OntoUML JSON export.

- **Input (auto-detected):** `ontologies/versioned/health-ri-ontology-vX.Y.Z.json` (picks the highest semver)
- **Outputs:**
  - `docs/ontology/documentation.md`
  - `ontologies/versioned/documentations/documentation-vX.Y.Z.md`
  - `ontologies/latest/documentations/documentation.md` (uses `../images` links + URL-encoding)
- **Key characteristics:**
  - Recursively documents packages only if they contain “meaningful content” (package description and/or diagrams with descriptions, including nested packages).
  - Diagram sections are only emitted when a diagram **has a description**.
  - Optional image embedding: if a file exists in `docs/ontology/assets/images/` named **exactly** `<diagram name>.png|.jpg|.jpeg`, it is included under the diagram section.
  - Idempotent behavior: if the versioned Markdown already exists, it **does not** regenerate it; it syncs `docs/` from the versioned file and regenerates only the `latest/` copy (to apply `../images` + URL-encoding).
  - Runs from the repository root (the script `chdir`s to the repo root at startup).
- **Run:** `python scripts/docgen-ontouml.py`

### `docgen-pylode.py` — TTL → HTML specification (PyLODE), with post-processing

Orchestrates generating HTML specifications from the latest versioned TTLs (ontology + vocabulary), while preserving historical (versioned) HTML artifacts.

- **Inputs (auto-detected, highest semver):**
  - Ontology TTL: `ontologies/versioned/health-ri-ontology-vX.Y.Z.ttl`
  - Vocabulary TTL: `vocabulary/versioned/health-ri-vocabulary-vX.Y.Z.ttl`

- **Outputs (per spec):**
  - **Ontology**
    - Docs: `docs/ontology/specification-ontology.html`
    - Versioned: `ontologies/versioned/documentations/specification-vX.Y.Z.html`
    - Latest: `ontologies/latest/documentations/specification.html`
    - Raw intermediate: `build/pylode/ontology/ontology-vX.Y.Z-raw.html`
  - **Vocabulary**
    - Docs: `docs/method/specification-vocabulary.html`
    - Versioned: `vocabulary/versioned/documentations/specification-vX.Y.Z.html`
    - Latest: `vocabulary/latest/documentations/specification.html`
    - Raw intermediate: `build/pylode/vocabulary/vocabulary-vX.Y.Z-raw.html`

- **Key characteristics:**
  - Creates required output folders if missing.
  - Uses `PYLODE_CMD` (environment variable) if set; otherwise defaults to `pylode`.
  - Requires sibling scripts:
    - `scripts/pylode-html-generate.py`
    - `scripts/pylode-html-postprocess.py`
    - If either is missing, exits with code `2`.
  - **Preserves versioned HTML (historical artifacts):**
    - If `.../specification-vX.Y.Z.html` already exists:
      - Copies **versioned → docs**
      - Runs post-processing **on the docs copy** (overwriting `docs/...html`)
      - Copies the post-processed **docs → latest**
      - The **versioned HTML is not modified**
  - **Generates new artifacts only when needed:**
    - If versioned HTML is missing:
      - Generates **raw HTML** via `pylode-html-generate.py` (into `build/pylode/...`)
      - Post-processes raw → **docs output** via `pylode-html-postprocess.py`
      - Copies **docs → versioned** and **docs → latest**
  - Vocabulary run disables package-based restructuring of the `#classes` section by default (`--no-classes-restructure`) to avoid failures when the generated HTML lacks `#classes`.

- **Run:**
  - `python scripts/docgen-pylode.py`

- **Exit codes:**
  - `0`: success
  - `1`: one or more specs failed
  - `2`: invalid inputs / missing scripts

### `pylode-html-generate.py` — TTL → raw HTML specification (PyLODE)

Minimal wrapper around PyLODE that turns a TTL file into a *raw* HTML specification. Intended to be called by an orchestrator that handles versioning/copying.

- **Inputs (CLI):**
  - `--ttl PATH` (required): input TTL file.
  - `--out PATH` (required): output HTML path.
  - `--pylode-cmd CMD` (optional, default `pylode`): PyLODE command to execute.
  - `--overwrite` (optional): overwrite output if it already exists (default is to skip).

- **Behavior:**
  - Ensures the output parent directory exists.
  - If `--out` already exists and `--overwrite` is **not** set, it logs a “skipping generation” message and exits successfully (`0`).
  - Runs PyLODE as: `<pylode-cmd> <ttl> -o <out>` (via `subprocess.run(..., check=True)`).

- **Run (examples):**
  - `python scripts/pylode-html-generate.py --ttl ontologies/versioned/health-ri-ontology-vX.Y.Z.ttl --out build/pylode/ontology/ontology-vX.Y.Z-raw.html --overwrite`
  - `python scripts/pylode-html-generate.py --ttl vocabulary/versioned/health-ri-vocabulary-vX.Y.Z.ttl --out build/pylode/vocabulary/vocabulary-vX.Y.Z-raw.html --overwrite`

- **Exit codes:**
  - `0`: success (including “skipped because output exists”)
  - `1`: PyLODE failed (non-zero subprocess exit)
  - `2`: input TTL not found

### `pylode-html-postprocess.py` — Post-process PyLODE HTML (Health-RI tweaks + optional RDF-driven enhancements)

Post-processes PyLODE-generated HTML using BeautifulSoup, and (optionally) a TTL file via RDFLib for ontology-aware enhancements. Designed to be idempotent.

- **Inputs (CLI):**
  - `--html-in PATH` (required): input HTML file.
  - `--html-out PATH` (optional): output HTML file (default: overwrite `--html-in`).
  - `--ttl PATH` (optional): TTL file used for RDF-driven edits (packages, maturity, synonyms).

- **HTML tweaks (legacy + always-on cleanup):**
  - Removes PyLODE “Is Defined By” table rows from entity tables.
  - Fixes internal links of the form `file://.../specification.html#Anchor` → `#Anchor` (unless `--no-link-fix`).
  - Sorts nested ToC lists (`ul.second` / `ul.third`) alphabetically (unless `--no-toc-sort`).
  - Inserts the Health-RI logo at the top of `<body>` (unless `--no-logo`; idempotent by `src`).
  - Injects a responsive TOC/content split CSS override (unless `--no-toc-css`; idempotent via `<style id="healthri-toc-split-override">`).

- **Ontology-aware enhancements (require `--ttl`, and can be individually disabled):**
  - **Restructure `#classes` by package** (disable with `--no-classes-restructure`):
    - Reads `dcterms:isPartOf` triples (class → package IRI).
    - If the package IRI contains `#package/<segment>/...`, it groups classes by the first `<segment>` and maps them to a *top-level package IRI* `...#package/<segment>`.
    - Inserts package headings (`<h3 id="pkg-<segment>">Package: <rdfs:label></h3>`) and rebuilds the “Classes” ToC subtree accordingly.
    - If a top-level package IRI exists in the TTL, `rdfs:label` is **mandatory** (missing/empty label triggers an error).
    - If a package has `vs:term_status` (`int|irv|erv|pub`), inserts a Shields.io maturity badge (linked to the maturity docs URL) under the package heading.
    - If `#classes` is missing and restructuring is enabled, this is treated as a structure error (exit code `2`).
    - Post-check: raises an error if the class count changes after restructuring.
  - **Insert/update a “Synonyms” row per class** from `skos:altLabel` (disable with `--no-synonyms`):
    - Adds/updates a table row labeled “Synonyms” (with a predicate-style header link to `skos:altLabel`).
    - Uses a comma-separated list of `skos:altLabel` values for that class IRI.
    - Inserts after “Description” if present; otherwise after “IRI”.

- **Validation:**
  - Ensures no duplicate class anchor IDs in `#classes` (hard error if duplicates).
  - Warns if any ToC `#anchor` target is missing in the HTML.

- **Options (summary):**
  - `--no-link-fix`, `--no-toc-sort`, `--no-logo`, `--logo-url ...`, `--logo-alt ...`, `--no-toc-css`,
    `--no-classes-restructure`, `--no-synonyms`

- **Run (examples):**
  - `python scripts/pylode-html-postprocess.py --html-in build/pylode/ontology/ontology-vX.Y.Z-raw.html --ttl ontologies/versioned/health-ri-ontology-vX.Y.Z.ttl --html-out docs/ontology/specification-ontology.html`
  - `python scripts/pylode-html-postprocess.py --html-in build/pylode/vocabulary/vocabulary-vX.Y.Z-raw.html --ttl vocabulary/versioned/health-ri-vocabulary-vX.Y.Z.ttl --no-classes-restructure --html-out docs/method/specification-vocabulary.html`

- **Exit codes:**
  - `0`: success
  - `1`: generic failure (unexpected exception)
  - `2`: input/structure error (e.g., missing input files, missing `#classes` when restructuring enabled, missing required package labels)

### `insert-metadata.py` — Merge release metadata into the latest ontology TTL

Merges a Turtle metadata template into the latest versioned ontology TTL, and (on first merge) adds release/versioning triples.

- **Inputs:**
  - Latest TTL (auto-detected): `ontologies/versioned/health-ri-ontology-vX.Y.Z.ttl`
  - Template: `scripts/utils/metadata-template.ttl`
- **Behavior:**
  - Auto-detects the latest TTL by parsing versions from filenames matching:
    `health-ri-ontology-v<MAJOR>.<MINOR>.<PATCH>.ttl`.
  - Guarded merge: performs the merge **only if** the graph does *not* already contain
    `?s dct:issued "2025-05-20"^^xsd:date` (hard-coded sentinel check). If the sentinel is found, the script logs and exits without modifying the TTL.
  - Merges the template TTL into the latest versioned TTL graph and carries over template namespaces/prefixes.
  - Adds (to `https://w3id.org/health-ri/ontology`):
    - `dct:modified` (today’s date, `xsd:date`)
    - `owl:versionInfo` (`X.Y.Z`)
    - `owl:versionIRI` (`https://w3id.org/health-ri/ontology/vX.Y.Z`)
    - `dct:conformsTo` links:
      - `https://w3id.org/health-ri/ontology/vX.Y.Z/vpp`
      - `https://w3id.org/health-ri/ontology/vX.Y.Z/json`
    - `dcat:hasVersion` for **prior** versions found in `ontologies/versioned/` as:
      - `https://w3id.org/health-ri/ontology/vA.B.C`
      - By default, only the latest patch per `(MAJOR, MINOR)` line is kept (`LATEST_PER_MINOR = True`).
  - Adds (to the current version IRI node `https://w3id.org/health-ri/ontology/vX.Y.Z`):
    - `owl:priorVersion` pointing to the immediate predecessor version IRI (highest version strictly lower than `X.Y.Z` found in the versioned TTL folder).
  - Output readability cleanup after RDFLib serialization:
    - Moves the ontology subject block (`<https://w3id.org/health-ri/ontology> a owl:Ontology ...`) to the top (after `@prefix`/`@base`).
    - Moves the current version subject block (`<.../vX.Y.Z> ...`) to appear immediately after the ontology block.
  - **Overwrites** the latest versioned TTL file in place.
- **Run:** `python scripts/insert-metadata.py`

### `owl-postprocess.py` — Post-process ontology TTL using the paired OntoUML JSON export

Enriches the latest versioned ontology TTL using the latest *matching* versioned OntoUML JSON export (same `X.Y.Z`), adding labeling, package resources, membership, package maturity/status, and minor literal cleanup.

- **Inputs (auto-detected):** latest *matching* semver pair from `ontologies/versioned/`:
  - `ontologies/versioned/health-ri-ontology-vX.Y.Z.ttl`
  - `ontologies/versioned/health-ri-ontology-vX.Y.Z.json`
- **Behavior:**
  - **Locating inputs**
    - Walks upward from the script location to find a repository directory that contains `ontologies/versioned/`.
    - Selects the latest version `X.Y.Z` for which *both* `.ttl` and `.json` exist.
  - **SKOS labels**
    - Keeps existing `rdfs:label` triples.
    - Mirrors every `rdfs:label` into `skos:prefLabel` (same literal, including language tag).
    - Avoids creating multiple `skos:prefLabel` values for the same subject+language:
      - If a `prefLabel` already exists for that language, the mirror is skipped (counted as a conflict).
    - For JSON elements with tagged value `synonyms` (or `synonym`) under `propertyAssignments`:
      - Splits the string on commas into multiple labels (trimmed; de-duplicated).
      - Adds one `skos:altLabel` per label to the RDF subject whose `rdfs:label` string matches the JSON element’s `name`.
      - Uses the same language tag as the matched `rdfs:label` literal.
      - Does **not** add an `altLabel` identical to the resource’s `prefLabel` for the same language (SKOS disjointness).
      - If the JSON `name` does not map uniquely to exactly one `rdfs:label`, the synonym record is skipped (tracked as “unmapped”).
  - **Ontology ownership**
    - Adds `rdfs:isDefinedBy <https://w3id.org/health-ri/ontology>` to every `hrio:` URI that appears anywhere in the graph (as subject, predicate, or object).
  - **Packages (from JSON)**
    - Creates/ensures a package resource for every JSON Package:
      - IRI pattern: `https://w3id.org/health-ri/ontology#package/{PackagePath}`
      - `{PackagePath}` is normalized per path segment to UpperCamelCase (alphanumeric tokenization) and joined with `/`.
    - For each package resource, ensures:
      - `rdf:type skos:Collection`
      - `rdfs:label "..."@en` (if missing; defaults to the raw last segment of the JSON package path)
      - `skos:prefLabel` is produced by the label-mirroring step (a second mirror pass is run after package labels are ensured).
  - **Package membership (from JSON)**
    - For each JSON Class nested in a JSON Package, adds:
      - `dcterms:isPartOf <...#package/{PackagePath}>`
      - Matches the RDF resource by `rdfs:label` string == JSON Class `name` (must map uniquely).
    - Optional reconciliation (enabled by default via `RECONCILE_PACKAGE_MEMBERSHIP = True`):
      - Removes other `dcterms:isPartOf` values in the `...#package/` namespace for the class, keeping only the JSON-derived membership.
  - **Package maturity/status (from JSON, with inheritance)**
    - For each JSON Package resource, writes:
      - `vs:term_status "int|irv|erv|pub"`
    - Stage values are inherited from the closest ancestor package that has `propertyAssignments.stage`.
      - If no ancestor has `stage`, no `vs:term_status` is written for that package.
    - Optional reconciliation (enabled by default via `RECONCILE_PACKAGE_STATUS = True`):
      - Removes existing `vs:term_status` values for each package before writing the computed one.
    - If an effective stage is not one of `int|irv|erv|pub`, the script warns but still writes it.
  - **Migration/cleanup (enabled by default via `MIGRATE_PERCENT_ENCODED_PACKAGE_IRIS = True`)**
    - Removes legacy percent-encoded package IRIs (e.g., `...#package/Health%20Condition`) and their related triples.
    - Normalizes `rdfs:comment` line endings to LF only (removes stray `\r` / CRLF).
  - **Safety/correctness**
    - File size guardrails (`MAX_TTL_BYTES`, `MAX_JSON_BYTES`).
    - Basic sanity check: warns (or errors in `STRICT_MODE`) if the ontology node is not found as `owl:Ontology`.
    - Atomic write (`.tmp` then replace) to avoid partially written TTL files on failure.
  - **Notes:**
    - RDFLib serialization does **not** preserve Turtle comments (`# ...`) or prefix ordering.
  - **Overwrites** the latest versioned TTL file in place.
- **Run:** `python scripts/owl-postprocess.py`

### `make-diff-ttl.py` — RDF diff graphs between two versions

Computes “additions”, “removals”, and optionally “unchanged” graphs between two RDF files, with normalization to reduce bnode/list noise.

- **Inputs:** two files: `OLD` and `NEW` (any RDF format supported by RDFLib; TTL is typical)
- **Outputs (defaults):**
  - `diff.additions.ttl` (NEW − OLD)
  - `diff.removals.ttl` (OLD − NEW)
  - `diff.unchanged.ttl` (intersection; omit with `--no-unchanged`)
  - Output extension matches `--format` (default `turtle` → `.ttl`)
- **Key characteristics:**
  - Canonicalizes RDF lists for OWL list-bearing predicates:
    - `owl:unionOf`, `owl:intersectionOf`, `owl:oneOf`, `owl:members`,
      `owl:disjointUnionOf`, `owl:propertyChainAxiom`, `owl:hasKey`
  - Determinizes list-head blank nodes by hashing the (sorted) member set and rewiring pointers.
  - Prunes orphaned list chains by default (disable with `--no-prune-lists`).
  - Canonicalizes `owl:equivalentClass` direction to `<URI> owl:equivalentClass _:bnode` when mixed.
  - Canonicalizes symmetric edges by default (disable with `--no-symmetric-canon`):
    - `owl:sameAs`, `owl:equivalentProperty`, `owl:disjointWith`
  - Two diff modes:
    - `isomorphic` (default; `rdflib.compare.graph_diff`)
    - `simple` (canonical NT set-diff after isomorphic canonicalization)
- **Run (example):**
  - `python scripts/make-diff-ttl.py old.ttl new.ttl --out-prefix diff --log-level INFO`

### `diff-ttl.py` — Convenience wrapper: metadata insertion + diff for last two versions

Runs `insert-metadata.py`, then runs `make-diff-ttl.py` using either provided paths or (by default) the last two versioned ontology TTLs.

- **Inputs:**
  - Optional: `OLD` and `NEW` TTL paths
  - Default: auto-picks the last two `health-ri-ontology-vX.Y.Z.ttl` files from `ontologies/versioned/`
- **Key characteristics:**
  - Enforces “both or none” for positional args:
    - provide both OLD and NEW, or provide none to auto-pick
  - `--dry-run` prints the commands without executing them
- **Run:**
  - `python scripts/diff-ttl.py`
  - `python scripts/diff-ttl.py path/to/old.ttl path/to/new.ttl`

### `move-latest.py` — Populate `ontologies/latest/` from versioned artifacts

Copies the latest versioned ontology artifacts to `ontologies/latest/` using versionless filenames.

- **Inputs (auto-detected):** latest semver-matching files in `ontologies/versioned/` for:
  - `.json`, `.ttl`, `.vpp`
- **Outputs:**
  - `ontologies/latest/health-ri-ontology.json`
  - `ontologies/latest/health-ri-ontology.ttl`
  - `ontologies/latest/health-ri-ontology.vpp`
- **Key characteristics:**
  - Uses semantic version parsing to pick the latest.
  - Preserves file metadata via `shutil.copy2`.
- **Run:** `python scripts/move-latest.py`

### `sssom-tsv2ttl.py` — Health-RI SSSOM TSV → TTL converter (tailored)

Converts the repository’s SSSOM TSV mappings file into Turtle, minting one `sssom:Mapping` resource per row and one `sssom:MappingSet` resource for the set.

- **Fixed paths (as implemented):**
  - Input: `./mappings/health-ri-mappings.tsv`
  - Output: `./mappings/health-ri-mappings.ttl`
- **Key characteristics:**
  - Parses a lightweight metadata block from commented header lines (YAML-like).
  - Parses a prefix map from `# prefixes:` or `# curie_map:` and emits a complete, deterministic `@prefix` block in the output (stripping any RDFLib-emitted prefixes).
  - Ensures core prefixes exist to avoid `ns1/ns2` fallbacks (e.g., `rdf`, `rdfs`, `owl`, `xsd`, `pav`, `dcat`, `skos`) and sets a default:
    - `hrim: https://w3id.org/health-ri/semantic-interoperability/mappings#`
  - For each row, mints a mapping URI from `record_id`:
    - If `record_id` is not already a CURIE/IRI, it becomes `hrim:<record_id>`.
    - Adds `rdf:type sssom:Mapping`.
    - Stores the core triple using:
      - `owl:annotatedSource` = `subject_id`
      - `owl:annotatedProperty` = `predicate_id`
      - `owl:annotatedTarget` = `object_id`
    - Adds selected SSSOM/related fields when present (examples):
      - `sssom:subject_label` / `sssom:object_label` (supports `@lang` parsing)
      - `sssom:predicate_modifier`, `sssom:object_category`, `sssom:mapping_justification`
      - `pav:authoredBy`, `pav:authoredOn` (`xsd:date`)
      - `dcterms:creator`, `dcterms:issued` (`xsd:date`)
      - `rdfs:comment` (always `@en`), `dcat:replaces`
      - `sssom:subject_type` (normalizes common EntityTypeEnum-like values)
      - `sssom:subject_source` (from column), `sssom:object_source` (forced to `hrio:`)
  - Creates a single MappingSet resource:
    - URI: `https://w3id.org/health-ri/semantic-interoperability/mappings#`
    - `rdf:type sssom:MappingSet`
    - Links all mappings via `sssom:mappings`
    - Populates mapping-set metadata from header comments where available (e.g., `dcterms:license` with default CC BY 4.0, `dcterms:title`, `dcterms:description`, `owl:versionInfo`, `sssom:sssom_version`, `sssom:mapping_set_id`, `sssom:issue_tracker`, etc.)
  - Note: The top docstring shows an `-i/-o` CLI example, but the script currently runs with fixed paths (edit the two `Path(...)` values in `main()` if needed).
- **Run:** `python scripts/sssom-tsv2ttl.py`

### `clean-unwanted-files.py` — Delete temporary/lock/backup artifacts across the repo

Deletes common unwanted files (locks, backups, OS junk) across the repository tree.

- **Scope:** walks from the repository root (computed as the parent of the `scripts/` directory).
- **Key characteristics:**
  - Deletes files matching patterns such as `*.tmp`, `*.bak`, `*.lock`, `Thumbs.db`, `catalog-v*.xml`, etc.
  - Special rule for `.bat`: preserves `.bat` files if their relative path contains a directory segment named `scripts`; deletes `.bat` elsewhere.
  - **Destructive**: permanently removes files.
- **Run:** `python scripts/clean-unwanted-files.py`

## Batch scripts (Windows)

These `.bat` files provide Windows-friendly wrappers around common tasks (diffing, cleanup, image prep, metadata merge).

### `make-diff-json.bat` — Unified diff between two OntoUML JSON exports (with noise reduction)

Creates a unified diff (`diff.txt`) between two JSON files after stripping fields that typically cause irrelevant churn.

- **Inputs:** `OLD.json` and `NEW.json` (optional)
  - Defaults if omitted:
    - `Health-RI Ontology-v0.4.0.json`
    - `Health-RI Ontology-v0.5.0.json`
- **Output:** `diff.txt` (unified diff with `-U0`, `-w`, `--minimal`)
- **Pre-processing (via `jq`):**
  - Deletes any `.shape` fields anywhere in the JSON
  - Deletes any JSON object whose `.type` is a string ending with `"View"`
- **Diff engine:**
  - Prefers GNU `diff` if available
  - Falls back to `git diff --no-index` if `diff` is not installed
- **Notes:**
  - Writes an empty `diff.txt` when there are no differences.
  - Uses a temporary folder under `%TEMP%` and cleans it up on exit.
- **Dependencies:** `jq` + (`diff` **or** `git`) available on `PATH`
- **Run:**
  - `make-diff-json.bat OLD.json NEW.json`
  - `make-diff-json.bat` (uses defaults)

### `prepare-image.bat` — Batch-process images for consistent presentation

Processes all `*.png`, `*.jpg`, `*.jpeg` images in the current folder and writes results to `processed\`.

- **Output folder:** `processed\` (created if missing)
- **Transformations (ImageMagick):**
  - Trims whitespace (`-trim +repage`)
  - Removes alpha channel onto white background (`-background white -alpha remove -alpha off`)
  - Adds ~10% padding around the image (`-extent w*1.1 x h*1.1`, centered)
  - Adds a 10px border in `#F7AD2C`
- **Dependencies:** ImageMagick (`magick`) available on `PATH`
- **Run:** place the `.bat` in (or `cd` to) a folder with images and execute `prepare-image.bat` (it pauses at the end)

### `run-clean-unwanted-files.bat` — Interactive wrapper for repo cleanup

Runs `clean-unwanted-files.py` from the script directory and optionally re-runs it in a loop.

- **Behavior:**
  - Uses `pushd "%~dp0"` to run from the folder where the `.bat` resides (so it can be launched from anywhere)
  - Prompts to re-run (`Y` to repeat; default is `N`)
- **Dependency:** Python available on `PATH`
- **Caution:** the underlying Python script deletes files; review its patterns before running.
- **Run:** `run-clean-unwanted-files.bat`

### `run-merge-metadata.bat` — Wrapper for TTL metadata merge

Runs `merge-metadata.py` and pauses on completion so you can read the console output.

- **Behavior:** does **not** change directories (no `pushd "%~dp0"`), so `merge-metadata.py` must be resolvable from the current working directory.
- **Dependency:** Python available on `PATH`
- **Typical run:** execute it from the directory that contains `merge-metadata.py` (commonly the `scripts/` folder).

## Workflow / CI integration

The repository’s documentation deployment workflow (`deploy.yml`) uses `scripts/requirements-deploy.txt` as the source of truth for installing Python dependencies (and as the pip cache key), then runs a fixed generation pipeline.

### Pipeline (high level)

1. Install dependencies: `pip install -r scripts/requirements-deploy.txt`
2. Run generation steps:
   - `clean-unwanted-files.py`
   - `insert-metadata.py`
   - `add-skos-labels.py`
   - `move-latest.py`
   - `docgen-ontouml.py`
   - `docgen-pylode.py`
   - `sssom-tsv2ttl.py`
3. Build and validate the site (`mkdocs build`) and check links (`linkchecker`).

### Keeping `scripts/requirements-deploy.txt` correct

- `scripts/requirements-deploy.txt` is for the deploy workflow only; keep it limited to what the workflow needs.
- Add script runtime dependencies to `scripts/requirements-scripts.txt`.
- If a new dependency is needed by the deploy workflow, add it to **both** files.
