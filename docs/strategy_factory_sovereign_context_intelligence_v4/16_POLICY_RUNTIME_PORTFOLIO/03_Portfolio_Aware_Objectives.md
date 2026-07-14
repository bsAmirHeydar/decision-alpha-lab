---
title: Portfolio-Aware Objectives
status: canonical
version: 4.0.0
created: '2026-07-13'
updated: '2026-07-13'
tags:
- saed-v4
- core-production
---

# Purpose

Evaluate setup policies by marginal portfolio value rather than standalone return alone.

## Capability tier

**Core Production**

## System design

### Marginal value

Incremental expected utility after dependence, concentration, risk reservation, capacity, and opportunity competition.

### Opportunity cost

Selecting one candidate may displace a better opportunity or consume scarce symbol/currency risk.

### Portfolio scenarios

Context-drop, correlation shock, capacity haircut, simultaneous signals, and regime concentration.

### Training boundary

Portfolio-aware labels and objectives are computed from training roles without allowing future portfolio state leakage.

## Input contracts

- `CandidateUtility`
- `DependenceModel`
- `RiskBudgets`
- `Capacity`

## Output contracts

- `PortfolioAdjustedScore`
- `MarginalRisk`
- `AllocationFeatures`

## Measurement framework

- Marginal risk-adjusted utility.
- Diversification contribution.
- Displacement regret.
- Capacity utilization.

## Adversarial questions

- Does standalone alpha disappear in a portfolio?
- Are correlations estimated with future data?
- Does training optimize against one fixed portfolio composition?

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

- [[Edge_Genome]]
