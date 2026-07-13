---
title: "03 - Canonical Strategy Doctrine"
tags: [exp0019, faerie-protocol, contextual-divergence, obsidian]
status: normative
experiment: EXP0019
context_id: FP-CONTEXT-001
context_version: 2.0.0-doc-freeze
doc_version: 2.0.0
last_updated: 2026-07-13
language: en
---
# 03 - Canonical Strategy Doctrine

## Purpose

Define the immutable principles that all Faerie Protocol modules must follow.

## Scope

This document defines the Faerie Protocol context-layer behavior for its subject. It does not modify the stable intermarket divergence core. The shared core continues to own symbol-local references, touch/hunt facts, hunter/protected roles, closed-candle confirmation primitives, signal identity, deduplication, and ledger mechanics.

## Frozen Decisions Applied

- Calendar-day depth, strict same-session confirmation, M1 first-sweep authority, and pair-global first-entry arbitration are owner-confirmed.
- WW is both a gate and a tradeable setup.

## Normative Invariants

1. **Each symbol hunts only its own reference.**
2. **Touch, equality, and cross qualify as hunt.**
3. **Hunter and protected roles are symbol-local facts.**
4. **Confirmed history is immutable evidence even after later neutralization.**
5. **Suppression changes eligibility and style, never raw detection existence.**
6. **Context rules do not alter the shared detector core.**

## Deterministic Procedure

```text
Observe symbol-local windows.
Build reference sides.
Detect one-sided M1 hunt.
Create candidate.
Require closed candle inside owning session.
Confirm or expire.
Apply WW and quota policies.
Preserve all outcomes in ledger.
```

## State and Evidence Requirements

| Field / Evidence | Requirement | Failure Behavior |
|---|---|---|
| `context_epoch_id` | Hash of all behavior-bearing configuration. | Do not mix signals across epochs. |
| `raw_detection_id` | Identity before policy gates. | Never delete on suppression. |
| `eligibility_state` | Reason-coded policy result. | Block order if unknown. |

## Edge-Case Catalogue

### Both symbols hunt same side in same M1

No ordered divergence exists; record symmetric touch.

### Protected symbol hunts after confirmation

Consume future reference side; preserve confirmed event.

### Current chart timeframe changes

Create a new configuration epoch and signal namespace.

## Executable Test Obligations

1. Prove detector output is unchanged by WW/quota modules.
2. Prove suppressed raw signals remain queryable.
3. Prove missing data cannot produce no-signal.

## Implementation Guidance

- Express policy in adapters and registries, not if/else scattered through shared cores.
- Add compatibility tests before any reuse change.


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
