---
title: Run the Conservative Offline Policy Challenge
status: canonical
version: 4.0.0
created: '2026-07-13'
updated: '2026-07-13'
capability_tier: canonical
tags:
  - saed-v4
  - runbook
  - operations
---

# Mission

Train and evaluate bounded sequential policies without online exploration or live authority.

## Entry conditions

- Finite action lattice.
- Behavior/support model.
- Reward/cost contract.

## Mandatory roles and separation of duties

- Offline RL researcher.
- Risk engineer.
- Independent OPE reviewer.

## Procedure

1. Train behavior cloning.
2. Train conservative/pessimistic candidates.
3. Project actions through compiler.
4. Evaluate with multiple OPE methods and behavior divergence.
5. Run reward, support, and constraint stress.
6. Compare against non-RL selector.

## Mandatory outputs

- Policy candidates.
- OPE disagreement report.
- Constraint and support dossier.

## Stop and escalation conditions

- Unsupported action.
- OPE methods disagree materially.
- Sequential abstraction invalid.
- No uplift over simpler selector.

## Evidence retained

- Policy/checkpoint hashes.
- OPE artifacts.
- Action traces.

## Completion gate

The runbook is complete only when all required artifacts are content-addressed, all exposures and deviations are recorded, an independent reviewer signs the completion state, and the downstream UCEE gate accepts the exact immutable bundle rather than a narrative summary.

## Related notes

- [[Conservative_Offline_Policy_Optimization_V3]]
- [[Safe_Offline_RL_Research_Register]]
