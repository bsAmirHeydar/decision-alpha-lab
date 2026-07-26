---
title: Active Experiment Planner
status: canonical
version: 2.0.0
created: '2026-07-13'
updated: '2026-07-13'
tags:
- saed-v2
- research-only
---

# Purpose

Rank proposed experiments by expected information, economic, diversification, reuse, and falsification value under resource and false-discovery constraints.

## Capability tier

**Research-Only**

## System design

### Candidate experiments

New context, treatment, feature view, model family, causal test, stress test, or prospective extension.

### Value components

Information gain, expected economic upside, uncertainty reduction, portfolio gap, artifact reuse, cost, time, and selection risk.

### Constraints

Compute, data access, reviewer capacity, prospective time, and program concentration.

### Authority

Planner recommends; humans approve budgets and data-role access.

## Input contracts

- `ResearchBacklog`
- `MemoryGraph`
- `ResourceState`

## Output contracts

- `ExperimentPriorities`
- `ValueDecomposition`
- `BudgetRecommendations`

## Measurement framework

- Realized versus predicted information gain.
- Promotion yield.
- Portfolio coverage improvement.
- Cost efficiency.

## Adversarial questions

- Does the planner exploit noisy early results?
- Does novelty crowd out replication?
- Can it allocate protected-data access automatically?

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

- [[Program_Level_Resource_Allocation]]
