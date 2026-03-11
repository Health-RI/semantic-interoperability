I want to improve my v4 prompt further. Please propose concrete wording changes and explain the rationale for each of the following recommendations.

## 1) Define exactly when to return `needs-new-concept`

Please fully specify this rule.

I want an explicit decision rule for when the model should stop trying to force a mapping and instead return `needs-new-concept`. This should cover cases such as:

- no candidate being semantically defensible as exact, broader, or narrower
- the best apparent matches being only lexical near-matches
- missing qualifier or bearer distinctions that are essential to the source concept
- any candidate causing loss of a core defining feature of the source concept

Please propose precise prompt wording for this and explain why it improves safety, determinism, and auditability.

## 2) Add a parser fallback policy, but only this part

I do **not** want the full fallback sequence. I only want a hard rule along the lines of:

- never fabricate structure from partially unread files

Please propose the best wording for that rule and explain how it should interact with the rest of the prompt, especially evidence extraction and `knowledge-access-failed`.

## 3) Separate candidate readiness from overall mapping status

Please use the earlier proposal, not my simplified binary version.

So I want something like:

- **Candidate Ready-to-Apply**: `yes | partial | no`
- **Overall Status**: `final | provisional | needs-new-concept`

Please explain why this separation is better than overloading one field, and propose the cleanest way to integrate it into the response format and final presentation matrix.

## 4) Add a hard no-hallucination evidence rule

Please include the full recommendation here.

I want a strict evidence-discipline rule covering points such as:

- do not paraphrase as evidence
- do not treat absence of evidence as positive evidence
- do not infer HRIO metadata fields that were not retrieved
- when required evidence is missing, explicitly state `Missing`

Please propose exact wording for this rule and explain where it should appear in the prompt so that it has maximum effect.

## What I want from you

For each of the four items above, please provide:

1. the recommended prompt text
2. where it should be inserted in v4
3. why it improves the prompt
4. any trade-offs or risks
5. whether it would likely improve the grading matrix, and in which criteria
