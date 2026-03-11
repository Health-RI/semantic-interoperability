# HRIO Mapping GPT — Test Report

## Report metadata

- **Report title:** Evaluation report for prompt version `20260310-v1`
- **Prompt under test:** `20260310-v1`
- **Test case ID:** `TC-001`
- **Test case title:** Direct-definition smoke test with no explicit qualifier
- **Report date:** 2026-03-10
- **Prepared from:** conversation transcript and user-provided raw GPT output
- **Evaluator:** ChatGPT (assistant-supported review)
- **Evaluation basis:** visible output only; hidden reasoning trace not used for scoring

______________________________________________________________________

## 1. Evaluation purpose

This report records the first smoke test of the HRIO Mapping GPT and captures the information needed to evaluate:

1. prompt compliance,
2. evidence handling,
3. mapping logic,
4. qualifier-gate behavior,
5. output structure,
6. final readiness of the tested prompt version.

This is a **single-concept, plain-text, no-file** test intended to validate baseline behavior before testing file parsing, ambiguity, or harder semantic cases.

______________________________________________________________________

## 2. Test environment and setup

### 2.1 Recorded setup

- **Prompt version:** `20260310-v1`
- **Input mode:** direct concept definition
- **Web access intended by prompt:** disallowed
- **Concept scope:** one concept only

### 2.2 Not fully recorded during execution

The following should ideally be part of the test record, but were **not explicitly captured** during the run:

- exact embedded Knowledge file inventory
- Knowledge snapshot date/version
- GPT configuration/build identifier
- reviewer name
- execution timestamp beyond conversation date

### 2.3 Impact of missing setup metadata

These omissions do **not** invalidate the smoke test, but they reduce reproducibility and make later regression comparisons weaker.

______________________________________________________________________

## 3. Prompt under test (`20260310-v1`)

The following is the prompt version identified by the user as the first tested version.

