---
title: Bayesian Optimization and Pareto Search
status: canonical
version: 3.0.0
created: '2026-07-13'
updated: '2026-07-13'
tags:
- saed-v3
- governed-challenger
---

# Purpose

Use sample-efficient search while respecting mixed spaces, noise, constraints, and multiple economic objectives.

## Capability tier

**Governed Challenger**

## System design

### Surrogates

Gaussian-process, tree-structured, random-forest, or neural surrogates chosen by space structure.

### Constraints

Hard feasibility and probabilistic constraints are modelled separately from objectives.

### Pareto objectives

Net utility, expected shortfall, drawdown, capacity, coverage, latency, and model risk.

### Batch search

Acquisition accounts for parallelism, duplicate avoidance, and pending trials.

## Input contracts

- `SearchObservations`
- `ConstraintModels`
- `ObjectiveProfiles`

## Output contracts

- `SuggestedTrials`
- `ParetoFront`
- `SearchAudit`

## Measurement framework

- Hypervolume on validation roles.
- Constraint violation.
- Surrogate calibration.
- Search efficiency.

## Adversarial questions

- Does the acquisition overexploit noisy winners?
- Were Pareto preferences set after results?
- Is model risk treated as a soft cosmetic metric?

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

- [[Hierarchical_Tournament_Architecture]]
