---
title: Institutional Trainer Task Graph
status: canonical
version: 3.0.0
created: '2026-07-13'
updated: '2026-07-13'
tags:
- saed-v3
- core-production
---

# Purpose

Decompose edge discovery into auditable prediction and decision tasks rather than one opaque end-to-end trade model.

## Capability tier

**Core Production**

## System design

### Shared encoder

Optional representation shared across tasks under gradient and leakage controls.

### Task heads

Eligibility, trigger/fill, competing risks, outcome distribution, treatment ranking, selection, trail suitability, uncertainty, and novelty.

### Dependency DAG

Upstream task outputs may be features only when generated out-of-fold and role-safe.

### Joint versus staged training

Every multi-task model is challenged against independently trained heads to detect negative transfer.

## Input contracts

- `TrainerProgramManifest`
- `DatasetManifest`
- `TaskDependencies`

## Output contracts

- `TaskModels`
- `OutOfFoldPredictions`
- `TaskAttribution`

## Measurement framework

- Task-level calibration.
- Incremental decision utility.
- Negative-transfer diagnostics.
- Head disagreement.

## Adversarial questions

- Does one easy task dominate the shared encoder?
- Are predicted features generated in-sample?
- Does end-to-end loss obscure economic failure?

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

- [[Multi_Task_Loss_And_Gradient_Governance]]
