---
title: "24 - State Machines"
tags: [exp0019, faerie-protocol, contextual-divergence, obsidian]
status: normative
experiment: EXP0019
context_id: FP-CONTEXT-001
context_version: 2.0.0-doc-freeze
doc_version: 2.0.0
last_updated: 2026-07-13
language: en
---
# 24 - State Machines

## Purpose

Formalize reference, candidate, WW, quota, and execution-plan transitions.

## Scope

This document defines the Faerie Protocol context-layer behavior for its subject. It does not modify the stable intermarket divergence core. The shared core continues to own symbol-local references, touch/hunt facts, hunter/protected roles, closed-candle confirmation primitives, signal identity, deduplication, and ledger mechanics.

## Frozen Decisions Applied

- Second-symbol weekly touch neutralizes WW.
- Strict same-session close expires candidates.
- Quota permanent consumption remains open.

## Normative Invariants

1. **Transitions are explicit and reason-coded.**
2. **Terminal evidence is immutable.**
3. **Invalid transitions fail closed.**
4. **Derived current state comes from append-only events.**

## Deterministic Procedure

```text
Validate current state.
Validate event preconditions.
Append transition event.
Recompute derived state.
Emit telemetry.
```

## State and Evidence Requirements

| Field / Evidence | Requirement | Failure Behavior |
|---|---|---|
| `entity_id` | Reference/candidate/WW/quota/plan ID. | Required. |
| `from_state` | Expected current state. | Mismatch rejects event. |
| `to_state` | Allowed next state. | Closed transition table. |
| `reason_code` | Causal reason. | Required. |

## Edge-Case Catalogue

### Duplicate transition event

Deduplicate by event ID.

### Out-of-order historical event

Rebuild by canonical event time and sequence policy.

### State version mismatch

Reject or migrate explicitly.

### Open quota policy

Allow AVAILABLE->RESERVED; block ambiguous permanent transition in live profile.

## Executable Test Obligations

1. Model-check all transitions.
2. Reject impossible transition fixtures.
3. Replay event log to same state.

## Implementation Guidance

- Generate transition tables from machine-readable contract where possible.


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
