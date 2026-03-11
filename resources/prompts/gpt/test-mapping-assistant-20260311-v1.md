# Evaluation Report — "Mapping One User Domain Concept to HRIO" Tests

## Scope

This report evaluates the GPT's behavior **against the prompt specification itself**, including:

- one-concept gating
- evidence discipline
- qualifier-bucket handling
- outcome ladder selection (T1–T5)
- stop-condition handling for `knowledge-access-failed`

It does **not** evaluate whether the underlying ontology content is factually complete or ideal.

______________________________________________________________________

## Executive Summary

| Test   | Main Focus                                                                       | Final Result | Score  | Registration Status |
| :----- | :------------------------------------------------------------------------------- | :----------- | :----: | :------------------ |
| Test 1 | One-concept-per-turn enforcement + weak-anchor avoidance                         | Pass         | 9.0/10 | PASS                |
| Test 2 | Exactness blocked by missing/mismatched qualifier support; avoid wrong-domain T4 | Partial fail | 5.0/10 | PARTIAL FAIL        |
| Test 3 | Composite source qualifier must not collapse into exact mapping                  | Pass         | 8.5/10 | PASS                |
| Test 4 | Avoid unsafe positive mapping when closest target is only a near-miss            | Pass         | 9.0/10 | PASS                |
| Test 5 | Unreadable/partial source must trigger `knowledge-access-failed` stop condition  | Partial fail | 4.5/10 | PARTIAL FAIL        |

### Overall outcome

- **Passed:** 3 / 5
- **Partial fail:** 2 / 5
- **Full fail:** 0 / 5

### Main pattern

The GPT is strongest at:

- blocking unsafe exact mappings
- respecting structure over lexical similarity
- handling T4 well when there are genuine semantic near-misses

The GPT is weakest at:

- distinguishing **true T4 near-miss negatives** from merely **qualifier-adjacent / wrong-domain contrasts**
- fully honoring the **stop condition** after `knowledge-access-failed`

______________________________________________________________________

## Detailed Results

## Test 1 — Single-concept gate

### Purpose

Verify that the GPT refuses to map more than one concept in the same turn, asks the user to choose one, and then avoids forcing a weak fallback mapping.

### Expected behavior

- detect that two concepts were supplied
- ask which one to map
- proceed with only one concept after the user selects it
- avoid weak generic anchors if no defensible smoking-related concept is retrieved
- likely return **T5 `needs-new-concept`**

### Observed behavior

- the GPT correctly refused to map both in one turn
- it asked the user to choose one concept
- after selection, it proceeded with only one concept
- it did not force an exact or directional mapping
- it returned **T5 `needs-new-concept`**
- remote contrasts were listed as candidates, but all were marked `no`

### Assessment

**Pass**

### Why it passes

This test’s primary gate was enforced correctly:

- the **one-concept-per-turn rule** was followed exactly

The downstream outcome was also appropriate:

- no defensible smoking concept was retrieved
- weak anchors were not promoted into final mapping statements
- T5 was chosen instead of an unsafe T3 or T4

### Weaknesses

- some remote contrasts were elevated into the **Candidates** section even though they were not especially semantically useful
- that is mostly a calibration/quality issue, not a logic failure

### Registration note

Record as a **successful enforcement of the one-concept gate and T5 fallback discipline**.

______________________________________________________________________

## Test 2 — Self-identified ethnicity

### Purpose

Verify that the GPT blocks exactness when qualifier alignment alone is present but the target is in the wrong semantic domain, and avoids using T4 for merely qualifier-adjacent near-misses.

### Expected behavior

- recognize `Source(Q): self-reported`
- retrieve no defensible ethnicity target
- avoid exact and directional mappings
- prefer **T5 `needs-new-concept`** if only gender concepts are retrieved through the self-identification pattern

### Observed behavior

- the GPT correctly extracted `Source(Q): self-reported`
- it correctly found no ethnicity concept
- it correctly blocked exact and directional mappings
- however, it selected **T4** and asserted final negatives against:
    - `hrio:SelfIdentifiedGender`
    - `hrio:SelfDesignatedGender`

### Assessment

**Partial fail**

### Why it does not fully pass

The main issue is **outcome ladder selection**.

Under the prompt:

- T4 should **not** be used when negatives are only structurally adjacent, lexically incidental, or semantically remote
- here, the retrieved targets are **gender** concepts, while the source is **ethnicity**
- the overlap is mainly in the **self-identification qualifier**, not in core meaning

That makes these targets useful as **contrastive retrieval results**, but too weak to promote into final T4 mapping statements.

### What the stronger answer should have done

- discuss the gender concepts in **Why These Candidates**
- keep them out of final T4 statements
- return **T5 `needs-new-concept`**

### Registration note

Record as a **failure of T4/T5 boundary selection** despite otherwise careful qualifier handling.

______________________________________________________________________

## Test 3 — Hypertension ascertainment by diagnosis or blood-pressure measurement

### Purpose

Verify that a source with **composite explicit qualifier buckets** is not collapsed into an exact diagnosis mapping.

### Expected behavior

- identify the composite source qualifier structure
- block any exact diagnosis mapping
- distinguish diagnosis, condition, indicator, and ascertainment/status
- likely return **T4** if genuine near-miss negatives are available

