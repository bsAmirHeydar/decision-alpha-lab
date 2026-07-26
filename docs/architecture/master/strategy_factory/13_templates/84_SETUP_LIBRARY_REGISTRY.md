---
type: strategy-factory-document
status: canonical
title: "Setup Library Registry"
tags:
  - strategy-factory
---

# Setup Library Registry

The setup library catalogs reusable execution policies separately from market anatomies.

## Registry fields

Setup ID/version, entry/stop/exit/time behavior, required feature fields, compatible anatomy classes, order type, cost assumptions, capacity notes, tests, and status. Setups are plugins; they do not own data or validation pipelines.

## Reuse

A first-pullback setup can be applied to divergence, NDS, Daye, or structural nodes through the same candidate interface. Results remain strategy-specific but policy identity allows cross-anatomy analysis.

## Governance

Changing a policy formula creates a new version. A policy can be retired globally for unrealistic fills or operational burden. No setup becomes default solely because it won one strategy's history.

