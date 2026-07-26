---
title: Orthogonal Cross-Fitted Policy Value
status: canonical
version: 3.0.0
created: '2026-07-13'
updated: '2026-07-13'
capability_tier: core-production
tags:
  - saed-v3
---

# Mission

Estimate incremental value of treatment-selection policies with nuisance-robust, chronological, cluster-aware cross-fitting.

## Why this component exists

- None declared.

## Authority and safety boundary

- This component may estimate, rank, simulate, challenge, or recommend only inside a declared research scope.
- It cannot create canonical Context truth, modify protected evidence roles, sign promotion, change portfolio risk, activate runtime generations, access live credentials, or place orders.
- Unsupported, stale, contradictory, OOD, hash-mismatched, uncalibrated, or incomplete paths resolve to **Skip**, **Abstain**, **Manual fallback**, **Reject**, or **Quarantine**.
- Every result is subordinate to UCEE I12 promotion admission, I13 authority/fallback, I14 immutable runtime, I17 portfolio/risk, and I18 release qualification.

## Input contracts

- Folded outcome cube.
- Propensity and outcome nuisance models.
- Candidate policy.

## Output contracts

- DR policy value.
- Influence-function uncertainty.
- Nuisance diagnostics.

## Algorithmic design

- Train nuisance models strictly out of fold and out of cluster.
- Use AIPW/DR/R-learner-style orthogonal scores where assumptions apply.
- Evaluate policy against Skip, manual, simple ranking, and fixed-treatment baselines.
- Propagate fill, censoring, and cost uncertainty.

## Formal objective and constraints

```text
V_DR(π)=E[m(X,π(X)) + I(A=π(X))/e(A|X)*(Y-m(X,A))]
```

## Data and known-time semantics

- None declared.

## Anti-overfit and model-risk controls

- Policy cannot train on evaluation pseudo-outcomes.
- Chronology, purge, embargo, and cluster blocks preserved.
- Nuisance complexity separately tuned.

## Measurement system

- DR value.
- Robust standard error.
- Nuisance stability.
- Effective sample size.
- Baseline incremental value.

## Scalability and operating model

- None declared.

## Adversarial failure modes

- Cross-fitting ignores time.
- Same occurrence siblings split.
- Pseudo-outcome leakage.
- Unstable propensity weights.

## UCEE integration

- None declared.

## Required tests and evidence

- Fold permutation.
- Nuisance ablation.
- Manual policy comparison.
- Influence outlier removal.

## Implementation slices

- None declared.

## Decision record

- None declared.

## Acceptance gate

The component is accepted only when its contracts are closed and versioned, all lineage and role boundaries are reconstructible, protected evaluation remains unexposed, negative and mutation tests pass, simpler baselines remain available, and an independent reviewer can reproduce the decision-equivalent result from immutable hashes.

## Related notes

- [[Doubly_Robust_And_Orthogonal_Learners]]
- [[Causal_Overlap_And_Positivity_Engine]]
