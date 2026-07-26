# Phase 03 Hunt Anatomy Specification

## Purpose

The purpose of Phase 03 is to let the robot detect raw hunts exactly according to the strategy architect doctrine.

A hunt is not a divergence. A hunt is not a trade. A hunt is not a confirmed signal. A hunt is only the event where one symbol's current-cycle price range touches or breaks one of its own prior same-day CG references.

## Inherited contracts

Phase 03 inherits these contracts without modification:

```text
Phase 01: New York 18:00 -> 17:00 trading-day field
Phase 01: complete Cycle Group registry
Phase 02: all previous same-day completed CG cycles are reference candidates
Phase 02: each symbol is compared only to its own references
```

Phase 03 must not create a second time system or a second reference system.

## Hunt definition

For a high reference:

```text
current_cycle_high >= reference_high
```

For a low reference:

```text
current_cycle_low <= reference_low
```

Equality counts. A close beyond the level is not required. A wick touch is enough.

## Current-cycle range

The current-cycle range is aggregated from M1 bars:

```text
current_cycle_high = max(M1.high from current_cycle_start to now)
current_cycle_low  = min(M1.low from current_cycle_start to now)
```

This gives the robot a neutral observation of what the current cycle has already touched.

## No close confirmation yet

Phase 03 intentionally does not wait for the chart timeframe candle close.

That belongs to Phase 04/Phase 05, where raw hunts become candidate divergence states and then confirmed tradeable signals.

The Phase 03 output is therefore a raw observation field:

```text
raw_hunt_detected
not_hunted
missing_reference
missing_current_range
```

## Both symbols may hunt

Phase 03 records whether:

```text
only Symbol A hunted
only Symbol B hunted
both symbols hunted
neither symbol hunted
```

However, it does not decide whether one-sided high/low hunts are divergence or whether both-symbol hunts invalidate divergence. That belongs to later phases.

## No quality judgment

Phase 03 does not know whether a hunt is good or bad. It does not rank CGs, directions, references, sessions, stop sizes, or symbol roles.

It only records the hunt anatomy.
