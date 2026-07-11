---
title: "Target Architecture"
tags:
  - strategy-factory
  - implementation-roadmap
  - alpha-lab
status: canonical
doc_version: 1.0.0
---

# Target Architecture

## Architectural Planes

### 1. Knowledge Plane

Contains doctrine, semantics, glossary, examples, ambiguity records, and source-of-truth definitions.

### 2. Research Plane

Builds datasets, candidate universes, outcome labels, statistical reports, null tests, walk-forward folds, and model comparisons.

### 3. Compilation Plane

Resolves manifests, plugin versions, feature dependencies, candidate templates, model routes, thresholds, and hashes into immutable runtime plans.

### 4. Decision Plane

Consumes a confirmed event and current context, builds a fixed vector, scores promoted candidates, applies abstention and pre-risk gates, and emits a decision record.

### 5. Capital Plane

Applies portfolio exposure, correlation, event-cluster, daily-loss, and strategy-level limits. It emits an action plan or rejects the decision.

### 6. Execution Plane

Maps approved action plans to broker requests, records acknowledgements, fills, rejects, slippage, and position lifecycle.

### 7. Observation Plane

Tracks latency, feature freshness, prediction distributions, decision disagreements, paper/live parity, data drift, execution drift, and incidents.

## Stable Kernel

- time semantics;
- identity and lineage;
- plugin protocol;
- artifact protocol;
- manifest compiler;
- validation engine;
- risk boundary;
- execution trace;
- telemetry and lifecycle.

## Extensible Plugin Surface

- anatomy adapters;
- feature providers;
- candidate policies;
- cost models;
- null generators;
- model implementations;
- decision policies;
- risk policies;
- execution adapters;
- report builders.
