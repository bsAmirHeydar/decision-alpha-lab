---
title: "09 - Symbol Pair and Role Model"
tags: [exp0019, faerie-protocol, contextual-divergence, obsidian]
status: normative
experiment: EXP0019
context_id: FP-CONTEXT-001
context_version: 2.0.0-doc-freeze
doc_version: 2.0.0
last_updated: 2026-07-13
language: en
---
# 09 - Symbol Pair and Role Model

## Purpose

Define two-symbol pair identity, symbol-local references, hunter/protected roles, and trade-symbol selection.

## Scope

This document defines the Faerie Protocol context-layer behavior for its subject. It does not modify the stable intermarket divergence core. The shared core continues to own symbol-local references, touch/hunt facts, hunter/protected roles, closed-candle confirmation primitives, signal identity, deduplication, and ledger mechanics.

## Frozen Decisions Applied

- The quota is pair-global across both symbols.
- The first eligible setup across either symbol wins the session.

## Normative Invariants

1. **Each symbol compares only to its own reference.**
2. **Hunter is the symbol that touches first; protected is the other symbol while its corresponding side remains untouched.**
3. **Roles are side- and event-specific.**
4. **Pair order is canonical for identity but does not imply preferred trading symbol.**

## Deterministic Procedure

```text
Load pair descriptor.
Build local reference for each symbol.
Detect first one-sided touch.
Assign roles.
Confirm divergence.
Resolve trade-symbol policy from protected/hunter doctrine.
```

## State and Evidence Requirements

| Field / Evidence | Requirement | Failure Behavior |
|---|---|---|
| `pair_id` | Canonical sorted or configured pair identity. | Reject duplicate symbols. |
| `hunter_symbol` | One member of pair. | Block unknown. |
| `protected_symbol` | The other member. | Block same as hunter. |
| `side` | HIGH/LOW. | Reject unset. |

## Edge-Case Catalogue

### Both touch same M1

No hunter/protected ordering exists.

### One symbol data missing

Pair observation is incomplete.

### Symbols have different point/tick sizes

Normalize comparisons symbol-locally; never compare raw prices across symbols.

## Executable Test Obligations

1. Swap display order and prove pair identity policy is stable.
2. Verify local references are never crossed between symbols.
3. Verify quota spans both symbols.

## Implementation Guidance

- Keep role assignment in shared divergence result; FP consumes it.


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
