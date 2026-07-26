---
title: "17 - Divergence Candidate, Confirmation, and Invalidation"
tags: [exp0019, faerie-protocol, contextual-divergence, obsidian]
status: normative
experiment: EXP0019
context_id: FP-CONTEXT-001
context_version: 2.0.0-doc-freeze
doc_version: 2.0.0
last_updated: 2026-07-13
language: en
---
# 17 - Divergence Candidate, Confirmation, and Invalidation

## Purpose

Define candidate creation, host-chart projection, strict session deadline, cancellation, confirmation, and post-confirmation state.

## Scope

This document defines the Faerie Protocol context-layer behavior for its subject. It does not modify the stable intermarket divergence core. The shared core continues to own symbol-local references, touch/hunt facts, hunter/protected roles, closed-candle confirmation primitives, signal identity, deduplication, and ledger mechanics.

## Frozen Decisions Applied

- Confirmation timeframe is current chart timeframe resolved at initialization.
- Confirmation close must be inside the owning A/L/N session.

## Normative Invariants

1. **Candidate begins at first one-sided M1 hunt.**
2. **Second-symbol touch before confirmation cancels candidate.**
3. **A candidate cannot migrate sessions.**
4. **Confirmed signal is immutable evidence.**

## Deterministic Procedure

```text
Create candidate from M1 asymmetry.
Find host-chart candle containing/after candidate according to projection rule.
Wait for close.
Check close time < session end.
Revalidate asymmetry and data.
Confirm or cancel/expire.
```

## State and Evidence Requirements

| Field / Evidence | Requirement | Failure Behavior |
|---|---|---|
| `candidate_id` | Raw one-sided event identity. | Required. |
| `owner_session_id` | Check session that owns candidate. | Immutable. |
| `confirmation_tf` | Resolved host chart timeframe. | Identity-bearing. |
| `deadline_utc` | Session end. | Expire after. |

## Edge-Case Catalogue

### Timeframe change before close

EA reinitialization creates new context epoch; prior candidate handling must be explicit and ledgered.

### Candle closes exactly at session end

Reject as out-of-session.

### Second touch in confirmation candle

If M1 evidence shows second touch before close, cancel.

### No candle close before deadline

Expire `CONFIRMATION_DEADLINE_MISSED`.

## Executable Test Obligations

1. Strict boundary fixture.
2. Timeframe variants.
3. Second-touch-before-close fixture.
4. No-close-before-deadline fixture.

## Implementation Guidance

- Do not use `PERIOD_CURRENT` dynamically after initialization; store resolved enum.


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
