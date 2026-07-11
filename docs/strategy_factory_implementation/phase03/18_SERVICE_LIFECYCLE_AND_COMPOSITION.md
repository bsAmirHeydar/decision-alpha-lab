---
title: "Service Lifecycle and Composition"
status: implemented
phase: PHASE_03
language: en
tags:
  - strategy-factory
  - phase03
  - mql5
  - market-services
---

# Bundle

`CSF03MarketServiceBundle` composes:

- time kernel;
- terminal source;
- market data service;
- symbol specification cache;
- session schedule.

The bundle binds dependencies explicitly.

## Lifecycle

```text
construct
→ configure
→ initialize
→ start
→ serve
→ stop
→ shutdown
```

A service cannot start before initialization. Shutdown clears volatile caches.

## Integration with Phase 02

Phase 03 services implement the existing lifecycle and market ports. The Strategy Host remains thin. In a later phase, startup composition will replace Phase 02 null adapters with the real bundle without adding market logic to the host.

## Failure ordering

Startup occurs dependency-first. Shutdown occurs consumer-first. If the clock fails, the terminal source and market service cannot initialize.

## One active strategy

V1 still runs one active anatomy per host. Market services are shared within that host and remain strategy-neutral.
