# HRIO Mapping GPT — Test Report

## Test Metadata

- **Test Case ID**: TC-001
- **Test Title**: Direct-definition smoke test with no explicit qualifier
- **Prompt Version Under Test**: `20260310-v2`
- **Previous Baseline for Comparison**: `20260310-v1`
- **Test Type**: Smoke test
- **Execution Mode**: Single concept, single turn
- **Reviewer**: [fill in]
- **Test Date**: [fill in]

______________________________________________________________________

## Test Objective

Evaluate whether the GPT:

1. correctly processes **one direct-definition concept**,
2. uses only embedded Knowledge and provided text,
3. applies the stricter v2 mapping rules,
4. avoids redundant negation,
5. handles `Source(Q)` and `Target(Q)` conservatively,
6. produces an auditable, structured result.

______________________________________________________________________

## Test Environment

### Embedded Knowledge Files Available

- `documentation-v1.6.2.md`
- `health-ri-ontology-v1.6.2.ttl`
- `specification-v1.6.2.html`
- `health-ri-vocabulary-v1.1.0.ttl`
- `health-ri-ontology-v1.6.2.json`
- `HRI-SSI SWAT4HCLS v1.1.1.docx`

### Relevant Ontology/Vocabulary Versions

- **HRIO ontology**: `v1.6.2`
- **HRIV vocabulary**: `v1.1.0`

______________________________________________________________________

## Test Input

### Source Concept

- **Source concept label**: `Biological Man`
- **Source concept definition**: `"Any human that is born with XY sexual chromosomes."`

### Input Mode

- **Input type**: direct definition
- **Source file**: none
- **Source location**: inline prompt only

### Source Context Sent to the GPT

- **Source/standard**: toy test case
- **Evidence type**: direct definition
- **Expected qualifier cues in source text**: none explicit
- **Important bearer cue**: human

______________________________________________________________________

## Prompt Behavior Being Tested

This test was specifically intended to verify:

- the new **Strictness Rule** in `20260310-v2`,
- the corrected **T3 (Directional)** behavior,
- explicit reporting of:
    - `Source(Q): [Bucket|None explicit|Missing]`
    - `Target(Q): [Bucket|Missing]`
- correct use of `Target(Q): Missing` when no allowed qualifier bucket is explicitly supported by HRIO metadata,
- conservative output status and readiness.

______________________________________________________________________

## Raw Result Summary

### Knowledge Access

- **Reported by GPT**: succeeded

### Retrieval Process Reported

- **Exact phrase**: no exact HRIO label for `Biological Man`
- **Head noun**: `Man` (`hrio:Man`)
- **Synonyms/tokens used**:
    - `Biological Male`
    - `XY`
    - chromosomal/karyotypic branch terms

### Source Normalization Keys Reported

- `biological man`
- `biological male`
- `man`
- `male`
- `xy`
- `sex chromosome`
- `human`

______________________________________________________________________

## Final Mapping Output Returned by the GPT

### Presentation Matrix Summary

| Rank | Target                               | Predicate                     | Q-Gate Status                                  | Confidence |
| ---- | ------------------------------------ | ----------------------------- | ---------------------------------------------- | ---------: |
| 1    | `hrio:KaryotypicMaleSexPerson`       | `hriv:hasNarrowerMeaningThan` | `Source(Q)=None explicit`, `Target(Q)=Missing` |        97% |
| 2    | `hrio:RegularKaryotypicalMalePerson` | `NOT hriv:hasExactMeaning`    | `Source(Q)=None explicit`, `Target(Q)=Missing` |        94% |
| 3    | `hrio:MaleSexPerson`                 | `hriv:hasNarrowerMeaningThan` | `Source(Q)=None explicit`, `Target(Q)=Missing` |        96% |
| 4    | `hrio:Man`                           | `hriv:hasNarrowerMeaningThan` | `Source(Q)=None explicit`, `Target(Q)=Missing` |        95% |
| 5    | `hrio:KaryotypicMaleSex`             | `NOT hriv:hasExactMeaning`    | `Source(Q)=None explicit`, `Target(Q)=Missing` |        99% |
| 6    | `hrio:VariantKaryotypicalMalePerson` | `NOT hriv:hasExactMeaning`    | `Source(Q)=None explicit`, `Target(Q)=Missing` |        99% |

### Mapping Record Returned

- `Biological Man → hriv:hasNarrowerMeaningThan → hrio:KaryotypicMaleSexPerson`
- `Biological Man → NOT hriv:hasExactMeaning → hrio:RegularKaryotypicalMalePerson`
- `Biological Man → NOT hriv:hasExactMeaning → hrio:KaryotypicMaleSex`
- `Biological Man → NOT hriv:hasExactMeaning → hrio:VariantKaryotypicalMalePerson`

### Status Returned

- **Status**: `mixed`
- **Ready-to-Apply**: `partial`

______________________________________________________________________

## Evaluation Against v2 Rules

## A. Instruction Compliance

### Result

