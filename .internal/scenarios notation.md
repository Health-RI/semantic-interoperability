# Notation for the **As is** and **To be** examples

## 1. Artifact layers

We use three artifact layers:

- `O` for the ontology layer
- `S1`, `S2`, ..., `SN` for standards
- `M1`, `M2`, ..., `MN` for models

Examples:

- `O={o1,o2}`
- `S1={s11,s12}`
- `S2={s21,s22}`
- `M1={m11,m12}`
- `M2={m21,m22}`

These set expressions indicate which concepts belong to each artifact.

---

## 2. Concept identifiers

### Ontology concepts
Ontology concepts are written as:

- `o1`, `o2`, ..., `on`

### Standard concepts
A standard concept is written as:

- `sij`

where:

- `i` identifies the standard
- `j` identifies the concept within that standard

Examples:

- `s11` = concept 1 in standard `S1`
- `s12` = concept 2 in standard `S1`
- `s21` = concept 1 in standard `S2`

### Model concepts
A model concept is written as:

- `mij`

where:

- `i` identifies the model
- `j` identifies the concept within that model

Examples:

- `m11` = concept 1 in model `M1`
- `m21` = concept 1 in model `M2`

---

## 3. Status notation

The default status is **valid**.

So:

- `s11` means standard concept `s11` is valid
- `m11` means model concept `m11` is valid
- `o1` means ontology concept `o1` is valid

### Invalid concepts
An invalid concept is marked with suffix `i`.

Examples:

- `s11i`
- `m21i`
- `o1i`

This same suffix convention is used whenever a concept appears inside a relation expression, such as `i(m11,s11i)` or `m(s11i,s21)`.

---

## 4. Set notation

Artifacts and their concepts are represented as sets.

Examples:

- `S1={s11,s12,s13}`
- `M1={m11,m12}`
- `O={o1,o2,o3}`

This means that those concepts belong to that artifact.

---

## 5. Implements relation

The relation **implements** is written as:

- `i(x,y)`

Meaning:

- concept `x` implements concept `y`

### Allowed uses

#### Model concept implements standard concept
- `i(m11,s11)`

#### Standard concept implements ontology concept
- `i(s11,o1)`

So a full implementation chain may be:

- `i(m11,s11)`
- `i(s11,o1)`

This means that `m11` is ultimately grounded in ontology concept `o1` through `s11`.

---

## 6. Maps relation

The relation **maps** is written as:

- `m(x,y)`

Meaning:

- standard concept `x` maps to standard concept `y`

Example:

- `m(s11,s21)`

This expresses a mapping between two standard concepts, typically from different standards.

---

## 7. Alignment interpretation

Two model concepts are understood to **align** when the standard concepts they implement are appropriately connected.

Typical cases:

### Same implemented standard concept
- `i(m11,s11)`
- `i(m21,s11)`

### Different implemented standard concepts, but mapped
- `i(m11,s11)`
- `i(m21,s21)`
- `m(s11,s21)`

### Different implemented standard concepts, same ontology grounding
- `i(m11,s11)`
- `i(m21,s21)`
- `i(s11,o1)`
- `i(s21,o1)`

Whether shared ontology grounding alone is sufficient for alignment depends on the specific scenario and governance rule being analyzed.

---

## 8. Auxiliary annotations used in examples

Some examples also include shorthand annotations to summarize scenario outcomes or analysis results.

Examples:

- `candidate={m(s11,s31)}`
- `targets={s11,s21,s31}`
- `affected={m(s11i,s21), i(m11,s11i)}`
- `selected(s21)`
- `no_valid_target(m11)`
- `requires_new_mapping(m(s11,s21))`
- `aligns(m11,m21)`
- `flagged(i(m11,s11i))`

These are not core structural relations like `i(...)` and `m(...)`. They are auxiliary annotations used to describe the result of a scenario.

---

## 9. Example of a complete chain

\```text
O={o1}
S1={s11}
S2={s21}
M1={m11}
M2={m21}

i(s11,o1)
i(s21,o1)
i(m11,s11)
i(m21,s21)
m(s11,s21)
\```

This means:

- `s11` implements ontology concept `o1`
- `s21` implements ontology concept `o1`
- `m11` implements `s11`
- `m21` implements `s21`
- `s11` maps to `s21`

In this situation, `m11` and `m21` may align.

---

## 10. Summary

### Core symbols
- `O` = ontology
- `S1...SN` = standards
- `M1...MN` = models

### Core concept naming
- `o1...on` = ontology concepts
- `sij` = standard concepts
- `mij` = model concepts

### Core relations
- `i(x,y)` = `x` implements `y`
- `m(x,y)` = `x` maps to `y`

### Status suffixes
- no suffix = valid
- `i` = invalid