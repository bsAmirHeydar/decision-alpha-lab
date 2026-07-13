---
title: "10 - Signal Taxonomy and Seven-Relation Registry"
tags: [exp0019, faerie-protocol, contextual-divergence, obsidian]
status: normative
experiment: EXP0019
context_id: FP-CONTEXT-001
context_version: 2.0.0-doc-freeze
doc_version: 2.0.0
last_updated: 2026-07-13
language: en
---
# 10 - Signal Taxonomy and Seven-Relation Registry

## Purpose

Define relation codes, selectors, direction, tradeability, priority metadata, and versioned registry behavior.

## Scope

This document defines the Faerie Protocol context-layer behavior for its subject. It does not modify the stable intermarket divergence core. The shared core continues to own symbol-local references, touch/hunt facts, hunter/protected roles, closed-candle confirmation primitives, signal identity, deduplication, and ledger mechanics.

## Frozen Decisions Applied

- WW is both a gate and a tradeable relation.
- Calendar-day depth applies only to NA/NL/NN historical N references.

## Normative Invariants

1. **Relation code means reference window first, check window second.**
2. **Registry order is not strategy priority except as technical tie-break.**
3. **Every relation has independent enable-detect/draw/execute flags.**
4. **Direction is separate from relation code.**

## Deterministic Procedure

```text
Resolve relation descriptor.
Select reference interval(s).
Select check interval.
Run shared divergence detector.
Apply relation-specific confirmation deadline.
Emit relation-qualified signal.
```

## State and Evidence Requirements

| Field / Evidence | Requirement | Failure Behavior |
|---|---|---|
| `relation_code` | AL/AN/LN/NA/NL/NN/WW. | Reject unknown. |
| `reference_selector` | Versioned selector. | Block absent. |
| `check_selector` | Versioned selector. | Block absent. |
| `execution_enabled` | Policy flag. | No order when false. |

## Edge-Case Catalogue

### Disabled execution but enabled detection

Signal remains detectable and drawable.

### Unknown relation code

Fail closed.

### Multiple historical N offsets trigger

Each reference interval produces a distinct signal identity.

## Executable Test Obligations

1. Registry schema closure test.
2. Relation-code naming test.
3. Per-relation golden cases.

## Implementation Guidance

- Use generated descriptors rather than switch statements distributed across modules.


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