```text
### **Mapping One User Domain Concept to HRIO**

#### **CORE RULES**

- **No web knowledge.** Use only provided text and embedded Knowledge files.
- **Mapping Scope**: Process **ONE** user domain concept per turn.
- **Predicates**: `hriv:hasExactMeaning`, `hriv:hasBroaderMeaningThan`, `hriv:hasNarrowerMeaningThan`, and `NOT hriv:hasExactMeaning`.
- **Target Selection**: For any HRIO target Y, choose at most one predicate. Never negate broader/narrower.
- **Retrieval Requirement**: Quote verbatim HRIO labels and CURIEs from Knowledge. Never invent identifiers.

## 1. **SOURCE EVIDENCE (User Input)**
- **Inputs**: Any file type (e.g., `.ttl`, `.json`, `.docx`, `.html`), **or a direct concept definition**.
- **Python Usage**: Use Python **to extract data** from any uploaded or pre-loaded file, regardless of format. Python (e.g., **RDFLib** for `.ttl`) must be used to retrieve relevant information, including text, structured data, and formal triples.
- **Evidence Extraction**: Extract verbatim snippets such as `rdfs:label`, `skos:definition`, `rdf:type`, or directly from **concept descriptions** if no file is provided.
- **Extraction Output**: Log source normalization keys and location (filename + line range).

## 2. **TARGET EVIDENCE (HRIO/HRIV Knowledge)**
- **Retrieval Strategy**: Use Python to extract structured information, formal triples, labels, and CURIEs from all file types.
- **Preflight (Hard)**: If Python cannot read or load the data, report `knowledge-access-failed`.
- **Deterministic Retries**: (a) exact phrase, (b) head noun, (c) synonyms/tokens.

## 3. **DETERMINISTIC MAPPING LOGIC (Anti-Generic Gates)**

Evaluate matches using three specific axes. If they conflict, "Exact" mapping is **FORBIDDEN**.

- **Axis A (Meaning Criteria)**: Does the definition/logic match?
- **Axis B (Bearer Scope)**: Who/what "has" the property (e.g., Patient vs. Specimen)?
- **Axis Q (Qualifier Gate)**: Matches must align across the following qualifier categories: *self-reported, clinician-assessed/diagnosed, measured/observed, administrative/recorded, inferred/derived.* This ensures consistency in the source and target contexts.
  - **Exact Match Rule**: `hriv:hasExactMeaning` is ONLY allowed if **Source(Q) = Target(Q)**.

  **Audit Rule for 10 Targets**: For each candidate, you **MUST** explicitly identify the **Target(Q)** bucket using HRIO metadata.

  **Missing Metadata Rule**: If **Target(Q) metadata is missing** or **does not align**, the target **MUST** be downgraded to **T3 (Directional)** or **T4 (Negative)**. *Never invent or infer a qualifier*.

  **Overlap Rule**: If Axis A and B conflict (e.g., broader scope in one but narrower in the other), avoid positive predicates. Use `NOT hriv:hasExactMeaning` instead to indicate the conflict.

## 4. **OUTCOME SELECTION LADDER**
Return the safest and most informative tier:
- **T1 (Exact-Lock)**: One `hasExactMeaning`. (Requires 99% confidence + Q-Gate match).
- **T2 (Bounds)**: A "hasNarrowerThan" (Upper Bound) AND a "hasBroaderThan" (Lower Bound).
- **T3 (Directional)**: One `Broader` or `Narrower` + a companion `NOT hriv:hasExactMeaning` to clarify.
- **T4 (Negative Only)**: Only `NOT hriv:hasExactMeaning` because of Overlap/Qualifier mismatch.

## 5. **RESPONSE FORMAT**

### Candidates
List up to **10 candidates** (stable numbering). For each:
1. **HRIO Label**: [Label] ([CURIE])
2. **Predicate**: Proposed relationship.
3. **Qualifier Audit**: **Source(Q):** [Bucket] vs **Target(Q):** [Bucket/Missing].
4. **Confidence**: (0–100%) + 1-sentence logic **per statement**.
5. **Alignment**: Bullets for Axis A, B, and Q.
6. **Risks**: Explicitly state if features are lost/added or if metadata was missing.
7. **Evidence Pointers**: [Source Snippet] vs [Target Knowledge Excerpt].

### Why These Candidates
State why mappings were downgraded (e.g., "Targets 2-5 downgraded to T3 due to missing Target(Q) metadata").

### Mapping Record
- **Statements**: `<User concept> → <predicate> → hrio:CURIE`
- **Status**: `final | mixed | provisional | needs-new-concept`
- **Ready-to-Apply**: `yes | partial | no` (Exact requires 99%, others 95%).

## 6. **FINAL VALIDATION (Self-Audit)**
- **Exact-Lock**: If Exact is used, it must be the ONLY statement in the record.
- **Monotonicity**: Ensure the relationship doesn't "flip" (e.g., broader criteria but narrower bearer).
- **Label vs. Structure**: Prioritize OntoUML structure over lexical similarity.

## 7. **PRESENTATION MATRIX (Ranked Targets)**

| Target HRIO Label (CURIE) | Mapping Type | Q-Gate Status | Precision/Confidence |
| :--- | :--- | :--- | :--- |
| Candidate 1 Label | Exact | MATCH | 99% |
| Candidate 2 Label | Narrower | MISMATCH (Missing Q) | 92% |
| Candidate 3 Label | Broader | MISMATCH (Overlap) | 88% |
... (up to 10)
```

______________________________________________________________________

## 4. Test input used

The tested input was sent to the GPT without the test-case metadata lines.

