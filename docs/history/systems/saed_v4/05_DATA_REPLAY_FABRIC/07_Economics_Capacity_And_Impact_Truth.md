---
title: Economics, Capacity and Impact Truth
status: canonical
version: 4.0.0
created: '2026-07-13'
updated: '2026-07-13'
tags:
- saed-v4
- core-production
---

# Purpose

Make all model selection sensitive to executable costs, fill constraints, capital use, and scale.

## Capability tier

**Core Production**

## System design

### Cost stack

Spread, commission, slippage, swap, reject cost, cancellation, partial fill, latency, and financing.

### Capacity model

Volume, participation, market depth proxies, symbol limits, portfolio concentration, and expected fill degradation.

### Scenario lattice

Base, stressed, severe, broker-specific, and scale-specific economics are frozen before selection.

### Utility integration

Costs and capital-time are row-level inputs to outcome and policy value, not a final cosmetic haircut.

## Input contracts

- `BrokerProfile`
- `CostModel`
- `CapacityModel`
- `OutcomeCube`

## Output contracts

- `NetOutcomeCube`
- `CapacityCurve`
- `CostStressReport`

## Measurement framework

- Net/gross edge ratio.
- Cost breakeven.
- Capacity curve.
- Impact sensitivity.
- Capital-time return.

## Adversarial questions

- Does an edge vanish at realistic size?
- Are costs learned from the same test period?
- Is execution capacity confused with statistical confidence?

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
