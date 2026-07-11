---
type: strategy-factory-document
status: canonical
title: "Test Strategy and Test Pyramid"
tags:
  - strategy-factory
---

# Test Strategy and Test Pyramid

The Strategy Factory requires far more than a successful compile or one backtest.

## Layers

Contract unit tests; policy geometry tests; data/schema tests; causality tests; simulator path fixtures; fold separation tests; anti-overfit function tests; model/calibration tests; paper lifecycle tests; broker adapter integration tests; replay parity; and monitored rehearsal.

## Golden fixtures

Maintain small hand-verifiable datasets for stop/target ordering, gaps, same-bar ambiguity, missing bars, DST, cross-symbol timing, duplicate events, partial fill, and restart. Expected artifacts are versioned.

## Mutation and property tests

Randomly perturb timestamps, order, missingness, and prices to verify invariants. Mutate future features into snapshots and ensure rejection. Candidate geometry properties should hold over broad generated inputs.

