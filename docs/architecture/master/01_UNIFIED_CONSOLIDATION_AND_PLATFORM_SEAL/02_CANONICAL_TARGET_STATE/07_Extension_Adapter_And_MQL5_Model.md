---
id: UCPS-69FB499625AD
title: "Extension, Adapter and MQL5 Model"
type: architecture
status: canonical
domain: unified-consolidation-platform-seal
version: 1.0.0
created: 2026-07-23
updated: 2026-07-23
tags:
  - consolidation
  - platform-seal
---
# Extension, Adapter and MQL5 Model

## Extensions

Extensions add bounded domain capability through declared ports: detectors, features, labels, Treatments, models and visualizers. Every extension has a manifest, version, owner, capabilities, input/output schemas, failure semantics and conformance tests.

## Adapters

Adapters isolate external volatility: market feeds, storage, terminals, brokers, model runtimes and notifications. Adapters translate external representation; they do not change Doctrine, evidence or authority.

## MQL5

`mql5/Include/AL/` contains shared terminal contracts. Experts, Indicators and Scripts consume these contracts. Compiled MetaEditor evidence, Strategy Tester evidence and Python/MQL5 parity are mandatory for terminal-affecting changes.

## Safety

No Extension or Adapter gains live-order, capital or secret authority by registration alone. Capabilities are deny-by-default and environment-specific.
