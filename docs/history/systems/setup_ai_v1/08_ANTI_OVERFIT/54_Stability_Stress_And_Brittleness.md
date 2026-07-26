---
id: SAED-E575F43F40
title: "Parameter Stability, Stress, and Brittleness"
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
  - anti-overfit
  - stability
  - stress
---

# Parameter Stability, Stress, and Brittleness

## Stability Maps

Evaluate neighborhoods around entry offsets, stop buffers, target R, trail activation/width, expiry, thresholds and model hyperparameters.

## Stress Families

- spread/commission/slippage multiples;
- entry/decision delay;
- missed/partial fills;
- cross-feed and tick-size changes;
- symbol/session/regime subsets;
- volatility/liquidity shocks;
- best-trade/period removal;
- feature missingness;
- model/preprocessing perturbation.

## Brittleness Rule

A narrow optimum surrounded by failure is evidence of overfit or execution fragility, even if the exact historical point is strong.
