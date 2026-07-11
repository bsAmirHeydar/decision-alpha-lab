---
type: strategy-factory-document
status: canonical
title: "Immutable Feature Snapshot"
tags:
  - strategy-factory
---

# Immutable Feature Snapshot

A snapshot freezes the decision context before outcomes exist. It is the only model input authority.

## Shared versus specific features

Shared features include spread, volatility, session, time-of-day, day-of-week, news distance, and execution environment. Strategy-specific features describe the anatomy: cycle group, hook family, zone width, reference age, divergence strength, or node state. Both obey the same availability-time contract.

## Schema behavior

Feature names, types, units, null policy, source, and version are registered. Categorical vocabularies are fit only on training data. Unknown live categories map to an explicit unknown token; they do not crash or borrow future frequency information.

## Missingness

Missing is information but must not be silently imputed. The snapshot records missing reason. Training pipelines may impute using train-only statistics and may add missing indicators. Live behavior is defined in the manifest: skip, fallback model, or deterministic baseline.

## Immutability

A snapshot cannot be enriched after the outcome. Derived reports may join additional fields, but model features must always be traceable to the original snapshot artifact.

