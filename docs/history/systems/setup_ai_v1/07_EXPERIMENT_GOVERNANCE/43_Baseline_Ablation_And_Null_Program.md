---
id: SAED-D1C72BF9F4
title: "Baseline, Ablation, Null, and Placebo Program"
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
  - experiment
  - nulls
  - ablation
---

# Baseline, Ablation, Null, and Placebo Program

## Baselines

Skip, always-trade, unconditional treatment, time/session-only, Context-only, Manual policy and strongest prior simple model.

## Ablations

Feature groups, Context views, candidate descriptors, entry mechanism, payoff profile, stop/exit atoms, calibration, regime router and ensemble components.

## Matched Nulls

Preserve nuisance variables such as session, volatility, direction balance, holding horizon and costs while removing or shifting the Context signal.

## Placebos

Timestamp shift, direction shuffle, irrelevant pair substitution, random feature injection, label shuffle and impossible-feature checks.

## Gate

A candidate must add information beyond matched baselines, not merely make money in the same favorable periods.
