---
title: "Broker Time to UTC Mapping"
status: implemented
phase: PHASE_03
language: en
tags:
  - strategy-factory
  - phase03
  - mql5
  - market-services
---

# Problem

MetaTrader bar timestamps are expressed in broker server time. Treating them as UTC silently shifts sessions, daily boundaries, cycle groups, cross-symbol joins, and label horizons.

## Phase 03 approach

`CSF03TerminalMarketSource` receives server timestamps and converts them through `CSF03TimeKernel::ServerSecondsToUtcMilliseconds`.

```text
server seconds
− configured broker offset
=
UTC milliseconds
```

The source then creates Phase 01 `SF01_MarketTimestamp` values with explicit clock lineage.

## Configuration policy

For production-quality runs:

1. Record broker name and account server.
2. Determine server offset during the tested period.
3. Store offset configuration in the run manifest.
4. Revalidate after DST or broker schedule changes.
5. Do not mix artifacts produced under different clock configurations without an explicit migration.

## Failure handling

If the configured offset is outside the permitted range, initialization fails. If the current broker offset cannot be verified, the runtime remains diagnostic or paper-only until resolved.

## Historical caveat

A single fixed offset may be insufficient for long historical studies if the broker changed server offset. The future historical clock provider will accept interval-based offset records. Phase 03 establishes the port and lineage required for that extension without contaminating strategy logic.
