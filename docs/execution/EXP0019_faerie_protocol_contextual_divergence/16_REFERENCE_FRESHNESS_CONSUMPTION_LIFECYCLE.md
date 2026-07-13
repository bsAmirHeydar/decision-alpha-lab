---
title: "16 - Reference Freshness and Consumption Lifecycle"
tags: [exp0019, faerie-protocol, contextual-divergence, obsidian]
status: normative
experiment: EXP0019
context_id: FP-CONTEXT-001
context_version: 2.0.0-doc-freeze
doc_version: 2.0.0
last_updated: 2026-07-13
language: en
---
# 16 - Reference Freshness and Consumption Lifecycle

## Purpose

Define when a reference side is eligible, reused, consumed, expired, or superseded.

## Scope

This document defines the Faerie Protocol context-layer behavior for its subject. It does not modify the stable intermarket divergence core. The shared core continues to own symbol-local references, touch/hunt facts, hunter/protected roles, closed-candle confirmation primitives, signal identity, deduplication, and ledger mechanics.

## Frozen Decisions Applied

- Reuse continues until protected-symbol touch.
- Hunter touch does not globally consume the reference.

## Normative Invariants

1. **Lifecycle is per symbol-reference-side.**
2. **Confirmed signals survive later consumption.**
3. **Consumption blocks future candidates only.**
4. **Expiry and consumption are distinct reasons.**

## Deterministic Procedure

```text
Create FRESH side.
Hunter touches -> HUNTER_SEEN but side remains reusable.
Protected touches -> CONSUMED_BY_PROTECTED_TOUCH.
Window policy expires -> EXPIRED.
Data revision -> SUPERSEDED.
```

## State and Evidence Requirements

| Field / Evidence | Requirement | Failure Behavior |
|---|---|---|
| `lifecycle_state` | FRESH/HUNTER_SEEN/CONSUMED/EXPIRED/SUPERSEDED. | Reject unknown. |
| `consumed_time` | Protected touch M1 time. | Required when consumed. |
| `consumed_by_symbol` | Protected symbol. | Must match role. |
| `side` | HIGH/LOW. | Independent lifecycle. |

## Edge-Case Catalogue

### Protected touch occurs in later session

All future relations using that side become ineligible.

### High consumed, low untouched

Low remains reusable.

### Multiple hunter events before protected touch

May form distinct relation/check-window signals with distinct IDs.

### Historical signal rebuild after consumption

Reconstruct using event time; do not retroactively suppress confirmed history.

## Executable Test Obligations

1. Cross-stage reuse test.
2. Protected-touch stop test.
3. Side independence test.
4. Historical immutability test.

## Implementation Guidance

- Implement lifecycle as append-only events plus derived current state.


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
