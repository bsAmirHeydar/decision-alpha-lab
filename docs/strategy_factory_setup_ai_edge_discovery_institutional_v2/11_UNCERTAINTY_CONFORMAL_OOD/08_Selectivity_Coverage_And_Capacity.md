---
title: Selectivity, Coverage and Capacity
status: canonical
version: 2.0.0
created: '2026-07-13'
updated: '2026-07-13'
tags:
- saed-v2
- core-production
---

# Purpose

Optimize how often the system acts while preserving conditional risk, economic opportunity, and portfolio capacity.

## Capability tier

**Core Production**

## System design

### Coverage curve

Opportunity coverage versus selective risk and net utility.

### Capacity coupling

Higher coverage may exceed symbol, liquidity, or portfolio capacity; selection is evaluated at deployable scale.

### Subgroup floors

A strong aggregate cannot hide unsafe coverage in a context, regime, broker, or profile subgroup.

### Business objective

Coverage is a constrained portfolio input, not a vanity metric.

## Input contracts

- `CalibratedPolicyScores`
- `CapacityCurves`
- `SubgroupDefinitions`

## Output contracts

- `CoveragePolicy`
- `SelectiveRiskReport`
- `CapacityAwareThresholds`

## Measurement framework

- Coverage-risk frontier.
- Net utility by coverage.
- Capacity utilization.
- Worst-subgroup risk.

## Adversarial questions

- Does the model cherry-pick a tiny easy subset?
- Does higher coverage crowd out better portfolio opportunities?
- Are abstentions concentrated in a hidden failure group?

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
