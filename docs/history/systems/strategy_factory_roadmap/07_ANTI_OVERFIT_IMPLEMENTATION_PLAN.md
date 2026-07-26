---
title: "Anti-Overfit Implementation Plan"
tags:
  - strategy-factory
  - implementation-roadmap
  - alpha-lab
status: canonical
doc_version: 1.0.0
---

# Anti-Overfit Implementation Plan

## Required Controls

- immutable trial registry;
- train-only transformations;
- label-horizon purge;
- embargo;
- event-cluster split;
- anchored and rolling walk-forward;
- nested model selection;
- event-cluster bootstrap;
- moving-block bootstrap;
- multiple-testing correction;
- deflated performance metrics;
- probability of backtest overfitting;
- reality-check style best-model test;
- parameter-surface stability;
- feature and policy ablation;
- cost and latency stress;
- best-trade removal;
- cross-feed, cross-broker, and cross-period validation;
- matched nulls and placebos.

## Enforcement Principle

Anti-overfit controls are not optional report decorations. Promotion code must consume their machine-readable outputs and reject candidates that violate configured gates.

## Trial Identity

Every hypothesis variation must produce a trial record containing:

- parent hypothesis;
- changed parameter or feature;
- reason for change;
- timestamp;
- author or agent;
- data window exposed before change;
- evaluation windows;
- result and disposition.
