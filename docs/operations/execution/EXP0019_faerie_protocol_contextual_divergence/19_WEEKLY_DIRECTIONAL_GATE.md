---
title: "19 - Weekly Directional Gate"
tags: [exp0019, faerie-protocol, contextual-divergence, obsidian]
status: normative
experiment: EXP0019
context_id: FP-CONTEXT-001
context_version: 2.0.0-doc-freeze
doc_version: 2.0.0
last_updated: 2026-07-13
language: en
---
# 19 - Weekly Directional Gate

## Purpose

Resolve the active WW context and apply it to lower-relation execution eligibility without deleting raw signals.

## Scope

This document defines the Faerie Protocol context-layer behavior for its subject. It does not modify the stable intermarket divergence core. The shared core continues to own symbol-local references, touch/hunt facts, hunter/protected roles, closed-candle confirmation primitives, signal identity, deduplication, and ledger mechanics.

## Frozen Decisions Applied

- No active WW with valid data allows both directions.
- Newest active confirmed WW wins.
- Suppressed signals remain visible.

## Normative Invariants

1. **Only CONFIRMED and non-NEUTRALIZED WW events are gate candidates.**
2. **Recency uses confirmation time then stable tie-breaks.**
3. **Bullish gate allows bullish lower setups and suppresses bearish; bearish gate does the inverse.**
4. **WW_DATA_INCOMPLETE is not WW_NONE.**

## Deterministic Procedure

```text
Load active WW events.
Discard neutralized/expired.
Sort by confirmation time descending.
Select newest active.
If none and data valid -> ALLOW_BOTH.
If data incomplete -> block execution with reason.
Apply gate to lower relation and direct WW setup.
```

## State and Evidence Requirements

| Field / Evidence | Requirement | Failure Behavior |
|---|---|---|
| `active_ww_signal_id` | Selected gate event. | Null only for valid no-context. |
| `gate_direction` | BULLISH/BEARISH/BOTH/BLOCKED_DATA. | Closed enum. |
| `resolution_time` | When gate computed. | Audit. |
| `suppression_reason` | WW_DIRECTION_MISMATCH or data reason. | Required when blocked. |

## Edge-Case Catalogue

### Newest WW neutralizes

Recompute from remaining active events.

### Opposite WW same confirmation time

Use first-hunt time then signal ID tie-break.

### No WW because no asymmetry

Allow both.

### No WW because missing week data

Block execution, draw reason-coded signals.

## Executable Test Obligations

1. No-WW allow-both fixture.
2. Newest-wins fixture.
3. Neutralization fallback fixture.
4. Missing-data fail-closed fixture.

## Implementation Guidance

- Implement resolver as pure function over append-only WW ledger.


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
