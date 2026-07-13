---
title: "28 - Existing Module Adapter Plan"
tags: [exp0019, faerie-protocol, contextual-divergence, obsidian]
status: normative
experiment: EXP0019
context_id: FP-CONTEXT-001
context_version: 2.0.0-doc-freeze
doc_version: 2.0.0
last_updated: 2026-07-13
language: en
---
# 28 - Existing Module Adapter Plan

## Purpose

Describe how EXP0019 integrates with CGT/CGR/CGH/CGD/CGV/CGX or their current successors without semantic duplication.

## Scope

This document defines the Faerie Protocol context-layer behavior for its subject. It does not modify the stable intermarket divergence core. The shared core continues to own symbol-local references, touch/hunt facts, hunter/protected roles, closed-candle confirmation primitives, signal identity, deduplication, and ledger mechanics.

## Frozen Decisions Applied

- FP context wraps fixed cores rather than modifying their context-independent logic.

## Normative Invariants

1. **Adapters translate contracts only.**
2. **Core outputs remain independently testable.**
3. **Context policy versions are explicit.**
4. **Any core change requires regression tests for previous divergence contexts.**

## Deterministic Procedure

```text
Map existing API.
Document semantic differences.
Implement adapter.
Run old-context compatibility suite.
Run FP golden suite.
```

## State and Evidence Requirements

| Field / Evidence | Requirement | Failure Behavior |
|---|---|---|
| `adapter_id` | Stable name/version. | Required. |
| `source_core` | Exact module/version. | Required. |
| `semantic_delta` | Documented mapping. | No hidden delta. |
| `regression_suite` | Affected contexts. | Must pass. |

## Edge-Case Catalogue

### Existing core uses tick ordering

Configure/extend M1 authority generically; do not bypass FP policy.

### Core confirmation permits boundary crossing

FP adapter applies stricter deadline.

### Core consumption is first-touch global

FP side lifecycle adapter overrides only context policy state.

### Visual core hides suppressed

Add explicit always-visible projection mode.

## Executable Test Obligations

1. Old-context regression.
2. Adapter contract test.
3. No duplicate implementation scan.

## Implementation Guidance

- Keep adapter code thin and declarative.


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