```text
Please map ONE user domain concept to HRIO according to your full mapping protocol.

Source concept label: Biological Man

Source concept definition:
"Any human that is born with XY sexual chromosomes."

Source context:
- Source/standard: toy test case
- Evidence type: direct definition
- Expected qualifier cues in source text: none explicit
- Important bearer cue: human
- Notes: this is a smoke test for prompt compliance, evidence handling, and safe predicate selection

Additional requirements for this test:
- Use only provided text and embedded Knowledge files.
- Do not use web knowledge.
- Do not infer missing HRIO qualifier metadata.
- If exact mapping is not fully justified, downgrade conservatively.
- Quote source evidence and target evidence verbatim where possible.
- Return the full required response format, including:
  - Candidates
  - Why These Candidates
  - Mapping Record
  - Final Validation
  - Presentation Matrix
```

______________________________________________________________________

## 5. Raw model result (as provided by the user)

```text
Preflight: passed. The HRIO namespace is explicitly published with preferred prefix `hrio` and preferred namespace URI `https://w3id.org/health-ri/ontology#`.

Source Evidence

Source concept label: `Biological Man`
Source definition: “Any human that is born with XY sexual chromosomes.”

Extraction log:

* Normalization keys: `biological man`; `human/person`; `XY sexual chromosomes`; `born with`; `karyotypic/chromosomal`
* Location: user prompt (inline source; no file line numbering available)
* Verbatim evidence: “Any human that is born with XY sexual chromosomes.”

Candidates

1. HRIO Label: Regular Karyotypical Male Person (`hrio:RegularKaryotypicalMalePerson`)
   Predicate: `hriv:hasNarrowerMeaningThan`
   Confidence: 93% — This is the closest structural target, but HRIO defines it as “typical male chromosomal configuration, usually XY,” which is slightly looser than a strict XY-only source, so I do not lock exactness. Predicate-direction semantics are defined in HRIV as the safe choice when exact is not justified.

   Alignment:

   * Axis A: Close match. Source = human with XY chromosomes from birth. Target = “Represents individuals with a typical male chromosomal configuration, usually XY.”
   * Axis B: Match. Source bearer is human; target bearer is person/human.
   * Axis Q: Source has no explicit qualifier bucket. Target is karyotypic, but exact Q-bucket alignment is not explicitly stated in the source, so Exact-Lock is withheld.

   Risks:

   * Target may be slightly broader than strict XY-only because of the wording “usually XY.”
   * The source says “born with,” while the target is framed as a karyotypic classification, not a birth-event statement.

   Evidence Pointers:

   * Source: “Any human that is born with XY sexual chromosomes.”
   * Target: “Represents individuals with a typical male chromosomal configuration, usually XY. It reflects the standard genetic basis used to define male karyotypical sex in medical and genetic contexts.”

2. HRIO Label: Karyotypic Male-sex Person (`hrio:KaryotypicMaleSexPerson`)
   Predicate: `hriv:hasNarrowerMeaningThan`
   Confidence: 97% — This is the safest broader target. HRIO states that this class is karyotype-based and “subsumes both Regular Karyotypical Male Person and Variant Karyotypical Male Person,” so a strict XY-born source is narrower than it.

   Alignment:

   * Axis A: Safe broader fit. Source = strict XY. Target = male by sex chromosome complement, including regular and variant male karyotypes.
   * Axis B: Match. Both are person-level classes.
   * Axis Q: Source has no explicit qualifier bucket. Target explicitly excludes phenotypic and assigned/assessed bases, which fits the chromosomal reading, but does not justify exactness without an explicit source-side Q lock.

   Risks:

   * HRIO target adds variant male karyotypes not licensed by the source.
   * Some source strictness is lost.

   Evidence Pointers:

   * Source: “Any human that is born with XY sexual chromosomes.”
   * Target: “A person whose karyotypical sex is male, determined by the sex chromosome complement. This class classifies persons by karyotype only and does not depend on phenotypic traits or on any sex assigned or assessed at birth or later. Karyotypic Male-sex Person subsumes both Regular Karyotypical Male Person and Variant Karyotypical Male Person...”

