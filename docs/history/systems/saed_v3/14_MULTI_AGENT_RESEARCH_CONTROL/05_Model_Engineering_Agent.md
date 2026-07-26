---
title: Model Engineering Agent
status: canonical
version: 3.0.0
created: '2026-07-13'
updated: '2026-07-13'
tags:
- saed-v3
- governed-challenger
---

# Purpose

Implement and benchmark models inside approved capability tiers, budgets, folds, and environments.

## Capability tier

**Governed Challenger**

## System design

### Responsibilities

Training code, baselines, advanced challengers, calibration, export, latency, model cards, and ablations.

### Restrictions

Cannot alter context, treatment universe, outcomes, data roles, objective profile, or promotion criteria.

### Code quality

Typed configs, deterministic seeds, test coverage, resource logging, and content-addressed outputs.

### Escalation

Any need to expand scope creates a review request rather than an ad hoc experiment.

## Input contracts

- `TrainerProgram`
- `CapabilityPolicy`
- `ComputeBudget`

## Output contracts

- `ModelArtifacts`
- `ModelCards`
- `BenchmarkReport`

## Measurement framework

- Baseline completeness.
- Reproducibility.
- Compute efficiency.
- Ablation quality.
- Export success.

## Adversarial questions

- Does the agent optimize visible final metrics?
- Are failed models retained?
- Are dependency upgrades reviewed?

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

- [[Model_Ladder_And_Champion_Challenger]]
