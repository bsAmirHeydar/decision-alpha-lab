---
id: SAED-C7690D4553
title: "P3 — Tight-Convex Path-Dependent Trail"
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
  - p3
  - path-dependent
---

# P3 — Tight-Convex Path-Dependent Trail

## Mission

Use a tight initial invalidation and a governed trailing policy to capture rare, very large moves while controlling loss size.

## Path Dependence

Exact high/low order matters. OHLC endpoint labels are insufficient when a trail can activate, ratchet, exit and later observe further movement.

## Trail Contract

- activation rule;
- initial anchor;
- update frequency;
- structural/volatility/reference source;
- ratchet-only invariant;
- minimum distance;
- spread side;
- gap handling;
- partial exit interaction;
- re-entry policy;
- time stop and Context invalidation.

## Metrics

- right-tail capture ratio;
- giveback ratio;
- premature exit rate;
- trail activation frequency;
- captured R conditional on MFE;
- path smoothness cohorts;
- post-exit continuation;
- latency sensitivity.

## Required Replay

Tick or sufficiently conservative lower-timeframe replay is mandatory. Ambiguous bars use a frozen pessimistic intrabar policy or are excluded with evidence.
