# EXE0005 — Continuation Close-Break Fixed-R

## Purpose

This execution module tests the clean continuation idea separately from trailing/regime-exit models.

It enters after a confirmed structural node is broken by candle close while the H0005/M0002 regime is continuation.

## Main idea

```text
Regime = continuation
Node break = close-confirmed
Entry = market on the next processing pass
SL = ATR multiple, default 4 ATR
TP = fixed R, default 1R
```

## Main inputs

```text
InpAtrPeriod = 14
InpAtrMultiplier = 4.0
InpRewardR = 1.0
InpMaxSimultaneousTrades = -1
InpMaxEntriesPerBar = 3
```

## Notes

E0005 is intentionally different from E0003.

E0003 can be a trailing/regime-exit continuation executor.

E0005 is a fixed-reward continuation executor, designed for clean statistical comparison of continuation close-break entries with fixed R exits.
