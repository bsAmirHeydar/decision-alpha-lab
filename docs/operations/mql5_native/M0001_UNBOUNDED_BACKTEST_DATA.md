# M0001 Unbounded Backtest Data

## Change

Backtests are no longer limited by an arbitrary candle count.

Default:

```text
InpBars = 0
```

Meaning:

```text
0 = use all bars available in the selected Strategy Tester date range/history
```

If you want a rolling cap for performance, set:

```text
InpBars = 5000
```

or any positive number.

## Live stream behavior

`DAL_AppendBarChronological()` now treats `max_bars <= 0` as unbounded. It keeps
every newly closed candle in chronological order and does not drop old candles.

This means Strategy Tester controls the sample using its own symbol/timeframe/date
range, not the EA.

## Fallback bulk loader

`DAL_LoadBarsChronological()` also treats `requested_bars <= 0` as all available
bars from `Bars(symbol, timeframe)`, instead of falling back to 500.

## Computation limits

Default computed event cap is now:

```text
InpMaxEvents = 0
```

Meaning unlimited computed events.

Visual caps are also zero by default:

```text
InpMaxNodesToDraw = 0
InpMaxEventsToDraw = 0
InpMaxAuditStatesToDraw = 0
```

Meaning draw all audit objects. For very long tests, set positive draw caps if the
chart becomes slow.

## Version

`M0001_LiveVisualLab.mq5` version: `1.25`.
