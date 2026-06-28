# Phoenix Flag Counting Implementation Ladder V1

This document is part of the implementation ladder for the Phoenix Flag Counting engine. The ladder is intentionally layered so that lower layers become frozen foundations before higher layers are allowed to depend on them.

Global non-negotiables:

- All structural decisions use candle `high` and `low` only.
- `open`, `close`, candle body, candle color, volume, and indicators are not structural inputs.
- Equality is not a break. A level is broken only by a strict pass beyond it.
- The renderer is non-authoritative. It may only draw logical objects emitted by engines.
- Main-chart rendering and audit rendering are separate products.
- Every layer must expose enough audit fields to prove why an object exists.
- A higher layer may never silently repair a lower-layer defect.

# Level 01 — Candle Stream and Timebase

Status: **implemented / foundation freeze candidate**.

Highest touched code level: **Level 01 only**.

## Purpose

This layer defines the only time and bar foundation used by all later engines. Phoenix must not build structural geometry from synthetic time interpolation. Market gaps, weekends, broker sessions, and missing bars must not distort curves, node ownership, or sequence ownership.

Level 01 is deliberately boring. It does not detect nodes, Hooks, F1, F2, or F3. It only guarantees that every higher layer receives the same canonical candle stream.

## Final canonical convention

Phoenix uses exactly one structural x-axis convention:

```text
index 0 = oldest canonical bar
index increases toward newer bars
current forming live candle is excluded by default
bar index is structural authority
time is display metadata
```

`InpBarsToScan` now means requested **closed** bars when `InpUseClosedBarsOnly=true`. The loader copies one extra raw terminal bar and drops the current forming live candle before structural engines run.

## Owned source modules

Level 01 is split into small modules so debugging can isolate failures quickly:

```text
mql5/Include/FlagCountingPhoenix/FP_BarSnapshot.mqh
mql5/Include/FlagCountingPhoenix/FP_TimebaseTypes.mqh
mql5/Include/FlagCountingPhoenix/FP_SeriesContract.mqh
mql5/Include/FlagCountingPhoenix/FP_Timebase.mqh
mql5/Experts/FlagCounting/FlagCountingPhoenixExperiment.mq5
```

Responsibilities:

| Module | Responsibility |
|---|---|
| `FP_BarSnapshot.mqh` | One-bar diagnostic snapshot and OHLC sanity helper. |
| `FP_TimebaseTypes.mqh` | Config/report structs for the candle stream contract. |
| `FP_SeriesContract.mqh` | Validates canonical ordering, duplicate time, OHLC sanity, minimum bar count. |
| `FP_Timebase.mqh` | The only Phoenix `CopyRates` gateway. Loads canonical closed-bar arrays. |
| `FlagCountingPhoenixExperiment.mq5` | Wires Level 01 output into the rest of Phoenix. |

Consumed by:

```text
FP_NodeEngine.mqh
FP_HookEngine.mqh
FP_FlagBodyEngine.mqh
FP_InternalCountEngine.mqh
FP_SequenceEngine.mqh
FP_Renderer.mqh
FP_Audit.mqh
```

Higher layers must consume the canonical `rates[]` passed by the EA. They must not call `CopyRates` privately.

## Inputs

EA inputs added by this level:

```text
InpBarsToScan             requested canonical closed bars when closed-only mode is on
InpUseClosedBarsOnly      default true; drop current live candle before structural scan
InpStrictTimebase         default true; abort if canonical contract fails
InpMinClosedBars          default 200; minimum accepted canonical closed bars
InpPrintTimebaseSanity    default true; print one structured Level 01 report per run
InpPrintTimebaseSamples   default false; print first/last bar snapshots for debugging
```

Raw terminal source:

```text
CopyRates(symbol, timeframe, 0, requested_bars + live_pad, raw_rates)
```

The loader then normalizes to:

```text
ArraySetAsSeries(canonical_rates, false)
canonical_rates[0]                  oldest closed bar
canonical_rates[canonical_bars - 1] newest closed bar
```

## Outputs

A canonical internal bar stream:

```text
MqlRates canonical_rates[]
int      canonical_bars
```

And an audit report:

```text
FP_TimebaseReport
```

Important report fields:

```text
status
ok
reason
symbol
timeframe
requested_bars
requested_copy_bars
raw_bars
canonical_bars
closed_only
dropped_live_bars
dropped_old_bars
raw_array_as_series
canonical_array_as_series
time_ascending
strict_increasing_time
duplicate_time_found
ohlc_valid
first_index
last_index
first_time
last_time
newest_raw_time
excluded_live_time
bad_time_idx
duplicate_idx
bad_ohlc_idx
```

