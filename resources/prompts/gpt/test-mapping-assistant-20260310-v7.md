# v7 Test Report

## Scope

This report evaluates v7 against three important test cases:

1. Clarification behavior on underspecified input
2. Exact-Lock with qualifier normalization
3. Composite `Source(Q)` and `needs-new-concept`

## Overall Assessment

v7 performed well overall. The most important improvements appear to be working:

- clarification is not asked unnecessarily
- qualifier normalization is functioning
- exact-lock is applied correctly
- candidate completeness is improved
- composite `Source(Q)` is handled correctly
- `needs-new-concept` is triggered appropriately in boundary cases

Overall verdict: **Pass**

______________________________________________________________________

## Test 1 — Underspecified input

### Input

`Male status`
Definition: `"A classification of a person as male."`

### Expected behavior

- avoid unsafe exactness
- avoid unnecessary clarification if a safe provisional outcome exists
- include the closest retrieved targets in Candidates and Final Matrix

### Observed behavior

- no clarification was asked
- exact mapping was avoided
- directional and negative mappings were proposed
- `hrio:Male` was included in both Candidates and Final Matrix
- overall status was `provisional`

### Assessment

**Pass**

### What worked well

- the earlier candidate-completeness issue appears fixed
- the result stayed structurally cautious
- the model recognized the source as underspecified between sex-based, gender-based, and umbrella male readings

### Minor note

There is still a natural semantic tension between:

- `hrio:Male` as an outcome-level umbrella, and
- `hrio:Man` as a person-level umbrella

The model handled this reasonably, but this remains the hardest part of this test case.

______________________________________________________________________

## Test 2 — Exact-Lock with qualifier normalization

### Input

`Self-identified male-gender person`
Definition: `"A person whose gender is self-identified as male."`

### Expected behavior

- normalize `self-identified` to `self-reported`
- retrieve the exact HRIO target
- satisfy Axis A, Axis B, and Axis Q
- stop at T1 Exact-Lock

### Observed behavior

- qualifier normalization worked correctly
- exact target retrieved: `hrio:SelfIdentifiedMaleGenderPerson`
- exact mapping asserted:
    - `Self-identified male-gender person → hriv:hasExactMeaning → hrio:SelfIdentifiedMaleGenderPerson`
- broader and near-miss candidates were handled appropriately
- overall status was `final`

### Assessment

**Pass**

### What worked well

- exact-lock behavior was correct
- qualifier normalization is now clearly working
- broader and negative candidates were reasonable and well-structured
- the model stopped correctly once exactness was justified

### Minor note

The negative candidates were marked `no` for readiness. This is not inconsistent with the prompt, but it may be stricter than your intended practice if some valid negative mappings should be kept in the mapping set.

______________________________________________________________________

## Test 3 — Composite `Source(Q)` and `needs-new-concept`

### Input

`Male-by-self-identification but female-in-administrative-records person`
Definition: `"A person whose gender is self-identified as male while being administratively recorded as female, where the disagreement between those two classifications is essential to the concept."`

### Expected behavior

- use composite `Source(Q)`
- retrieve facet-level near matches
- avoid forcing a positive mapping
- trigger `needs-new-concept` if no single target preserves the essential disagreement
- include closest retrieved facet targets in Candidates and Final Matrix

### Observed behavior

- composite `Source(Q)` was handled correctly:
    - `self-reported + administrative/recorded`
- closest facet targets were included:
    - `hrio:SelfIdentifiedMaleGenderPerson`
    - `hrio:AdministrativeFemaleGenderPerson`
- broader partial candidates were also included
- transgender-related near-misses were rejected for the right structural reason
- final result:
    - `Final Statements: none`
    - `Overall Status: needs-new-concept`

### Assessment

**Pass**

### What worked well

- no forced positive mapping
- essential disagreement was treated as constitutive of the source concept
- facet preservation and boundary reasoning were both strong
- `needs-new-concept` was triggered for the right reason

### Minor note

None that affects the result materially.

______________________________________________________________________

## Summary by Test

| Test | Focus                                                          | Outcome                                               | Verdict |
| ---- | -------------------------------------------------------------- | ----------------------------------------------------- | ------- |
| 1    | Clarification + candidate completeness on underspecified input | Safe provisional result, no unnecessary clarification | Pass    |
| 2    | Exact-Lock + qualifier normalization                           | Correct exact match and final status                  | Pass    |
| 3    | Composite `Source(Q)` + `needs-new-concept`                    | Correct boundary behavior and no forced mapping       | Pass    |

______________________________________________________________________

## Main Conclusions

v7 is behaving well on the tested core scenarios.

The strongest confirmed improvements are:

- explicit qualifier normalization
- candidate completeness
- composite `Source(Q)` handling
- correct `needs-new-concept` triggering
- safe refusal to overcommit exactness on underspecified sources

## Remaining Small Watchpoints

1. The semantic boundary between outcome-level and person-level umbrella targets in underspecified cases still deserves attention.
2. Readiness for negative mappings may still be a policy choice worth watching, depending on whether you want strong negative statements commonly marked as `yes`, `partial`, or `no`.

## Final Verdict

**v7 passes the current three-test set and appears materially improved over earlier versions.**
