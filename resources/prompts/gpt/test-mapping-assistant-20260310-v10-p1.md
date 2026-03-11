# Validation Report — Prompt Tests 1–5

## Scope

This report re-checks and consolidates the evaluations for Tests 1–5 against two separate criteria:

1. **Prompt-compliance result** — whether the GPT behaved correctly under the prompt.
2. **Test-objective result** — whether the test actually validated the intended behavior being probed.

This distinction matters because a test can be procedurally correct while still failing to validate its intended branch.

______________________________________________________________________

## Executive Summary

| Test | Intended behavior                                               | Prompt-compliance result | Test-objective result   | Registration outcome                                       |
| :--- | :-------------------------------------------------------------- | :----------------------- | :---------------------- | :--------------------------------------------------------- |
| 1    | T1 exact-match with explicit qualifier and exact-lock           | **Pass with caveats**    | **Inconclusive for T1** | **Register as: Pass (fallback/T5), objective not reached** |
| 2    | Composite qualifier blocks exactness                            | **Pass**                 | **Pass**                | **Register as: Pass**                                      |
| 3    | Do not infer Q from karyotypic/chromosomal wording              | **Strong pass**          | **Pass**                | **Register as: Pass**                                      |
| 4    | Bearer-scope conflict blocks unsafe positive mapping            | **Pass with caveats**    | **Pass**                | **Register as: Pass with caveats**                         |
| 5    | T4 negative-only near-miss for administrative/legal distinction | **Strong pass**          | **Pass**                | **Register as: Pass**                                      |

______________________________________________________________________

## Test 1

### Test ID

**Test 1 — Measured body mass index**

### Intended behavior

Validate **T1 exact-match behavior**, including:

- exact retrieval
- explicit qualifier confirmation
- exact-lock
- Mapping Record containing only the exact statement

### Observed behavior

The GPT did **not** retrieve a BMI target and therefore did **not** reach T1.
It instead produced a conservative **T5 (`needs-new-concept`)** outcome with weak negative contrasts and no final statements.

### Re-checked judgment

**Prompt-compliance result:** **Pass with caveats**
**Test-objective result:** **Inconclusive for T1**

### Why

The GPT behaved safely and consistently under retrieval failure:

- retrieval order was followed
- unsafe exact/directional mappings were avoided
- T5 was justified
- negative candidates were not promoted into final statements

However, this does **not** validate the intended T1 branch, because the Knowledge search did not support that branch.

### Main caveats

- Candidate list included some overly remote contrasts.
- The response validated **fallback conservatism**, not **exact-match behavior**.

### Registration outcome

**Pass (fallback/T5), objective not reached**

______________________________________________________________________

## Test 2

### Test ID

**Test 2 — Depression status from self-report and clinician diagnosis**

### Intended behavior

Validate that a **composite Source(Q)** blocks exactness when a target:

- captures only one part of the composite qualifier, or
- lacks explicit qualifier support

### Observed behavior

The GPT rejected exactness and chose **T4 negative-only** using plausible condition-side and diagnosis-side near-miss targets.

### Re-checked judgment

**Prompt-compliance result:** **Pass**
**Test-objective result:** **Pass**

### Why

This is a good validation of the intended rule:

- `Source(Q) = self-reported + clinician-assessed/diagnosed`
- no retrieved target supported that full composite as exact
- exactness was correctly blocked
- T4 was reasonably preferred over weak T3

### Main caveats

- Too many targets were marked `Candidate Ready-to-Apply: yes`.
- Some weaker contrasts, especially `Self-diagnosis`, should likely have remained outside the final candidate set.
- Confidence values were somewhat inflated.

### Registration outcome

**Pass**

______________________________________________________________________

## Test 3

### Test ID

**Test 3 — Karyotypic sex**

### Intended behavior

Validate that the GPT does **not infer qualifier buckets** from lexical cues such as:

- karyotypic
- chromosomal

### Observed behavior

The GPT retrieved the exact semantic target **`hrio:KaryotypicSex`** but still refused exactness because:

