---
title: Uncertainty Decomposition
status: canonical
version: 2.0.0
created: '2026-07-13'
updated: '2026-07-13'
tags:
- saed-v2
- core-production
---

# Purpose

Separate aleatoric, epistemic, data-quality, simulation, execution, and policy uncertainty so the system can respond correctly.

## Capability tier

**Core Production**

## System design

### Aleatoric

Irreducible path and outcome variation conditional on known state.

### Epistemic

Model and parameter uncertainty from limited support.

### Data uncertainty

Missing, stale, corrected, or conflicting inputs.

### Simulator uncertainty

Fill, path ordering, broker, and counterfactual-model uncertainty.

### Policy uncertainty

Instability of candidate ranks or decisions across models, folds, seeds, and assumptions.

## Input contracts

- `ModelPredictions`
- `DataQualityState`
- `SimulationScenarios`

## Output contracts

- `UncertaintyBundle`
- `UncertaintyAttribution`
- `DecisionConstraints`

## Measurement framework

- Uncertainty calibration.
- Decision sensitivity.
- Source attribution.
- Abstention effectiveness.

## Adversarial questions

- Is all uncertainty reduced to one confidence score?
- Does ensemble disagreement miss shared bias?
- Are simulator assumptions excluded from confidence?

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

- [[Deep_Ensembles_And_Bayesian_Challengers]]
