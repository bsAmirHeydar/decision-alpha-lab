---
title: "05 - Shared Core Reuse Matrix"
tags: [exp0019, faerie-protocol, contextual-divergence, obsidian]
status: normative
experiment: EXP0019
context_id: FP-CONTEXT-001
context_version: 2.0.0-doc-freeze
doc_version: 2.0.0
last_updated: 2026-07-13
language: en
---
# 05 - Shared Core Reuse Matrix

## Purpose

Map each requirement to an existing stable module, an FP adapter, or a new context-specific component.

## Scope

This document defines the Faerie Protocol context-layer behavior for its subject. It does not modify the stable intermarket divergence core. The shared core continues to own symbol-local references, touch/hunt facts, hunter/protected roles, closed-candle confirmation primitives, signal identity, deduplication, and ledger mechanics.

## Frozen Decisions Applied

- Reuse is mandatory where behavior is already canonical.
- The FP layer owns calendar-day N selectors, WW recency, strict session-close policy, and first-entry arbitration.

## Normative Invariants

1. **No duplicated DST logic.**
2. **No duplicated signal hashing.**
3. **No duplicated risk sizing formula.**
4. **All extensions identify owner and test suite.**

## Deterministic Procedure

```text
Inventory requirement.
Find stable core capability.
Assess semantic fit.
Create adapter if fit is partial.
Create FP module only when context-specific.
Add compatibility test.
```

## State and Evidence Requirements

| Field / Evidence | Requirement | Failure Behavior |
|---|---|---|
| `requirement_id` | Stable FP requirement. | No untracked feature. |
| `owner_module` | Core or FP module. | Reject dual ownership. |
| `compatibility_test` | Test proving unchanged behavior. | No merge without test. |

## Edge-Case Catalogue

### Core API is close but not exact

Do not alter semantics through hidden flags; create explicit adapter.

### Core lacks M1 tie state

Extend generically with `SIMULTANEOUS_TOUCH` if reusable.

### Execution spread adjustment

Supply stop transformer to shared risk engine; do not fork lot sizing.

## Executable Test Obligations

1. Verify every requirement has one owner.
2. Verify all reused cores have compatibility tests.
3. Verify no circular dependency.

## Implementation Guidance

- Maintain matrix as a code-review checklist and architectural guard.


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
