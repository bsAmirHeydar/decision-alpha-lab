---
title: "Strategy Factory V2 — Ultra-Modular Anatomy-to-Decision Platform"
domain: strategy-factory-v2
status: canonical
language: en
version: 2.0.0
tags:
  - alpha-lab
  - strategy-factory
  - anatomy-to-decision
---

# Strategy Factory V2

Strategy Factory V2 is the canonical platform for converting any deterministic market anatomy into a research program, a family of executable setups, a trained decision system, and a governed paper/live execution path.

The architecture is built around one constraint:

> A new market view must require only a small anatomy adapter, a bounded set of strategy-specific feature providers, and optional policy plugins. Statistics, candidate generation, outcome accounting, anti-overfit validation, model training, decision serving, risk authorization, execution tracing, and monitoring are shared.

## Primary objective

Compress the path from a validated anatomy event to a reproducible decision without sacrificing causal integrity, statistical defensibility, explainability, or operational safety.

The system therefore has two deliberately separate operating lanes:

1. **Deep research lane** — exhaustive candidate generation, full statistical decomposition, controlled model comparison, null tests, anti-overfit controls, and promotion evidence.
2. **Compiled decision lane** — bounded feature recomputation, pre-resolved candidate templates, local model inference, deterministic ranking, explicit abstention, hard risk authorization, and execution intent generation.

Research may be broad. The live path must be narrow, immutable, measurable, and fast.

## Canonical flow

```text
Anatomy Engine
  -> Anatomy Adapter
  -> Canonical AnatomyEvent
  -> Incremental Context Graph
  -> Immutable Feature Snapshot
  -> Precompiled Candidate Templates
  -> Local Model Routes
  -> Candidate Utility Ranking
  -> Abstention / Fallback
  -> DecisionEnvelope
  -> Hard Risk Gate
  -> ExecutionIntent
  -> Paper or Broker Adapter
  -> ExecutionTrace
  -> Drift / Performance / Promotion Loop
```

## Start here

- [[01_SPEED_ACCURACY_AND_FLEXIBILITY_CHARTER]]
- [[02_TWO_LANE_ARCHITECTURE]]
- [[03_END_TO_END_REFERENCE_FLOW]]
- [[04_WHAT_REMAINS_STRATEGY_SPECIFIC]]
- [[05_MODULAR_KERNEL_AND_PLUGIN_BOUNDARIES]]
- [[24_CONTEXT_TO_DECISION_FAST_PATH]]
- [[50_ANTI_OVERFIT_MASTER_PROTOCOL]]
- [[59_TESTING_MASTER_MATRIX]]
- [[66_NEW_ANATOMY_FAST_ONBOARDING]]
- [[70_V1_TO_V2_MIGRATION]]

## Non-negotiable invariants

1. `event_time <= known_time <= confirmation_time <= decision_time`.
2. No feature can become known after the decision timestamp.
3. The anatomy adapter cannot inspect outcomes or allocate capital.
4. Training transformations are fit on training data only.
5. Events from the same underlying market cluster cannot be split across train and test.
6. Candidate, label, model, threshold, and cost changes count as separate trials.
7. The live decision thread performs no file I/O, network I/O, manifest parsing, dynamic imports, dataframe construction, or unbounded search.
8. Missing critical context causes abstention, not silent imputation.
9. Model confidence cannot override hard risk, broker, lifecycle, or promotion gates.
10. Paper and live consume the same DecisionEnvelope and ExecutionIntent contracts.

## Design target

V2 does not promise a universal fixed latency because hardware, broker topology, model size, and platform differ. It creates the conditions for predictable speed:

- startup compilation;
- dependency-aware incremental context updates;
- bounded candidate count;
- pre-resolved callables;
- local inference;
- fixed feature vectors;
- cache generation keys;
- deterministic fallbacks;
- per-stage latency budgets and telemetry.

Accuracy is not defined as raw classification accuracy. It is defined as calibrated, out-of-sample decision utility after costs, with explicit uncertainty, abstention, and stability evidence.
