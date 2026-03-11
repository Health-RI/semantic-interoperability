# HRIO Mapping GPT — Test Report

## Test Cycle Metadata

- **Prompt Version:** v6
- **Scope:** three targeted behavioral tests
- **Evaluation Basis:** observed outputs against the current prompt requirements
- **Overall Result:** **Pass with minor issues**

______________________________________________________________________

## Executive Summary

The current prompt version performs well on its core goals. Across the three tests, the GPT showed strong behavior in:

- evidence-bounded reasoning
- structural over lexical matching
- bearer-scope control
- qualifier-aware mapping
- conservative use of exact mappings
- legitimate use of `needs-new-concept`
- compact final presentation matrix

The most important improvements introduced in later prompt versions are now visible in practice:

- explicit qualifier normalization works
- composite `Source(Q)` works
- `needs-new-concept` works in genuine boundary cases
- negative mappings can be treated as valid mapping statements

Remaining issues are relatively small and mostly concern edge-case prompt precision rather than broad failure.

______________________________________________________________________

## Test 1 — Clarification / underspecified source

### Input

- **Source label:** `Male status`
- **Source definition:** “A classification of a person as male.”

### Intended behavior

This test was meant to check whether the GPT would:

- ask clarification questions only if truly necessary
- avoid premature exact mapping
- fall back to safe directional or provisional outputs if possible

### Observed behavior

The GPT did **not** ask clarification questions and instead produced a **safe provisional directional result** with bounds-like reasoning:

- narrower than `hrio:SexGender`
- broader than `hrio:MaleSex`
- broader than `hrio:MaleGender`

It correctly avoided an exact mapping and set:

- **Overall Status:** `provisional`

### Assessment

**Pass, with one mild issue**

The no-clarification decision was acceptable because a safe non-exact outcome was available from the evidence.

### Main issue

The output stated that `hrio:Male` was the closest semantic target, but it did not include `hrio:Male` as a formal candidate. This is slightly inconsistent: if it is the closest semantic candidate, it should preferably appear in the candidate list and then be downgraded explicitly if exactness is blocked.

### Conclusion

The clarification rule is working reasonably well, but candidate completeness can still improve in underspecified cases.

______________________________________________________________________

## Test 2 — Exact-Lock with qualifier normalization

### Input

- **Source label:** `Self-identified male-gender person`
- **Source definition:** “A person whose gender is self-identified as male.”

### Intended behavior

This test was meant to check:

- explicit qualifier normalization
- exact-match discipline
- proper T1 stopping behavior
- proper treatment of negative mappings

### Observed behavior

The GPT normalized:

- `self-identified` → `self-reported`

It then produced:

- `Self-identified male-gender person → hriv:hasExactMeaning → hrio:SelfIdentifiedMaleGenderPerson`

with:

- **Axis A:** aligned
- **Axis B:** aligned
- **Axis Q:** aligned
- **Overall Status:** `final`

It also correctly handled surrounding candidates:

- broader person-level classes as directional only
- mode-level classes as bearer mismatches
- administrative / externally attributed classes as qualifier mismatches

### Assessment

**Strong pass**

This test confirms that later prompt improvements are functioning well.

### Minor note

The self-audit line saying that Q buckets were “not inferred” is slightly imprecise in wording, because qualifier normalization did occur. However, this is acceptable under the current prompt because normalization is now explicitly allowed. This is a wording nit, not a substantive defect.

### Conclusion

This is the clearest confirmation that qualifier normalization and exact-lock behavior are now working as intended.

______________________________________________________________________

## Test 3 — Composite qualifier + `needs-new-concept`

### Input

- **Source label:** `Male-by-self-identification but female-in-administrative-records person`
- **Source definition:** “A person whose gender is self-identified as male while being administratively recorded as female, where the disagreement between those two classifications is essential to the concept.”

### Intended behavior

This test was meant to check:

- explicit support for composite `Source(Q)`
- preservation of essential defining conflict
- avoidance of forced positive mappings
- proper use of `needs-new-concept`

### Observed behavior

The GPT correctly derived:

- **Source(Q):** `self-reported + administrative/recorded`

It identified plausible facet-level candidates:

- `hrio:SelfIdentifiedMaleGenderPerson`
- `hrio:AdministrativeFemaleGenderPerson`

but correctly determined that no single retrieved named HRIO target preserved:

- both facets
- and the fact that the disagreement is **essential**

It therefore returned:

- **Final Statements:** `none`
- **Overall Status:** `needs-new-concept`

It also correctly treated negative mappings as valid candidate statements.

### Assessment

**Strong pass, with one minor issue**

### Main issue

One candidate used:

- `Target(Q): measured/observed + administrative/recorded`

However, the prompt explicitly allowed **composite `Source(Q)`**, but did **not** explicitly allow **composite `Target(Q)`**. So this behavior is understandable semantically, but it is not fully licensed by the current prompt wording.

### Conclusion

The most important intended behavior is working: the GPT does not force a mapping when the source concept depends on an essential structured disagreement that is not preserved by a single retrieved target.

______________________________________________________________________

## Cross-Test Findings

### Strengths confirmed

- Evidence-bounded reasoning is consistently strong.
- The GPT prefers ontology structure over label similarity.
- Bearer-scope mismatches are handled well.
- Exact matching is used conservatively.
- Final presentation matrix behavior is good and operationally useful.
- Negative mappings are being treated as legitimate mapping statements.
- `needs-new-concept` is now functioning appropriately in real boundary cases.

### Remaining issues

1. **Candidate completeness in underspecified cases**

    - The model may identify a closest semantic target in prose without including it formally as a candidate.

2. **Composite `Target(Q)` remains underspecified**

    - Composite source qualifiers are now supported, but composite target qualifiers are not yet explicitly licensed.

3. **Minor wording precision in self-audit**

    - Some audit language may blur the distinction between prohibited inference and permitted normalization.

______________________________________________________________________

## Overall Evaluation

### Final judgment

**Pass with minor issues**

### Interpretation

The prompt is now robust on the most important mapping behaviors. The remaining issues are mostly precision / edge-case specification issues rather than systemic failures.

### Informal score

- **Instruction compliance:** 18.5/20
- **Evidence discipline:** 19/20
- **Mapping logic:** 19/20
- **Qualifier handling:** 18.5/20
- **Output quality / presentation:** 19/20

**Estimated total:** **94/100**

______________________________________________________________________

## Recommended Next Step

The prompt is already in a strong state. The next refinement should focus on **small precision fixes**, especially:

1. explicitly decide whether `Target(Q)` may also be composite
2. encourage inclusion of the closest semantic target in the formal candidate list when it is mentioned in prose
3. slightly refine self-audit wording around normalization vs inference

These are incremental improvements, not major redesign needs.
