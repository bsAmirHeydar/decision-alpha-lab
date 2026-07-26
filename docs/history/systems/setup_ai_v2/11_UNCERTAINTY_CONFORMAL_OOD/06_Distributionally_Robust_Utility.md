---
title: Distributionally Robust Utility
status: canonical
version: 2.0.0
created: '2026-07-13'
updated: '2026-07-13'
tags:
- saed-v2
- governed-challenger
---

# Purpose

Select treatments that retain utility under plausible distribution, cost, and dependence perturbations.

## Capability tier

**Governed Challenger**

## System design

### Ambiguity sets

Empirical divergence balls, Wasserstein neighborhoods, scenario sets, moment/tail constraints, and domain mixtures.

### Robust objective

Worst-case or penalized expected utility with CVaR, capacity, and coverage constraints.

### Calibration

Ambiguity size is selected inside nested validation and stress evidence, not tuned to the final test.

### Interpretation

Robustness cost is reported as the gap between nominal and robust utility.

## Input contracts

- `OutcomeScenarios`
- `DomainWeights`
- `RiskConstraints`

## Output contracts

- `RobustCandidateUtility`
- `WorstCaseScenario`
- `RobustnessReport`

## Measurement framework

- Robust lower-bound utility.
- Sensitivity to ambiguity size.
- Worst-domain performance.
- Conservatism cost.

## Adversarial questions

- Is ambiguity too small to matter or too large to trade?
- Does DRO simply encode arbitrary pessimism?
- Are dependence shifts represented?

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

- [[Objective_Functions_And_Constraint_System]]
