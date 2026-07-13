---
title: "22 - Drawing and Session-Box Contract"
tags: [exp0019, faerie-protocol, contextual-divergence, obsidian]
status: normative
experiment: EXP0019
context_id: FP-CONTEXT-001
context_version: 2.0.0-doc-freeze
doc_version: 2.0.0
last_updated: 2026-07-13
language: en
---
# 22 - Drawing and Session-Box Contract

## Purpose

Define persistent, reason-coded visual evidence for active, confirmed, neutralized, and suppressed signals.

## Scope

This document defines the Faerie Protocol context-layer behavior for its subject. It does not modify the stable intermarket divergence core. The shared core continues to own symbol-local references, touch/hunt facts, hunter/protected roles, closed-candle confirmation primitives, signal identity, deduplication, and ledger mechanics.

## Frozen Decisions Applied

- Suppressed signals are always drawn with distinct style.
- Confirmed drawings remain historical evidence.

## Normative Invariants

1. **Drawing is a projection of ledger state, not state storage.**
2. **Object names are collision-free and include absolute IDs.**
3. **Suppression affects color/opacity/line style, not existence.**
4. **Rebuild is deterministic.**

## Deterministic Procedure

```text
Read ledger events.
Resolve visual state and reason code.
Build immutable object descriptor.
Upsert by signal/object ID.
On reinit, clear managed namespace and rebuild.
```

## State and Evidence Requirements

| Field / Evidence | Requirement | Failure Behavior |
|---|---|---|
| `object_id` | Hash of context/signal/visual role. | Reject collision. |
| `visual_state` | RAW/CONFIRMED/SUPPRESSED/NEUTRALIZED/INVALID. | Closed enum. |
| `reason_code` | Why style differs. | Required for non-active. |
| `style_id` | Registry key. | Reject unknown. |

## Edge-Case Catalogue

### Same relation across multiple days

Absolute window IDs prevent collision.

### WW neutralized after confirmation

Retain confirmed annotation and overlay neutralized style/status.

### Quota-suppressed setup

Draw with `SUPPRESSED_BY_QUOTA` style.

### Missing data

Draw diagnostic marker only when configured.

## Executable Test Obligations

1. Rebuild parity test.
2. Collision test across days.
3. All suppression reasons have styles.
4. No chart object is treated as business state.

## Implementation Guidance

- Keep drawing adapter read-only against core state.


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