### Observed behavior

- the GPT assigned:
    - `clinician-assessed/diagnosed`
    - `measured/observed`
    - `inferred/derived`
- it explicitly noted a risk around the `derived from` interpretation
- it blocked exactness for diagnosis-side candidates
- it treated diagnosis classes and condition classes as near-misses rather than exact matches
- it selected **T4**

### Assessment

**Pass**

### Why it passes

This test was mainly about preventing a collapse from:

- **diagnosis OR repeated measurement**
    into
- **diagnosis only**

The GPT handled that correctly.

It recognized that:

- the source is a **mixed ascertainment/status rule**
- diagnosis-side targets capture only one branch
- condition-side targets lose the ascertainment semantics
- exactness is therefore blocked

### Weaknesses

- the set of final negative candidates was somewhat overexpanded
- `ResearchDiagnosis`, `EpidemiologicalDiagnosis`, and `HealthcareDiagnosis` are weaker than the strongest contrasts
- the logic is good, but the final negative set is broader than necessary

### Registration note

Record as a **successful handling of composite qualifier logic**, with minor overgeneration of T4 negatives.

______________________________________________________________________

## Test 4 — Algorithmically inferred type 2 diabetes risk

### Purpose

Verify that the GPT does not force a positive mapping from a predictive score or derived risk artifact into a condition or diagnosis class.

### Expected behavior

- distinguish a predictive **score / inferred artifact** from a **condition**
- avoid exact or directional mapping to a condition or diagnosis
- prefer **T4** if semantically relevant near-miss negatives exist

### Observed behavior

- the GPT identified the closest target as `Risk-based Health Condition`
- it correctly blocked exactness because the source is a **computed score**, while the target is a **condition**
- it also used `Diagnosis` as a negative comparison because the source explicitly states it is **not a diagnosis**
- it selected **T4**
- it kept `Target(Q): Missing` rather than inventing qualifier metadata

### Assessment

**Pass**

### Why it passes

This is a strong result because it captures the key modeling distinction:

- source = predictive, algorithmically derived risk score
- target = risk-based condition

The GPT correctly treated that as a **structure-level mismatch**, not as a missing detail that could be bridged.

### Weaknesses

- confidence values were somewhat high
- `Diagnosis` is a valid negative contrast, but weaker than the central `Risk-based Health Condition` near-miss

### Registration note

Record as a **successful T4 negative-only result with strong structure-over-lexicon behavior**.

______________________________________________________________________

## Test 5 — Garbled / partial source

### Purpose

Verify that an unreadable, partial, or unreliable source triggers `knowledge-access-failed` and stops normal mapping flow.

### Expected behavior

- detect that the source is too damaged or unreliable for safe concept recovery
- return **`knowledge-access-failed`**
- do **not** continue into a normal mapping outcome such as T4 or T5
- do **not** convert source unreliability into `needs-new-concept`

### Observed behavior

- the GPT correctly detected that the source was partial, garbled, and unreliable
- it explicitly stated **knowledge access failed for safe mapping**
- however, it then continued with:
    - retrieval analysis
    - candidate construction
    - final matrix
    - mapping record
    - final status of **`needs-new-concept`**

### Assessment

**Partial fail**

### Why it does not pass cleanly

This is a logic inconsistency:

- `knowledge-access-failed` means the workflow cannot safely evaluate the source concept
- `needs-new-concept` means the source concept is understood well enough, but no defensible target exists

Those are not interchangeable.

The GPT recognized the stop condition but did **not** obey its consequence.

### What the stronger answer should have done

After detecting the unreadable/partial source, it should have:

- stopped normal mapping evaluation
- returned **`knowledge-access-failed`**
- optionally noted nearby semantic areas only as non-binding context
- avoided a standard Mapping Record outcome such as `needs-new-concept`

### Registration note

Record as a **stop-condition failure after correctly detecting source unreliability**.

______________________________________________________________________

## Final Registration Summary

## Pass

- **Test 1** — one-concept gate and T5 fallback discipline
- **Test 3** — composite qualifier handling without unsafe exactness
- **Test 4** — correct T4 negative-only handling for predictive risk score vs condition

## Partial fail

- **Test 2** — wrong T4/T5 boundary; wrong-domain qualifier-adjacent concepts promoted into final negatives
- **Test 5** — `knowledge-access-failed` detected but not honored as a stop condition

______________________________________________________________________

## Suggested Follow-up Actions

1. Tighten the T4 rule in the GPT instructions so that **wrong-domain concepts sharing only a qualifier pattern** are less likely to become final negative statements.
2. Add an explicit hard stop after `knowledge-access-failed`, such as:
    - “If `knowledge-access-failed` is triggered, do not produce Candidates, Final Statements, or T1–T5 status.”
3. Consider adding a preference rule for T4 candidate selection:
    - prefer fewer, stronger, semantically central negative candidates over broader contrast lists.

______________________________________________________________________

## Canonical Result Set

| Test   | Canonical Result |
| :----- | :--------------- |
| Test 1 | PASS             |
| Test 2 | PARTIAL FAIL     |
| Test 3 | PASS             |
| Test 4 | PASS             |
| Test 5 | PARTIAL FAIL     |
