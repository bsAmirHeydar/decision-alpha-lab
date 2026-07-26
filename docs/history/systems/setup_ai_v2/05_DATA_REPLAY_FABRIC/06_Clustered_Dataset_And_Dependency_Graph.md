---
title: Clustered Dataset and Dependency Graph
status: canonical
version: 2.0.0
created: '2026-07-13'
updated: '2026-07-13'
tags:
- saed-v2
- core-production
---

# Purpose

Build learning tables that preserve temporal, sibling, shared-event, and cross-market dependence.

## Capability tier

**Core Production**

## System design

### Primary row

One occurrence-treatment pair with immutable feature snapshot and outcome target.

### Dependency graph

Edges encode sibling treatments, overlapping contexts, same market event, symbol/currency/session dependence, and label-window overlap.

### Fold unit

Connected components or conservative clusters are assigned as units where required.

### Weights

Opportunity, cluster, regime, and inverse-propensity weights are versioned and never inferred silently by a trainer.

## Input contracts

- `OutcomeCube`
- `FeatureSnapshot`
- `DependencyEdges`

## Output contracts

- `DatasetManifest`
- `ClusterAssignments`
- `WeightManifest`

## Measurement framework

- Effective sample size.
- Cluster size distribution.
- Fold contamination.
- Weight concentration.

## Adversarial questions

- Are thousands of sibling rows presented as thousands of trades?
- Do overlapping label windows cross folds?
- Do extreme weights dominate causal estimates?

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

- [[Purged_Nested_Walk_Forward]]
