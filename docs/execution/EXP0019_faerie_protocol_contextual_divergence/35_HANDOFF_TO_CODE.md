---
title: "35 - Handoff to Code"
tags: [exp0019, faerie-protocol, contextual-divergence, obsidian]
status: normative
experiment: EXP0019
context_id: FP-CONTEXT-001
context_version: 2.0.0-doc-freeze
doc_version: 2.0.0
last_updated: 2026-07-13
language: en
---
# 35 - Handoff to Code

## Purpose

Translate the documentation freeze into explicit developer instructions, acceptance criteria, and prohibited shortcuts.

## Scope

This document defines the Faerie Protocol context-layer behavior for its subject. It does not modify the stable intermarket divergence core. The shared core continues to own symbol-local references, touch/hunt facts, hunter/protected roles, closed-candle confirmation primitives, signal identity, deduplication, and ledger mechanics.

## Frozen Decisions Applied

- Use v2 owner decision contract.
- Treat Q12 as a live-execution gate.

## Normative Invariants

1. **Developer may not reinterpret option letters.**
2. **Module boundaries are mandatory.**
3. **Every state transition and reason code is observable.**
4. **No hidden fallback to legacy FP101 behavior.**

## Deterministic Procedure

```text
Read MOC and decision freeze.
Validate manifest.
Implement contracts/enums.
Implement phases in roadmap order.
Run golden and compatibility suites.
Produce code-phase handoff evidence.
```

## State and Evidence Requirements

| Field / Evidence | Requirement | Failure Behavior |
|---|---|---|
| `implementation_manifest` | Versions and decisions. | Required. |
| `test_report` | Golden/negative/compatibility. | Required. |
| `open_decisions` | Must contain FP-DEC-012 until answered. | Live blocked. |
| `code_hashes` | Patch inventory. | Required. |

## Edge-Case Catalogue

### Question arises during coding

Add decision/assumption record; do not silently choose.

### Legacy code easier to copy

Reuse only verified portions.

### Chart object seems convenient for state

Forbidden; use ledger/store.

### Tick data available

Do not use for first-sweep ordering.

## Executable Test Obligations

1. Compiler/static tests.
2. Runtime diagnostic EA.
3. Historical replay.
4. Paper-trade fixture.

## Implementation Guidance

- First coding deliverable should be a diagnostic context engine, not a trading EA.


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
