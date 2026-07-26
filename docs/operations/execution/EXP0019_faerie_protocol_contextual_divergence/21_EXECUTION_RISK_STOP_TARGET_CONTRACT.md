---
title: "21 - Execution, Risk, Stop, and Target Contract"
tags: [exp0019, faerie-protocol, contextual-divergence, obsidian]
status: normative
experiment: EXP0019
context_id: FP-CONTEXT-001
context_version: 2.0.0-doc-freeze
doc_version: 2.0.0
last_updated: 2026-07-13
language: en
---
# 21 - Execution, Risk, Stop, and Target Contract

## Purpose

Define execution eligibility, protected-symbol trade mapping, SELL stop spread adjustment, risk sizing, and target behavior.

## Scope

This document defines the Faerie Protocol context-layer behavior for its subject. It does not modify the stable intermarket divergence core. The shared core continues to own symbol-local references, touch/hunt facts, hunter/protected roles, closed-candle confirmation primitives, signal identity, deduplication, and ledger mechanics.

## Frozen Decisions Applied

- WW can execute directly.
- SELL stop is raw structural stop plus exactly one spread.
- Pair-session first entry controls entitlement.

## Normative Invariants

1. **Risk is computed after spread-adjusted stop is finalized.**
2. **Spread snapshot source and timestamp are recorded.**
3. **Invalid broker geometry suppresses execution but not signal.**
4. **Lot sizing uses shared risk core.**

## Deterministic Procedure

```text
Resolve trade symbol and direction.
Build raw structural stop.
For SELL, add one spread snapshot.
Validate stop level and freeze distance.
Compute size from risk budget.
Build target/R multiple.
Submit only with quota entitlement.
```

## State and Evidence Requirements

| Field / Evidence | Requirement | Failure Behavior |
|---|---|---|
| `raw_stop` | Structural stop before spread. | Required. |
| `spread_snapshot` | Ask-bid or configured test model. | Required for SELL. |
| `adjusted_stop` | raw_stop + one spread for SELL. | Risk uses this. |
| `risk_amount` | Configured risk budget. | Reject non-positive. |
| `volume` | Shared risk output. | Validate broker steps. |

## Edge-Case Catalogue

### Spread unavailable

No live SELL order; reason `SPREAD_SNAPSHOT_UNAVAILABLE`.

### Spread widens between plan and send

Revalidate immediately before send; behavior must follow quota-consumption profile.

### Adjusted stop violates max distance

Suppress plan.

### Broker minimum stop distance

Apply explicit geometry validator, never silently move target/reference.

## Executable Test Obligations

1. BUY stop unchanged fixture.
2. SELL + one spread fixture.
3. Risk size uses adjusted distance.
4. Spread unavailable fixture.

## Implementation Guidance

- Use an FP stop-transform adapter feeding the existing execution/risk engine.


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
