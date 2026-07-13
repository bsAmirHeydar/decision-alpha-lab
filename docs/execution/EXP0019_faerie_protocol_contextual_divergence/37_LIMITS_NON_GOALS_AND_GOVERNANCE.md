---
title: "37 - Limits, Non-Goals, and Governance"
tags: [exp0019, faerie-protocol, contextual-divergence, obsidian]
status: normative
experiment: EXP0019
context_id: FP-CONTEXT-001
context_version: 2.0.0-doc-freeze
doc_version: 2.0.0
last_updated: 2026-07-13
language: en
---
# 37 - Limits, Non-Goals, and Governance

## Purpose

Define what this context does not claim and how future policy changes are governed.

## Scope

This document defines the Faerie Protocol context-layer behavior for its subject. It does not modify the stable intermarket divergence core. The shared core continues to own symbol-local references, touch/hunt facts, hunter/protected roles, closed-candle confirmation primitives, signal identity, deduplication, and ledger mechanics.

## Frozen Decisions Applied

- Documentation freeze does not prove edge.
- Only Q12 remains open.

## Normative Invariants

1. **No market-edge claim.**
2. **No guarantee of broker parity without data.**
3. **No direct modification of other context semantics.**
4. **No silent policy change.**
5. **No live execution with unset consumption policy.**

## Deterministic Procedure

```text
Version decision set.
Version context manifest.
Run impact analysis.
Run regression suites.
Record ADR.
Release patch with exact file index.
```

## State and Evidence Requirements

| Field / Evidence | Requirement | Failure Behavior |
|---|---|---|
| `governance_version` | Policy process version. | Required. |
| `canonical_profile` | Exact manifest. | Required. |
| `research_profile` | Explicit non-canonical label. | No production confusion. |
| `change_record` | Reason/impact/tests. | Required. |

## Edge-Case Catalogue

### Owner changes chart-timeframe rule

New decision-set and signal namespace.

### Research override desired

Separate profile; do not call canonical.

### New symbol pair

New pair descriptor and validation.

### New relation

Registry/schema/version update and tests.

## Executable Test Obligations

1. Policy-change identity test.
2. Cross-context regression.
3. Production-profile refusal for open decisions.

## Implementation Guidance

- Use ADRs for all behavior changes after v2 freeze.


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
