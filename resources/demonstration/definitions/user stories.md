# User Stories for the Demo

## Framing note

In this demo, the stakeholder-facing story is told in terms of **datasets hosted by different institutions** and **catalog entries curated for discovery and reuse**. Each dataset is described through its metadata or data dictionary, and its columns are treated as the **representation concepts** that are mapped to shared ontology meanings.

Technically, the current demo operates at the **metadata and mapping layer**, not at the patient-data layer. Patient data remain inside each institution. The queryable graph is the enriched semantic graph generated from the demo inputs and materialized in `instances_extended.ttl`.

______________________________________________________________________

## 1) Dr. Amir Hassan — Researcher

**As Dr. Amir Hassan, a researcher preparing a multicenter study across datasets hosted by different institutions, I want to discover which cataloged datasets contain variables that match the exact meaning I need for cohort selection and analysis, and I want to verify whether similarly labeled variables across institutions are truly compatible or not, so that I can select the right datasets for reuse and avoid combining data that represent different concepts.**

### Narrative

Dr. Amir Hassan is preparing a study whose inclusion criteria depend on a clinically important semantic distinction. His real research question is not “sex and gender” in isolation; rather, he is studying a condition, subgroup, or outcome for which semantic precision matters. To answer that question correctly, he needs to know whether the datasets available through different institutions actually implement the concept he needs.

At first glance, multiple datasets appear promising. Their catalogs contain columns with labels such as “sex,” “gender,” `Patient.gender`, or other related terms. However, Dr. Hassan cannot rely on labels alone. One dataset may implement **biological sex**, another may implement **administrative gender**, and another may implement **self-identified gender**. These are not interchangeable for many research purposes.

In the demo story, Dr. Hassan therefore begins at the **catalog and semantic metadata level**. He does not query patient records directly. Instead, he uses the semantic interoperability layer to determine which dataset columns correspond to the meaning he needs, which ones only partially match, which ones remain uncertain, and which ones are clearly incompatible.

### What he is trying to achieve

Dr. Hassan wants to:

- identify which institution-hosted datasets are relevant for his study;
- determine which dataset columns implement the exact meaning he needs;
- compare similar-looking variables across institutions and standards;
- exclude variables whose meanings are incompatible or too ambiguous;
- build a defensible dataset-selection strategy before requesting access.

### How the demo supports him

A plausible researcher workflow is:

1. **Define the semantic scope of the concept of interest**
    He starts from an ontology concept and retrieves its narrower concepts to clarify the semantic boundary of the cohort or variable he is looking for.

2. **Find which representation concepts are connected to that meaning**
    He then discovers where that meaning already appears across available dataset columns, standards, and local models.

3. **Inspect the meaning of a selected dataset column**
    For a promising variable, he retrieves the ontology meanings already associated with it, including polarity and provenance.

4. **Compare two candidate columns directly**
    He checks whether two variables from different institutions fully align, partially align, may align, or cannot align.

5. **Assess the semantic neighborhood around one selected concept**
    He retrieves exact matches, incompatible concepts, potential matches for review, and partial matches, so he can decide what is safe to reuse.

6. **Check consistency before reuse**
    Before trusting a variable in study design, he verifies that it is not semantically inconsistent.

7. **Optionally assess the effect of treating two concepts as equivalent**
    If he is considering a broader reuse decision, he can assess the consequences of a proposed alignment before acting on it.

### Why this matters

This story shows the value of the initiative from the researcher’s perspective: it helps him choose the **right datasets**, not just the right-looking labels. It reduces the risk of invalid cohort selection, inappropriate variable pooling, and wasted effort requesting access to datasets that do not actually implement the concept required by the study.

### One-sentence presentation version

**Dr. Amir Hassan uses the semantic interoperability layer to identify which datasets across institutions truly implement the concept he needs, and to avoid combining variables that only look similar by label.**

______________________________________________________________________

## 2) Inge de Boer — Data Steward

