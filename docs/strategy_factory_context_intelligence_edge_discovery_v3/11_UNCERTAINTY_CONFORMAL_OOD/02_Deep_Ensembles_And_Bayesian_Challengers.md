---
title: Deep Ensembles and Bayesian Challengers
status: canonical
version: 3.0.0
created: '2026-07-13'
updated: '2026-07-13'
tags:
- saed-v3
- governed-challenger
---

# Purpose

Use model diversity and posterior approximations to estimate epistemic uncertainty without pretending they provide complete guarantees.

## Capability tier

**Governed Challenger**

## System design

### Deep ensembles

Independent seeds, bootstraps, architectures, and data perturbations with diversity diagnostics.

### Bayesian approximations

Laplace, variational, dropout, or Bayesian last-layer challengers.

### Shared bias audit

Ensemble agreement is challenged with cross-model families, temporal shifts, and nulls.

### Runtime budget

Only compact, exportable ensembles can become production challengers.

## Input contracts

- `ModelFamilySet`
- `ResamplingPolicy`
- `PredictionRows`

## Output contracts

- `EnsemblePrediction`
- `EpistemicScore`
- `DiversityReport`

## Measurement framework

- NLL/proper score.
- Disagreement calibration.
- OOD separation.
- Ensemble marginal value.

## Adversarial questions

- Are members truly diverse?
- Does bootstrap violate cluster/time structure?
- Does low disagreement reflect common leakage?

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

- [[OOD_Novelty_And_Support]]
