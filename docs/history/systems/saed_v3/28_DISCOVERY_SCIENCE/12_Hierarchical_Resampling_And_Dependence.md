---
title: Hierarchical Resampling and Dependence
status: canonical
version: 3.0.0
created: '2026-07-13'
updated: '2026-07-13'
capability_tier: core-production
tags:
  - saed-v3
---

# Mission

Quantify uncertainty under temporal, occurrence, session, symbol, event, and regime dependence.

## Why this component exists

- None declared.

## Authority and safety boundary

- This component may estimate, rank, simulate, challenge, or recommend only inside a declared research scope.
- It cannot create canonical Context truth, modify protected evidence roles, sign promotion, change portfolio risk, activate runtime generations, access live credentials, or place orders.
- Unsupported, stale, contradictory, OOD, hash-mismatched, uncalibrated, or incomplete paths resolve to **Skip**, **Abstain**, **Manual fallback**, **Reject**, or **Quarantine**.
- Every result is subordinate to UCEE I12 promotion admission, I13 authority/fallback, I14 immutable runtime, I17 portfolio/risk, and I18 release qualification.

## Input contracts

- Outcome and influence values.
- Dependency graph and clusters.

## Output contracts

- Hierarchical bootstrap distributions.
- Sensitivity to block design.

## Algorithmic design

- Resample at the highest defensible independent unit.
- Use nested blocks: macro event → day/session → occurrence cluster → treatment sibling.
- Compare stationary/block bootstrap, cluster bootstrap, and subsampling.
- Report effective sample size and uncertainty inflation.


## Data and known-time semantics

- None declared.

## Anti-overfit and model-risk controls

- Block choice frozen or included in multiplicity.
- No row-wise bootstrap for dependent observations.
- Sparse regimes retain wide uncertainty.

## Measurement system

- CI coverage in simulation.
- Uncertainty inflation.
- Block sensitivity.
- Tail stability.

## Scalability and operating model

- None declared.

## Adversarial failure modes

- Thousands of treatment rows imply false precision.
- Shared macro events resampled independently.
- Best block chosen by significance.

## UCEE integration

- None declared.

## Required tests and evidence

- Known-dependence simulation.
- Block-size sweep.
- Event-drop stress.
- Sparse cluster case.

## Implementation slices

- None declared.

## Decision record

- None declared.

## Acceptance gate

The component is accepted only when its contracts are closed and versioned, all lineage and role boundaries are reconstructible, protected evaluation remains unexposed, negative and mutation tests pass, simpler baselines remain available, and an independent reviewer can reproduce the decision-equivalent result from immutable hashes.

## Related notes

- [[Context_Identity_And_Occurrence_Clustering]]
- [[Bootstrap_Monte_Carlo_And_Cluster_Inference]]
