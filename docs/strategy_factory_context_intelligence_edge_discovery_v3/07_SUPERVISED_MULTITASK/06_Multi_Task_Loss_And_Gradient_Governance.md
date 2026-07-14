---
title: Multi-Task Loss and Gradient Governance
status: canonical
version: 3.0.0
created: '2026-07-13'
updated: '2026-07-13'
tags:
- saed-v3
- governed-challenger
---

# Purpose

Control loss scaling, gradient conflict, task dominance, and representation leakage in multi-head systems.

## Capability tier

**Governed Challenger**

## System design

### Loss registry

Every task loss, weight, transformation, and schedule is immutable in the run manifest.

### Gradient diagnostics

Norms, cosine conflicts, task interference, and head-specific learning curves are recorded.

### Balancing

Static weights are baselines; uncertainty weighting, gradient surgery, or Pareto balancing are challengers.

### Ablation

Each head and shared component is removed to verify incremental value and detect hidden target leakage.

## Input contracts

- `TaskGraph`
- `LossDefinitions`
- `TrainingFolds`

## Output contracts

- `TrainingTrace`
- `GradientAudit`
- `AblationReport`

## Measurement framework

- Per-task validation.
- Gradient conflict rate.
- Shared-versus-separate uplift.
- Loss-weight sensitivity.

## Adversarial questions

- Did tuning weights use locked-test outcomes?
- Does a high-frequency target dominate rare tail tasks?
- Does one head leak post-treatment information?

## Mandatory controls

1. Exact upstream hashes and data roles are recorded.
2. Candidate and failure ledgers are complete.
3. Costs, capacity, missingness, censoring, and support are explicit.
4. Validation uses chronological, cluster-aware, purged folds.
5. Advanced outputs cannot bypass manual policy, hard risk, portfolio, or UCEE promotion.
6. Any runtime handoff requires deterministic export, parity, latency, fallback, and revocation evidence.

## Acceptance boundary

Passing research metrics is necessary but never sufficient. The component remains non-authoritative until its evidence is admitted through UCEE I12, compiled by I14, challenged prospectively under I15, bounded by I17, and qualified under I18.

## Related notes

- [[Trainer_Task_Graph]]
