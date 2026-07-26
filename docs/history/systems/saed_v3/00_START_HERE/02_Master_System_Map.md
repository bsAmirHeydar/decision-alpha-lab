---
title: Master System Map
status: canonical
version: 3.0.0
created: '2026-07-13'
updated: '2026-07-13'
tags:
- saed-v3
- architecture
- map
---

# Layered architecture

```text
L0  UCEE Context Truth
L1  Setup Ontology and Finite Treatment Compiler
L2  Event-Sourced Market Replay and Counterfactual Outcome Cube
L3  Representation Learning and Shared Market State Encoders
L4  Supervised Multi-Task, Survival, Distributional, and Ranking Models
L5  Causal Treatment-Effect and Policy-Value Estimation
L6  Sequence, Graph, Foundation-Model, and World-Model Challengers
L7  Conservative Offline Policy Learning for Bounded Management Actions
L8  Uncertainty, Conformal Risk Control, Novelty, and Abstention
L9  Hierarchical Tournament and Distributed Experiment Fabric
L10 Statistical Adversary and Anti-Overfit Promotion System
L11 Multi-Agent Research Control Plane with Human Governance
L12 Manual / AI / Hybrid Policy Compiler
L13 UCEE Immutable Runtime, Portfolio, and Production Qualification
L14 Research Memory, Edge Genome, and Active Experiment Planning
```

# Three planes

## Research plane

Can generate hypotheses, candidates, representations, models, stress scenarios, and diagnostic reports. It has no live authority.

## Governance plane

Owns data-role locks, experiment budgets, statistical challenges, model-risk review, promotion signatures, revocation, and audit.

## Runtime plane

Consumes only signed immutable artifacts. It cannot retrain, browse the research registry, or relax policy/risk constraints.

# Separation that prevents architectural collapse

- **Context** answers what market state exists.
- **Setup archetype** answers what exploitation hypothesis is being tested.
- **Payoff profile** defines the desired distributional shape.
- **Entry mechanism** defines the premium paid for confirmation, immediacy, or price improvement.
- **Treatment bundle** defines executable entry, stop, exit, trail, management, and expiry.
- **Trainer** estimates outcomes and ranks bounded treatments.
- **Policy** decides within support.
- **Risk and portfolio** determine authorization and capital.
- **Execution** performs idempotent broker operations.
