---
title: Dreamer and TD-MPC-Style Challengers
status: canonical
version: 4.0.0
created: '2026-07-13'
updated: '2026-07-13'
tags:
- saed-v4
- research-only
---

# Purpose

Study latent imagination and model-predictive control for bounded trail and management research while preserving conservative offline boundaries.

## Capability tier

**Research-Only**

## System design

### Action lattice

Only compiler-approved management transitions are available.

### Offline training

No environment interaction with live capital; historical/replay trajectories only.

### Model-error penalty

Planning objective includes ensemble disagreement, support distance, and conservative value penalties.

### Benchmark

Compare against fixed state machines, dynamic programming on replay, and supervised policy selection.

## Input contracts

- `WorldModel`
- `BoundedActionLattice`
- `OfflineTrajectories`

## Output contracts

- `ResearchPolicy`
- `PlanningTrace`
- `ModelExploitationReport`

## Measurement framework

- Offline policy value.
- Support violation rate.
- Model exploitation diagnostics.
- Stress robustness.

## Adversarial questions

- Does the agent discover simulator bugs?
- Can imagined rollouts enter unsupported states?
- Does value improve only under the learned model?

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

- [[Conservative_Offline_RL]]
