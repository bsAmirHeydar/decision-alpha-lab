---
title: "Phase 04 Handoff — Static Plugin Registry"
status: implemented
phase: PHASE_03
language: en
tags:
  - strategy-factory
  - phase03
  - mql5
  - market-services
---

# Next phase

Phase 04 builds the plugin kernel and anatomy adapter SDK while still avoiding legacy integration.

## Inputs now available

- canonical event and feature contracts;
- runtime lifecycle and ports;
- shared market, time, session, synchronization, and symbol services;
- fixture and diagnostic infrastructure;
- dependency and authority guards.

## Required Phase 04 outputs

1. Static plugin descriptor.
2. Plugin ID and semantic version.
3. Capability declaration.
4. Required symbols and timeframes.
5. Maximum lookback and update scope.
6. Required synchronization contracts.
7. Anatomy provider base class or interface refinement.
8. Bounded event queue.
9. Fixture anatomy plugin.
10. Plugin registry compile/startup validation.
11. Golden plugin test pack.
12. No legacy strategy code yet.

## Exit criterion

A fixture plugin must declare requirements, bind to Phase 03 services, emit a valid Phase 01 event, and run through the Phase 02 host without modifying the core.
