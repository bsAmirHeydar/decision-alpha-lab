---
title: MT5 Acquisition Is an Adapter, Not Engine Logic
status: roadmap-approved-for-implementation
version: 1.0.0
updated: 2026-07-22
tags: [rthp, mt5, atomic-concept]
---
# MT5 Acquisition Is an Adapter, Not Engine Logic

The MetaTrader integration discovers terminals, resolves symbols, acquires and validates M1 bars, and emits immutable source artifacts. It does not implement model training, dataset selection, validation policy, promotion, or RTHP semantics. Those responsibilities remain with existing packages.
