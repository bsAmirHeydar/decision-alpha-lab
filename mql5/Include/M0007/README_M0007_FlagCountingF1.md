# M0007 — F1 Flag Counting MQL5 Module

M0007 counts and draws F1 flag structures on chart for visual/audit research.

## Correct F1 topology

The detector now uses the actual four-node F1 origin logic.

Bullish F1:

```text
Start LOW -> Leg 1 HIGH -> Correction LOW -> Leg 2 HIGH
```

A bullish F1 is accepted only when:

```text
Leg 1 high > Start low
Correction low is below Leg 1 high
Correction low remains above Start low
Leg 2 high breaks/sweeps Leg 1 high
```

Bearish F1:

```text
Start HIGH -> Leg 1 LOW -> Correction HIGH -> Leg 2 LOW
```

A bearish F1 is accepted only when:

```text
Leg 1 low < Start high
Correction high is above Leg 1 low
Correction high remains below Start high
Leg 2 low breaks/sweeps Leg 1 low
```

This fixes the earlier schematic problem where the chart origin was synthetic or taken from the wrong side of the structure.

## Visual contract

The renderer draws only the clean F1 grammar:

```text
Start -> straight Leg 1 -> end of Leg 1
end of Leg 1 -> smooth curved correction -> end of Leg 2
```

No horizontal guide levels, no vertical audit lines, and no internal N/R labels are drawn by default.

## Files

```text
mql5/Experts/M0007/M0007_FlagCountingF1.mq5
mql5/Include/M0007/DAL_M0007F1Types.mqh
mql5/Include/M0007/DAL_M0007F1NodeDetector.mqh
mql5/Include/M0007/DAL_M0007F1Detector.mqh
mql5/Include/M0007/DAL_M0007F1Renderer.mqh
```

## Inputs

Important inputs:

```text
InpLMin / InpLMax          adaptive L-node range
InpBreakMode              wick break or close break for Leg 2 confirmation
InpEpsilonPoints          extra sweep/break distance
InpMaxEventsToDraw        number of latest F1 schematics to draw
InpShowTextLabels         show/hide Start, Leg 1, Correction, Pullback, Leg 2 labels
InpShowBadge              show/hide BULLISH F1 / BEARISH F1 badge
InpRedrawOnNewBar         redraw only on new bar, not every tick
```

## Scope

M0007 is visual/audit-only. It does not place orders.


## 2026-06 fix — real origin plus post-leg-2 internal 1/2

The renderer must not invent the origin. `Start` is now a first-class detector node and is stored in every `M0007_F1Event`.

Current core:

```text
Bullish F1:
Start LOW -> Leg1 HIGH -> Correction LOW -> Leg2 HIGH

Bearish F1:
Start HIGH -> Leg1 LOW -> Correction HIGH -> Leg2 LOW
```

The chart numbers are **not** leg labels.

Current numeric count:

```text
Bullish after Leg2:
1 = first internal low after H2
2 = later internal low below 1

Bearish after Leg2:
1 = first internal high after L2
2 = later internal high above 1
```

Default overlay:

```text
F1 path
F1
internal 1
internal 2
```

Removed from the default overlay:

```text
Start text
Leg 1 text
Correction text
Pullback / Correction text
Leg 2 text
BULLISH F1 / BEARISH F1 text
horizontal/vertical audit guide lines
status panel
```


## Confirmation contract update

Current default F1 confirmation is intentionally stricter:

- `InpRequireLeg2BreakForConfirm = true` by default.
  The four-node structure can exist after `Start -> Leg 1 -> Correction -> Leg 2`, but it is not confirmed until price breaks the Leg-2 extreme after `H2/L2`.

- `InpRequireInternal12ForF1 = true` by default.
  The detector only keeps F1 candidates that have the post-leg-2 internal `1` and `2` count.

The chart labels `1` and `2` remain internal post-leg-2 counts, not Leg-1/Leg-2 labels.
Bullish F1 counts two descending lows after Leg 2. Bearish F1 counts two ascending highs after Leg 2.

## Strict confirmation after internal 1/2

The current strict F1 contract is:

1. Build the four-node F1 skeleton: `Start -> Leg1 -> Correction/Waist -> Leg2`.
2. Build the post-leg2 internal count:
   - bullish: internal `1` and `2` are two descending lows after Leg2,
   - bearish: internal `1` and `2` are two ascending highs after Leg2.
3. The internal `1` and `2` must not break the flag waist/correction level:
   - bullish internals must remain above `W`,
   - bearish internals must remain below `W`.
4. Only after valid internal `1/2`, price must move again in the original F1 direction and re-break the Leg2 extreme.
5. F1 is confirmed only at that post-internal re-break.

Default inputs enforce this strict behavior:

```mql5
InpRequireLeg2BreakForConfirm = true;
InpRequireInternal12ForF1 = true;
InpProtectWaistDuringInternal12 = true;
```


## Live forming / confirmed rendering contract

The default renderer now keeps all non-deleted F1 structures visible on the chart.

- Pending bullish F1 structures are drawn in a pending bullish color.
- Pending bearish F1 structures are drawn in a pending bearish color.
- Confirmed bullish F1 structures are recolored to the final bullish color.
- Confirmed bearish F1 structures are recolored to the final bearish color.
- Invalidated or deleted structures are not drawn on the next refresh.

Confirmation is strict: after Start, Leg 1, Correction/Waist, Leg 2, and internal 1/2, price must move again in the original direction and re-break the Leg 2 extreme. Until that post-1/2 rebreak happens, the F1 and its internal 1/2 labels remain pending. The internal 1/2 sequence is valid only while it stays before the waist; if the waist is broken first, the structure is invalidated and removed on redraw.


## Incremental chart object contract

The EA no longer clears the whole M0007 overlay on every recalculation.  Each F1 candidate has a stable object key based on:

```text
direction + Start.time + Leg1.time + Correction.time + Leg2.time
```

That means a pending structure is updated/recolored in place when its own state changes:

```text
pending bullish  -> InpBullishPendingColor
pending bearish  -> InpBearishPendingColor
confirmed bullish -> InpBullishConfirmedColor
confirmed bearish -> InpBearishConfirmedColor
invalidated/deleted -> only that event's objects are removed
```

`InpCleanObjectsOnInit` is enabled by default only to clear old legacy index-based objects when the EA is attached.  After that, redraws are event-key based and do not wipe previous valid drawings.


## Renderer hotfix: no default `Text` labels

The renderer now writes chart text through an update-in-place helper.  It verifies that `OBJPROP_TEXT` was committed successfully; if not, it deletes the half-created object instead of leaving the terminal default `Text` label on chart.

`InpCleanBrokenDefaultTextLabels` is enabled by default to remove legacy default `Text` objects left by earlier broken builds.  Normal redraws remain incremental and event-key based.


## Renderer repair — compact object names

The renderer now uses compact stable object keys instead of full timestamp chains in the chart object name.
This prevents MetaTrader from creating broken default `Text` labels when object names become too long.
`InpCleanObjectsOnInit=true` and `InpCleanBrokenDefaultTextLabels=true` should be kept enabled for one attach cycle to clean legacy broken objects from previous builds.


## Renderer rollback / safe draw contract

The renderer was restored to the stable safe-draw model:

- clear the M0007 object layer on each recalculation,
- redraw all current non-invalidated F1 events from the detector,
- use short event-number based object names,
- avoid long stable event keys,
- avoid text commit verification that can leave MT5 default `Text` labels,
- keep the minimal visual grammar: `F1`, internal `1`, internal `2`, and the F1 path.

This keeps the latest detector logic intact while restoring the chart output to a reliable drawing path.
