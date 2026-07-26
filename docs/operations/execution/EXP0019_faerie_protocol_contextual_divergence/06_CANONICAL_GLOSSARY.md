---
title: "06 - Canonical Glossary"
tags: [exp0019, faerie-protocol, contextual-divergence, obsidian]
status: normative
experiment: EXP0019
context_id: FP-CONTEXT-001
context_version: 2.0.0-doc-freeze
doc_version: 2.0.0
last_updated: 2026-07-13
language: en
---
# 06 - Canonical Glossary

## Purpose

Provide one unambiguous vocabulary for windows, references, hunts, candidates, confirmation, WW, quota, and visual states.

## Scope

This document defines the Faerie Protocol context-layer behavior for its subject. It does not modify the stable intermarket divergence core. The shared core continues to own symbol-local references, touch/hunt facts, hunter/protected roles, closed-candle confirmation primitives, signal identity, deduplication, and ledger mechanics.

## Frozen Decisions Applied

- Terms reflect the frozen owner decisions.

## Normative Invariants

1. **A term has one meaning.**
2. **Codes are not overloaded.**
3. **Time fields include timezone and interval semantics.**
4. **State names are enumerable.**

## Deterministic Procedure

```text
Define term.
Define type.
Define lifecycle.
Define non-example.
Link owner decision and contract field.
```

## State and Evidence Requirements

| Field / Evidence | Requirement | Failure Behavior |
|---|---|---|
| `term_id` | Stable uppercase identifier. | Reject free-text state. |
| `definition` | Normative meaning. | No synonym drift. |
| `decision_link` | Relevant decision ID. | Missing link is warning. |

## Edge-Case Catalogue

### "First" without clock authority

Use `first_hunt_m1_time` only.

### "No WW" with missing data

Use `WW_NONE_VALID_DATA` versus `WW_DATA_INCOMPLETE`.

### "Entry" ambiguity

Distinguish plan, attempt, accepted order, and fill.

## Executable Test Obligations

1. Lint docs/contracts for deprecated terms.
2. Verify all reason codes and states are defined.

## Implementation Guidance

- Generate enums from the canonical glossary where practical.


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
