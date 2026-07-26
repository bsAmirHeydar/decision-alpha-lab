---
title: "33 - Ambiguity and Decision Register"
tags: [exp0019, faerie-protocol, contextual-divergence, obsidian]
status: normative
experiment: EXP0019
context_id: FP-CONTEXT-001
context_version: 2.0.0-doc-freeze
doc_version: 2.0.0
last_updated: 2026-07-13
language: en
---
# 33 - Ambiguity and Decision Register

## Purpose

Record the complete decision set, exact option mapping, authority, interpretation, and remaining blockers.

## Scope

This document defines the Faerie Protocol context-layer behavior for its subject. It does not modify the stable intermarket divergence core. The shared core continues to own symbol-local references, touch/hunt facts, hunter/protected roles, closed-candle confirmation primitives, signal identity, deduplication, and ledger mechanics.

## Frozen Decisions Applied

- Fourteen decisions are owner-confirmed.
- FP-DEC-012 is the only open decision.

## Normative Invariants

1. **No unanswered item is hidden by a default.**
2. **Derived tie-breaks are not mislabelled as strategy preference.**
3. **Each decision has implementation and test impact.**

## Deterministic Procedure

```text
Load owner response.
Map option letters to archived question text.
Assign canonical policy.
Classify authority.
Update manifest/open-decision contract.
```

## State and Evidence Requirements

| Field / Evidence | Requirement | Failure Behavior |
|---|---|---|
| `decision_id` | FP-DEC-001..015. | Required. |
| `owner_option` | A/B/C/... or UNANSWERED. | Required. |
| `canonical_policy` | Machine-readable enum. | Required. |
| `authority` | OWNER_CONFIRMED/OPEN_DECISION. | Required. |

## Edge-Case Catalogue

### Option C in WW lifecycle only defines neutralization

Activation/confirmation use shared candidate-confirmation architecture and are labelled derived.

### Option A no-WW

Applies to valid complete weekly evaluation; incomplete data remains separate.

### Q12 unanswered

Live consumption policy stays unset.

## Executable Test Obligations

1. Decision count equals 15.
2. Exactly one open decision.
3. Manifest references decision-set hash.
4. Traceability links each decision.

## Implementation Guidance

- Use `fp_owner_decisions.v2.json` as machine authority.


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
