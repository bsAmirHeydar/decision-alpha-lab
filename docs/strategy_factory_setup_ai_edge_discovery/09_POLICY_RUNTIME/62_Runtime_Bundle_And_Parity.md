---
id: SAED-7970E1572F
title: "Immutable Runtime Bundle and Python/MQL5 Parity"
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
  - runtime
  - parity
---

# Immutable Runtime Bundle and Python/MQL5 Parity

## Bundle

Context refs, feature schema/order, preprocessing, model/export, calibration, thresholds, candidate registry, policy graph, manual/fallback policies, authority matrix, risk/portfolio handoff, monitoring contract and rollback pointer.

## Parity

Golden, edge, missing, extreme and OOD vectors compare Python source, approved export and MQL5 mirror. Decision labels and fallback reasons require exact parity; numeric tolerances are explicit.

## Activation

Build → warm → validate → atomic activate. Failed validation quarantines the generation. Restart reconciles generation and decision identity without duplicate action.
