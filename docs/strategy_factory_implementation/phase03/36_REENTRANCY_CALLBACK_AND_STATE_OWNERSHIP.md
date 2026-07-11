---
title: "Reentrancy, Callbacks, and State Ownership"
status: implemented
phase: PHASE_03
language: en
tags:
  - strategy-factory
  - phase03
  - mql5
  - market-services
---

# MetaTrader event model

MQL5 callbacks are serialized per program, but service methods may be invoked from `OnTick`, `OnTimer`, and future tester callbacks. The architecture must still define ownership and avoid partial updates.

# Ownership

- terminal source owns no durable cache;
- market service owns tick and bar caches;
- time kernel owns clock configuration;
- symbol cache owns specification generations;
- strategy host owns service lifecycle;
- future plugins own only anatomy state.

# Update atomicity

A source observation is validated before replacing cached state. Failed observations leave the last valid item intact and increment error telemetry.

# Callback policy

`OnTick` should not trigger large historical refreshes. `OnTimer` or new-bar paths may refresh declared series. A future scheduler will coalesce duplicate refresh requests.

# Future concurrency

If file workers or external processes are introduced, messages must cross explicit artifact or IPC boundaries. Core in-memory services should not be retrofitted with uncontrolled shared mutable state.
