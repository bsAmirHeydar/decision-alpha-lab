---
id: SAED-E218733AE5
title: "P1 — Wide-Survival High-Hit Fixed"
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
  - payoff-profile
  - p1
---

# P1 — Wide-Survival High-Hit Fixed

## Mission

Maximize calibrated hit probability while keeping net reward at or above 1R and respecting tail, capital-usage and duration constraints.

## Typical Structure

- wide structural invalidation;
- fixed target or bounded structural destination;
- no hidden averaging down;
- lower position size due to stop width;
- longer allowed holding horizon;
- strong preference for Contexts with high directional conviction but internal noise.

## Objective

```text
maximize lower-confidence-bound(hit_rate)
subject to:
  net_reward_r >= 1.0
  net_expectancy > hurdle
  tail_loss <= limit
  capital_time_usage <= limit
  cost_stress_pass = true
```

## Required Diagnostics

- MAE distribution relative to stop;
- target distance feasibility;
- time underwater;
- gap/tail behavior;
- win-rate confidence interval;
- best-period concentration;
- comparison with tighter-stop variants;
- whether high hit rate is created merely by distant stops.

## Failure Modes

Small sample, hidden negative skew, rare catastrophic losses, low capital efficiency, target not executable after spread/slippage, or Context decay before the trade resolves.
