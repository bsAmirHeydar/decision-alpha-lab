---
id: SAED-502073AFD0
title: "Candidate-Level Dataset Row and Feature Contract"
type: architecture
status: canonical
domain: strategy-factory-setup-ai-edge-discovery
version: 1.0.0
created: 2026-07-13
updated: 2026-07-13
tags:
  - strategy-factory
  - setup-factory
  - ai-training
  - dataset
  - features
---

# Candidate-Level Dataset Row and Feature Contract

## Row Grain

One row equals one Context occurrence times one candidate Treatment. Candidate siblings share `opportunity_cluster_id`.

## Feature Groups

- Context semantic and lifecycle features;
- temporal/session features;
- multi-view and intermarket features;
- regime/volatility/liquidity features;
- entry geometry;
- stop/exit/management descriptors;
- cost and broker state available at decision time;
- candidate capability flags.

## Forbidden Features

Outcome columns, label end timestamps unavailable at decision time, future missingness, post-fill statistics, final-test-derived encodings, row order and identifiers proxying period.

## Preprocessing

Imputation, scaling, categorical vocabulary, rare grouping, clipping and feature selection are fit inside folds and packaged with the model. Runtime uses the identical artifact.
