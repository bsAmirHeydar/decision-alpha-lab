---
title: Multiplicity, PBO and Deflated Performance
status: canonical
version: 4.0.0
created: '2026-07-13'
updated: '2026-07-13'
tags:
- saed-v4
- core-production
---

# Purpose

Adjust confidence for the number, dependence, and selection process of strategies, models, thresholds, and human iterations.

## Capability tier

**Core Production**

## System design

### Multiplicity universe

All material variants, seeds, transformations, treatments, hypotheses, and exposures.

### PBO/CSCV

Estimate the probability that in-sample winners underperform out of sample.

### Deflated metrics

Adjust Sharpe-like evidence for non-normality and multiple trials.

### Hierarchical correction

Correct within and across context, profile, treatment, and model families.

## Input contracts

- `TrialLedger`
- `ExposureLedger`
- `FoldResults`

## Output contracts

- `MultiplicityReport`
- `PBOReport`
- `DeflatedMetrics`

## Measurement framework

- Effective number of trials.
- PBO.
- Deflated performance.
- False discovery control.

## Adversarial questions

- Are correlated trials counted as one without evidence?
- Are failed trials missing?
- Is a favorable metric selected after seeing results?

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

- [[Reality_Check_SPA_And_Null_Program]]
