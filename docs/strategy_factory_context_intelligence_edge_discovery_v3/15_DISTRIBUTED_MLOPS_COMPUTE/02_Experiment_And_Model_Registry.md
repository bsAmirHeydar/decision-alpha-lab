---
title: Experiment and Model Registry
status: canonical
version: 3.0.0
created: '2026-07-13'
updated: '2026-07-13'
tags:
- saed-v3
- core-production
---

# Purpose

Create one authoritative registry for programs, trials, models, calibration, policies, evidence, and lifecycle state.

## Capability tier

**Core Production**

## System design

### Experiment identity

Program, hypothesis, search family, treatment universe, data roles, code, environment, and budget.

### Model identity

Architecture, parameters, training run, folds, features, calibration, capability tier, export, and support.

### Lifecycle

Research, challenger, challenged, promoted, shadow, active, reduced, quarantined, retired, revoked.

### Queries

Reproduce, compare, trace ancestors, find descendants, detect duplicates, and retrieve failure memory.

## Input contracts

- `RunArtifacts`
- `ModelCards`
- `PromotionDecisions`

## Output contracts

- `RegistryRecords`
- `LineageQueries`
- `LifecycleEvents`

## Measurement framework

- Registry completeness.
- Duplicate detection.
- Reproduction success.
- Lifecycle consistency.

## Adversarial questions

- Can notebook files bypass the registry?
- Are model and calibration versions separable?
- Does retirement preserve lineage?

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

- [[Research_Memory_Graph]]
