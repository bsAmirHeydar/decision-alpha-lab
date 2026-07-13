---
id: SAED-CB91191550
title: "Payoff-Profile-Specific Anti-Overfit Controls"
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
  - payoff-profile
---

# Payoff-Profile-Specific Anti-Overfit Controls

## P1 Wide High-Hit

Test hidden tail loss, distant-stop dependence, time/capital occupancy and minimum net 1R robustness.

## P2 Tight Convex Fixed

Test winner concentration, tail stability, destination sensitivity and losing-streak distribution.

## P3 Tight Convex Trail

Test path resolution, intrabar assumptions, trail parameter neighborhoods and post-exit continuation.

## P4 Wide Open Trail

Test regime dependence, chop losses, duration, capacity, trend scarcity and correlated drawdowns.

## P5 Tight High-Hit

Test one-tick/bar delay, spread/slippage, feed differences, stop normalization and false timing precision.

A single generic Sharpe gate is not sufficient across these profiles.
