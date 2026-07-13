---
title: "23 - Signal Identity, Deduplication, and Ledger"
tags: [exp0019, faerie-protocol, contextual-divergence, obsidian]
status: normative
experiment: EXP0019
context_id: FP-CONTEXT-001
context_version: 2.0.0-doc-freeze
doc_version: 2.0.0
last_updated: 2026-07-13
language: en
---
# 23 - Signal Identity, Deduplication, and Ledger

## Purpose

Define canonical IDs for raw candidates, confirmed signals, WW gate events, quota arbitration, and execution plans.

## Scope

This document defines the Faerie Protocol context-layer behavior for its subject. It does not modify the stable intermarket divergence core. The shared core continues to own symbol-local references, touch/hunt facts, hunter/protected roles, closed-candle confirmation primitives, signal identity, deduplication, and ledger mechanics.

## Frozen Decisions Applied

- Resolved chart timeframe, calendar-day offset, M1 hunt time, and owner decision version are identity-bearing.

## Normative Invariants

1. **One economic event maps to one canonical ID.**
2. **Policy outcomes are child ledger events, not mutated signal fields.**
3. **Hash input ordering is canonical.**
4. **Confirmed and suppressed history is append-only.**

## Deterministic Procedure

```text
Canonicalize context epoch.
Canonicalize relation/reference/check/direction/roles/times.
Hash raw candidate.
Create confirmation child event.
Create gate/quota/execution child events.
```

## State and Evidence Requirements

| Field / Evidence | Requirement | Failure Behavior |
|---|---|---|
| `signal_id` | Canonical SHA-256 or stable compact derivative. | Reject duplicate conflicting payload. |
| `parent_event_id` | Lineage. | Required for policy child events. |
| `config_hash` | All behavior-bearing inputs. | Block absent. |
| `ledger_sequence` | Append order. | Monotonic. |

## Edge-Case Catalogue

### Same signal reconstructed after restart

ID must match exactly.

### Same N price from different calendar dates

Different reference interval IDs.

### Current chart timeframe differs

Different context epoch and signal identity.

### Later neutralization

New ledger event, original signal ID unchanged.

## Executable Test Obligations

1. Restart reconstruction test.
2. Timeframe identity-change test.
3. Policy-child lineage test.
4. Duplicate conflict test.

## Implementation Guidance

- Use shared canonical serialization and ledger core.


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
