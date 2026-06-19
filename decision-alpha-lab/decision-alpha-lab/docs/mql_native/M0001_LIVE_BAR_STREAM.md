# M0001 Live Bar Stream

## Problem

The first MQL-native version recomputed the engine by loading a whole bar window
with `CopyRates()` on every update. That is convenient for research snapshots,
but it does not express the strict live mental model:

```text
new candle closes -> append exactly that candle -> update state
```

## Decision

The active M0001 Expert now runs in live-stream mode by default.

```text
InpUseLiveBarStream = true
InpWarmupHistoricalBars = 0
InpStartFromNextClosedBar = true
```

This means:

1. The Expert does not bulk-copy history at attach time.
2. It waits for the next newly closed candle.
3. On each new closed candle, it reads only `shift=1`.
4. That single bar is appended to the in-memory chronological stream.
5. L-rule nodes, M0001 events, and visuals are recomputed from that live stream.

## Inputs

```text
InpBars = 800
InpUseLiveBarStream = true
InpWarmupHistoricalBars = 0
InpStartFromNextClosedBar = true
InpTimerMilliseconds = 100
```

`InpBars` is now the rolling stream capacity, not a bulk-copy request, when
`InpUseLiveBarStream=true`.

## Optional warmup

For research convenience, you may set:

```text
InpWarmupHistoricalBars = 200
```

This loads only historical context at attach time. For strict forward-only visual
validation, keep it at `0`.

## Fallback mode

The old snapshot mode remains available:

```text
InpUseLiveBarStream = false
```

In that mode, the Expert uses `DAL_LoadBarsChronological()` / `CopyRates()` as a
fallback research snapshot loader.
