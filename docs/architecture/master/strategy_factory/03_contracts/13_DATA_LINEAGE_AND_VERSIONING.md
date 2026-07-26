---
type: strategy-factory-document
status: canonical
title: "Data Lineage and Versioning"
tags:
  - strategy-factory
---

# Data Lineage and Versioning

Every number in a promotion report must be traceable to source data, code commit, manifest, feature set, candidate set, labels, folds, and model artifact.

## Version dimensions

Track source feed, bar normalization, anatomy version, event schema, feature schema, candidate-policy version, cost model, simulation policy, label version, fold plan, model code, hyperparameters, random seed, and repository commit. One generic “strategy version” is insufficient.

## Artifact manifests

Each run writes hashes and paths for all materialized artifacts. Re-running the same inputs should reproduce hashes except for explicitly nondeterministic metadata. If not, the run is marked non-reproducible and cannot promote.

## Data corrections

Vendor corrections, timezone changes, DST fixes, and symbol specification changes create new data versions. Reports compare versions and explain changed events rather than overwriting history.

