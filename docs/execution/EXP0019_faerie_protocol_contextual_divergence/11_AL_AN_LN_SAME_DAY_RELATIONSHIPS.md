---
title: "11 - AL, AN, and LN Same-Day Relationships"
tags: [exp0019, faerie-protocol, contextual-divergence, obsidian]
status: normative
experiment: EXP0019
context_id: FP-CONTEXT-001
context_version: 2.0.0-doc-freeze
doc_version: 2.0.0
last_updated: 2026-07-13
language: en
---
# 11 - AL, AN, and LN Same-Day Relationships

## Purpose

Specify same-trading-day reference-to-check relations and their deadlines.

## Scope

This document defines the Faerie Protocol context-layer behavior for its subject. It does not modify the stable intermarket divergence core. The shared core continues to own symbol-local references, touch/hunt facts, hunter/protected roles, closed-candle confirmation primitives, signal identity, deduplication, and ledger mechanics.

## Frozen Decisions Applied

- Strict same-session close applies to L and N check sessions.
- M1 is first-sweep authority.

## Normative Invariants

1. **AL uses completed/current A reference and L check.**
2. **AN uses A reference and N check.**
3. **LN uses L reference and N check.**
4. **References are symbol-local.**
5. **Confirmation cannot close after check-session end.**

## Deterministic Procedure

```text
Build reference at source-window completion.
Observe M1 in check window.
Create one-sided candidate.
Project to host chart timeframe.
Confirm before check end or expire.
```

## State and Evidence Requirements

| Field / Evidence | Requirement | Failure Behavior |
|---|---|---|
| `reference_window_id` | Same trading-day source interval. | Block absent. |
| `check_window_id` | Same trading-day target interval. | Block absent. |
| `candidate_first_hunt_m1` | Earliest one-sided touch. | No tick override. |
| `confirmation_close` | Host chart close inside session. | Expire otherwise. |

## Edge-Case Catalogue

### A reference incomplete at L open

Mark relation `REFERENCE_INCOMPLETE`.

### Both symbols hunt in same M1

Symmetric touch; no divergence candidate.

### Second symbol hunts before confirmation

Cancel candidate.

### Second symbol hunts after confirmation

Preserve signal; consume future side state per lifecycle.

## Executable Test Obligations

1. Golden bullish and bearish case for each relation.
2. Same-minute symmetric touch case.
3. Boundary-close rejection case.

## Implementation Guidance

- Share one generic relation evaluator parameterized by registry descriptor.


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
