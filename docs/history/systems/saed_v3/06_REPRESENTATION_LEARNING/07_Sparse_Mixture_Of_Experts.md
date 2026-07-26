---
title: Sparse Mixture of Experts
status: canonical
version: 3.0.0
created: '2026-07-13'
updated: '2026-07-13'
tags:
- saed-v3
- governed-challenger
---

# Purpose

Use sparse experts to model heterogeneous regimes and context families while preventing router collapse and unsupported specialization.

## Capability tier

**Governed Challenger**

## System design

### Expert domains

Payoff profile, context family, regime, market microstructure, horizon, or treatment family.

### Router constraints

Known-time features only, load balancing, entropy floors, minimum support, and deterministic fallback.

### Expert admission

Each expert must satisfy independent support, calibration, and stability gates; a strong aggregate cannot hide a dangerous specialist.

### Runtime strategy

Only exportable bounded MoE variants can become Tier B challengers; larger research MoE remains offline.

## Input contracts

- `ExpertRegistry`
- `RouterFeatures`
- `SupportThresholds`

## Output contracts

- `ExpertOutputs`
- `RoutingTrace`
- `MoERiskReport`

## Measurement framework

- Per-expert effective sample size.
- Router calibration.
- Load balance.
- Worst-expert risk.
- Fallback frequency.

## Adversarial questions

- Does router infer regime from future path?
- Do rare experts overfit tiny samples?
- Does aggregate utility conceal expert tail failures?

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

- [[Regime_Specialists_And_Mixture_Of_Experts]]
