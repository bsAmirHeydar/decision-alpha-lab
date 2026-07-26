---
title: "ADR FP-010 - Confirmation Uses Resolved Host Chart Timeframe"
tags: [exp0019, faerie-protocol, contextual-divergence, obsidian]
status: accepted
experiment: EXP0019
context_id: FP-CONTEXT-001
context_version: 2.0.0-doc-freeze
doc_version: 2.0.0
last_updated: 2026-07-13
language: en
---
# ADR FP-010 - Confirmation Uses Resolved Host Chart Timeframe

## Decision

Resolve the current chart timeframe at initialization and include it in context identity.

## Context

This matches owner answer 5-A.

## Consequences

Changing chart timeframe creates a new context epoch and may change confirmed signals.

## Alternatives Rejected or Deferred

- Silent fallback to legacy code.
- Unversioned runtime inference.
- Deleting historical events when policy state changes.

## Verification

- Contract/schema test.
- Golden M1 replay fixture.
- Negative or boundary fixture.
- Traceability link to owner decision.

## Rollback

A policy rollback requires a new decision-set version and context epoch; historical v2 evidence is not rewritten.

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
