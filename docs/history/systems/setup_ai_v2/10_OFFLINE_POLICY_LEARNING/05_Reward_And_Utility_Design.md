---
title: Reward and Utility Design
status: canonical
version: 2.0.0
created: '2026-07-13'
updated: '2026-07-13'
tags:
- saed-v2
- core-production
---

# Purpose

Define decomposable economic utility that cannot be gamed by a policy learner.

## Capability tier

**Core Production**

## System design

### Reward components

Realized net P&L, expected shortfall penalty, capital occupancy, turnover, slippage, drawdown contribution, concentration, and operational incidents.

### Temporal allocation

Intermediate rewards reflect actual economics, not future-derived shaping.

### Profile alignment

P1–P5 have different objective constraints but map to a common capital-aware utility.

### Anti-gaming

Reward audits test stop avoidance, delayed loss recognition, excessive holding, and tail-risk hiding.

## Input contracts

- `EconomicsContract`
- `RiskPolicy`
- `ProfileObjective`

## Output contracts

- `RewardFunctionVersion`
- `RewardAudit`
- `UtilityTrace`

## Measurement framework

- Reward-component attribution.
- Policy sensitivity to weights.
- Tail outcomes.
- Capital-time utility.

## Adversarial questions

- Can the agent avoid terminal losses by never closing?
- Does mark-to-market reward favor churn?
- Are utility weights selected on final performance?

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