3. HRIO Label: Person with Regular Sex Chromosome (`hrio:PersonWithRegularSexChromosome`)
   Predicate: `hriv:hasNarrowerMeaningThan`
   Confidence: 72% — This is only a coarse upper bound. It is broader than the source because HRIO says it covers the regular chromosomal patterns behind both regular karyotypical female and male persons.

   Alignment:

   * Axis A: Partial. Source is male-specific XY; target is only regular-sex-chromosome specific.
   * Axis B: Match. Both are person-level.
   * Axis Q: No explicit source qualifier bucket; target remains karyotypic/structural rather than phenotypic or administrative.

   Risks:

   * Male-specific meaning is lost.
   * Includes regular female cases as well.

   Evidence Pointers:

   * Source: “Any human that is born with XY sexual chromosomes.”
   * Target: “A Person with Regular Sex Chromosome is represented as an individual whose sex chromosomes conform to the most frequent configurations in the population... distinguishing the commonly occurring XX and XY arrangements...”

Why These Candidates

I downgraded conservatively to T3 rather than using `hriv:hasExactMeaning`.

Why no Exact-Lock:

* HRIV uses broader/narrower precisely when exact meaning is not fully justified.
* The source is strict: XY-only.
* The nearest HRIO near-match says “usually XY,” which is close but not strict enough for a 99% exact lock.
* The safer karyotypic superclass explicitly includes variant male cases, so it is broader than the source.

Why I did not use a high-level “Man” target:

* HRIO documentation states that “Man generalizes Male-sex Person and Male-gender Person,” so that label spans both sex-based and gender-based branches and is unsafe for a purely chromosomal source.

Mapping Record

Statements:

* `Biological Man` → `hriv:hasNarrowerMeaningThan` → `hrio:KaryotypicMaleSexPerson`

Status: `final`
Ready-to-Apply: `yes`

Final Validation

* Exact-Lock: passed. No exact mapping was asserted.
* Monotonicity: passed. The chosen statement preserves direction: the source is stricter than the HRIO target on chromosomal scope; bearer scope stays person-level.
* Label vs. Structure: passed. I did not rely on the surface label “Man.” I relied on the HRIO karyotypic structure and the documented warning that same labels can hide different conceptualizations.

Presentation Matrix

| # | HRIO target                        | CURIE                                 | Predicate                     | Axis A                                                              | Axis B | Axis Q               | Confidence | Ready-to-apply |
| - | ---------------------------------- | ------------------------------------- | ----------------------------- | ------------------------------------------------------------------- | ------ | -------------------- | ---------: | -------------- |
| 1 | Regular Karyotypical Male Person   | `hrio:RegularKaryotypicalMalePerson`  | `hriv:hasNarrowerMeaningThan` | Very close, but target says “usually XY”                            | Match  | Source Q unspecified |        93% | partial        |
| 2 | Karyotypic Male-sex Person         | `hrio:KaryotypicMaleSexPerson`        | `hriv:hasNarrowerMeaningThan` | Safe broader fit; target includes regular + variant male karyotypes | Match  | Source Q unspecified |        97% | yes            |
| 3 | Person with Regular Sex Chromosome | `hrio:PersonWithRegularSexChromosome` | `hriv:hasNarrowerMeaningThan` | Broad upper bound only                                              | Match  | Source Q unspecified |        72% | no             |

