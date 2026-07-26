---
title: "25 - Data Contracts"
tags: [exp0019, faerie-protocol, contextual-divergence, obsidian]
status: normative
experiment: EXP0019
context_id: FP-CONTEXT-001
context_version: 2.0.0-doc-freeze
doc_version: 2.0.0
last_updated: 2026-07-13
language: en
---
# 25 - Data Contracts

## Purpose

Define closed schemas for context manifest, windows, references, hunts, signals, WW resolution, quota, drawings, and execution plans.

## Scope

This document defines the Faerie Protocol context-layer behavior for its subject. It does not modify the stable intermarket divergence core. The shared core continues to own symbol-local references, touch/hunt facts, hunter/protected roles, closed-candle confirmation primitives, signal identity, deduplication, and ledger mechanics.

## Frozen Decisions Applied

- All frozen owner decisions are serialized.
- Q12 is represented as `UNSET` rather than omitted.

## Normative Invariants

1. **Unknown fields are rejected in strict mode.**
2. **Enums are closed.**
3. **Timestamps include UTC instant and NY identity where needed.**
4. **Hashes are lowercase SHA-256.**

## Deterministic Procedure

```text
Validate incoming record.
Normalize enums and numbers.
Compute canonical hash.
Persist immutable record.
Reference by ID downstream.
```

## State and Evidence Requirements

| Field / Evidence | Requirement | Failure Behavior |
|---|---|---|
| `schema_version` | Exact semantic version. | No implicit migration. |
| `decision_set_id` | Owner decision freeze identity. | Required. |
| `context_hash` | Canonical manifest hash. | Required. |
| `data_revision` | Market-data lineage. | Required for replay. |

## Edge-Case Catalogue

### Older v1 manifest

Migrate explicitly to v2; do not assume defaults.

### Missing Q12 field

Treat live execution as disabled.

### Unknown reason code

Reject visual/execution projection.

### Non-finite price

Reject record.

## Executable Test Obligations

1. Schema round-trip tests.
2. Unknown-property rejection.
3. Hash stability.
4. v1-to-v2 migration fixture.

## Implementation Guidance

- Keep examples in `contracts/` and sync with code structs.


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
