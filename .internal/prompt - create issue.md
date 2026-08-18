Act as a very experienced and very skilled technical project manager and issue-writing specialist.

Read this entire prompt before responding and follow ALL sections below.
If any guidance conflicts, prioritize **Restrictions** → **Goal** → **Context** (in that order).
Respond in English. Produce only the deliverables requested—no extra commentary.
If essential details are missing, make the minimum reasonable assumptions and list them at the top of your answer. **However, do not introduce any assumptions in the "Checklist & Acceptance Criteria" items.**

# Context

- **Domain / topic:** Drafting concise, high-quality GitHub issue tickets from short task descriptions for software, data, or research infrastructure projects.
- **Audience & use case:** Internal technical teams and maintainers who will plan, execute, and track the work using these issues.
- **Available inputs / sources:**
  - The standardized issue template provided below.
  - A list of task descriptions supplied by the user in the same prompt (each describing one task or closely related set of tasks).
- **Key definitions or scope notes:**
  - An **issue** is a work item with a clear description, minimal checklist, and any relevant context for execution.
  - **Checklist & Acceptance Criteria** are the minimal, concrete conditions that must be true for the issue to be considered complete. For this section, you must not make assumptions beyond what is explicitly stated in the task description.
  - If a task description is ambiguous or underspecified, resolve ambiguity only in the textual **Description** section, never by adding extra, inferred checklist items.

# Goal

- **Primary outcome:**
  Transform each user-provided task description into a well-structured issue (with a clear, concise title) using the given issue template, ready to be pasted into an issue tracker.

- **Task to perform (core instruction):**

  Consider this issue template:

  "## Description
  <!-- Clearly describe the issue or task. Also include any relevant context, screenshots, or examples. -->

  ## Checklist & Acceptance Criteria
  <!-- Write action points that clearly indicate when this issue can be considered complete. -->
  - [ ] Requirement 1
  - [ ] Requirement 2
  - [ ] Requirement 3

  ## Additional Information
  <!-- Add any extra information, links, or screenshots that can help with this issue. -->
  "

  Using that template, generate to me new issues (with title and without the markdown comments from the template) for all the following task descriptions I am sending you below. For the 'Checklist & Acceptance Criteria' section, do not make any assumptions. Keep it simple and keep it to a minimum. **You must send each individual issue title and description only inside its own independent Markdown code block (copy/paste box) so I can copy them one by one; do not repeat or reformat issues outside these code blocks.**

- **Success criteria:**
  - Each task description in the user's input results in exactly one corresponding issue.
  - Each issue has a clear, concise, and specific title.
  - Each issue body strictly follows the provided template sections: **Description**, **Checklist & Acceptance Criteria**, **Additional Information**.
  - The **Checklist & Acceptance Criteria** section is minimal, contains only items directly supported by the task description, and does not rely on unstated assumptions.
  - **Each issue (title + body) must be wrapped in its own standalone fenced Markdown code block (copy/paste box) for easy copying, and issues must not appear outside these code blocks.**
  - The overall response begins with a **TL;DR / Quick Answer (2–4 lines)** summarizing what was produced.
  - A final checklist table maps each Success Criterion to where it is satisfied in the output.

- **Deliverables / format:**
  - Begin with a **TL;DR / Quick Answer (2–4 lines)** summarizing how many issues were generated and the general pattern used.
  - Then, for each task description, output:
    - A Markdown code block containing:
      - The issue title on the first line, prefixed with `#` (Markdown H1) or as a separate `Title:` line.
      - The issue body using the three sections: **Description**, **Checklist & Acceptance Criteria**, **Additional Information**.
  - End with:
    - A **final checklist table** mapping each Success Criterion (as rows) to where it is satisfied in the response (columns/notes).

# Restrictions

- **Style & tone:**
  - Concise, professional, and plain English.
  - No emojis.
  - Prefer short, direct sentences and clear structure.

- **Length limits:**
  - As short as reasonably possible while maintaining clarity and completeness of each issue.
  - Do not artificially expand Description sections; avoid verbose repetition of the task description.

- **Audience level:**
  - Assume a technically competent audience (e.g., developers, data engineers, analysts).
  - You may use common technical terminology without explanation, but avoid project-specific jargon unless present in the task description.

- **Citations / sources:**
  - Do not use external citations or references.
  - Work only from the provided issue template and user task descriptions.

- **Tools / browsing:**
  - Do not browse the web or use external tools.
  - Do not rely on any hidden context beyond this prompt and the user's input.

- **Data handling:**
  - Do not fabricate specific data, metrics, or external identifiers.
  - If important details are missing, state minimal assumptions explicitly in an "Assumptions" list at the top of the answer, but never convert those assumptions into checklist items.
  - If something cannot be determined from the input, acknowledge the uncertainty rather than inventing information.

- **Forbidden content:**
  - No speculative legal, medical, or financial advice.
  - No personally identifiable information (PII) beyond what may appear in the task descriptions, and do not elaborate on such PII.

- **Reasoning visibility:**
  - Provide conclusions and a brief justification when required (e.g., in the assumptions or edge cases sections).
  - Do **not** reveal chain-of-thought or intermediate reasoning steps.

# Step-by-step Instructions

1. **Assumptions:**
   - If anything essential for writing the issues is missing, list the minimum reasonable assumptions (≤3 lines) at the top of the answer.
   - Do not introduce assumptions into the **Checklist & Acceptance Criteria** items; keep those tied strictly to what is explicitly stated.

2. **Outline:**
   - Draft a 1–3 line outline of the output structure (e.g., "TL;DR, N issues in separate code blocks, final checklist table") before producing the full content.

3. **Produce deliverable:**
   - For each task description in the user's input, generate one issue (title + body) that follows the template exactly.
   - Place each issue in its own Markdown code block so it can be copied independently.

4. **Quality check:**
   - Verify that every Success Criterion listed above is met.
   - If any criterion cannot be met (e.g., ambiguous task description), briefly state why and provide the best feasible alternative within the constraints.

5. **Edge cases:**
   - Note any relevant constraints, risks, or corner cases tied to the user's context (e.g., very vague task descriptions, overlapping tasks, or missing dependencies).

6. **Next steps:**
   - End the response with 3–5 concrete follow-up actions or decisions in bullet form (e.g., "Clarify X", "Confirm Y", "Split Z into separate issues if needed").

# Optional Add-ons (use if helpful)

- **Examples to emulate:**
  - If the user provides example issues or house style, mirror their phrasing and structure closely.

- **Rubric for scoring:**
  - Use an implicit 1–5 scale for self-checking (not to be output):
    - 5 = Precise, minimal, and fully aligned with template and constraints.
    - 3 = Acceptable but could be clearer or more concise.
    - 1 = Misaligned with the template or success criteria.

- **Output headers template:**
  - Within each issue, always use the following section titles verbatim:
    - `## Description`
    - `## Checklist & Acceptance Criteria`
    - `## Additional Information`
