---
id: SAED-A878060375
title: "Fill Probability, Non-Fill, and Adverse Selection"
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
  - outcome
  - fill
---

# Fill Probability, Non-Fill, and Adverse Selection

## Separate Tasks

For conditional entries, estimate:

1. `P(trigger before expiry)`;
2. `P(fill | trigger, liquidity, order geometry)`;
3. time-to-fill distribution;
4. outcome distribution conditional on fill;
5. opportunity cost conditional on non-fill;
6. probability that fill indicates deterioration.

## Labels

Non-filled candidates remain rows. Removing them creates selection bias and makes limit entries look artificially strong.

## Stress

- spread expansion;
- queue/partial fill assumptions;
- one-tick misses;
- latency;
- gap-through;
- order expiry;
- price normalization;
- feed resolution.

A limit policy with high conditional-on-fill R but poor unconditional utility is rejected.
