---
title: "34 - Implementation Roadmap"
tags: [exp0019, faerie-protocol, contextual-divergence, obsidian]
status: normative
experiment: EXP0019
context_id: FP-CONTEXT-001
context_version: 2.0.0-doc-freeze
doc_version: 2.0.0
last_updated: 2026-07-13
language: en
---
# 34 - Implementation Roadmap

## Purpose

Provide a phase-by-phase implementation sequence that protects shared cores and closes evidence before execution.

## Scope

This document defines the Faerie Protocol context-layer behavior for its subject. It does not modify the stable intermarket divergence core. The shared core continues to own symbol-local references, touch/hunt facts, hunter/protected roles, closed-candle confirmation primitives, signal identity, deduplication, and ledger mechanics.

## Frozen Decisions Applied

- Detection/drawing can proceed now.
- Live execution completion waits on FP-DEC-012.

## Normative Invariants

1. **Each phase has contracts, code, tests, docs, and handoff.**
2. **Shared-core compatibility precedes FP adapter integration.**
3. **No monolithic EA rewrite.**
4. **Diagnostics precede trading.**

## Deterministic Procedure

```text
Phase 0 compatibility harness.
Phase 1 types/contracts/manifest.
Phase 2 time/session/windows.
Phase 3 references and relation registry.
Phase 4 detection/candidates/confirmation.
Phase 5 WW gate/setup.
Phase 6 drawing/ledger.
Phase 7 quota arbitration.
Phase 8 risk/paper execution.
Phase 9 live execution after Q12 freeze.
```

## State and Evidence Requirements

| Field / Evidence | Requirement | Failure Behavior |
|---|---|---|
| `phase_id` | Stable implementation phase. | Required. |
| `entry_gate` | Tests/evidence required. | Block if unmet. |
| `exit_artifacts` | Code/docs/tests/manifest. | Required. |
| `rollback_boundary` | Files/state to revert. | Required. |

## Edge-Case Catalogue

### Core regression appears

Stop and fix before advancing.

### Data coverage incomplete

Continue diagnostics; block execution.

### Q12 still open

Ship non-live profile only.

### MetaEditor unavailable

Record static validation separately.

## Executable Test Obligations

1. Phase-level test counts.
2. Golden end-to-end replay.
3. Paper execution simulation.
4. Live profile refuses unset quota policy.

## Implementation Guidance

- Commit each phase independently and stage only indexed files.


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
