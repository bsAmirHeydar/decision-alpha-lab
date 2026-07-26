---
title: Conservative Offline Policy Optimization V3
status: canonical
version: 4.0.0
created: '2026-07-13'
updated: '2026-07-13'
capability_tier: core-production
tags:
  - saed-v4
---

# Mission

Learn bounded treatment-selection policies from static data while penalizing unsupported actions and preserving hard constraints.

## Why this component exists

- None declared.

## Authority and safety boundary

- This component may estimate, rank, simulate, challenge, or recommend only inside a declared research scope.
- It cannot create canonical Context truth, modify protected evidence roles, sign promotion, change portfolio risk, activate runtime generations, access live credentials, or place orders.
- Unsupported, stale, contradictory, OOD, hash-mismatched, uncalibrated, or incomplete paths resolve to **Skip**, **Abstain**, **Manual fallback**, **Reject**, or **Quarantine**.
- Every result is subordinate to UCEE I12 promotion admission, I13 authority/fallback, I14 immutable runtime, I17 portfolio/risk, and I18 release qualification.

## Input contracts

- Finite treatment MDP/POMDP abstraction.
- Behavior/support model.
- Reward and cost definitions.

## Output contracts

- Conservative challenger policy.
- OPE and constraint dossier.

## Algorithmic design

- Behavior cloning baseline, conservative Q/value methods, implicit policy extraction, safe policy switching, and pessimistic lower bounds.
- Project all actions through treatment compiler and risk-independent constraints.
- Evaluate with multiple OPE estimators and stress tests.


## Data and known-time semantics

- None declared.

## Anti-overfit and model-risk controls

- No online exploration.
- No continuous unbounded order action.
- No direct risk or capital action.
- OPE alone cannot promote.

## Measurement system

- Lower-bound policy value.
- Behavior divergence.
- Constraint violation.
- Support-weighted regret.

## Scalability and operating model

- None declared.

## Adversarial failure modes

- Policy selects rare high-Q action.
- Reward shaping hides tail risk.
- Sequential abstraction invents Markov property.

## UCEE integration

- None declared.

## Required tests and evidence

- Behavior-policy holdout.
- Action-support removal.
- Reward perturbation.
- OPE disagreement.

## Implementation slices

- None declared.

## Decision record

- None declared.

## Acceptance gate

The component is accepted only when its contracts are closed and versioned, all lineage and role boundaries are reconstructible, protected evaluation remains unexposed, negative and mutation tests pass, simpler baselines remain available, and an independent reviewer can reproduce the decision-equivalent result from immutable hashes.

## Related notes

- [[Conservative_Offline_Policy_Learning]]
- [[Safe_Offline_RL_Research_Register]]
