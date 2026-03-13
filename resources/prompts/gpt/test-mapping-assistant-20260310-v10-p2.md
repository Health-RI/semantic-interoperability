# Validation Report — Prompt Tests 6–10

## Scope

This report re-checks and consolidates the evaluations for Tests 6–10 against two separate criteria:

1. **Prompt-compliance result** — whether the GPT behaved correctly under the prompt.
2. **Test-objective result** — whether the test actually validated the intended behavior being probed.

This distinction is important for Tests 6 and 10, where a result can look methodologically reasonable while still missing the intended branch.

______________________________________________________________________

## Executive Summary

| Test | Intended behavior                                                                                       | Prompt-compliance result | Test-objective result            | Registration outcome               |
| :--- | :------------------------------------------------------------------------------------------------------ | :----------------------- | :------------------------------- | :--------------------------------- |
| 6    | Highly specific inferred longitudinal concept should resist forced mapping                              | **Pass with caveats**    | **Partial pass / borderline**    | **Register as: Pass with caveats** |
| 7    | Enforce one concept per turn                                                                            | **Fail**                 | **Fail**                         | **Register as: Fail**              |
| 8    | Clarification restraint when a safe non-exact outcome already exists                                    | **Pass**                 | **Pass**                         | **Register as: Pass**              |
| 9    | Retrieval-order discipline and correct T5 when only lexical accidents exist                             | **Strong pass**          | **Pass**                         | **Register as: Pass**              |
| 10   | Return `knowledge-access-failed` when the attachment is unreadable/partial enough to block safe mapping | **Fail**                 | **Fail / objective not reached** | **Register as: Fail**              |

______________________________________________________________________

## Test 6

### Test ID

**Test 6 — Algorithmically inferred frailty trajectory**

### Intended behavior

Probe a **highly specific inferred longitudinal concept** and verify that the GPT does **not** force:

- an exact match
- a weak broader/narrower mapping
- or invented structure

The likely target behavior was a strong non-positive outcome, most plausibly **T5**, though **T4** can still be defensible if there are genuinely useful near-miss targets.

### Observed behavior

The GPT rejected T1/T3 and chose **T4 negative-only**, with final negatives against:

- `hrio:ConditionIndicator`
- `hrio:HealthcareDiagnosis`
- `hrio:EstablishedHealthCondition`

### Re-checked judgment

**Prompt-compliance result:** **Pass with caveats**
**Test-objective result:** **Partial pass / borderline**

### Why

The core safety behavior was correct:

- no exact target was found
- no unsafe broader/narrower mapping was asserted
- the source qualifier `inferred/derived` was handled correctly
- no unretrieved semantics were invented

However, the result is **borderline between T4 and T5**. A strong argument can be made that the remaining anchors are too generic and lose too much of the source's defining identity:

- frailty
- trajectory
- last-12-month longitudinal scope
- algorithmic derivation from repeated EHR signals

So while **T4 is defensible**, **T5 would also have been highly defensible**.

### Main caveats

- Too many negative candidates were elevated.
- Some final negatives are weaker than ideal.
- Confidence values are inflated.
- This validates safe restraint more clearly than it validates a crisp T5 branch.

### Registration outcome

**Pass with caveats**

______________________________________________________________________

## Test 7

### Test ID

**Test 7 — Two concepts in one turn**

### Intended behavior

Validate strict enforcement of the rule:

- **One concept per turn**

### Observed behavior

The GPT explicitly processed **both concepts** in one answer, even though it separated them into two sections.

### Re-checked judgment

**Prompt-compliance result:** **Fail**
**Test-objective result:** **Fail**

### Why

The prompt rule is explicit and core:

- **One concept per turn**

Handling two concepts “separately” inside one answer does **not** satisfy that rule. A compliant response should have stopped, redirected, or otherwise enforced a one-concept workflow.

### Main caveats

- The individual mappings were reasonably consistent.
- That does **not** rescue the result, because the primary behavior under test was workflow enforcement, not mapping quality.

### Registration outcome

**Fail**

______________________________________________________________________

## Test 8

### Test ID

**Test 8 — Administrative ethnicity**

### Intended behavior

Validate **clarification restraint**: the GPT should **not** ask unnecessary follow-up questions when a safe non-exact outcome already exists.

### Observed behavior

The GPT noted missing/ambiguous source details, did **not** ask clarification questions, and returned a **T4 negative-only** outcome against `hrio:AdministrativeGender`.

### Re-checked judgment

**Prompt-compliance result:** **Pass**
**Test-objective result:** **Pass**

