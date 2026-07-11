---
title: "New York DST and Golden Fixtures"
status: implemented
phase: PHASE_03
language: en
tags:
  - strategy-factory
  - phase03
  - mql5
  - market-services
---

# Rule

New York daylight saving time is implemented using current United States rules:

- begins on the second Sunday in March at 07:00 UTC;
- ends on the first Sunday in November at 06:00 UTC.

The interval is half-open:

```text
[start, end)
```

## Why this matters

The project contains temporal doctrines in which five minutes of displacement can change:

- session membership;
- trading-day ownership;
- cycle identity;
- reference freshness;
- outcome horizon;
- event order.

DST is therefore a causal contract, not a display preference.

## Golden fixtures

Both MQL5 and Python tests cover:

- winter offset = −300 minutes;
- summer offset = −240 minutes;
- one millisecond before DST start;
- exact DST start;
- one millisecond before DST end;
- exact DST end.

Future Daye and quarterly modules must consume this service rather than embedding their own DST tables.

## Versioning

If legal rules change, the time-kernel version must change. Historical experiments keep the version used when the run was generated. A change to time semantics may require artifact invalidation and full regeneration.
