---
title: Capital and Risk Handoff
status: canonical
version: 4.0.0
created: '2026-07-13'
updated: '2026-07-13'
tags:
- saed-v4
- core-production
---

# Purpose

Keep setup edge discovery separate from capital policy while providing the distributions and constraints needed for safe sizing.

## Capability tier

**Core Production**

## System design

### Trainer output

Outcome distribution, tail loss, uncertainty, capacity, holding time, and support.

### Capital policy

Fixed cash, fractional, volatility, drawdown-responsive, quality-scaled, or fractional-Kelly variants are separately validated.

### Hard limits

AI suggestions cannot override maximum cash loss, portfolio budget, margin, or kill switches.

### Attribution

Edge value and capital-policy value are reported separately.

## Input contracts

- `OutcomeDistribution`
- `UncertaintyBundle`
- `CapacityCurve`

## Output contracts

- `RiskRequest`
- `CapitalEligibility`
- `SizingInputs`

## Measurement framework

- Sizing sensitivity.
- Ruin and recovery distribution.
- Drawdown contribution.
- Capital-policy incremental value.

## Adversarial questions

- Is money management manufacturing apparent edge?
- Does uncertainty shrink position size consistently?
- Can capital policy use unavailable future volatility?

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

- [[Portfolio_Aware_Objectives]]