### Why

This test was mainly about whether the GPT would resist asking extra questions when they were not needed to reach a safe decision. It did that correctly:

- bearer ambiguity was noted
- structural ambiguity was noted
- no unnecessary clarification was asked
- a safe non-exact outcome was returned

That matches the prompt's clarification policy.

### Main caveats

- `hrio:AdministrativeGender` is only a **moderately** strong T4 near-miss.
- The result is acceptable as **T4**, but **T5 would also have been defensible** because the domain shift from ethnicity to gender is substantial.
- Confidence is too high for a cross-domain negative candidate.

### Registration outcome

**Pass**

______________________________________________________________________

## Test 9

### Test ID

**Test 9 — Residential ZIP code**

### Intended behavior

Validate:

- required retrieval order
- resistance to lexical false positives
- correct use of **T5** when no defensible candidate exists

### Observed behavior

The GPT followed the search order, found only lexical accidents, did not elevate them to candidates, and returned **T5 (`needs-new-concept`)**.

### Re-checked judgment

**Prompt-compliance result:** **Strong pass**
**Test-objective result:** **Pass**

### Why

This is a clean result:

- exact phrase, head noun, and synonyms/tokens were reported in order
- lexical accidents such as `PreferredPronoun` were correctly rejected as non-semantic
- T4 was correctly **not** used
- T5 was well justified

This is exactly the kind of behavior the test was designed to validate.

### Main caveats

- The placeholder row in the final matrix (`none | none | 0% | no`) is slightly awkward stylistically, but not wrong.
- The head-noun choice is not perfectly strict linguistically, but it is not outcome-affecting.

### Registration outcome

**Pass**

______________________________________________________________________

## Test 10

### Test ID

**Test 10 — Attachment-only source with intended unreadable/partial failure case**

### Intended behavior

Validate that the GPT returns:

- `knowledge-access-failed`

when the attachment is unreadable, partial, or otherwise unreliable enough to block safe mapping.

### Observed behavior

The GPT did **not** return `knowledge-access-failed`. Instead, it said knowledge access succeeded, selected one concept from the attached paper on its own, and then performed a normal T5 mapping workflow.

### Re-checked judgment

**Prompt-compliance result:** **Fail**
**Test-objective result:** **Fail / objective not reached**

### Why

This result misses the intended failure mode.

There are two possibilities, and both are unfavorable:

#### Case A — The attachment was actually unreadable/partial

Then the GPT should have returned:

- `knowledge-access-failed`

and it failed to do so.

#### Case B — The attachment was readable

Then the GPT still should **not** have unilaterally selected a concept from a full paper, because:

- the workflow is one concept per turn
- the chosen concept materially changes the mapping outcome
- the response itself admits that choosing a different concept could change the result

So even under the more charitable interpretation, the behavior is still non-compliant.

### Main caveats

- The downstream T5 reasoning for the chosen concept was reasonable.
- That does **not** rescue the result, because the primary behavior under test was the failure mode, not the fallback mapping logic.

### Registration outcome

**Fail**

______________________________________________________________________

## Recommended Registry Entries

| Test | Final registry label  | Notes                                                                                         |
| :--- | :-------------------- | :-------------------------------------------------------------------------------------------- |
| 6    | **Pass with caveats** | Safe non-positive behavior validated; T4 vs T5 remains borderline                             |
| 7    | **Fail**              | Did not enforce one-concept-per-turn rule                                                     |
| 8    | **Pass**              | Correct clarification restraint; T4 acceptable though T5 was also arguable                    |
| 9    | **Pass**              | Strong retrieval-order discipline and correct T5                                              |
| 10   | **Fail**              | Did not validate `knowledge-access-failed`; also selected a concept from a paper unilaterally |

______________________________________________________________________

## Overall Assessment for Tests 6–10

Across these five tests, the GPT shows strong tendencies toward:

- conservative rejection of unsafe positive mappings
- good handling of missing evidence
- good resistance to lexical accidents
- appropriate T5 behavior when no real candidate exists

The main recurring weaknesses are:

- **overgeneration of negative candidates** in T4 cases
- **inflated confidence scores** for weak near-misses
- **borderline T4/T5 decisions** where generic anchors may be too weak
- **workflow non-compliance** when a test explicitly probes one-concept discipline or failure handling

______________________________________________________________________

## Final Registration Summary

- **Test 6:** Pass with caveats
- **Test 7:** Fail
- **Test 8:** Pass
- **Test 9:** Pass
- **Test 10:** Fail
