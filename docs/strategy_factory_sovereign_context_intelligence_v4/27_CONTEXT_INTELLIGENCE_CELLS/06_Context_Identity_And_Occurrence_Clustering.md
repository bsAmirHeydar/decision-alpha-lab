---
title: Context Identity and Occurrence Clustering
status: canonical
version: 4.0.0
created: '2026-07-13'
updated: '2026-07-13'
capability_tier: core-production
tags:
  - saed-v4
---

# Mission

Define independent statistical units and prevent sibling treatments, overlapping windows, shared events, or repeated detections from inflating sample size.

## Why this component exists

- None declared.

## Authority and safety boundary

- This component may estimate, rank, simulate, challenge, or recommend only inside a declared research scope.
- It cannot create canonical Context truth, modify protected evidence roles, sign promotion, change portfolio risk, activate runtime generations, access live credentials, or place orders.
- Unsupported, stale, contradictory, OOD, hash-mismatched, uncalibrated, or incomplete paths resolve to **Skip**, **Abstain**, **Manual fallback**, **Reject**, or **Quarantine**.
- Every result is subordinate to UCEE I12 promotion admission, I13 authority/fallback, I14 immutable runtime, I17 portfolio/risk, and I18 release qualification.

## Input contracts

- Context occurrences.
- Event graph.
- Candidate treatment lattice.

## Output contracts

- Occurrence cluster IDs.
- Dependency blocks and effective sample size.

## Algorithmic design

- Cluster all treatment siblings under one opportunity identity.
- Merge detections sharing causal event, anchor, path, or overlapping maturity horizon.
- Build higher-level blocks for day, session, macro event, symbol family, and market shock.
- Use cluster-robust inference and block resampling.


## Data and known-time semantics

- None declared.

## Anti-overfit and model-risk controls

- Clustering rules freeze before final evaluation.
- Independent count is never row count.
- Uncertain dependence receives conservative grouping.

## Measurement system

- Raw rows versus effective opportunities.
- Cluster-size distribution.
- Inference sensitivity to block definitions.

## Scalability and operating model

- None declared.

## Adversarial failure modes

- One occurrence with 100 treatments counts as 100 samples.
- Same market event appears in train and test.
- Overlapping labels cross folds.

## UCEE integration

- None declared.

## Required tests and evidence

- Sibling split mutation.
- Shared-event leakage.
- Cluster-rule sensitivity.
- Effective sample size floor.

## Implementation slices

- None declared.

## Decision record

- None declared.

## Acceptance gate

The component is accepted only when its contracts are closed and versioned, all lineage and role boundaries are reconstructible, protected evaluation remains unexposed, negative and mutation tests pass, simpler baselines remain available, and an independent reviewer can reproduce the decision-equivalent result from immutable hashes.

## Related notes

- [[Cluster_Aware_Dataset_Design]]
- [[Hierarchical_Resampling_And_Dependence]]
