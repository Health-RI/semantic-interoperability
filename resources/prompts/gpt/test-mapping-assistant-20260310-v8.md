# HRIO Mapping Prompt Test Report

## Scope

This report formalizes five targeted tests for the prompt **“Mapping One User Domain Concept to HRIO”** and records the corrected evaluation of each observed result.

## Evaluation Basis

All judgments below are based on the prompt **as written**, with particular attention to:

- predicate constraints
- qualifier handling
- the clarification rule
- the outcome selection ladder (T1–T5)
- candidate readiness (`yes | partial | no`)
- mapping status (`final | provisional | needs-new-concept`)

## Evaluation Legend

- **Pass**: compliant or largely compliant with only minor issues
- **Pass with issues**: substantively correct, but with one or more formal inconsistencies
- **Fail**: not compliant with the prompt’s decision logic

______________________________________________________________________

## Test 1 — Exact match with explicit qualifier lock

### Test objective

Verify whether the prompt supports a clean **T1 Exact-Lock** outcome when the source concept and HRIO target align on:

- meaning
- bearer scope
- qualifier bucket

### Test input

- **Source label:** Self-identified gender identity
- **Source definition:** A person’s gender identity as explicitly self-identified by the person.
- **Key source evidence:** “Gender identity reported by the individual themself.”

### Expected outcome pattern

- Exact target identified
- `Source(Q)` and `Target(Q)` explicitly match
- Final Mapping Record contains **only** one exact statement
- Status = `final`

### Observed result summary

- Exact target selected: `"Self-identified Gender" (hrio:SelfIdentifiedGender)`
- Final statement:
    - `Self-identified gender identity → hriv:hasExactMeaning → hrio:SelfIdentifiedGender`
- Status:
    - `final`

### Corrected evaluation

**Pass with issues**

### Why

The exact mapping is correct and the final Mapping Record is compliant with **T1**. The output also correctly avoided adding additional final statements once exactness was established.

The main issue is in the **candidate readiness labels** for broader candidates:

- `"Self-designated Gender"` was marked `yes`
- `"Gender"` was marked `yes`

Under the prompt, those should be **`partial`**, because they rely on:

- directional approximation
- `Target(Q): Missing`
- generalization beyond the source’s specific self-identification constraint

### Formal verdict

- **Mapping Record:** correct
- **Overall Status:** correct
- **Candidate readiness:** partially incorrect
- **Final assessment:** **Pass with issues**

______________________________________________________________________

## Test 2 — Directional mapping caused by qualifier restriction and missing disease-specific target

### Test objective

Verify whether the prompt supports a **T3 directional** outcome when:

- no diabetes-specific HRIO target is retrieved
- the source is condition-level
- diagnosis-class targets are near-misses, not exact condition targets

### Test input

- **Source label:** Clinically diagnosed diabetes mellitus
- **Source definition:** Diabetes mellitus only when established through clinical diagnosis by a healthcare professional.
- **Key source evidence:** “Presence of diabetes mellitus confirmed by clinical diagnosis.”

### Expected outcome pattern

- No exact match
- Safe broader condition-level mapping may be allowed
- Diagnosis outcome classes may support `NOT hriv:hasExactMeaning`
- Final result may remain `final` if at least one safe final statement is present

### Observed result summary

- Positive directional statement:
    - `Clinically diagnosed diabetes mellitus → hriv:hasNarrowerMeaningThan → hrio:Disease`
- Negative exact statement:
    - `Clinically diagnosed diabetes mellitus → NOT hriv:hasExactMeaning → hrio:ClinicalDiagnosis`
- Status:
    - `final`

### Corrected evaluation

**Pass with issues**

### Why

The final statement set is valid under **T3**:

- the source is narrower than `"Disease"`
- `"Clinical Diagnosis"` is a strong near-miss negative exact target because it matches the diagnostic qualifier but not the ontological category

The main issue is again **candidate readiness**:

