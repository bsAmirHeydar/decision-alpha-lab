# EXP0017 Lab — Cycle Group Intermarket Divergence

## Lab role

This lab folder is the execution research container for the independent CG Intermarket Divergence EA.

The strategy is intentionally separate from previous STC/SMT implementations. It uses a New York 18:00-to-17:00 trading day and many configurable cycle groups.

## Current phase

```text
Phase 01 — Documentation and architecture only
```

No MQL5 code is included in this patch.

## Core rule

```text
If one symbol hunts a reference high/low and the other symbol does not, divergence exists after candle close.
```

## Baseline assumptions

- two symbols: SPXUSD and NDXUSD by default;
- all CGs start at 18:00 New York;
- day ends at 17:00 New York;
- hunt is touch-only and inclusive;
- confirmation requires closed chart timeframe candle;
- trade occurs on clean symbol;
- stop uses clean symbol reference level;
- target is current cycle end;
- risk is 1% of equity;
- previous trading day data is not required for entry.

## Next implementation phase

The next patch should add:

```text
mql5/Experts/IntermarketDivergenceCG/CG_IntermarketDivergence_EA.mq5
mql5/Include/IntermarketDivergenceCG/*.mqh
```

Recommended first code scope:

1. compile-safe EA skeleton;
2. full inputs for all 21 CGs;
3. modular time and cycle calendar;
4. non-trading divergence detector;
5. audit prints/logs;
6. drawing only after detection is stable.

