---
title: Capability Tier Policy
status: canonical
version: 3.0.0
created: '2026-07-13'
updated: '2026-07-13'
tags:
- saed-v3
- governance
- capability-tiers
---

# Tier A — Core Production

Allowed after ordinary UCEE promotion and parity gates:

- regularized linear and generalized linear models;
- calibrated tree ensembles and gradient boosting;
- monotonic and shape-constrained models;
- survival and competing-risk baselines;
- learning-to-rank over a finite treatment lattice;
- deep ensembles only when export/parity and latency budgets are satisfied;
- conformal prediction and conformal risk controls with time-series caveats;
- deterministic manual/AI/hybrid policy graphs.

# Tier B — Governed Challengers

Require additional model-risk review, ablation, compute accounting, shadow parity, and fallback proofs:

- patch-based time-series transformers;
- state-space and selective-state-space models;
- graph neural networks and graph transformers;
- sparse mixture-of-experts;
- time-series foundation-model adapters;
- neural causal estimators;
- multi-task sequence models;
- deep distributional and neural survival models.

# Tier C — Research-Only

May improve representations, stress tests, candidate priors, or scientific understanding. Outputs cannot directly enter a live policy:

- learned world models;
- diffusion and flow-matching path generators;
- conservative offline RL and sequence-policy models;
- neural architecture search;
- automated feature synthesis;
- autonomous research agents;
- synthetic-market generators;
- model-based counterfactual simulators.

# Tier D — Prohibited-to-Live

- online reinforcement learning with real capital;
- self-modifying runtime policies;
- direct LLM order placement;
- silent or automatic live retraining;
- dynamic expansion of the action space;
- agent-signed promotion;
- unsigned external model downloads;
- non-reproducible closed data transformations;
- models that cannot emit support, uncertainty, and lineage evidence.

# Promotion principle

Capability sophistication increases the burden of proof. It never reduces it.
