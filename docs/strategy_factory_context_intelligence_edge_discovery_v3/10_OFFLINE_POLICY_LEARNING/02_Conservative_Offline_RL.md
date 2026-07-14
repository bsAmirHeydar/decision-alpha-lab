---
title: Conservative Offline Reinforcement Learning
status: canonical
version: 3.0.0
created: '2026-07-13'
updated: '2026-07-13'
tags:
- saed-v3
- research-only
---

# Purpose

Evaluate CQL-, IQL-, and conservative value-learning approaches for path-dependent management while penalizing out-of-distribution actions.

## Capability tier

**Research-Only**

## System design

### CQL-style control

Conservative value estimates lower unsupported action values.

### IQL-style control

Avoid explicit maximization over unseen actions and extract policies from expectile-weighted advantages.

### Action masks

Treatment state machine and risk policy define valid actions at every state.

### Evaluation

Fitted Q evaluation, DR off-policy evaluation, replay, and stress tests must agree directionally.

## Input contracts

- `OfflineTrajectories`
- `RewardContract`
- `ActionMasks`

## Output contracts

- `ValueModel`
- `ConservativePolicy`
- `OPEReport`

## Measurement framework

- Conservative policy value.
- OOD action rate.
- Q calibration.
- Policy stability across seeds and penalties.

## Adversarial questions

- Does value increase by exploiting reward or simulator defects?
- Are behavior propensities estimable?
- Does policy collapse when costs are stressed?

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

- [[Decision_Transformer_And_Sequence_Policies]]
