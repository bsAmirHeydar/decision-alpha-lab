---
title: "15 - Hunt, Touch, and First-Sweep Contract"
tags: [exp0019, faerie-protocol, contextual-divergence, obsidian]
status: normative
experiment: EXP0019
context_id: FP-CONTEXT-001
context_version: 2.0.0-doc-freeze
doc_version: 2.0.0
last_updated: 2026-07-13
language: en
---
# 15 - Hunt, Touch, and First-Sweep Contract

## Purpose

Define touch semantics and canonical ordering under the owner-selected M1-only authority.

## Scope

This document defines the Faerie Protocol context-layer behavior for its subject. It does not modify the stable intermarket divergence core. The shared core continues to own symbol-local references, touch/hunt facts, hunter/protected roles, closed-candle confirmation primitives, signal identity, deduplication, and ledger mechanics.

## Frozen Decisions Applied

- M1 only controls first sweep in historical and live modes.
- Tick timestamps cannot break an M1 tie.

## Normative Invariants

1. **High hunt occurs when M1 high >= reference high.**
2. **Low hunt occurs when M1 low <= reference low.**
3. **Equality counts.**
4. **Only the first M1 timestamp of contact is canonical.**
5. **Dual contact in the same M1 is symmetric/ambiguous, not ordered divergence.**

## Deterministic Procedure

```text
For each symbol and side, scan M1 chronologically.
Record first contact minute.
Compare pair contact states.
If exactly one contacted, create candidate.
If both contact in same minute, record symmetric touch.
If second contacts later, cancel/neutralize according to state.
```

## State and Evidence Requirements

| Field / Evidence | Requirement | Failure Behavior |
|---|---|---|
| `first_hunt_m1_time` | Bar-open or canonical M1 timestamp. | Required for ordering. |
| `touch_kind` | EQUALITY/CROSS/GAP. | Optional descriptive evidence. |
| `symmetric_same_m1` | Boolean. | Prevents first-signal claim. |
| `source_bar_id` | Exact M1 bar. | Block absent. |

## Edge-Case Catalogue

### Tick says A first but same M1 bar shows both

Ignore tick ordering; canonical result is symmetric.

### Gap opens through level

The opening M1 high/low crossing counts as hunt.

### M1 missing for one symbol

No pair ordering can be established.

### Multiple contacts after first

Do not change first-hunt timestamp.

## Executable Test Obligations

1. Equality test.
2. Gap-cross test.
3. Same-M1 dual touch test.
4. Live replay parity without tick ordering.

## Implementation Guidance

- Ticks may be logged as non-authoritative diagnostics only if clearly separated.


## Authority Classification

| Classification | Meaning |
|---|---|
| `OWNER_CONFIRMED` | Explicitly selected by the owner in the 15-question decision response. |
| `SOURCE_CONFIRMED` | Directly present in the original Faerie Protocol source package or owner narrative. |
| `ARCHITECTURAL_DERIVATION` | Required to make the confirmed behavior deterministic, modular, testable, or compatible with shared cores. |
| `LEGACY_OBSERVATION` | Behavior observed in `FP 101.mq5`; not automatically canonical. |
| `OPEN_DECISION` | Must not be silently hard-coded. |

Canonical priority is: `OWNER_CONFIRMED` > `SOURCE_CONFIRMED` > reviewed `ARCHITECTURAL_DERIVATION` > `LEGACY_OBSERVATION`.


## Navigation

- [[00_EXP0019_MOC|EXP0019 Master MOC]]
- [[38_OWNER_DECISION_FREEZE_V2|Owner Decision Freeze v2]]
- [[33_AMBIGUITY_AND_DECISION_REGISTER|Decision Register]]
- [[40_NORMATIVE_ALGORITHM_SPECIFICATION|Normative Algorithm Specification]]
- [[44_ACCEPTANCE_GATE_FOR_CODING|Acceptance Gate for Coding]]
