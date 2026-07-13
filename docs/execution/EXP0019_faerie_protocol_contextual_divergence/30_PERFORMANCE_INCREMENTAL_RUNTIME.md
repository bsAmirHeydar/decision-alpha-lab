---
title: "30 - Performance and Incremental Runtime"
tags: [exp0019, faerie-protocol, contextual-divergence, obsidian]
status: normative
experiment: EXP0019
context_id: FP-CONTEXT-001
context_version: 2.0.0-doc-freeze
doc_version: 2.0.0
last_updated: 2026-07-13
language: en
---
# 30 - Performance and Incremental Runtime

## Purpose

Define scalable history processing for long weekly/calendar lookbacks without rescanning all data.

## Scope

This document defines the Faerie Protocol context-layer behavior for its subject. It does not modify the stable intermarket divergence core. The shared core continues to own symbol-local references, touch/hunt facts, hunter/protected roles, closed-candle confirmation primitives, signal identity, deduplication, and ledger mechanics.

## Frozen Decisions Applied

- Calendar-day gaps remain explicit even when cached.
- M1 is canonical input.

## Normative Invariants

1. **Process each new M1 once per symbol.**
2. **Cache completed windows immutably.**
3. **Recompute only affected active windows.**
4. **Drawing updates are event-driven.**

## Deterministic Procedure

```text
Backfill required M1 range.
Build completed A/L/N/W windows.
Persist cache.
Set cursor.
On new M1 update active windows and detectors.
Emit events only on state changes.
```

## State and Evidence Requirements

| Field / Evidence | Requirement | Failure Behavior |
|---|---|---|
| `last_processed_m1` | Per symbol cursor. | Required. |
| `window_cache_key` | symbol/interval/data revision. | Canonical. |
| `processing_latency_ms` | Telemetry. | Alert threshold. |
| `backfill_state` | PENDING/READY/FAILED. | Execution blocked unless READY. |

## Edge-Case Catalogue

### History arrives late

Invalidate only affected data revision/windows.

### Symbol reconnect gap

Enter DATA_INCOMPLETE until backfilled.

### Large calendar depth

Selector uses indexed window store, not repeated CopyRates scans.

### Chart redraw storm

Batch visual updates.

## Executable Test Obligations

1. Long-history performance benchmark.
2. Incremental versus full replay parity.
3. Reconnect gap test.
4. No duplicate event test.

## Implementation Guidance

- Use immutable completed-window cache and small active-window state.


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
