---
title: Regime Specialists and Mixture of Experts
status: canonical
version: 4.0.0
created: '2026-07-13'
updated: '2026-07-13'
tags:
- saed-v4
- governed-challenger
---

# Purpose

Route opportunities to specialists only when regime definitions and router support are known-time, stable, and independently validated.

## Capability tier

**Governed Challenger**

## System design

### Regime sources

Exogenous doctrine, unsupervised states fitted only in training roles, or bounded learned routing.

### Specialist models

Each specialist has support minimums, calibration, and fallback to a generalist.

### Router uncertainty

Low-confidence routing triggers generalist or abstention.

### Regime transition

Hysteresis and minimum dwell prevent rapid unsupported switching.

## Input contracts

- `RegimeSnapshot`
- `GeneralistModel`
- `ExpertRegistry`

## Output contracts

- `ExpertChoice`
- `RoutingUncertainty`
- `SpecialistDecision`

## Measurement framework

- Router accuracy is secondary to policy utility.
- Worst-regime loss.
- Fallback rate.
- Transition stability.

## Adversarial questions

- Is regime defined from future returns?
- Are specialist sample sizes illusory due to dependence?
- Does routing amplify drawdown in transitions?

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

- [[Sparse_Mixture_Of_Experts]]
