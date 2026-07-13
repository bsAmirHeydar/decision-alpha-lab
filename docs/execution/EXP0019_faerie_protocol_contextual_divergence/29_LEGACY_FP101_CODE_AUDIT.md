---
title: "29 - Legacy FP101 Code Audit"
tags: [exp0019, faerie-protocol, contextual-divergence, obsidian]
status: normative
experiment: EXP0019
context_id: FP-CONTEXT-001
context_version: 2.0.0-doc-freeze
doc_version: 2.0.0
last_updated: 2026-07-13
language: en
---
# 29 - Legacy FP101 Code Audit

## Purpose

Audit current code behavior against the v2 frozen contract and define retain/replace/retire actions.

## Scope

This document defines the Faerie Protocol context-layer behavior for its subject. It does not modify the stable intermarket divergence core. The shared core continues to own symbol-local references, touch/hunt facts, hunter/protected roles, closed-candle confirmation primitives, signal identity, deduplication, and ledger mechanics.

## Frozen Decisions Applied

- Owner-confirmed v2 policies supersede conflicting legacy code.

## Normative Invariants

1. **Legacy behavior is evidence, not authority.**
2. **Every retained function has a target module.**
3. **Known defects have tests before replacement.**
4. **Performance issues are addressed structurally.**

## Deterministic Procedure

```text
Inventory inputs/functions.
Map to requirement.
Classify MATCH/PARTIAL/CONFLICT/ABSENT.
Assign migration action.
Create regression fixture where useful.
```

## State and Evidence Requirements

| Field / Evidence | Requirement | Failure Behavior |
|---|---|---|
| `legacy_symbol` | Function/input/constant. | Required. |
| `classification` | MATCH/PARTIAL/CONFLICT/ABSENT. | Closed enum. |
| `target_module` | New owner. | Required for migration. |
| `test_case` | Regression or negative test. | Required for conflict. |

## Edge-Case Catalogue

### PERIOD_CURRENT used for range construction

Replace with M1 window aggregation; PERIOD_CURRENT only for confirmation.

### D0/K1 object naming collision

Replace with absolute window IDs.

### No WW implementation

Add dedicated weekly provider/gate/setup.

### Full rescan every timer

Replace with incremental cursors/cache.

### Hunter touch consumes globally

Replace with protected-touch side lifecycle.

## Executable Test Obligations

1. Compile original source fixture if environment permits.
2. Behavior capture for matching portions.
3. Defect reproduction tests.

## Implementation Guidance

- Do not edit legacy file in documentation phase.


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
