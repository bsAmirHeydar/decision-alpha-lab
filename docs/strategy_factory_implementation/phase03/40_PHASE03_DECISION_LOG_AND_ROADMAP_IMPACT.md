---
title: "Phase 03 Decision Log and Roadmap Impact"
status: implemented
phase: PHASE_03
language: en
tags:
  - strategy-factory
  - phase03
  - mql5
  - market-services
---

# Confirmed decisions

- Build the central engine before migrating old strategies.
- MQL5 owns runtime market/time/symbol truth.
- Python remains a strict research mirror.
- Terminal APIs are isolated.
- Closed bars are canonical.
- Missing required data fails closed.
- Broker symbols have separate validation grammar.
- Direct typed calls remain the fast path; audit remains side-channel.
- One active anatomy per host remains the V1 rule.

# Roadmap impact

Phase 04 can now focus exclusively on plugin descriptors and event emission. It no longer needs to solve market caching, DST, session identity, or synchronization.

Phase 06 real-anatomy integration remains intentionally deferred until the fixture plugin proves that the SDK can consume Phase 03 services without modifying the core.

# Change-control rule

A modification to Phase 03 contracts after real strategy integration requires:

- ADR;
- regression fixture;
- cross-language tests where applicable;
- impact analysis on generated event IDs and datasets;
- compatibility or migration plan.