- `Source(Q) = None explicit`
- `Target(Q) = Missing`

It then chose **T4** rather than forcing T1 or weak T3.

### Re-checked judgment

**Prompt-compliance result:** **Strong pass**
**Test-objective result:** **Pass**

### Why

This is one of the strongest results:

- the correct target was retrieved
- Q was **not** inferred from “karyotypic” or “chromosomal”
- exactness was blocked correctly
- T4 was preferred over a weak broader mapping to `hrio:Sex`

### Main caveats

- One target-side qualifier assignment for `PhenotypicSex` may be slightly overcommitted.
- Confidence for the near-exact negative candidate is a bit high.

### Registration outcome

**Pass**

______________________________________________________________________

## Test 4

### Test ID

**Test 4 — Family history of colorectal cancer**

### Intended behavior

Validate that **bearer-scope conflict** prevents unsafe positive mappings.

### Observed behavior

The GPT correctly avoided broader/narrower mappings and chose **T4 negative-only**, using nearby contrasts on the indicator, risk, lineage, and disease axes.

### Re-checked judgment

**Prompt-compliance result:** **Pass with caveats**
**Test-objective result:** **Pass**

### Why

The core behavior was correct:

- the source is an informational family-history concept
- the retrieved targets were on different ontological/bearer axes
- the GPT did **not** collapse the source into disease, risk, or kinship relation
- positive mapping was correctly rejected

### Main caveats

- The final negative set was too broad.
- `ParentChildRelation` and `Disease` are better treated as contrastive discussion items than final negative mapping statements.
- Confidence values were too high for some weak negatives.

### Registration outcome

**Pass with caveats**

______________________________________________________________________

## Test 5

### Test ID

**Test 5 — Legal gender marker**

### Intended behavior

Validate **T1 exact mapping**, including:

- correct qualifier match
- structure over label similarity
- exact-lock in the Mapping Record

### Observed behavior

The GPT mapped the source exactly to **`hrio:AdministrativeGender`**, treated **`hrio:LegalGender`** as narrower, and kept only the exact statement in the Mapping Record.

### Re-checked judgment

**Prompt-compliance result:** **Strong pass**
**Test-objective result:** **Pass**

### Why

This is a strong result:

- explicit `administrative/recorded` qualifier match was correctly identified
- the source **definition** overrode the potentially misleading source **label**
- ontology structure was used correctly
- exact-lock was respected fully

### Main caveats

- Confidence for the exact match is slightly assertive, but still acceptable.
- The head-noun retrieval step is methodologically a bit loose, though not outcome-affecting.

### Registration outcome

**Pass**

______________________________________________________________________

## Recommended Registry Entries

| Test | Final registry label                          | Notes                                                            |
| :--- | :-------------------------------------------- | :--------------------------------------------------------------- |
| 1    | **Pass (fallback/T5), objective not reached** | Good conservative behavior, but did not validate T1 exact branch |
| 2    | **Pass**                                      | Correct composite-qualifier blocking of exactness                |
| 3    | **Pass**                                      | Correctly refused Q inference from lexical cues                  |
| 4    | **Pass with caveats**                         | Correct bearer-scope restraint, but negative set too broad       |
| 5    | **Pass**                                      | Strong T1 result with correct exact-lock                         |

______________________________________________________________________

## Overall Assessment for Tests 1–5

The GPT is performing **well** on:

- qualifier strictness
- conservative rejection of unsafe exact mappings
- preference for T4/T5 over weak generic anchors
- structure-aware reasoning
- exact-lock behavior when T1 is reached

The main recurring weaknesses across these tests are:

- **overgeneration of negative candidates**
- **overuse of `Candidate Ready-to-Apply: yes`**
- **inflated confidence scores for weak near-misses**

These do **not** overturn the passes in Tests 2, 3, and 5, but they should be tracked as recurring quality issues.

______________________________________________________________________

## Final Registration Summary

- **Test 1:** Pass (fallback/T5), objective not reached
- **Test 2:** Pass
- **Test 3:** Pass
- **Test 4:** Pass with caveats
- **Test 5:** Pass
