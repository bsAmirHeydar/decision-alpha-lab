---
title: "UCE-I11 — Experiment DAG, Hyperparameter Search, Compute Budgeting, and Reproducibility"
tags:
  - strategy-factory
  - universal-context-engine
  - implementation-program
status: canonical
doc_version: 3.0.0
last_updated: 2026-07-12
---
# UCE-I11 — Experiment DAG, Hyperparameter Search, Compute Budgeting, and Reproducibility

## Mission

Turn contexts, views, tasks, treatments, trainers, folds, seeds, thresholds, calibrators, and ensembles into a resumable, budgeted, fully accounted experiment graph.

## Implementation Status

Implemented in UCE-I11 v1.0.0 with deterministic Python compiler/scheduler/search/budget/cache/ledger/reproducibility contracts, spawn-based local worker isolation, 24 closed JSON schemas, MQL5 contract mirrors, conformance vectors, detailed delivery documentation, and executable acceptance evidence. MetaEditor compilation remains a separate local Windows gate. See [[../phase_deliveries/uce_i11/00_UCE_I11_DELIVERY_MOC|UCE-I11 delivery MOC]].

## Architecture Mapping

This implementation phase realizes: UCE-09. It is an execution decomposition of the V2 architecture, not a change to doctrine.

## Entry Preconditions

- UCE-I07 trainer SDK stable
- At least classical pack available
- Dataset manifests immutable

## Implementation Slices

### I11.1 — Experiment manifest compiler

Compile the declared search universe into exact nodes and edges: dataset, split, transform, trainer, trial, fold, seed, calibration, threshold, ensemble, validation, report, and export.

**Required artifacts:** schema/contract changes; implementation; golden fixtures; negative fixtures; tests; telemetry; documentation; manifest and hashes; downstream handoff.

### I11.2 — Scheduler and worker isolation

Implement local process isolation, dependency-aware scheduling, resource claims, deterministic environment capture, cancellation, retries, and failure quarantine.

**Required artifacts:** schema/contract changes; implementation; golden fixtures; negative fixtures; tests; telemetry; documentation; manifest and hashes; downstream handoff.

### I11.3 — Search adapters

Implement grid, random, quasi-random, Bayesian/TPE, successive halving/Hyperband, evolutionary where justified, and constrained multi-objective search.

**Required artifacts:** schema/contract changes; implementation; golden fixtures; negative fixtures; tests; telemetry; documentation; manifest and hashes; downstream handoff.

### I11.4 — Budget policy

Set context-level, trainer-level, phase-level, wall-clock, memory, CPU/GPU, trial, seed, and artifact retention budgets with hard cutoffs.

**Required artifacts:** schema/contract changes; implementation; golden fixtures; negative fixtures; tests; telemetry; documentation; manifest and hashes; downstream handoff.

### I11.5 — Selection ledger

Record every attempted, skipped, invalid, pruned, failed, timed-out, selected, rejected, thresholded, calibrated, ensembled, and manually overridden choice.

**Required artifacts:** schema/contract changes; implementation; golden fixtures; negative fixtures; tests; telemetry; documentation; manifest and hashes; downstream handoff.

### I11.6 — Caching and resume

Content-address datasets/transforms/folds/models/predictions, validate cache provenance, resume interrupted DAGs, and refuse stale/incompatible cache entries.

**Required artifacts:** schema/contract changes; implementation; golden fixtures; negative fixtures; tests; telemetry; documentation; manifest and hashes; downstream handoff.

### I11.7 — Reproducibility audit

Re-run selected paths from the manifest, compare artifacts within declared tolerance, and reconcile declared versus executed search counts.

**Required artifacts:** schema/contract changes; implementation; golden fixtures; negative fixtures; tests; telemetry; documentation; manifest and hashes; downstream handoff.


## Required Test Families

| Family | Required proof |
|---|---|
| Contract | schema, identity, version, canonical serialization, migration/rejection |
| Causality | known-time, future perturbation, stale/reordered data, maturity where applicable |
| Determinism | repeated run, seed/worker control, restart/cache behavior |
| Economics | long/short executable sides, costs, broker constraints, maximum loss where applicable |
| Failure | corrupt/missing/incompatible resource, timeout, resource pressure, unsupported capability |
| Differential | prior accepted version or legacy parity where applicable |
| Cross-mode | Python/MQL5, research/tester/paper/runtime as applicable |
| Governance | manifest, hashes, QA, limitations, residual risk, handoff |

## Acceptance Gates

- [ ] The hidden test role is never referenced by search nodes
- [ ] Declared and executed trial counts reconcile
- [ ] Same manifest reproduces selected artifacts within tolerance
- [ ] Cancellation and resource ceilings work under failure injection
- [ ] Every model in a report exists in the selection ledger

## Primary Outputs

- `experiment_dag_compiler`
- `scheduler`
- `search_registry`
- `budget_policy`
- `selection_ledger`
- `content_cache`
- `reproducibility_report`

## Non-Completion Conditions

- A behavior-changing parameter is absent from identity or serialization.
- A consumer must infer semantics from prose.
- A critical test is marked passed without executable evidence.
- A future observation can influence a past decision artifact.
- Research and runtime use different treatment, economics, feature, or risk semantics.
- Failed or rejected work is removed from the evidence trail.

## Key Risks

- Invisible search multiplicity
- Cache contamination across schemas
- Compute exhaustion from treatment × model explosion

## Handoff

The phase handoff lists exact artifact hashes, schema versions, capability flags, accepted/rejected gates, residual risks, migration impact, rollback instructions, and the first downstream golden test. The next phase may not infer missing data.

## Source Architecture References

- [[12_UNIVERSAL_TRAINING_ORCHESTRATOR]]
- [[13_SEARCH_OPTIMIZATION_AND_EXPERIMENT_BUDGETING]]
- [[CON_10_EXPERIMENT_MANIFEST]]
- [[OPS_01_DAG_SCHEDULER]]
- [[OPS_02_COMPUTE_BUDGET]]
