---
title: "Time Kernel Reference"
status: implemented
phase: PHASE_03
language: en
tags:
  - strategy-factory
  - phase03
  - mql5
  - market-services
---

# Responsibilities

`CSF03TimeKernel` is the only canonical runtime clock service. It implements the Phase 02 clock port and supports four modes:

- GMT native;
- fixed broker offset;
- inferred server offset;
- fixture time.

Fixture mode exists for deterministic tests. Inferred mode is diagnostic and must not replace explicit broker configuration without verification.

## Canonical representation

```text
UTC epoch milliseconds
```

The kernel also preserves source identifiers and offsets through Phase 01 timestamp contracts.

## Supported transformations

- terminal server time → UTC;
- UTC → New York offset;
- UTC → fixed-offset local wall time;
- UTC → broker-local wall time;
- UTC → trading-day identity.

## Invariants

1. Offsets are bounded to ±14 hours.
2. Naive Python datetimes are rejected in the mirror.
3. DST intervals are half-open.
4. Trading-day rollover is explicit and versionable.
5. Timezone conversion is never performed ad hoc inside strategies.
6. Timestamps from the future fail validation.

## Performance

DST boundary calculations are deterministic calendar arithmetic and do not require external timezone databases in MQL5. Later optimization may cache yearly boundaries, but the current computation is already bounded and independent of history length.

## Deferred concern

Some brokers change server offset seasonally on a schedule that is not identical to New York. The kernel supports fixed and inferred offsets, but broker-specific offset calendars will be added only when an actual deployment requires them and fixtures are available.
