---
id: SAED-24046C9B96
title: "P2 — Tight-Convex Fixed Destination"
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
  - p2
---

# P2 — Tight-Convex Fixed Destination

## Mission

Accept frequent small losses to participate in occasional large moves using a tight thesis/trigger invalidation and fixed or structural destination.

## Objective

Win rate is secondary. Optimize robust net expectancy, right-tail magnitude, positive skew and probability of reaching large R thresholds.

## Key Labels

- stop-before-destination;
- destination-before-stop;
- MFE at 2R/3R/5R/10R;
- realized R;
- right-tail contribution;
- consecutive-loss distribution;
- time to expansion.

## Anti-Overfit Focus

This style is vulnerable to dependence on a handful of exceptional winners. Mandatory tests include best-trade/cluster removal, tail bootstrap, destination stability and cross-period tail participation.

## Evaluation

Do not reject merely for low hit rate. Reject when large winners are not stable, costs erase convexity, or drawdown/recovery exceeds declared limits.
