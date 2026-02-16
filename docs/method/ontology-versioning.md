# Versioning Strategy for Ontology Releases

This document specifies the version number semantics (`X.Y.Z`), priority rules, increment/reset logic, and triggers for `X`/`Y`/`Z`. It also includes the semantic vs. non-semantic decision tests, worked examples, and the versioning flowchart. Stage concepts are referenced only insofar as they drive `Y`-level changes.

This versioning strategy applies to all ontology artifacts released as part of the Health-RI Ontology (HRIO). In any given release, all artifacts share the same version identifier (`X.Y.Z`) and correspond to the same underlying HRIO OntoUML model.

## Purpose & Scope

Defines how versions are assigned and incremented for the ontology/model releases, including precedence (`X > Y > Z`), single-step increments, and resets. Stage mechanics (`int`/`irv`/`erv`/`pub`) are covered in *Validation Strategy*; they are referenced here only where they directly affect `Y`. This strategy is effective for releases starting at `v1.0.0`; earlier releases (`< v1.0.0`) followed an [earlier versioning policy](./ontology-versioning-old.md).

!!! note "Artifacts covered and alignment"

    The `X.Y.Z` version identifier applies uniformly to the ontology artifacts released by this initiative:

    - HRIO OntoUML model in Visual Paradigm (`.vpp` project).
    - HRIO OntoUML model exported as JSON (`.json`).
    - HRIO gUFO/OWL ontology (`.ttl`, in Turtle).
    - SHACL shapes file (`.shacl`, in Turtle).
    - Ontology documentation and specification.

    Model changes are authored in the OntoUML `.vpp` project first. For each release, the derived artifacts above are regenerated or updated from that source so they remain synchronized under the same version identifier.

## Definitions & Glossary

- Version format: `X.Y.Z`
    - `X` — Package index (`1, 2, 3, …`): increases when a new package (new domain scope) is introduced.
    - `Y` — Stage increment (`0, 1, 2, …`): increases for every domain package stage change.
    - `Z` — Minor fixes (`0, 1, 2, …`): minor modifications that should not significantly impact the domain representation (layout, labeling, diagramming, minor corrections, etc.).
    - Examples: `3.0.0`, `3.7.15`, `4.0.1`.

> Note on stages. Stages are tracked per domain packages (see *Validation Strategy*). A stage transition causes `Y++` and resets `Z → 0`, per rules below.

!!! note "Published tags are rarely "round""

    GitHub releases are created when the relevant domain package is in `pub` stage, occurring after stage transitions (`int → irv → erv → pub`). Stage transitions bump `Y`, so published versions are **unlikely** to be exactly `X.0.0` (e.g., `2.0.0`), and `Z` may be non-zero. Expect tags like `2.1.0` or `2.3.4`. "Round" versions may still occur because we version the ontology as a whole (not per package), while domain packages' independent state transitions influence the overall ontology version.

## Version Numbering & Semantics — Increment & Reset Rules

- Single-step per release. Exactly one component increments by `+1` per release — the highest-priority applicable one (`X > Y > Z`). Lower components never increment concurrently; they only reset (`Y → 0` on `X++`; `Z → 0` on `X++` or `Y++`).
    - Not allowed: `1.5.3 → 1.6.4` or `1.5.3 → 1.7.0` in a single release.
    - Allowed: `1.5.3 → 1.6.0` (`Y++`) or `1.5.3 → 2.0.0` (`X++`).
- Priority. If multiple qualifying changes occur together, apply only the highest-priority bump (`X > Y > Z`). Lower components reset accordingly.
- No skipping within a component. Always increment by exactly `+1` within `X`, `Y`, or `Z`.
- Mixed `X` with `Y/Z`. If any `X` trigger occurs in a release, apply `X++` (once). Record `Y`/`Z`-qualifying changes in the changelog; do not increment `Y` or `Z` in that same release (`Y = 0`, `Z = 0` after `X++`).
- Mixed `Y` with `Z`. If any `Y` trigger occurs in a release, apply `Y++` (once). Record `Z`-qualifying changes in the changelog; do not increment `Z` in that same release (`Z → 0` on `Y++`).
- Semantic changes mandate a stage transition. Any semantic change (meaning of classes/relations/constraints/definitions) must be recorded as a package stage reversion to `int` (see *Validation Strategy*). This causes `Y++` and `Z → 0`.
- Resets.
    - When `Y` increases, `Z` resets to `0`.
    - When `X` increases, `Y` and `Z` reset to `0`.

