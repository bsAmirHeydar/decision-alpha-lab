---
title: "Phase 01 Handoff Contract"
tags: [strategy-factory, phase-00, phase-01, handoff]
status: canonical
---

# Phase 01 Handoff Contract

## Purpose

Phase 01 freezes explicit contracts and schemas. It receives evidence from Phase 00 and must not infer the old repository privately.

## Required input artifacts

Phase 01 consumes:

- `repository_inventory.json`
- `module_classification.json`
- `contract_schema_map.csv`
- `duplicate_engine_matrix.csv`
- `execution_authority_scan.csv`
- `migration_risk_register.json`
- `pilot_selection.json`
- `test_baseline.json`
- `phase00_qa_report.json`

## Contract priorities

Phase 01 should define contracts in this order:

1. `SchemaIdentity`
2. `SourceLineage`
3. `MarketTimestamp`
4. `BarRecord` / `BarFrameDescriptor`
5. `AnatomyEvent`
6. `FeatureValue` / `FeatureSnapshot`
7. `ArtifactIdentity`
8. `CandidateTemplate` / `TradeCandidate`
9. `OutcomeRecord`
10. `ModelDecision`
11. `ActionPlan`
12. `ExecutionIntent`
13. `ExecutionTrace`

Only the first seven need deep legacy compatibility analysis in the initial Phase 01 implementation.

## Binding Phase 00 constraints

### Constraint 1 — No market semantics in kernel contracts

A contract may carry node type or anatomy metadata, but the kernel must not define what makes a valid node.

### Constraint 2 — Explicit time semantics

Every event/feature/output contract must distinguish observation, known, confirmation, decision, and label-end time where applicable.

### Constraint 3 — Stable identity

Identity must not depend on mutable row order or current cache path.

### Constraint 4 — Source lineage

Every generated artifact must identify source data, producer version, schema version, and configuration hash.

### Constraint 5 — Missing values are explicit

Missing, unavailable, stale, not-applicable, and invalid must not collapse into one untyped `None`.

### Constraint 6 — No order authority

Execution contracts can be modeled, but Phase 01 must not add broker calls.

## Phase 01 acceptance tests derived from Phase 00

- legacy MT5 bars can map to canonical bars;
- terminal-local time cannot silently pass as UTC;
- L-rule output can map to `AnatomyEvent` without redefining L-rule;
- M0001 output can map to a versioned feature/label record;
- schema major mismatch fails closed;
- serialization round trips preserve identity;
- deterministic IDs remain stable across row ordering;
- no execution authority token is introduced.
