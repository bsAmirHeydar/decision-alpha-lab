---
title: "UCE-I15 — First Real Context Tournament: Infrastructure Pilot and Doctrine-Rich Challenge"
tags:
  - strategy-factory
  - universal-context-engine
  - implementation-program
status: implemented_reference_and_gate_ready
doc_version: 3.0.0
last_updated: 2026-07-13
---
# UCE-I15 — First Real Context Tournament: Infrastructure Pilot and Doctrine-Rich Challenge

## Mission

Prove the complete engine on real data by running an infrastructure pilot on EXP0017 and a doctrine-rich treatment/model tournament on Hook/Zone, then freezing prospective paper evidence.

## Architecture Mapping

This implementation phase realizes: UCE-13. It is an execution decomposition of the V2 architecture, not a change to doctrine.

## Entry Preconditions

- UCE-I02–I14 passed for the selected context scope
- Data inventory and causal cut approved

## Implementation Slices

### I15.1 — EXP0017 infrastructure tournament

Use the already-integrated pilot to validate dataset, treatment matrix, classical trainers, search ledger, anti-overfit gate, runtime bundle, and paper replay end to end.

**Required artifacts:** schema/contract changes; implementation; golden fixtures; negative fixtures; tests; telemetry; documentation; manifest and hashes; downstream handoff.

### I15.2 — Hook/Zone context package

Encode Hook/F/Rally/Zone doctrine, lifecycle, freshness, structure, feature packs, cluster rules, personal setup, and known-time behavior without exploitation leakage.

**Required artifacts:** schema/contract changes; implementation; golden fixtures; negative fixtures; tests; telemetry; documentation; manifest and hashes; downstream handoff.

### I15.3 — Treatment universe freeze

Declare tight-convex, wide-survival, limit, confirmation, fixed target, runner, fixed-plus-trail, partial-plus-runner, and capital policy families before outcomes are inspected.

**Required artifacts:** schema/contract changes; implementation; golden fixtures; negative fixtures; tests; telemetry; documentation; manifest and hashes; downstream handoff.

### I15.4 — Algorithm/task tournament

Run manual, naive, classical, ranking, treatment-choice, survival/distributional, and qualified deep variants under the same folds, budgets, and selection ledger.

**Required artifacts:** schema/contract changes; implementation; golden fixtures; negative fixtures; tests; telemetry; documentation; manifest and hashes; downstream handoff.

### I15.5 — Confirmatory anti-overfit report

Lock families, metrics, thresholds, and critical gates; produce promotion/rejection evidence and select at most a bounded challenger set.

**Required artifacts:** schema/contract changes; implementation; golden fixtures; negative fixtures; tests; telemetry; documentation; manifest and hashes; downstream handoff.

### I15.6 — Frozen prospective paper challenge

Freeze runtime generation and paper period; prohibit retraining/tuning; reconcile expected and observed fills, costs, decisions, and drift.

**Required artifacts:** schema/contract changes; implementation; golden fixtures; negative fixtures; tests; telemetry; documentation; manifest and hashes; downstream handoff.

### I15.7 — Champion or rejection decision

Promote only if prospective, parity, risk, and operational gates pass; otherwise document the failure and iterate from the correct upstream phase.

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

- [ ] Infrastructure pilot completes without manual data surgery
- [ ] Hook/Zone context replay is causally stable
- [ ] Treatment and algorithm universes are frozen before confirmatory evaluation
- [ ] Prospective paper period is untouched by tuning
- [ ] Promotion can legitimately end in rejection

## Primary Outputs

- `exp0017_tournament_report`
- `hook_zone_context_package`
- `frozen_treatment_universe`
- `experiment_ledger`
- `anti_overfit_report`
- `prospective_paper_report`
- `champion_or_rejection_decision`

## Non-Completion Conditions

- A behavior-changing parameter is absent from identity or serialization.
- A consumer must infer semantics from prose.
- A critical test is marked passed without executable evidence.
- A future observation can influence a past decision artifact.
- Research and runtime use different treatment, economics, feature, or risk semantics.
- Failed or rejected work is removed from the evidence trail.

## Key Risks

- Using pilot success as evidence of alpha
- Changing treatment universe after seeing results
- Short prospective period with false confidence

## Handoff

The phase handoff lists exact artifact hashes, schema versions, capability flags, accepted/rejected gates, residual risks, migration impact, rollback instructions, and the first downstream golden test. The next phase may not infer missing data.

## Source Architecture References

- [[30_END_TO_END_REFERENCE_PIPELINES]]
- [[36_EXAMPLE_CONTEXT_HOOK_AND_ZONE]]
- [[EX_01_HOOK_ZONE]]
- [[VAL_16_PROSPECTIVE_PAPER]]
- [[UCE_13_FIRST_REAL_CONTEXT_TOURNAMENT]]


## Implementation status note

The I15 orchestration, reference EXP0017 pilot, Hook/Zone package contract, frozen universes, prospective plan, reconciliation, evidence, and legitimate-rejection gates are implemented and Python/static validated. No real historical dataset or completed prospective paper period is embedded; the current reference decision is therefore rejection, not promotion.
