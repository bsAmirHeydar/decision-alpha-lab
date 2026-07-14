---
title: Program-Level Resource Allocation
status: canonical
version: 3.0.0
created: '2026-07-13'
updated: '2026-07-13'
tags:
- saed-v3
- core-production
---

# Purpose

Allocate research capital to experiments with the highest expected information and economic value rather than the loudest hypothesis.

## Capability tier

**Core Production**

## System design

### Program portfolio

Context programs compete for compute, data engineering, review, and prospective-paper capacity.

### Value model

Expected information gain, economic upside, reuse, diversification, uncertainty, cost, and false-discovery risk.

### Stage gates

Small exploratory budgets precede expensive model and prospective stages.

### Stop rules

Programs can be retired for lack of support, poor economics, redundancy, or operational infeasibility.

## Input contracts

- `ResearchProgramBacklog`
- `ProgramEvidence`
- `ResourcePrices`

## Output contracts

- `ProgramPriorities`
- `BudgetAllocations`
- `StopDecisions`

## Measurement framework

- Information gain per cost.
- Promotion yield.
- Reused artifacts.
- Program concentration.

## Adversarial questions

- Is resource allocation biased by recent winners?
- Are sunk costs driving continuation?
- Does compute scale outrun evidence quality?

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

- [[Active_Experiment_Planner]]
