---
id: SAED-96777F36C5
title: "Dependence-Aware Inference and Effective Sample"
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
  - dependence
---

# Dependence-Aware Inference and Effective Sample

## Sources of Dependence

Treatment siblings, overlapping holding periods, repeated Contexts from one structure, session/regime blocks, multi-symbol shared events and portfolio interactions.

## Methods

- opportunity-cluster bootstrap;
- block/stationary bootstrap;
- cluster-robust intervals;
- effective sample diagnostics;
- purged/embargoed folds;
- hierarchical reporting by Context/period/symbol.

## Rule

Raw trade count is never presented as independent sample count without a dependence analysis.
