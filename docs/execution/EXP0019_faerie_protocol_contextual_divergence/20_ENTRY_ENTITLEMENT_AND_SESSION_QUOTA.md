---
title: "20 - Entry Entitlement and Pair-Session Quota"
tags: [exp0019, faerie-protocol, contextual-divergence, obsidian]
status: normative
experiment: EXP0019
context_id: FP-CONTEXT-001
context_version: 2.0.0-doc-freeze
doc_version: 2.0.0
last_updated: 2026-07-13
language: en
---
# 20 - Entry Entitlement and Pair-Session Quota

## Purpose

Define pair-global one-entry scope, first-signal ownership, reservation, and the remaining open consumption decision.

## Scope

This document defines the Faerie Protocol context-layer behavior for its subject. It does not modify the stable intermarket divergence core. The shared core continues to own symbol-local references, touch/hunt facts, hunter/protected roles, closed-candle confirmation primitives, signal identity, deduplication, and ledger mechanics.

## Frozen Decisions Applied

- Only one entry across both symbols and all relations in each A/L/N session.
- Earliest canonical M1 hunt wins.
- Permanent quota consumption moment is still open.

## Normative Invariants

1. **Quota key is context epoch + trading day + pair + session.**
2. **Raw signals are never deleted by quota.**
3. **Winner selection precedes live order attempt.**
4. **Tie-breaks are technical and versioned.**
5. **Reservation and permanent consumption are distinct states.**

## Deterministic Procedure

```text
Collect confirmed eligible candidates for session.
Sort by first_hunt_m1_time.
Apply stable tie-breaks.
Atomically reserve quota for winner.
Suppress later candidates with reason.
At configured consumption event, mark CONSUMED; on pre-consumption failure, RELEASE according to policy.
```

## State and Evidence Requirements

| Field / Evidence | Requirement | Failure Behavior |
|---|---|---|
| `quota_key` | context_epoch/trading_day/pair/session. | Required. |
| `quota_state` | AVAILABLE/RESERVED/CONSUMED/RELEASED. | Closed enum. |
| `winner_signal_id` | First eligible candidate. | Required after reservation. |
| `consumption_policy` | Open owner decision. | Live execution disabled if unset. |

## Edge-Case Catalogue

### Two signals same M1

Use confirmation close, relation-code order, direction enum, then signal ID as non-strategic tie-breaks.

### Winner fails geometry before send

Reservation release behavior depends on FP-DEC-012 profile.

### Order rejected by broker

Permanent consumption remains open policy.

### WW setup and lower setup compete

Both share same pair-session quota.

## Executable Test Obligations

1. Pair-global competition fixture.
2. Both-symbol competition fixture.
3. Same-M1 tie fixture.
4. Reservation atomicity fixture.
5. Each candidate remains in ledger.

## Implementation Guidance

- Build quota store as atomic compare-and-set service.
- Do not hard-code plan/attempt/accepted/fill until owner freezes Q12.


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
