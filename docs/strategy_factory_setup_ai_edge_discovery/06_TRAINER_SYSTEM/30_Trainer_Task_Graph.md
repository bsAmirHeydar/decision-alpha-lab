---
id: SAED-0ED30277FD
title: "Universal Trainer Task Graph"
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
  - task-graph
---

# Universal Trainer Task Graph

## Task Graph

```mermaid
flowchart TD
  X[Decision-Time Context + Candidate Features] --> A[Eligibility / Trade-Skip]
  X --> B[Trigger & Fill]
  X --> C[Outcome Distribution]
  X --> D[Survival / Competing Risk]
  X --> E[Candidate Ranker]
  X --> F[Regime & Novelty]
  B --> G[Treatment Selector]
  C --> G
  D --> G
  E --> G
  F --> G
  A --> G
  G --> H[Calibration & Uncertainty]
  H --> I[Select Treatment / Skip / Fallback / Abstain]
```

## Principle

Do not force one monolithic model to solve every task. Use task-compatible plugins and compose outputs through a versioned selector. A multi-task model is a challenger that must beat specialist baselines.

## OOF Requirement

Every downstream selector, calibrator or ensemble is trained on out-of-fold upstream predictions, never in-sample predictions.
