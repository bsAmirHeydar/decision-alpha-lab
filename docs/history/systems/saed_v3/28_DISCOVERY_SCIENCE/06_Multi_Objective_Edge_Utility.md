---
title: Multi-Objective Edge Utility
status: canonical
version: 3.0.0
created: '2026-07-13'
updated: '2026-07-13'
capability_tier: core-production
tags:
  - saed-v3
---

# Mission

Evaluate setup candidates using an explicit vector of economic value, uncertainty, tails, capacity, stability, complexity, and portfolio contribution.

## Why this component exists

- None declared.

## Authority and safety boundary

- This component may estimate, rank, simulate, challenge, or recommend only inside a declared research scope.
- It cannot create canonical Context truth, modify protected evidence roles, sign promotion, change portfolio risk, activate runtime generations, access live credentials, or place orders.
- Unsupported, stale, contradictory, OOD, hash-mismatched, uncalibrated, or incomplete paths resolve to **Skip**, **Abstain**, **Manual fallback**, **Reject**, or **Quarantine**.
- Every result is subordinate to UCEE I12 promotion admission, I13 authority/fallback, I14 immutable runtime, I17 portfolio/risk, and I18 release qualification.

## Input contracts

- Outcome distributions.
- Uncertainty bounds.
- Capacity and portfolio diagnostics.

## Output contracts

- Objective vector.
- Pareto frontier.
- Governed scalar decision score.

## Algorithmic design

- Maintain raw objective vector before scalarization.
- Use lower confidence bounds and expected shortfall penalties.
- Penalize turnover, capital occupancy, fragility, model concentration, and operational complexity.
- Apply payoff-profile-specific constraints before common economic comparison.

## Formal objective and constraints

```text
score = LCB(net_utility) - λ_ES*ES - λ_cap*capacity_cost - λ_complex*complexity - λ_fragile*fragility
```

## Data and known-time semantics

- None declared.

## Anti-overfit and model-risk controls

- Weights and constraints freeze before protected evaluation.
- No aggregate score may hide hard limit violation.
- Pareto dominated candidates rejected.

## Measurement system

- Lower-bound net utility.
- Expected shortfall.
- Capacity-adjusted return.
- Stability.
- Complexity cost.
- Marginal portfolio utility.

## Scalability and operating model

- None declared.

## Adversarial failure modes

- Sharpe-only ranking.
- High win rate hides tail loss.
- Convex strategy rejected only for low win rate.
- Complex model wins by tiny unstable gain.

## UCEE integration

- None declared.

## Required tests and evidence

- Weight sensitivity.
- Pareto stability.
- Hard-constraint mutation.
- Best-period removal.

## Implementation slices

- None declared.

## Decision record

- None declared.

## Acceptance gate

The component is accepted only when its contracts are closed and versioned, all lineage and role boundaries are reconstructible, protected evaluation remains unexposed, negative and mutation tests pass, simpler baselines remain available, and an independent reviewer can reproduce the decision-equivalent result from immutable hashes.

## Related notes

- [[Multi_Objective_Utility_And_Pareto_Governance]]
- [[Payoff_Profile_Specific_Estimands]]
