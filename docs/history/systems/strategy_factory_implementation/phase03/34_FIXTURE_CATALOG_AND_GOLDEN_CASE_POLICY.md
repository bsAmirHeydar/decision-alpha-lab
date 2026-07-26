---
title: "Fixture Catalog and Golden Case Policy"
status: implemented
phase: PHASE_03
language: en
tags:
  - strategy-factory
  - phase03
  - mql5
  - market-services
---

# Fixture source

`CSF03FixtureMarketSource` provides deterministic ticks, bars, and symbol specifications to MQL5 tests without terminal access.

# Minimum fixture catalog

- ordinary ordered bars;
- duplicate closed bar;
- same-open-time replacement;
- one-bar gap;
- historical regression;
- stale tick;
- ask below bid;
- prefixed broker symbol;
- specification drift;
- New York DST start and end;
- cross-midnight session;
- synchronized pair;
- skewed pair;
- missing secondary symbol.

# Golden-case rule

Every production bug in market/time/synchronization code must become a permanent fixture before the fix is accepted.

# Cross-language parity

Where Python mirrors a rule, the fixture should be represented in a machine-readable form and evaluated in both runtimes. Time and identity differences are release blockers.

# Isolation

Fixtures are not production adapters. They may expose deterministic setters and simplified storage that would be inappropriate in live runtime.
