---
title: "Phase 03 Definition of Done"
status: implemented
phase: PHASE_03
language: en
tags:
  - strategy-factory
  - phase03
  - mql5
  - market-services
---

# Functional

- Shared time kernel returns canonical UTC milliseconds.
- New York DST fixtures pass.
- Broker time conversion is explicit.
- Trading-day and session resolution work.
- Tick cache enforces order and freshness.
- Closed-bar cache enforces identity, order, bounded capacity, and gaps.
- Multi-symbol synchronization returns explicit readiness state.
- Symbol specifications are cached and versioned.
- Terminal calls are isolated.
- MQL5 and Python mirrors exist.

# Architectural

- No strategy imports.
- No order authority.
- No duplicated terminal market APIs.
- No current forming bars in canonical history.
- Fail-closed policies are documented and machine-readable.

# Quality

- Combined Python tests pass.
- Static boundaries pass.
- MetaEditor and terminal self-test evidence is attached locally.
- Documentation and manifests are complete.
- Phase 04 handoff is unambiguous.
