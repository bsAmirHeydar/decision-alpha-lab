---
title: Payoff-Profile-Specific Estimands
status: canonical
version: 3.0.0
created: '2026-07-13'
updated: '2026-07-13'
capability_tier: core-production
tags:
  - saed-v3
---

# Mission

Define distinct scientific targets for wide high-hit, tight convex fixed, tight convex trail, wide open trail, and tight high-hit profiles.

## Why this component exists

- None declared.

## Authority and safety boundary

- This component may estimate, rank, simulate, challenge, or recommend only inside a declared research scope.
- It cannot create canonical Context truth, modify protected evidence roles, sign promotion, change portfolio risk, activate runtime generations, access live credentials, or place orders.
- Unsupported, stale, contradictory, OOD, hash-mismatched, uncalibrated, or incomplete paths resolve to **Skip**, **Abstain**, **Manual fallback**, **Reject**, or **Quarantine**.
- Every result is subordinate to UCEE I12 promotion admission, I13 authority/fallback, I14 immutable runtime, I17 portfolio/risk, and I18 release qualification.

## Input contracts

- Payoff profile registry.
- Outcome cube.

## Output contracts

- Profile-specific estimand card.
- Profile-specific gate metrics.

## Algorithmic design

- P1 estimates hit rate subject to net reward floor, tail and capital constraints.
- P2 estimates right-tail utility and destination reach under tight loss.
- P3 estimates path-dependent tail capture and trail robustness.
- P4 estimates trend persistence, occupancy, and open-tail capture under wide survival.
- P5 estimates execution-robust hit rate with tight stop and reward floor.


## Data and known-time semantics

- None declared.

## Anti-overfit and model-risk controls

- Profiles cannot share one naive objective.
- Reward floor evaluated after cost.
- Profile comparison occurs only after internal constraints pass.

## Measurement system

- Profile-specific primary and guardrail metrics.
- Cross-profile economic utility.
- Profile instability by regime.

## Scalability and operating model

- None declared.

## Adversarial failure modes

- Optimize all profiles for win rate.
- Trail and fixed exit labels mixed.
- Tight stop evaluated on mid-price.

## UCEE integration

- None declared.

## Required tests and evidence

- Objective swap mutation.
- Cost-adjusted reward-floor test.
- Profile label consistency.

## Implementation slices

- None declared.

## Decision record

- None declared.

## Acceptance gate

The component is accepted only when its contracts are closed and versioned, all lineage and role boundaries are reconstructible, protected evaluation remains unexposed, negative and mutation tests pass, simpler baselines remain available, and an independent reviewer can reproduce the decision-equivalent result from immutable hashes.

## Related notes

- [[Multi_Objective_Edge_Utility]]
- [[Payoff_Profile_Registry]]
