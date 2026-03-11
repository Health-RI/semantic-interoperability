# HRIO Mapping GPT — Test Report

## Prompt Version Under Test

20260310-v4

## Scope

This report evaluates the three test prompts previously run against the GPT:

1. Exact-Lock with explicit qualifier match
2. Directional / provisional mapping with missing target Q
3. `needs-new-concept` boundary case

______________________________________________________________________

## Executive Summary

Overall, the prompt is performing well across the three target behaviors.

- **Test 1** shows strong exact-match behavior with correct qualifier handling and a clean final selection.
- **Test 2** shows good semantic caution and correct directional reasoning, but still reveals a weakness in status/readiness calibration.
- **Test 3** shows that the new `needs-new-concept` logic is working well and that the model can avoid forcing mappings when the defining structure is not preserved by any single HRIO target.

### Overall assessment

- **Strengths**

    - Good structural reasoning
    - Good avoidance of unsafe exact mappings
    - Good final presentation matrix behavior
    - Good handling of person-vs-property bearer mismatches
    - Good use of `needs-new-concept` in a true boundary case

- **Main remaining weakness**

    - The model is still somewhat too optimistic when assigning:
        - `Candidate Ready-to-Apply: yes`
        - `Overall Status: final`
            in cases that are clearly directional, non-exact, or missing explicit target qualifier evidence.

______________________________________________________________________

## Test 1

### Name

Exact-Lock with explicit qualifier match

### Source concept

Self-identified male-gender person

### Intended behavior

The test was designed to verify whether the GPT:

- finds a person-level exact target when one exists
- applies the Q-gate correctly
- selects exact only when Axis A, Axis B, and Axis Q align explicitly
- keeps the final matrix compact and correct

### Observed result

The GPT selected:

- `Self-identified male-gender person → hriv:hasExactMeaning → hrio:SelfIdentifiedMaleGenderPerson`

### Verdict

**Pass**

### Main strengths

- Correct exact target selected
- Exact-Lock rule respected
- Good separation between candidate reasoning and final compact matrix
- Good rejection of mode-level target (`SelfIdentifiedMaleGender`) because of bearer mismatch
- Good broader fallback candidate (`MaleGenderPerson`)
- Correct decision not to trigger `needs-new-concept`

### Minor issue

The only notable ambiguity is the qualifier interpretation:

- The output mapped the target to `self-reported`
- The ontology wording appears closer to `self-identification`

This is acceptable if `self-identification` is intentionally treated as falling under the `self-reported` bucket, but it still indicates a small ontology-to-bucket alignment ambiguity.

### Score estimate

**94–96 / 100**

### Conclusion

This is a strong demonstration that the prompt works well for:

- exact matching
- explicit qualifier control
- bearer-aware mapping
- final presentation formatting

______________________________________________________________________

## Test 2

### Name

Directional / provisional mapping with missing target Q

### Source concept

Biological man

### Intended behavior

The test was designed to verify whether the GPT:

- avoids unsafe exactness
- prefers a safe directional mapping when the ontology contains a defensible broader target
- avoids triggering `needs-new-concept` when a structural directional mapping is available
- keeps readiness/status conservative when target qualifier metadata is missing

### Observed result

The GPT selected:

- `Biological man → hriv:hasNarrowerMeaningThan → hrio:KaryotypicMaleSexPerson`

### Verdict

**Pass with notable issues**

### Main strengths

- Correctly avoided an unsafe exact match
- Correctly found a plausible structural target in the karyotypic person branch
- Correctly rejected:
    - `hrio:KaryotypicMaleSex` because it is a sex/property class rather than a person class
    - `hrio:MaleSexPerson` because it is grounded in broader dimorphic traits rather than specifically XY chromosomes
- Correctly did not trigger `needs-new-concept`
- Final matrix format was correct

### Main issues

1. **Candidate readiness inflation**

    - Candidate 1 was marked:
        - `Candidate Ready-to-Apply: yes`
    - But the same candidate also had:
        - `Target(Q): Missing`
        - only 88% confidence
        - directional, non-exact mapping
    - This should almost certainly have been `partial`, not `yes`.

2. **Overall status inflation**

    - The final mapping was marked:
        - `Overall Status: final`
    - Given the missing target Q, non-exact mapping, and acknowledged broadening, this should have been:
        - `Overall Status: provisional`