**Pass**

### Notes

- Processed only **one** concept.
- Did not use web knowledge.
- Used only allowed predicates.
- Did not assign more than one predicate to the same source-target pair.
- Did not negate broader/narrower.
- Respected the v2 non-redundancy rule.

______________________________________________________________________

## B. Evidence Discipline

### Result

**Pass**

### Notes

- Reported knowledge access success.
- Used embedded Knowledge and direct user input.
- Quoted verbatim labels and CURIEs.
- Included retrieval trace and ontology line references.
- Logged source normalization keys and source location.

______________________________________________________________________

## C. Qualifier Gate Handling

### Result

**Pass**

### Notes

- Explicitly reported:
    - `Source(Q): None explicit`
    - `Target(Q): Missing`
- Did **not** force “karyotypic,” “chromosomal,” or similar descriptors into one of the allowed Q buckets.
- Did **not** assert exact meaning without Q alignment.
- Correctly downgraded because `Target(Q)` was missing.

### Importance

This is the strongest improvement over `20260310-v1`.

______________________________________________________________________

## D. T3 / Negation Logic

### Result

**Pass**

### Notes

- The final record uses one positive directional mapping and negative exact statements only for **different** targets.
- No redundant pattern of:
    - `A → hasNarrowerMeaningThan → B`
    - `A → NOT hasExactMeaning → B`

### Importance

This confirms that the main v2 fix worked.

______________________________________________________________________

## E. Mapping Logic

### Result

**Pass**

### Notes

- `hrio:KaryotypicMaleSexPerson` as the best directional candidate is defensible.
- `hrio:RegularKaryotypicalMalePerson` as a near-match rejected for exactness is defensible.
- `hrio:MaleSexPerson` and `hrio:Man` were treated as broader person-level targets.
- `hrio:KaryotypicMaleSex` was correctly rejected as a positive mapping because of bearer mismatch.
- `hrio:VariantKaryotypicalMalePerson` was correctly rejected as a positive mapping because it includes non-XY variants.

______________________________________________________________________

## F. Output Format

### Result

**Pass with minor observations**

### Notes

Required sections were present:

- Presentation Matrix
- Candidates
- Why These Candidates
- Mapping Record
- Self-audit

Minor observations:

- Confidence values remain somewhat too precise for a toy case.
- Some lower-ranked candidates are semantically valid but operationally less useful.

______________________________________________________________________

## Comparison with v1

## Key Improvements in v2 Result

1. **No redundant negation for the same source-target pair**
2. **Proper use of `Target(Q): Missing`**
3. **No invented qualifier buckets**
4. **More conservative final status**
5. **Better protocol compliance overall**

## Main Defects from v1 That Were Resolved

- T3 structural failure
- informal/non-compliant qualifier language
- overconfident `Status: final`
- overconfident `Ready-to-Apply: yes`

______________________________________________________________________

## Defects / Issues Logged for This Test

### Critical Failures

- **None**

### Minor Observations

- **OBS-001**: Confidence values are very granular for a toy concept.
- **OBS-002**: Some additional ranked candidates are valid but not especially operationally useful.
- **OBS-003**: This remains primarily a prompt-discipline test, not a realistic domain test.

______________________________________________________________________

## Suggested Scoring

| Dimension                       |  Score |     Max |
| ------------------------------- | -----: | ------: |
| Instruction compliance          |     18 |      20 |
| Evidence extraction / grounding |     14 |      15 |
| Mapping logic                   |     18 |      20 |
| Qualifier gate handling         |     10 |      10 |
| Output format compliance        |      9 |      10 |
| Final decision quality          |      9 |      10 |
| **Total**                       | **92** | **100** |

### Overall Outcome

- **Result**: `Pass`
- **Critical Failure**: `No`
- **Confidence in Evaluation**: high

______________________________________________________________________

## Reviewer Conclusion

`20260310-v2` materially improved the behavior observed in `20260310-v1`.

The model now:

- respects the strictness / non-redundancy rule,
- applies the qualifier gate conservatively,
- avoids inventing qualifier categories,
- and produces a safer final mapping record.

For this smoke test, the prompt version `20260310-v2` is acceptable and should proceed to the next evaluation stage.

______________________________________________________________________

## Recommended Next Test

### Next Test Case ID

- `TC-002`

### Recommended Focus

A **true qualifier-gate test** using a source concept with an explicit qualifier, such as:

- self-reported
- clinician-assessed/diagnosed
- measured/observed
- administrative/recorded

### Purpose

To verify whether the GPT can correctly use:

- explicit `Source(Q)` evidence,
- explicit or missing `Target(Q)` evidence,
- downgrade logic under real Q-gate pressure.

______________________________________________________________________

## Registration Fields

Fill these in for your records:

- **Registered by**: [fill in]
- **Repository / folder**: [fill in]
- **Linked raw output file**: [fill in]
- **Linked defect log entry**: [fill in]
- **Approved for next test round**: `yes | no`
- **Notes**: [fill in]