- `"Disease"` was marked `yes`

This should be **`partial`**, because the statement depends on:

- directional approximation
- loss of diabetes-specificity
- `Target(Q): Missing`

However, under the current status rule, `Overall Status: final` is still **defensible**, because the prompt allows `final` when at least one final statement is safe to apply directly, including an exact-negative one.

### Formal verdict

- **Mapping Record:** correct
- **Overall Status:** defensible and acceptable
- **Candidate readiness:** partially incorrect
- **Final assessment:** **Pass with issues**

______________________________________________________________________

## Test 3 — Negative exact mappings as valid proposal entries with a safe directional statement

### Test objective

Verify whether the prompt treats `NOT hriv:hasExactMeaning` as a **valid mapping statement** and allows it to appear in a valid final proposal alongside a directional statement.

### Test input

- **Source label:** Administrative sex registration
- **Source definition:** A person’s sex value as officially recorded in an administrative or legal record.
- **Key source evidence:** “Sex as officially registered in the administrative record.”

### Expected outcome pattern

- No exact match
- Safe directional mapping may be possible to `"Sex at Birth"` if supported as narrower
- Near-miss gender targets should support negative exactness
- Final result may validly contain both directional and negative exact statements

### Observed result summary

Final statements included:

- `Administrative sex registration → hriv:hasBroaderMeaningThan → hrio:SexAtBirth`
- `Administrative sex registration → NOT hriv:hasExactMeaning → hrio:AdministrativeGender`
- `Administrative sex registration → NOT hriv:hasExactMeaning → hrio:LegalGender`
- `Administrative sex registration → NOT hriv:hasExactMeaning → hrio:Sex`

Status:

- `final`

### Corrected evaluation

**Pass with issues**

### Why

The output correctly identified the structural problem:

- HRIO does not provide a direct general target for administratively or legally recorded sex
- `"Sex at Birth"` is narrower due to the birth-time restriction
- `"Administrative Gender"` and `"Legal Gender"` are valid near-miss negative exact candidates

The negative exact use is valid and should count as a legitimate proposal component under the prompt.

The main issue is again the readiness label for the directional statement:

- `"Sex at Birth"` was marked `yes`

This should more cautiously be **`partial`**, because the statement depends on:

- directional approximation
- a narrower birth-time restriction
- incomplete preservation of the source scope

The negative candidate against `"Sex"` is also **defensible** under the prompt, because it is in the same semantic domain and exactness is blocked by the missing administrative/legal-recorded modality.

### Formal verdict

- **Mapping Record:** correct
- **Overall Status:** defensible and acceptable
- **Candidate readiness:** partially incorrect for the directional candidate
- **Final assessment:** **Pass with issues**

______________________________________________________________________

## Test 4 — Clarification should not be asked when T5 is already safe

### Test objective

Verify whether the prompt correctly prefers **T5 needs-new-concept** over clarification when:

- the source is underspecified
- but no relevant HRIO target exists anyway
- clarification would not materially change the safe outcome

### Test input

- **Source label:** Ethnicity
- **Source definition:** Ethnicity of a person.
- **Key source evidence:** “Ethnicity”

### Expected outcome pattern

- No clarification question
- No forced mapping
- `needs-new-concept`
- Any remote negative exact candidates, if discussed, should not be promoted into the final mapping set

### Observed result summary

- No clarification question asked
- No final mapping statements
- Final status:
    - `needs-new-concept`

### Corrected evaluation

**Pass**

### Why

This is a strong example of correct prompt behavior.

The output correctly reasoned that:

- missing source qualifier detail did not matter, because no ethnicity target was retrieved
- no safe exact, broader, or narrower mapping was available
- remote concepts such as `"Gender"` or `"Person"` were too semantically distant to include in the final mapping set

This matches the clarification rule and **T5** very well.

### Formal verdict

- **Mapping Record:** correct
- **Overall Status:** correct
- **Clarification rule application:** correct
- **Final assessment:** **Pass**