**As Inge de Boer, a data steward responsible for curating dataset descriptions and catalog entries across institutions, I want to associate dataset columns with the correct shared meanings, review how local concepts relate to standard concepts, detect inconsistencies, and assess the consequences of proposed alignments before publication, so that the catalog remains semantically trustworthy and researchers can reliably discover and compare datasets.**

### Narrative

Inge de Boer is responsible for the semantic quality of dataset descriptions published through organizational or cross-institutional catalogs. She does not manipulate raw patient data directly. Instead, she curates the **semantic layer above the data**: metadata, data-dictionary columns, mappings to ontology concepts, and alignments between local and standard concepts.

In the demo story, each dataset column is treated as a representation concept. Inge’s job is to make sure that these representation concepts are mapped to the correct shared meanings, that reused mappings are trustworthy, and that misleading or unsafe alignments are caught before publication.

This is especially important when datasets from different institutions use overlapping or ambiguous labels. A local column may appear to correspond to a familiar standard term, but the semantic relation may turn out to be only partial, uncertain, or even incompatible. Inge therefore needs tools not only for mapping, but also for **quality control, remediation, and impact assessment**.

### What she is trying to achieve

Inge wants to:

- curate catalog entries so dataset columns carry the correct shared meanings;
- reuse existing trusted mappings where possible;
- compare local columns with standard or external concepts before publication;
- identify semantically inconsistent concepts that require remediation;
- prevent harmful alignments from being published into the catalog;
- make dataset discovery more reliable for downstream researchers.

### How the demo supports her

A plausible stewardship workflow is:

1. **Clarify the semantic scope of a target concept**
    She explores the ontology hierarchy to decide whether a local column should map to a broad concept or to a more specific descendant.

2. **Check where a meaning is already in use**
    She retrieves all concepts connected to a selected ontology meaning so she can reuse prior work and avoid duplicate mapping effort.

3. **Inspect the current commitments of a selected concept**
    She reviews the meanings already attached to a local data element before editing or publishing its mappings.

4. **Compare a local concept with a candidate target**
    She checks whether two concepts already align, partially align, may align, or cannot align.

5. **Assess all semantic alignments around a concept**
    She retrieves exact matches, incompatible concepts, potential candidates, and partial overlaps to determine what can safely be reused.

6. **Check the consistency of one selected concept**
    Before publication, she verifies that a local concept does not carry contradictory semantic commitments.

7. **Retrieve all semantically inconsistent concepts**
    At the catalog level, she identifies and prioritizes concepts that require remediation.

8. **Assess the consequences of a proposed alignment**
    Before accepting a new alignment, she simulates what additional relations it would introduce and whether those consequences are acceptable.

### Why this matters

This story shows the governance value of the initiative. It is not only about helping people find datasets; it is also about maintaining a semantic layer that researchers can trust. Inge’s work ensures that published catalog entries support accurate discovery, safer comparison, and more reliable reuse across institutions.

### One-sentence presentation version

**Inge de Boer curates the semantic layer behind dataset catalogs so researchers can discover, compare, and select datasets across institutions with much greater trust and precision.**

______________________________________________________________________

## Combined value proposition

Together, these two stories show both sides of the initiative:

- **Research value:** researchers can identify which datasets are truly fit for purpose.
- **Governance value:** data stewards can maintain a trustworthy semantic layer that makes that selection possible.

The same semantic infrastructure supports both personas: the researcher uses it to make better reuse decisions, and the data steward uses it to create and maintain the semantic quality required for those decisions.

______________________________________________________________________

## Very short slide-ready version

### Dr. Amir Hassan — Researcher

Dr. Amir Hassan is preparing a multicenter study and needs to know which institution-hosted datasets actually implement the concept required for his research question. Because similar-looking columns may represent different meanings, he uses the semantic interoperability layer to discover relevant dataset columns, compare concepts across institutions, and exclude variables that are incompatible or ambiguous before requesting access.

### Inge de Boer — Data Steward

Inge de Boer curates dataset descriptions and catalog entries across institutions. She uses the semantic interoperability layer to map dataset columns to the correct shared meanings, review how local concepts relate to standards, detect inconsistencies, and assess the consequences of proposed alignments before publication, so that researchers can reliably discover and compare datasets.
