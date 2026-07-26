---
title: "36 - Traceability Matrix"
tags: [exp0019, faerie-protocol, contextual-divergence, obsidian]
status: normative
experiment: EXP0019
context_id: FP-CONTEXT-001
context_version: 2.0.0-doc-freeze
doc_version: 2.0.0
last_updated: 2026-07-13
language: en
---
# 36 - Traceability Matrix

## Purpose

Link source statements, owner decisions, canonical requirements, modules, contracts, tests, and visual evidence.

## Scope

This document defines the Faerie Protocol context-layer behavior for its subject. It does not modify the stable intermarket divergence core. The shared core continues to own symbol-local references, touch/hunt facts, hunter/protected roles, closed-candle confirmation primitives, signal identity, deduplication, and ledger mechanics.

## Frozen Decisions Applied

- Every frozen decision maps to at least one requirement and test.

## Normative Invariants

1. **Traceability is many-to-many but explicit.**
2. **No requirement exists only in prose.**
3. **Open decisions map to blocking gates.**
4. **Legacy conflicts remain linked.**

## Deterministic Procedure

```text
Assign requirement IDs.
Link source/decision.
Link module and contract.
Link test and reason code.
Audit for orphans.
```

## State and Evidence Requirements

| Field / Evidence | Requirement | Failure Behavior |
|---|---|---|
| `requirement_id` | FP-REQ-xxx. | Required. |
| `decision_id` | Optional when not decision-driven. | Link when applicable. |
| `module_id` | Implementation owner. | Required before coding. |
| `test_id` | Verification. | Required for normative rule. |

## Edge-Case Catalogue

### Requirement without test

Not code-ready.

### Test without requirement

Classify as regression/quality test.

### Decision changes

Increment decision-set version and affected identities.

### Source conflict

Record precedence outcome.

## Executable Test Obligations

1. Orphan scan.
2. 15-decision coverage.
3. Relation coverage.
4. Reason-code coverage.

## Implementation Guidance

- Machine matrix is stored in CSV beside source audit.


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