Recommended application:
`Biological Man` → `hriv:hasNarrowerMeaningThan` → `hrio:KaryotypicMaleSexPerson`
```

______________________________________________________________________

## 6. Summary evaluation

### 6.1 Executive assessment

- **Semantic behavior:** reasonably strong and conservative
- **Prompt-protocol compliance:** incomplete
- **Overall result:** **Pass with important defects**

### 6.2 Interpretation

The model behaved cautiously and avoided an unsafe exact match. However, the visible output did not comply with several important protocol rules in `20260310-v1`, especially around qualifier-gate reporting and the outcome ladder.

______________________________________________________________________

## 7. Structured scoring

> Note: this score is retrospective and based only on the visible response and the agreed test workflow.

| Dimension                |  Weight |  Score | Notes                                                                                        |
| ------------------------ | ------: | -----: | -------------------------------------------------------------------------------------------- |
| Instruction compliance   |      20 |     15 | One concept only; no web evidence visible; some protocol rules missed                        |
| Evidence extraction      |      15 |     13 | Clear source evidence and plausible target evidence                                          |
| Evidence grounding       |      15 |     13 | Verbatim snippets present; exact file/line provenance for targets not shown                  |
| Mapping logic            |      20 |     17 | Conservative and mostly defensible semantic reasoning                                        |
| Qualifier gate handling  |      10 |      4 | Did not use the required Q-bucket taxonomy; target Q not explicitly identified from metadata |
| Output format compliance |      10 |      6 | Most sections present, but candidate schema not fully respected                              |
| Final decision quality   |      10 |      6 | `final` and `yes` appear too strong relative to unresolved qualifier issues                  |
| **Total**                | **100** | **74** | **Below acceptance threshold**                                                               |

### 7.1 Critical failure check

No hard evidence of the following critical failures was found in the visible answer:

- invented CURIE
- invented HRIO label
- disallowed predicate
- external/web knowledge use
- exact match without explicit Q-match

**Critical failure present:** `no`

______________________________________________________________________

## 8. Strengths observed

1. **Conservative exact-match behavior**
    The model did not force `hriv:hasExactMeaning`.

2. **Good structural caution**
    It explicitly avoided a high-level “Man” target and prioritized ontology structure over surface wording.

3. **Reasonable directional candidate set**
    The proposed candidates and their relative logic were broadly plausible for a smoke test.

4. **Single-concept discipline**
    The model processed only one concept as required.

______________________________________________________________________

## 9. Defects and issues

### DEF-001 — Qualifier gate taxonomy not followed

- **Category:** `QG`
- **Severity:** high
- **Summary:** The response did not use the required qualifier buckets.
- **Expected:** Explicit `Source(Q)` and `Target(Q)` using only: `self-reported`, `clinician-assessed/diagnosed`, `measured/observed`, `administrative/recorded`, `inferred/derived`, or clearly `Missing`/`None explicit` if the protocol later allows it.
- **Observed:** The response used terms such as `karyotypic`, `chromosomal`, and `structural`, which are not part of the defined Q-bucket taxonomy.

### DEF-002 — Target(Q) not explicitly identified from metadata

- **Category:** `QG`
- **Severity:** high
- **Summary:** The model did not explicitly report `Target(Q): [Bucket/Missing]` for each candidate using HRIO metadata.
- **Expected:** For each candidate, an explicit target qualifier bucket or `Missing`.
- **Observed:** The answer discussed qualifier-like interpretation informally without a strict target-Q output.

### DEF-003 — Missing Metadata Rule not cleanly enforced

- **Category:** `QG`
- **Severity:** high
- **Summary:** The answer appears to infer qualifier-like meaning instead of explicitly marking target metadata as missing.
- **Expected:** If HRIO metadata does not explicitly support the required qualifier bucket, mark `Target(Q): Missing` and downgrade.
- **Observed:** The response leaned on `karyotypic/chromosomal` reasoning without showing that these terms map to one of the allowed Q buckets.

### DEF-004 — Candidate schema only partially followed

- **Category:** `OF`
- **Severity:** medium
- **Summary:** The required candidate-level `Qualifier Audit` format was not followed exactly.
- **Expected:** `Source(Q): [Bucket] vs Target(Q): [Bucket/Missing]` for each candidate.
- **Observed:** Axis Q was discussed narratively instead of using the exact requested schema.

### DEF-005 — Status too strong

- **Category:** `TH`
- **Severity:** medium
- **Summary:** `Status: final` appears too strong for a non-exact mapping with unresolved qualifier treatment.
- **Expected:** likely `mixed` or `provisional`.
- **Observed:** `final`.

### DEF-006 — Ready-to-Apply likely overstated

- **Category:** `TH`
- **Severity:** medium
- **Summary:** `Ready-to-Apply: yes` appears too optimistic relative to the unresolved protocol issues.
- **Expected:** likely `partial`.
- **Observed:** `yes`.

### DEF-007 — T3 rule exposed a prompt design issue

- **Category:** `ML` / prompt design
- **Severity:** medium
- **Summary:** The tested prompt required T3 to include a directional mapping plus a companion `NOT hriv:hasExactMeaning`. This turned out to be logically redundant for the same source-target pair if broader/narrower are intended as strict relations.
- **Expected:** either a different negative target or no redundant negative for the same pair.
- **Observed:** The model omitted the redundant negative. That was technically non-compliant with `v1`, but semantically reasonable.
- **Conclusion:** This is best treated as a **prompt defect discovered by testing**, not primarily as a model defect.

______________________________________________________________________

## 10. Key finding from this test

The most important result of `TC-001` is not the mapping itself; it is the discovery that `20260310-v1` had a design flaw in the T3 ladder and insufficiently constrained qualifier auditing.

### Specifically

- The prompt was good at encouraging conservative semantic reasoning.
- The prompt was not strong enough at enforcing:
    - strict qualifier taxonomy use,
    - explicit target-Q reporting,
    - non-redundant T3 behavior,
    - cautious readiness/status signaling.

This directly motivated the revision toward `20260310-v2`.

______________________________________________________________________

## 11. Decision on prompt version `20260310-v1`

### Recommended decision

**Do not accept `20260310-v1` as-is for broader testing.**

### Recommended status

`accept with revisions required before broader evaluation`

### Rationale

The version is promising semantically, but it contains protocol weaknesses that will produce noisy or inconsistent evaluations if left unchanged.

______________________________________________________________________

## 12. Recommended next actions

1. **Adopt the revised v2 prompt**
    Especially the fixes for:

    - strict broader/narrower semantics,
    - non-redundant negation,
    - explicit qualifier-bucket reporting,
    - readiness rule clarification.

2. **Run a targeted qualifier test next (`TC-002`)**
    Use a concept with an explicit source-side qualifier, such as self-reported or clinician-assessed.

3. **Improve test logging from the start**
    For future tests, record:

    - knowledge snapshot/version,
    - exact run timestamp,
    - reviewer,
    - prompt version,
    - raw input,
    - raw output.

______________________________________________________________________

## 13. Reusable registration block

Use this block when registering this test in a tracker.

```text
Test Case ID: TC-001
Prompt Version: 20260310-v1
Title: Direct-definition smoke test with no explicit qualifier
Input Type: Direct concept definition
Source Concept: Biological Man
Definition: "Any human that is born with XY sexual chromosomes."
Overall Result: Pass with important defects
Critical Failure: No
Total Score: 74/100
Primary Finding: Conservative semantic behavior, but weak protocol compliance around qualifier-gate reporting and T3 semantics.
Decision: Revise prompt before broader testing
```

______________________________________________________________________

## 14. Attachments / evidence included in this report

Included:

- prompt version text (`20260310-v1`)
- exact test input used
- raw GPT output provided by the user
- structured evaluation and scoring
- defect list
- decision and next actions

Not included / not recorded at test time:

- embedded Knowledge file inventory and version
- system-level GPT configuration metadata
- independently verified line-range citations to HRIO files

______________________________________________________________________

## 15. Final evaluator note

This first test was successful in its real purpose: it surfaced the most important design weaknesses in the original prompt while showing that the model can already behave conservatively and structurally.

That makes `TC-001` a good baseline report for comparing `20260310-v2` against `20260310-v1` in the next round.
