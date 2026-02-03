# Scripts

This folder contains utility scripts used across the Health-RI Semantic Interoperability repository—mainly for documentation generation, version housekeeping, ontology release prep, and mapping conversions.

<!-- omit from toc -->
## Table of Contents

- [Dependencies (Python)](#dependencies-python)
- [Python scripts](#python-scripts)
  - [`docgen-ontouml.py` — OntoUML JSON → Markdown docs](#docgen-ontoumlpy--ontouml-json--markdown-docs)
  - [`docgen-pylode.py` — TTL → HTML specification (PyLODE), with post-processing](#docgen-pylodepy--ttl--html-specification-pylode-with-post-processing)
  - [`insert-metadata.py` — Merge release metadata into the latest ontology TTL](#insert-metadatapy--merge-release-metadata-into-the-latest-ontology-ttl)
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
  - [Keeping `scripts/requirements.txt` correct](#keeping-scriptsrequirementstxt-correct)

## Dependencies (Python)

Depending on the script, you may need:

- Python 3.x
- `packaging`
- `rdflib`
- `beautifulsoup4`
- `pylode` CLI available on `PATH` (for `docgen-pylode.py`)

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

Builds HTML specifications from the latest ontology TTL and the latest mapping vocabulary TTL using PyLODE, then patches the generated HTML.

- **Inputs (auto-detected):**
  - Ontology: `ontologies/versioned/health-ri-ontology-vX.Y.Z.ttl`
  - Vocabulary: `vocabulary/versioned/health-ri-vocabulary-vX.Y.Z.ttl`
- **Outputs:**
  - Ontology:
    - `docs/ontology/specification-ontology.html`
    - `ontologies/versioned/documentations/specification-vX.Y.Z.html`
    - `ontologies/latest/documentations/specification.html`
  - Vocabulary:
    - `docs/method/specification-vocabulary.html`
    - `vocabulary/versioned/documentations/specification-vX.Y.Z.html`
    - `vocabulary/latest/documentations/specification.html`
- **Key characteristics:**
  - Only runs PyLODE if the versioned output for the detected version does **not** exist.
    - If the versioned output exists, it simply copies it into `docs/` and `latest/` (no re-generation).
  - Post-processing on freshly generated HTML:
    - Rewrites broken internal `file://...specification.html#...` links to `#...`
    - Sorts ToC entries for section IDs `classes` and `annotationproperties`
    - Inserts a Health-RI logo at the top of `<body>` using `../assets/images/health-ri-logo-blue.png`
- **Run:** `python scripts/docgen-pylode.py`

### `insert-metadata.py` — Merge release metadata into the latest ontology TTL

Merges a Turtle metadata template into the latest versioned ontology TTL, and adds/updates release triples.

- **Inputs:**
  - Latest TTL (auto-detected): `ontologies/versioned/health-ri-ontology-vX.Y.Z.ttl`
  - Template: `scripts/utils/metadata-template.ttl`
- **Behavior:**
  - Guarded merge: merges the template **only if** the graph does *not* already contain
    `?s dct:issued "2025-05-20"^^xsd:date` (hard-coded sentinel check).
  - Adds (to `https://w3id.org/health-ri/ontology`):
    - `dct:modified` (today’s date, `xsd:date`)
    - `owl:versionInfo` (`X.Y.Z`)
    - `owl:versionIRI` (`https://w3id.org/health-ri/ontology/vX.Y.Z`)
    - `dct:conformsTo` links:
      - `https://w3id.org/health-ri/ontology/vX.Y.Z/vpp`
      - `https://w3id.org/health-ri/ontology/vX.Y.Z/json`
  - **Overwrites** the latest versioned TTL file in place.
- **Run:** `python scripts/insert-metadata.py`

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

The repository’s documentation deployment workflow (`deploy.yml`) uses `scripts/requirements.txt` as the source of truth for installing Python dependencies (and as the pip cache key), then runs a fixed generation pipeline.

### Pipeline (high level)

1. Install dependencies: `pip install -r scripts/requirements.txt`
2. Run generation steps:
   - `clean-unwanted-files.py`
   - `insert-metadata.py`
   - `move-latest.py`
   - `docgen-ontouml.py`
   - `docgen-pylode.py`
   - `sssom-tsv2ttl.py`
3. Build and validate the site (`mkdocs build`) and check links (`linkchecker`).

### Keeping `scripts/requirements.txt` correct

- This file should include dependencies for **all scripts executed in the workflow**.
- In particular, `insert-metadata.py` depends on `rdflib`, so `rdflib` should be listed here.
