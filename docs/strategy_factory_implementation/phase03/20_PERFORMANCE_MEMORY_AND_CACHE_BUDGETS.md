---
title: "Performance, Memory, and Cache Budgets"
status: implemented
phase: PHASE_03
language: en
tags:
  - strategy-factory
  - phase03
  - mql5
  - market-services
---

# Performance goal

Shared services must reduce repeated work, not become a universal history database.

## Bounded structures

- one latest tick per symbol;
- bounded bar arrays per symbol/timeframe;
- bounded audit bus from Phase 02;
- fixed number of active services.

## Update scopes

- tick cache: on demand or tick event;
- closed-bar cache: new-bar or scheduled refresh;
- symbol specifications: startup and periodic/incident refresh;
- session resolution: constant-time calendar arithmetic;
- synchronization: only for declared required series.

## Prohibited patterns

- full-history `CopyRates` on every tick;
- multiple modules pulling the same bars;
- unbounded dynamic arrays;
- synchronous large file writes in market callbacks;
- scanning every known symbol when only a declared universe is active.

## Measurement

The diagnostic EA prints refresh behavior, while telemetry records maximum latency. Later phases will add benchmark fixtures and runtime budgets.

## Memory sizing

A future plugin descriptor must declare maximum bar lookback. Startup compilation will calculate required capacities and reject a plugin whose requirements exceed configured resource budgets.
