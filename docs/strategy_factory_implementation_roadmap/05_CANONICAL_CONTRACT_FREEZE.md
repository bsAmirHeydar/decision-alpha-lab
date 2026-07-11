---
title: "Canonical Contract Freeze"
tags:
  - strategy-factory
  - implementation-roadmap
  - alpha-lab
status: canonical
doc_version: 1.0.0
---

# Canonical Contract Freeze

## Required Core Contracts

1. `AnatomyEvent`
2. `ContextSnapshot`
3. `FeatureValue`
4. `CandidateTemplate`
5. `TradeCandidate`
6. `OutcomeRecord`
7. `FoldAssignment`
8. `ModelArtifact`
9. `ModelDecision`
10. `ActionPlan`
11. `ExecutionIntent`
12. `ExecutionTrace`
13. `TelemetryRecord`
14. `PromotionDecision`

## Contract Rules

- Every contract has semantic version, schema version, producer version, and creation time.
- Every causal record contains `known_time_utc`.
- Every derived record carries lineage to its source event and manifest hash.
- Fields cannot silently change meaning.
- Optional fields require explicit missing-value semantics.
- Python and MQL5 serializers must pass identical golden fixtures.
- Unknown enum values fail closed in runtime code.

## Compatibility Policy

- Patch: bug fix without schema change.
- Minor: additive optional fields or new enum values supported by old readers.
- Major: breaking meaning or required-field change.
