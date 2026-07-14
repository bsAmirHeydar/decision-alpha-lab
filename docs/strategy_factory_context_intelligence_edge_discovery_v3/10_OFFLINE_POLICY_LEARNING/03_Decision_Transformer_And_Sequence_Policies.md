---
title: Decision Transformer and Sequence Policies
status: canonical
version: 3.0.0
created: '2026-07-13'
updated: '2026-07-13'
tags:
- saed-v3
- research-only
---

# Purpose

Study return-conditioned sequence policies as research challengers for bounded treatment and management trajectories.

## Capability tier

**Research-Only**

## System design

### Trajectory tokens

State, action, reward, time, context, treatment, and remaining-risk tokens.

### Return conditioning

Targets are bounded, achievable, and stress-tested; impossible returns cannot become action requests.

### Action projection

Every generated action is projected into the valid state-machine action set.

### Interpretation

Attention and nearest-trajectory analysis identify whether the policy is copying rare winners.

## Input contracts

- `TrajectoryDataset`
- `ReturnTargets`
- `ActionVocabulary`

## Output contracts

- `SequencePolicy`
- `ActionTrace`
- `MemorizationAudit`

## Measurement framework

- Offline return.
- Action validity.
- Rare-trajectory dependence.
- Conditioning sensitivity.

## Adversarial questions

- Does high return conditioning select unsupported winner paths?
- Does the model memorize exact episodes?
- Can tokenization leak future trajectory length?

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

- [[Offline_Policy_Learning_Boundary]]
