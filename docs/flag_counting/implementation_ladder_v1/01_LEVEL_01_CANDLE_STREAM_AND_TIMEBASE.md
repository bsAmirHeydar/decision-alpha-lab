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

## Purpose

This layer defines the only time and bar foundation used by all later engines. Phoenix must not build structural geometry from synthetic time interpolation. Market gaps, weekends, broker sessions, and missing bars must not distort curves or node ownership.

## Owned source modules

Primary:

```text
mql5/Experts/FlagCounting/FlagCountingPhoenixExperiment.mq5
mql5/Include/FlagCountingPhoenix/FP_Types.mqh
```

Consumed by:

```text
FP_NodeEngine.mqh
FP_Renderer.mqh
FP_Audit.mqh
```

## Inputs

- `MqlRates rates[]`
- `rates_total`
- symbol
- timeframe
- configured lookback range

## Outputs

A normalized internal bar view:

```text
bar_index
bar_time
high
low
```

## Non-negotiable rules

### Rule 1 — Bar index is the structural x-axis

All structural objects must store candle anchors by index. Time is display metadata. The index is the structural position.

### Rule 2 — Curve sampling uses bar index, not linear time

Curves must be sampled across candle indices and then mapped to real `rates[index].time`. They must not generate artificial timestamps between bars.

### Rule 3 — Time gaps are display gaps only

A weekend gap cannot change whether a flag exists. A missing broker candle cannot make a curve bow incorrectly. A curve has to step through existing bars only.

### Rule 4 — Index direction must be globally fixed

The code must choose one convention and document it:

```text
older bars have lower index
newer bars have higher index
```

or the opposite. All modules must use the same convention. No module may reverse arrays privately without mapping back to canonical anchors.

## Acceptance tests

### Test 01 — Gap-safe curve

Given three anchors:

```text
start_idx = 100
waist_idx = 120
end_idx = 150
```

The renderer must sample indices 100..150 and map each sample to `rates[i].time`. It must not calculate `start_time + ratio * (end_time - start_time)`.

### Test 02 — Anchor stability

If chart history contains a weekend gap between indices 120 and 121, the object anchors remain 100, 120, and 150.

### Test 03 — Deterministic replay

Running the engine twice over the same `rates[]` must emit the same anchor indices.

## Common failure symptoms

- Curves look broken or stretched across session gaps.
- A curve endpoint lands between candles.
- The same object moves horizontally after zoom/history reload.
- Different modules refer to the same node by different index conventions.

## Freeze condition

This layer is frozen when all structural objects in `FP_Types.mqh` contain canonical index anchors and renderer uses real `rates[index].time` only for display.
