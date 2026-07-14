---
title: Multi-Fidelity and Early Stopping
status: canonical
version: 3.0.0
created: '2026-07-13'
updated: '2026-07-13'
tags:
- saed-v3
- governed-challenger
---

# Purpose

Allocate compute efficiently without biasing selection toward fast-learning, high-frequency, or low-tail candidates.

## Capability tier

**Governed Challenger**

## System design

### Fidelity axes

Time span, symbols, folds, seeds, path resolution, candidate subset, and model size.

### Promotion rules

Successive halving or Bayesian schedulers use profile-aware intermediate objectives and minimum tail evidence.

### Rare-event protection

Convex and tail-dependent profiles cannot be pruned before minimum independent opportunity and event counts.

### Audit

Every pruned trial retains reason, observations, scheduler state, and counterfactual eligibility.

## Input contracts

- `TrialManifest`
- `FidelitySchedule`
- `ProfileObjective`

## Output contracts

- `PruningDecision`
- `SchedulerState`
- `FidelityAudit`

## Measurement framework

- Compute saved.
- False-prune estimate.
- Profile-specific survival.
- Final rank correlation.

## Adversarial questions

- Does early stopping favor high win rate over convexity?
- Are cheap approximations rank-preserving?
- Did scheduler observe validation roles too often?

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

- [[Compute_Fabric_And_Schedulers]]
