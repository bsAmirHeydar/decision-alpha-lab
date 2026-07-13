---
title: "31 - Data Gaps, Expiry, Weekends, and Calendar-Day Depth"
tags: [exp0019, faerie-protocol, contextual-divergence, obsidian]
status: normative
experiment: EXP0019
context_id: FP-CONTEXT-001
context_version: 2.0.0-doc-freeze
doc_version: 2.0.0
last_updated: 2026-07-13
language: en
---
# 31 - Data Gaps, Expiry, Weekends, and Calendar-Day Depth

## Purpose

Define the consequences of the owner-selected calendar-day lookback and all incomplete-data states.

## Scope

This document defines the Faerie Protocol context-layer behavior for its subject. It does not modify the stable intermarket divergence core. The shared core continues to own symbol-local references, touch/hunt facts, hunter/protected roles, closed-candle confirmation primitives, signal identity, deduplication, and ledger mechanics.

## Frozen Decisions Applied

- Weekends and missing days consume lookback offsets.
- They are not replaced by older valid N sessions.

## Normative Invariants

1. **`NO_SIGNAL` requires complete evaluable data.**
2. **Missing/partial/non-trading offsets are distinct evidence.**
3. **A missing historical offset cannot create a reference.**
4. **Data gaps block only affected relations unless a required gate is unavailable.**

## Deterministic Procedure

```text
For each calendar offset, derive expected interval.
Inspect market calendar/data coverage.
Classify state.
Create reference only when complete.
Record skipped offset.
Continue to next fixed offset without depth compensation.
```

## State and Evidence Requirements

| Field / Evidence | Requirement | Failure Behavior |
|---|---|---|
| `offset_date` | Exact calendar date. | Required. |
| `coverage_ratio` | Expected versus observed M1. | Threshold versioned. |
| `gap_reason` | WEEKEND/HOLIDAY/MISSING/PARTIAL. | Closed enum. |
| `eligible_reference` | Boolean derived. | False unless complete. |

## Edge-Case Catalogue

### Lookback=3 across weekend

Offsets remain Friday/Saturday/Sunday or exact date sequence according to current day; no fourth-day replacement.

### Holiday with no bars

Classify NON_TRADING or MISSING per calendar source.

### Partial bars

PARTIAL, no reference.

### Weekly data incomplete

WW gate becomes BLOCKED_DATA, not no-context.

## Executable Test Obligations

1. Weekend lookback fixtures.
2. Holiday fixture.
3. Partial coverage fixture.
4. No backfill compensation test.

## Implementation Guidance

- Maintain explicit market-calendar policy; do not infer holiday from absence alone if a calendar source exists.


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
