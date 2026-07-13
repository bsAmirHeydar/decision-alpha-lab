---
title: "32 - Test Strategy and Golden Cases"
tags: [exp0019, faerie-protocol, contextual-divergence, obsidian]
status: normative
experiment: EXP0019
context_id: FP-CONTEXT-001
context_version: 2.0.0-doc-freeze
doc_version: 2.0.0
last_updated: 2026-07-13
language: en
---
# 32 - Test Strategy and Golden Cases

## Purpose

Define unit, contract, integration, replay, negative, differential, performance, and model-checking obligations.

## Scope

This document defines the Faerie Protocol context-layer behavior for its subject. It does not modify the stable intermarket divergence core. The shared core continues to own symbol-local references, touch/hunt facts, hunter/protected roles, closed-candle confirmation primitives, signal identity, deduplication, and ledger mechanics.

## Frozen Decisions Applied

- All fourteen frozen decisions require direct tests.
- Q12 requires tests for each selectable consumption profile but no owner-canonical assertion yet.

## Normative Invariants

1. **Tests use deterministic fixtures.**
2. **Live and historical M1 outcomes must match.**
3. **Suppressed events remain visible and ledgered.**
4. **Previous divergence contexts must not regress.**

## Deterministic Procedure

```text
Build synthetic M1 pair streams.
Generate A/L/N/W windows.
Exercise relation and policy modules.
Assert event sequences and hashes.
Replay after restart.
Compare outputs.
```

## State and Evidence Requirements

| Field / Evidence | Requirement | Failure Behavior |
|---|---|---|
| `fixture_id` | Stable test fixture. | Required. |
| `expected_event_hash` | Golden output identity. | Review on change. |
| `decision_ids` | Rules covered. | Coverage matrix. |
| `mode` | historical/live-replay/paper. | Required. |

## Edge-Case Catalogue

### Same-M1 dual touch

No ordered first sweep.

### Confirmation boundary

Reject close at/after end.

### Opposite WW

Newest active wins.

### Calendar weekend

No compressed lookback.

### Two simultaneous setups

Earliest hunt wins, stable tie-break.

### SELL execution

Stop includes one spread and volume recalculates.

## Executable Test Obligations

1. One golden per relation/direction.
2. One negative per invariant.
3. Property tests for identity and lifecycle.
4. Performance benchmark.
5. Legacy regression tests.

## Implementation Guidance

- Maintain a decision-to-test matrix and refuse code-ready status if any owner decision lacks a test.


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
