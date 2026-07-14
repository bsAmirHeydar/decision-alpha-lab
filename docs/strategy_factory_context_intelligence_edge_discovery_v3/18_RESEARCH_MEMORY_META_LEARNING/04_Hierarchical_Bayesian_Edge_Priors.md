---
title: Hierarchical Bayesian Edge Priors
status: canonical
version: 3.0.0
created: '2026-07-13'
updated: '2026-07-13'
tags:
- saed-v3
- governed-challenger
---

# Purpose

Pool evidence across related contexts, treatments, symbols, and regimes without pretending they are identical.

## Capability tier

**Governed Challenger**

## System design

### Hierarchy

Global, context family, payoff profile, treatment family, market, and local occurrence-level parameters.

### Partial pooling

Shrink noisy local estimates toward evidence-weighted group priors.

### Prior governance

Priors are versioned, source-backed, and selected without protected-target outcomes.

### Decision use

Posterior lower bounds and prior sensitivity inform research prioritization and conservative policy selection.

## Input contracts

- `HistoricalPrograms`
- `EdgeGenomes`
- `HierarchyDefinition`

## Output contracts

- `PosteriorEdgeEstimates`
- `PriorCard`
- `SensitivityReport`

## Measurement framework

- Posterior calibration.
- Shrinkage benefit.
- Prior sensitivity.
- Local effective sample size.

## Adversarial questions

- Are priors contaminated by selected winners?
- Does pooling erase genuine heterogeneity?
- Can a strong prior overpower new adverse evidence?

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

- [[Causal_Transport_And_Domain_Shift]]
