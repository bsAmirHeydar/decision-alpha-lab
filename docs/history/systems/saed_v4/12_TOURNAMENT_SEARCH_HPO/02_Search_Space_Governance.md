---
title: Search Space Governance
status: canonical
version: 4.0.0
created: '2026-07-13'
updated: '2026-07-13'
tags:
- saed-v4
- core-production
---

# Purpose

Declare every tunable dimension, prior, conditional dependency, and budget before execution.

## Capability tier

**Core Production**

## System design

### Typed domains

Continuous, discrete, categorical, conditional, architecture, and data-transformation parameters.

### Semantic bounds

Bounds come from market, execution, risk, and runtime feasibility rather than arbitrary wide ranges.

### Conditional graph

Only compatible parameters activate; inactive dimensions are not counted as hidden trials.

### Freeze discipline

Search space changes create a new experiment family and multiplicity scope.

## Input contracts

- `SearchSpaceManifest`
- `CompatibilityGraph`
- `BudgetPolicy`

## Output contracts

- `CompiledSearchSpace`
- `SearchSpaceHash`
- `ChangeLedger`

## Measurement framework

- Effective search volume.
- Parameter activation frequency.
- Boundary concentration.
- Duplicate trials.

## Adversarial questions

- Are bounds selected after seeing promising regions?
- Are manual experiments outside the registry?
- Can a failed trial disappear?

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

- [[Complete_Trial_And_Exposure_Ledger]]
