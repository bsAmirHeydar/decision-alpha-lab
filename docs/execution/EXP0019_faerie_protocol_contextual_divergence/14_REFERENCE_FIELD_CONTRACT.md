---
title: "14 - Reference Field Contract"
tags: [exp0019, faerie-protocol, contextual-divergence, obsidian]
status: normative
experiment: EXP0019
context_id: FP-CONTEXT-001
context_version: 2.0.0-doc-freeze
doc_version: 2.0.0
last_updated: 2026-07-13
language: en
---
# 14 - Reference Field Contract

## Purpose

Define immutable symbol-local reference windows, sides, completeness, freshness, and lineage.

## Scope

This document defines the Faerie Protocol context-layer behavior for its subject. It does not modify the stable intermarket divergence core. The shared core continues to own symbol-local references, touch/hunt facts, hunter/protected roles, closed-candle confirmation primitives, signal identity, deduplication, and ledger mechanics.

## Frozen Decisions Applied

- Calendar-day selection and protected-touch consumption are owner-confirmed.

## Normative Invariants

1. **A reference belongs to one symbol and one interval.**
2. **High and low sides have independent lifecycle state.**
3. **Reference price is immutable after source window completion.**
4. **Incomplete source windows cannot produce canonical references.**

## Deterministic Procedure

```text
Aggregate M1 source interval.
Validate coverage.
Freeze high/low with bar provenance.
Create side lifecycle records.
Expose read-only reference to detector.
```

## State and Evidence Requirements

| Field / Evidence | Requirement | Failure Behavior |
|---|---|---|
| `reference_id` | Hash of symbol, interval, side, data revision. | Reject collision. |
| `price` | Symbol-native price. | Reject non-finite. |
| `source_bar_ids` | M1 provenance. | Block absent. |
| `coverage_state` | Complete or explicit failure. | No eligible reference otherwise. |

## Edge-Case Catalogue

### Late historical data repair

Create new data revision and context epoch; do not silently mutate prior ledger.

### Equal high/low flat window

Valid only if coverage rules pass; touch semantics remain equality.

### Corporate symbol rollover

New symbol mapping/version required.

## Executable Test Obligations

1. Immutable price test.
2. Side identity test.
3. Coverage failure test.
4. Data revision identity change test.

## Implementation Guidance

- Reuse shared reference store with FP interval providers.


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
