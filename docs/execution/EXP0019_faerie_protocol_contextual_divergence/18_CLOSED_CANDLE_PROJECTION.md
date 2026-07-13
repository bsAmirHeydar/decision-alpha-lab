---
title: "18 - Closed-Candle Projection"
tags: [exp0019, faerie-protocol, contextual-divergence, obsidian]
status: normative
experiment: EXP0019
context_id: FP-CONTEXT-001
context_version: 2.0.0-doc-freeze
doc_version: 2.0.0
last_updated: 2026-07-13
language: en
---
# 18 - Closed-Candle Projection

## Purpose

Specify how M1 candidate facts are projected onto the current chart timeframe without changing M1 ordering.

## Scope

This document defines the Faerie Protocol context-layer behavior for its subject. It does not modify the stable intermarket divergence core. The shared core continues to own symbol-local references, touch/hunt facts, hunter/protected roles, closed-candle confirmation primitives, signal identity, deduplication, and ledger mechanics.

## Frozen Decisions Applied

- Host chart timeframe is owner-confirmed.
- M1 remains first-sweep authority.

## Normative Invariants

1. **Projection never changes hunt timestamp.**
2. **Only a fully closed chart candle can confirm.**
3. **Projection includes exact constituent M1 evidence.**
4. **Session deadline is checked against candle close.**

## Deterministic Procedure

```text
Resolve chart timeframe at init.
Map candidate time to chart bar.
Determine first eligible closed bar.
Collect constituent M1 coverage.
At close, re-evaluate confirmation predicate.
```

## State and Evidence Requirements

| Field / Evidence | Requirement | Failure Behavior |
|---|---|---|
| `chart_bar_id` | Symbol/timeframe/open time. | Required. |
| `bar_close_utc` | Actual close instant. | Deadline check. |
| `constituent_m1_hash` | Coverage lineage. | Block incomplete. |
| `projection_version` | Mapping algorithm version. | Identity-bearing. |

## Edge-Case Catalogue

### Non-divisible broker bar alignment

Use actual bar open/close timestamps, not arithmetic assumptions.

### Chart timeframe larger than session remainder

Candidate expires.

### Missing constituent M1

Confirmation data incomplete.

### Chart timeframe changed

New context epoch.

## Executable Test Obligations

1. M5/M15/H1 fixtures.
2. Boundary-crossing bar fixture.
3. Missing M1 constituent fixture.

## Implementation Guidance

- Projection is a shared confirmation adapter; FP supplies strict deadline policy.


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