## Non-negotiable rules

### Rule 1 — Bar index is the structural x-axis

All structural objects must store candle anchors by index. Time is display metadata. The index is the structural position.

### Rule 2 — Curve sampling uses bar index, not linear time

Curves must be sampled across candle indices and then mapped to real `rates[index].time`. They must not generate artificial timestamps between bars.

### Rule 3 — Time gaps are display gaps only

A weekend gap cannot change whether a flag exists. A missing broker candle cannot make a curve bow incorrectly. A curve has to step through existing bars only.

### Rule 4 — Index direction is globally fixed

No module may reverse arrays privately. No module may use MT5 series indexing as structural truth. The only accepted convention is:

```text
older bars lower index
newer bars higher index
```

### Rule 5 — Closed-bar structural truth

Canonical historical detection uses closed bars only by default. The live candle can be inspected only when an explicit diagnostic mode disables `InpUseClosedBarsOnly`; it must not become the default historical truth.

### Rule 6 — Open/close remain non-structural

Level 01 may inspect open/close only to detect corrupted OHLC bars. Open/close/body/color still cannot create, confirm, invalidate, or rank nodes, Hooks, or F-levels.

## Sanity log contract

A normal run should print a line shaped like:

```text
FP_LEVEL01 status=ok ok=true reason=canonical_timebase_ready symbol=GOLD tf=PERIOD_M1 requested=5000 copy_requested=5001 raw=5001 canonical=5000 min_closed=200 closed_only=true dropped_live=1 dropped_old=0 raw_series=false canonical_series=false ascending=true strict_time=true duplicate_time=false ohlc=true first_idx=0 last_idx=4999 first_time=... last_time=... newest_raw=... excluded_live=... bad_time_idx=-1 duplicate_idx=-1 bad_ohlc_idx=-1
```

This line is now the first audit proof that every later node index uses the same base.

## Acceptance tests

### Test 01 — Closed-only loader

Given `InpBarsToScan=5000` and `InpUseClosedBarsOnly=true`, the report must show:

```text
copy_requested=5001
closed_only=true
dropped_live=1
canonical=5000
```

If fewer bars exist in terminal history, `canonical` may be lower, but the status must explain why.

### Test 02 — Canonical index direction

The report must show:

```text
canonical_series=false
ascending=true
strict_time=true
first_idx=0
last_idx=canonical_bars-1
first_time < last_time
```

### Test 03 — Strict failure behavior

If duplicate time, reversed time, invalid OHLC, or insufficient bars are detected while `InpStrictTimebase=true`, the EA must print:

```text
FP_SUMMARY status=timebase_failed
```

or:

```text
FP_SUMMARY status=not_enough_closed_bars
```

and must not run node/flag detection.

### Test 04 — Gap-safe curve

Given three anchors:

```text
start_idx = 100
waist_idx = 120
end_idx = 150
```

The renderer must sample indices 100..150 and map each sample to `rates[i].time`. It must not calculate `start_time + ratio * (end_time - start_time)`.

### Test 05 — Anchor stability

If chart history contains a weekend gap between indices 120 and 121, object anchors remain 100, 120, and 150. The time gap is display metadata only.

### Test 06 — Deterministic replay

Running the engine twice over the same canonical `rates[]`, inputs, and range must emit the same anchor indices and Level 01 report except for terminal/environment fields such as available raw history.

## Common failure symptoms

- `canonical_series=true` appears in the Level 01 report.
- `ascending=false` or `strict_time=false` appears.
- A structural layer calls `CopyRates` directly.
- A curve endpoint lands between candles.
- A node id changes only because a module reversed its private array.
- Live candle movement changes historical nodes when closed-only mode is enabled.

## Freeze condition

This layer is frozen when:

1. Phoenix has exactly one `CopyRates` gateway: `FP_LoadCanonicalRates`.
2. The EA passes only canonical bars to downstream engines.
3. `FP_LEVEL01` sanity output proves closed-only, ascending, non-series arrays.
4. Every structural object in `FP_Types.mqh` stores canonical index anchors.
5. Renderer uses real `rates[index].time` only for display.

## Patch note

This implementation is intentionally modular and conservative. It changes the input stream from “whatever `CopyRates` returned” to “validated canonical closed-bar stream.” Higher-layer behavior may shift by one bar compared with older Phoenix output because the current live candle is no longer structural truth by default. That change is intentional and canon-aligned.
