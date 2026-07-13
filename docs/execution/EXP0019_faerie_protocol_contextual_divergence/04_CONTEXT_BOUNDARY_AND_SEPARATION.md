---
title: "04 - Context Boundary and Separation"
tags: [exp0019, faerie-protocol, contextual-divergence, obsidian]
status: normative
experiment: EXP0019
context_id: FP-CONTEXT-001
context_version: 2.0.0-doc-freeze
doc_version: 2.0.0
last_updated: 2026-07-13
language: en
---
# 04 - Context Boundary and Separation

## Purpose

Define precisely what belongs to the fixed shared divergence cores and what belongs to Faerie Protocol.

## Scope

This document defines the Faerie Protocol context-layer behavior for its subject. It does not modify the stable intermarket divergence core. The shared core continues to own symbol-local references, touch/hunt facts, hunter/protected roles, closed-candle confirmation primitives, signal identity, deduplication, and ledger mechanics.

## Frozen Decisions Applied

- All owner choices are context policies except spread-adjusted SELL stop, which configures shared execution risk behavior through an adapter.

## Normative Invariants

1. **Shared cores remain context-agnostic.**
2. **Faerie modules may compose but may not duplicate shared services.**
3. **Context outputs are explicit data contracts.**
4. **Execution remains downstream of detection.**

## Deterministic Procedure

```text
Read shared facts.
Apply FP window selectors.
Apply relation rules.
Apply WW gate.
Apply arbitration and drawing policies.
Hand eligible plan to execution adapter.
```

## State and Evidence Requirements

| Field / Evidence | Requirement | Failure Behavior |
|---|---|---|
| `shared_core_version` | Exact compatible version. | Reject incompatible runtime. |
| `context_policy_version` | FP policy version. | Create new epoch on change. |
| `adapter_contract_hash` | Hash of mapping rules. | Block silent adapter drift. |

## Edge-Case Catalogue

### Needed behavior absent in core

Add a generic capability only if reusable and covered by compatibility tests; otherwise keep it in FP adapter.

### Legacy FP101 utility duplicates core

Do not port blindly; map to shared service.

### Policy needs historical audit

Store decision version in manifest and signal ID.

## Executable Test Obligations

1. Scan FP modules for forbidden duplicate time/reference/hunt implementations.
2. Verify shared core imports are one-way.
3. Verify execution cannot call detection internals mutably.

## Implementation Guidance

- Use interfaces: `ITimeKernel`, `IWindowProvider`, `IReferenceStore`, `IDivergenceDetector`, `IConfirmationProjector`, `ILedger`.


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
