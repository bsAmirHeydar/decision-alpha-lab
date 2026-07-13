---
title: "12 - NA, NL, and NN Cross-Day Relationships"
tags: [exp0019, faerie-protocol, contextual-divergence, obsidian]
status: normative
experiment: EXP0019
context_id: FP-CONTEXT-001
context_version: 2.0.0-doc-freeze
doc_version: 2.0.0
last_updated: 2026-07-13
language: en
---
# 12 - NA, NL, and NN Cross-Day Relationships

## Purpose

Specify historical N-reference selection using exact calendar-day offsets and current-day A/L/N check windows.

## Scope

This document defines the Faerie Protocol context-layer behavior for its subject. It does not modify the stable intermarket divergence core. The shared core continues to own symbol-local references, touch/hunt facts, hunter/protected roles, closed-candle confirmation primitives, signal identity, deduplication, and ledger mechanics.

## Frozen Decisions Applied

- Question 1 selected calendar-day depth.
- Question 2 permits reuse until protected touch.

## Normative Invariants

1. **Offset `d` means trading-day calendar key minus exactly `d` days.**
2. **Weekend/missing offsets occupy depth and are not replaced.**
3. **Each historical N interval is a distinct reference identity.**
4. **Reference high and low lifecycles are side-specific.**

## Deterministic Procedure

```text
For d=1..lookback, derive calendar date.
Build expected N interval.
Classify data complete/missing/partial.
If complete, register high and low sides.
Evaluate current A/L/N check windows.
Retain reference side until protected touch or expiry.
```

## State and Evidence Requirements

| Field / Evidence | Requirement | Failure Behavior |
|---|---|---|
| `calendar_offset` | Exact integer depth. | Reject zero/negative. |
| `expected_n_window_id` | Calendar-derived interval. | No compression. |
| `data_completeness` | COMPLETE/PARTIAL/MISSING/NON_TRADING. | Only COMPLETE eligible. |
| `side_consumed` | Per HIGH/LOW. | Do not consume opposite side. |

## Edge-Case Catalogue

### Weekend offset

Record non-trading/missing interval; do not fetch d+1 replacement.

### Partial N history

Do not form a valid reference side.

### Same reference triggers A then L

Allowed if protected side has not touched.

### Protected low consumed but high intact

Only low side is exhausted.

## Executable Test Obligations

1. Lookback with weekend fixture.
2. Missing-day no-backfill fixture.
3. Reuse across A/L/N fixture.
4. Side-specific consumption fixture.

## Implementation Guidance

- Selector should return both eligible references and explicit skipped-offset evidence.


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
