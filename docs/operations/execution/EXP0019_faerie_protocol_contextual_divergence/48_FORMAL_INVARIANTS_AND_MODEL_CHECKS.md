---
title: "48 - Formal Invariants and Model Checks"
tags: [exp0019, faerie-protocol, contextual-divergence, obsidian]
status: normative
experiment: EXP0019
context_id: FP-CONTEXT-001
context_version: 2.0.0-doc-freeze
doc_version: 2.0.0
last_updated: 2026-07-13
language: en
---
# 48 - Formal Invariants and Model Checks

## Invariant Register

| ID | Invariant |
|---|---|
| `INV-001` | A reference price is symbol-local and immutable after completion. |
| `INV-002` | A signal never compares symbol A price to symbol B reference. |
| `INV-003` | First-sweep ordering is derived from M1 only. |
| `INV-004` | Two contacts in the same M1 cannot be ordered. |
| `INV-005` | A candidate cannot confirm at or after its check-session end. |
| `INV-006` | A historical N selector never substitutes an older valid session for a missing calendar offset. |
| `INV-007` | Hunter touch alone does not consume a reference globally. |
| `INV-008` | Protected touch consumes only the corresponding reference side for future candidates. |
| `INV-009` | A confirmed event is never deleted by later neutralization, suppression, or consumption. |
| `INV-010` | No active WW with complete data permits both directions. |
| `INV-011` | WW data incomplete is not equivalent to no active WW. |
| `INV-012` | The newest confirmed active WW is the sole directional gate. |
| `INV-013` | At most one quota winner exists per context/trading-day/pair/session key. |
| `INV-014` | The quota winner has the minimum first_hunt_m1_time among eligible contenders. |
| `INV-015` | Every suppressed signal remains in ledger and visual projection. |
| `INV-016` | SELL adjusted stop equals raw stop plus exactly one spread snapshot. |
| `INV-017` | Risk sizing uses adjusted stop distance. |
| `INV-018` | Live execution is disabled while quota consumption policy is UNSET. |
| `INV-019` | Changing resolved confirmation timeframe changes context epoch. |
| `INV-020` | Restart/replay of the same inputs produces identical IDs and state. |


## Model-Checking Targets

### Candidate Machine

Forbidden states:

- confirmed after deadline,
- confirmed after second touch before close,
- transferred to a new session,
- confirmed without complete data.

### Reference Machine

Forbidden states:

- consumed by hunter touch,
- high and low consumed together without separate events,
- immutable price changed in same data revision.

### WW Machine

Forbidden states:

- neutralized event remains active,
- incomplete weekly data resolves to BOTH,
- older event controls while newer active confirmed event exists.

### Quota Machine

Forbidden states:

- two RESERVED/CONSUMED winners for one key,
- later-hunt candidate wins while earlier eligible candidate exists,
- live CONSUMED transition occurs with policy UNSET.

## Property-Based Testing

Generate random but valid M1 event sequences, replay in different batching and symbol-arrival orders, and assert invariant preservation plus identical final ledger/state hashes.

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
