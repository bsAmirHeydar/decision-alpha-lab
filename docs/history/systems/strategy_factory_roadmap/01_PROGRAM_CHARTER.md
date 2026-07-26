---
title: "Program Charter"
tags:
  - strategy-factory
  - implementation-roadmap
  - alpha-lab
status: canonical
doc_version: 1.0.0
---

# Program Charter

## Objective

Build one permanent codebase that supports multiple strategy anatomies without duplicating research, training, validation, execution, or monitoring logic.

## Success Definition

The platform is successful when a new event-driven directional anatomy can be onboarded by adding only:

- one anatomy doctrine;
- one event adapter;
- strategy-specific feature providers;
- allowed candidate policies;
- matched null definitions;
- golden fixtures and strategy tests;
- one versioned manifest.

The new strategy must then inherit the full platform:

- dataset construction;
- causal snapshots;
- candidate enumeration;
- cost-aware simulation;
- statistical reporting;
- purged walk-forward validation;
- anti-overfit controls;
- model training and ranking;
- paper execution;
- risk gates;
- monitoring and lifecycle governance.

## Non-Goals for V1

- high-frequency market making;
- options-volatility surface engines;
- full reinforcement learning;
- broker-agnostic live order submission without broker profiles;
- unrestricted dynamic strategy code in the fast path;
- automatic mutation of anatomy definitions by AI.

## Program Constraints

- Python is authoritative for research, training, artifacts, and offline validation.
- MQL5 is authoritative for MetaTrader market integration, runtime event detection, broker constraints, and final deterministic execution.
- Contracts are cross-language and versioned.
- Live runtime is fail-closed.
- Research outputs never automatically gain capital authority.
