---
id: SAED-06EE25AD1C
title: "Task 2 — Trigger, Fill, Survival, and Competing Risks"
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
  - trainer
  - survival
---

# Task 2 — Trigger, Fill, Survival, and Competing Risks

## Events

Fill, stop, target, trail exit, expiry, Context invalidation and cancellation can compete.

## Models

Start with empirical hazards and interpretable survival models. Add boosted survival or sequence challengers only after sample and conformance requirements are met.

## Outputs

- event probabilities by horizon;
- survival curves;
- time quantiles;
- competing-risk cumulative incidence;
- uncertainty and support flags.

## Use

Outputs inform candidate utility and expiry, but do not simulate fills outside the frozen execution model.
