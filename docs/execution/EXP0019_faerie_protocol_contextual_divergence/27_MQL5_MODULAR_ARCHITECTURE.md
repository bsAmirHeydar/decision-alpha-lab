---
title: "27 - MQL5 Modular Architecture"
tags: [exp0019, faerie-protocol, contextual-divergence, obsidian]
status: normative
experiment: EXP0019
context_id: FP-CONTEXT-001
context_version: 2.0.0-doc-freeze
doc_version: 2.0.0
last_updated: 2026-07-13
language: en
---
# 27 - MQL5 Modular Architecture

## Purpose

Define files, interfaces, ownership boundaries, lifecycle, and dependency direction for the eventual implementation.

## Scope

This document defines the Faerie Protocol context-layer behavior for its subject. It does not modify the stable intermarket divergence core. The shared core continues to own symbol-local references, touch/hunt facts, hunter/protected roles, closed-candle confirmation primitives, signal identity, deduplication, and ledger mechanics.

## Frozen Decisions Applied

- Stable cores are reused through adapters.
- FP-specific policies are isolated in modules.

## Normative Invariants

1. **One module, one responsibility.**
2. **No business state in chart objects.**
3. **No full-history rescan on every timer.**
4. **No cross-layer mutable globals.**

## Deterministic Procedure

```text
Initialize context manifest.
Initialize shared-core adapters.
Backfill incremental windows.
Process new M1 events.
Project confirmations.
Resolve policies.
Persist ledger.
Render view.
```

## State and Evidence Requirements

| Field / Evidence | Requirement | Failure Behavior |
|---|---|---|
| `module_id` | Versioned component. | Required. |
| `dependency_version` | Exact compatibility. | Reject mismatch. |
| `health_state` | READY/DEGRADED/BLOCKED. | Telemetry. |
| `last_processed_m1` | Incremental cursor. | Persist/rebuild. |

## Edge-Case Catalogue

### Module init failure

Fail EA initialization with diagnostic code.

### Partial history

Run detection in diagnostic-only state until coverage passes.

### Timeframe change

Reinitialize epoch.

### Dependency version mismatch

Fail closed.

## Executable Test Obligations

1. Static dependency guard.
2. Unit tests per module.
3. Integration replay.
4. No forbidden order calls from detection modules.

## Implementation Guidance

- Recommended modules: FPTimeAdapter, FPSessionCalendar, FPRelationRegistry, FPHistoricalNSelector, FPWWProvider, FPReferenceLifecycle, FPConfirmationPolicy, FPWeeklyGate, FPQuotaArbiter, FPVisualProjector, FPExecutionAdapter.


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