______________________________________________________________________

## Test 5 — No positive mapping and remote negative candidates should still trigger T5

### Test objective

Verify whether the prompt resists treating remote genomics-adjacent classes as valid final mapping proposals when the source concept is:

- ancestry-cluster based
- computationally inferred
- potentially multi-valued
- confidence-scored

### Test input

- **Source label:** Algorithmically inferred multi-ancestry genomic cluster membership
- **Source definition:** A person’s membership in a genomic ancestry cluster assigned by computational inference from genotype data, where the output may include multiple cluster memberships with confidence scores.
- **Key source evidence:** “Cluster membership derived computationally from genotype data, potentially assigning more than one ancestry cluster with associated confidence values.”

### Expected outcome pattern

- No safe exact mapping
- No safe broader/narrower mapping
- Remote sex-related or diagnosis-related contrasts may be discussed
- Final outcome should be `needs-new-concept`, not a negative-only final proposal

### Observed result summary

Final statements included:

- `Algorithmically inferred multi-ancestry genomic cluster membership → NOT hriv:hasExactMeaning → hrio:KaryotypicSex`
- `Algorithmically inferred multi-ancestry genomic cluster membership → NOT hriv:hasExactMeaning → hrio:PersonWithRegularSexChromosome`

Status:

- `final`

### Corrected evaluation

**Fail**

### Why

This result conflicts with **T5**.

The output itself established that the retrieved targets lose the source’s defining features, including:

- ancestry-cluster meaning
- computational inference structure
- multi-membership
- confidence-score structure

Under the prompt, that should lead to:

- `Final Statements: none`
- `Overall Status: needs-new-concept`

The negative exact candidates are too remote to serve as a good final mapping proposal. They are better treated as inspected contrasts, not as valid final statements.

### Formal verdict

- **Mapping Record:** incorrect
- **Overall Status:** incorrect
- **Final assessment:** **Fail**

______________________________________________________________________

## Consolidated Results Table

| Test | Focus                                            | Expected pattern                                    | Corrected assessment |
| :--- | :----------------------------------------------- | :-------------------------------------------------- | :------------------- |
| 1    | Exact-Lock with explicit Q match                 | T1 exact-only final statement                       | Pass with issues     |
| 2    | Directional + negative near-miss                 | T3 with valid negative exact entry                  | Pass with issues     |
| 3    | Negative exact as valid proposal component       | T3 with valid directional + negative statements     | Pass with issues     |
| 4    | Clarification restraint + T5                     | needs-new-concept without unnecessary clarification | Pass                 |
| 5    | Remote near-miss negatives should not replace T5 | needs-new-concept                                   | Fail                 |

______________________________________________________________________

## Cross-Test Findings

### Stable strengths of the prompt

The prompt is working well at:

- preventing unsafe exact mappings
- supporting legitimate negative exact statements
- enforcing T5 when no safe semantic target exists
- preferring no clarification when clarification would not change the outcome

### Stable weakness exposed by the tests

The main recurring weakness is the model’s tendency to over-assign:

- `Candidate Ready-to-Apply: yes`

in cases that should be:

- `partial`

This happens especially for **directional** candidates that involve:

- approximation
- scope loss
- `Target(Q): Missing`

### Practical interpretation

The prompt’s core logic is sound. The main operational risk is **overconfident readiness labeling**, not gross semantic failure, except in Test 5.

______________________________________________________________________

## Final Conclusion

The five tests collectively show that the prompt is already strong in its:

- exactness discipline
- qualifier discipline
- T3/T5 separation
- support for valid negative exact mappings

The main refinement still needed is tighter control over:

- when a candidate is `yes` versus `partial`

A concise operational rule that would likely improve consistency is:

- mark **directional** candidates as `partial` by default whenever they lose a defining source feature, rely on approximation, or have `Target(Q): Missing`

This would likely improve Tests 1–3 without changing the prompt’s overall decision structure.