## Triggers & Decision Rules

### Conditions for increasing `X`

- Triggers:

    - Starting a new package (new domain scope) in the repository.
    - Removing an existing package from the official package set (any removal from scope is `X`).

- Non-triggers:

    - Advancing a package through stages (`int`, `irv`, `erv`, `pub`): that is `Y`, not `X`.
    - Renaming/regrouping classes within an existing package without adding a new package.

### Conditions for increasing `Y`

- Triggers:

    - Any domain package stage transition: `int → irv`, `irv → erv`, `erv → pub`, or a recorded reversion (e.g., `irv → int`) via the package's stage tagged value.
    - Any semantic change that alters model meaning within a package (e.g., adding/removing/retaxonomizing classes, retyping relations, changing multiplicities or constraints, revising authoritative definitions, introducing/removing key axioms).
        - Action: record `<current> → int` for the package (see *Validation Strategy*).
        - Result: `Y++` for that release; `Z → 0`.
    - When multiple packages transition in the same release, perform a single `Y++` (`Z` resets to `0`).

- Non-triggers:

    - Being in a stage without a transition since last release.
    - Diagram/class edits that do not change the package stage.
    - Tagged-value corrections that leave stage history unchanged.
    - Removing a package (this is `X`, not `Y`).

### Conditions for increasing `Z`

- Triggers:

    - Minor, non-semantic corrections that do not materially change domain representation: label/name normalization, spelling/typos, diagram layout, link/URI fix, file reorganization, export settings, docstring wording, small diagram tweaks.

- Non-triggers:

    - Any package stage transition (`int/irv/erv/pub`) → that is `Y` (and resets `Z` to `0`).
    - Starting/adding a new package → that is `X` (and resets `Y` and `Z` to `0`).
    - Semantic modeling changes are never `Z`; they require a stage reset to `int` and thus `Y++`.

## Semantic vs. Non-Semantic — Decision Tests

Treat the change as **semantic** (counts for `Y`) if any of the following is **yes**; otherwise it is `Z`:

1. Entailment / constraints test. Does the change alter logical consequences, constraints, or permitted structures (e.g., subsumption, typing, multiplicities, keys, disjointness)? → yes ⇒ semantic (`Y`).
2. Extension / instances test. Would at least one previously valid instance become invalid (or vice versa) solely due to this change? → yes ⇒ semantic (`Y`).
3. Identity / reference stability test. Does the change alter IRIs/identifiers or definitions in a way that affects element identity/meaning? → yes ⇒ semantic (`Y`).
    - Label-only edits (e.g., `rdfs:label`, typos, capitalization) with unchanged IRI/definition are `Z`.
4. Diagram-only test. Is the change confined to visuals (positions, routing, styling) with no change to model elements or constraints? → yes ⇒ non-semantic (`Z`).

### Edge-case examples

| Change                                                                            | Y or Z? | Rationale                                                      |
| --------------------------------------------------------------------------------- | ------- | -------------------------------------------------------------- |
| Rename class label "Person" → "Individual" (label only; IRI/definition unchanged) | Z       | Terminology-only; no entailment or instance impact.            |
| Rename class IRI or revise textual definition to narrow/broaden scope             | Y       | Identity/meaning changed; instance/entailment impact possible. |
| Add an association previously only *visually implied* by layout                   | Y       | New relation; changes entailments/instances.                   |
| Move boxes/arrows, improve diagram readability                                    | Z       | Diagram-only; model unchanged.                                 |
| Change multiplicity `0..* → 1..*`                                                 | Y       | Constraint tightened; prior instances may become invalid.      |
| Retype association end or change superclass                                       | Y       | Taxonomic/typing change; affects entailments/instances.        |
| Fix spelling/capitalization in labels                                             | Z       | Surface-only.                                                  |

## Examples / Decision Table (Worked Examples)

*(Assume current version is `v1.5.8` unless noted.)*

