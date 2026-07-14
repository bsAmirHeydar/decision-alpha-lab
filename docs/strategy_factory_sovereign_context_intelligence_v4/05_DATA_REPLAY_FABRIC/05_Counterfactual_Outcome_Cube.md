---
title: Counterfactual Outcome Cube
status: canonical
version: 4.0.0
created: '2026-07-13'
updated: '2026-07-13'
tags:
- saed-v4
- core-production
---

# Purpose

Evaluate every compiler-approved sibling treatment on the same context occurrence and market path.

## Capability tier

**Core Production**

## System design

### Cube axes

Occurrence, candidate treatment, path resolution, economics scenario, broker profile, and stress scenario.

### Outcome dimensions

Trigger, fill, stop/target/trail events, MFE, MAE, holding time, gross/net return, utility, capital time, and censoring.

### Counterfactual discipline

The cube represents policy alternatives under a declared simulator; it does not claim causal identification without overlap and assumptions.

### Materialization

Partitioned, content-addressed outputs support deterministic incremental rebuilds.

## Input contracts

- `TreatmentUniverseManifest`
- `ReplayManifest`
- `EconomicsScenarioSet`

## Output contracts

- `OutcomeCubeManifest`
- `TreatmentOutcomeRows`
- `SimulationFailures`

## Measurement framework

- Candidate coverage.
- Simulator completeness.
- Censoring rate.
- Economic scenario sensitivity.

## Adversarial questions

- Are unrealistic counterfactuals treated as observed?
- Can treatment-specific data availability bias comparisons?
- Does the cube omit failed simulation paths?

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

- [[Causal_Identification_And_Assumptions]]
