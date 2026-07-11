---
title: "Speed, Accuracy, and Flexibility Charter"
domain: strategy-factory-v2
status: canonical
language: en
version: 2.0.0
tags:
  - alpha-lab
  - strategy-factory
  - anatomy-to-decision
---

# Charter

The platform optimizes three properties simultaneously, but never confuses them.

## Speed

Speed means reducing time and engineering effort in two distinct places:

- **development speed:** a new anatomy reaches dataset, setup matrix, model experiment, paper decision, and monitoring through existing modules;
- **decision speed:** a confirmed event reaches a deterministic decision with bounded computation and no nonessential work.

Speed is achieved by reuse and compilation, not by deleting controls.

### Development-speed mechanisms

- anatomy scaffolding;
- versioned manifests;
- plugin contracts;
- standard candidate libraries;
- shared outcome engine;
- reusable anti-overfit suite;
- common model training and reporting;
- standard paper/live adapters;
- generated test packets and run manifests.

### Decision-speed mechanisms

- compile the feature graph at startup;
- resolve plugin versions before market events arrive;
- expand and prune candidate templates before runtime;
- use numeric fixed-order model vectors;
- recompute only providers affected by a new state generation;
- keep authoritative work in memory;
- send logging and analytics to non-authoritative observers;
- enforce candidate, feature, and model budgets.

## Accuracy

Accuracy has five layers:

1. **semantic accuracy** — the event represents the intended anatomy.
2. **causal accuracy** — only information known at decision time is used.
3. **simulation accuracy** — fills, costs, ambiguity, and holding logic approximate executable reality.
4. **statistical accuracy** — uncertainty, dependence, multiple testing, and selection bias are controlled.
5. **operational accuracy** — research decisions reproduce in paper/live with measured latency, spread, slippage, and rejection behavior.

A model that predicts labels well but fails any earlier layer is not accurate.

## Flexibility

Flexibility means the kernel does not know what a hook, divergence, cycle, node, astro state, or future anatomy means. Those concepts enter through plugins. Flexibility does not mean every module can mutate every other module.

The platform uses **bounded extensibility**:

- stable contracts;
- explicit capabilities;
- versioned plugins;
- dependency graphs;
- immutable plans;
- admission tests;
- compatibility matrices;
- reversible deployment.

## Optimization order

When trade-offs occur, use this order:

1. causal correctness;
2. capital safety;
3. deterministic reproducibility;
4. statistical validity;
5. decision accuracy and calibration;
6. latency;
7. convenience.

Latency work may optimize an already correct path. It may not legalize leakage or remove risk gates.