3. **Internal decision inconsistency**

    - The answer itself explicitly says:
        - exact is unsafe
        - target Q is missing
        - the chosen mapping is only the safest directional option
    - But then still reports the result as fully final and ready.
    - This weakens decision discipline.

### Score estimate

**84–88 / 100**

### Conclusion

This result is semantically good, but decision-status calibration is still too optimistic. It is the clearest indicator that the prompt still has a remaining weakness around:

- `yes` vs `partial`
- `final` vs `provisional`

______________________________________________________________________

## Test 3

### Name

`needs-new-concept` boundary case

### Source concept

Male-by-self-identification but female-in-administrative-records person

### Intended behavior

The test was designed to verify whether the GPT:

- avoids forcing a positive mapping when no single HRIO class preserves the essential conceptual structure
- recognizes that component meanings may exist separately without a safe single target existing
- triggers `needs-new-concept` when the defining disagreement is itself essential to the source concept

### Observed result

The GPT selected no final mapping and returned:

- `Overall Status: needs-new-concept`
- `Final Statements: none`

### Verdict

**Pass**

### Main strengths

- Correctly recognized this as a true `T5 / needs-new-concept` case
- Correctly did not force a positive mapping
- Correctly identified that the ontology contains:
    - the self-identified male component
    - the administratively female component
    - but not a single class where the disagreement itself is the defining concept
- Correctly rejected transgender-related near-matches because they are based on the wrong comparison axis
- Correct final matrix structure
- Correct use of `Final Statements: none`

### Minor issue

The result used a composite source qualifier:

- `Source(Q): self-reported + administrative/recorded`

This is reasonable for this source concept, but it exposes a small prompt gap:

- the prompt currently describes qualifier reporting in a way that sounds single-bucket oriented
- this test shows that composite qualifier structures may need to be explicitly allowed

A second small presentation issue:

- some negative-only candidates were marked `partial`
- in practice, `no` may be cleaner for pure negative candidate states

### Score estimate

**95–97 / 100**

### Conclusion

This is the strongest evidence that the new `needs-new-concept` rule is working properly. The prompt successfully prevented forced mapping and preserved the source’s essential structure.

______________________________________________________________________

## Comparative Summary

| Test   | Intended focus                            | Verdict                  | Estimated score | Main takeaway                                   |
| :----- | :---------------------------------------- | :----------------------- | :-------------: | :---------------------------------------------- |
| Test 1 | Exact-Lock with explicit qualifier match  | Pass                     |      94–96      | Exact-match behavior is strong                  |
| Test 2 | Directional mapping with missing target Q | Pass with notable issues |      84–88      | Semantics good, status/readiness too optimistic |
| Test 3 | `needs-new-concept` boundary case         | Pass                     |      95–97      | T5 behavior is working well                     |

### Cross-test pattern

- **Exact matching** works well when the ontology provides a direct person-level match with explicit qualifier support.
- **T5 / `needs-new-concept`** works well when the concept depends on a defining structure not preserved by any one target.
- **Directional cases** are the current weak point only in terms of **decision labeling**, not target discovery or semantic logic.

______________________________________________________________________

## Overall Evaluation of v4

### Overall verdict

**Good prompt; close to production-ready for supervised use**

### What is already working well

- compact final presentation matrix
- candidate-level reasoning separated from final record
- good structural reasoning
- good protection against unsafe exact matches
- good use of bearer constraints
- strong `needs-new-concept` behavior
- improved evidence discipline

### Main remaining issue

The prompt still allows the model to overstate certainty in directional cases by assigning:

- `Candidate Ready-to-Apply: yes`
- `Overall Status: final`
    even when:
- target qualifier evidence is missing
- the mapping is only directional
- the reasoning itself acknowledges semantic broadening or incompleteness

### Recommended priority for next refinement

The highest-priority refinement is to make readiness and overall status more conservative in non-exact cases, especially when:

- `Target(Q): Missing`
- the predicate is broader/narrower rather than exact
- the target loses any defining source feature

______________________________________________________________________

## Final Decision

Based on these three tests, I would assess the prompt as:

- **Suitable for continued evaluation**
- **Strong enough for supervised/manual use**
- **Not yet ideal for unattended application without a small additional refinement to decision-status calibration**