1. A: `int → irv` → `Y++` → `v1.6.0` (`Z → 0`).
2. A: `irv → erv`, B: `int → irv` (same release) → `Y++` once → `v1.6.0` (`Z → 0`).
3. Start new package C and A: `erv → pub` (same release) → `X++` → `v2.0.0` (`Y, Z → 0`).
4. Typos/layout only → `Z++` → `v1.5.9`.
5. B: `irv → int` (recorded) → `Y++` → `v1.6.0` (`Z → 0`).
6. Later A: `erv → pub` (new release) → `Y++` → `v1.7.0` (`Z → 0`).
7. Semantic change at `erv` (retype relation): record `erv → int` → `Y++` → `v1.6.0` (`Z → 0`).
8. Remove a package (scope contraction) from `v1.5.8` → `X++` → `v2.0.0` (`Y = 0`, `Z = 0`).
9. `X` present with multiple `Y` events → `X++` once → `v2.0.0` (no `Y++`).
10. `Y` present with several `Z` events → `Y++` once → `v1.6.0` (no `Z++`).
11. Label rename only ("Person" → "Individual") → `Z++` → `v1.5.9`.
12. Definition/IRI change ("Person" narrowed/broadened): record `<current> → int` → `Y++` → `v1.6.0` (`Z → 0`).

## Figures

### Versioning Flow

```mermaid
flowchart LR

  subgraph ALL[ ]
    direction LR

    S((Start))

    B{Package added<br/>or removed?}
    C{Any package<br/>stage change?}
    D{Non-semantic<br/>modifications?}

    X[X++ set Y=0; set Z=0]
    Y[Y++ set Z=0]
    Z[Z++]
    N[No version bump]

    yes1([Yes]):::yes
    no1([No]):::no
    yes2([Yes]):::yes
    no2([No]):::no
    yes3([Yes]):::yes
    no3([No]):::no

    S --> B
    B --- yes1
    B --- no1
    C --- yes2
    C --- no2
    D --- yes3
    D --- no3
    yes1 --> X
    no1    --> C
    yes2 --> Y
    no2    --> D
    yes3 --> Z
    no3    --> N
  end

  %% Node styling (Option A adjustments)
  %% - Semi-transparent fills improve readability on any theme
  %% - Bold font, rounded corners, small padding
  classDef stage fill:#0f5d73cc,stroke:#e6f2f6,color:inherit,font-weight:bold,rx:6,ry:6,padding:4;
  classDef pub   fill:#1f6f2acc,stroke:#e6f2f6,color:inherit,font-weight:bold,rx:6,ry:6,padding:4;
  classDef yes   fill:#1f6f2acc,stroke:#1f6f2a,color:inherit,font-weight:bold,rx:6,ry:6,padding:4;
  classDef no    fill:#8B0000cc,stroke:#8B0000,color:inherit,font-weight:bold,rx:6,ry:6,padding:4;
  classDef result fill:#009fadcc,stroke:#e6f2f6,color:inherit,font-weight:bold,rx:6,ry:6,padding:4;

  class B,C,D stage;
  class S,X,Y,Z,N pub;
  class X,Y,Z,N result;

  %% Soft text halo for light themes (increases contrast slightly)
  style S text-shadow:0px 0px 3px #00000033
  style B text-shadow:0px 0px 3px #00000033
  style C text-shadow:0px 0px 3px #00000033
  style D text-shadow:0px 0px 3px #00000033
  style X text-shadow:0px 0px 3px #00000033
  style Y text-shadow:0px 0px 3px #00000033
  style Z text-shadow:0px 0px 3px #00000033
  style N text-shadow:0px 0px 3px #00000033

  %% Edge styling
  linkStyle default stroke:#000000,stroke-width:2px;
  linkStyle 3,4,5 stroke:#8B0000,stroke-width:2px;
```

## Edge Cases & Notes

- Reverting a stage. Any recorded stage transition (forward or backward) increments `Y` and resets `Z` to `0`.
- Simultaneous edits across many packages. Combine into one release → at most one increment; apply `X > Y > Z` priority and resets.
- Semantic change at any stage (including `pub`). Reset stage to `int` (`<current> → int`) and issue `Y++` (`Z → 0`). If missed earlier, correct the stage and bump `Y` in the release that fixes the record.
- Definition of semantic change. A change is semantic iff it alters at least one of: (i) logical consequences; (ii) admissible instance space; or (iii) intentional content (identity) via IRI/definition changes. All other changes are non-semantic.
- Moving classes between existing packages. If entailments/constraints/definitions change → treat as semantic (`Y`); otherwise `Z`.
