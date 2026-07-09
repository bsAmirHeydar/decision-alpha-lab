# PHASE06 HOTFIX 004 — Real Drawing Lines, Markers, and Vertical Objects

## Purpose

The screenshot showed that Phase 06 was placing text labels on both charts but the actual visual geometry was not visible. This hotfix repairs the visual layer so the chart receives visible, selectable, non-hidden drawing objects rather than text-only audit labels.

## Problem Observed

Visible:

- text labels
- possible platform/current-price lines

Missing or not visually obvious:

- main divergence origin-to-destination line
- origin marker
- destination marker
- origin vertical
- destination vertical
- confirmation vertical
- strong visual leg between reference and current extreme

## Root Cause Category

This was treated as a visual-object robustness problem, not a strategy problem.

The strategy anatomy is unchanged. The hotfix focuses on the drawing layer only:

- force all visual object flags on by default
- repair cases where saved EA inputs leave new drawing flags disabled
- make trend objects visible with no left/right rays
- add high-z-order / non-hidden object settings
- add a black shadow under the main divergence leg
- enforce a minimum time span if origin and destination times collapse to the same timestamp

## What Changed

### New input

```mql5
input bool InpForceAllVisualObjectsOn = true;
```

When this is true, the drawing module forces these flags on internally:

- enable drawing
- draw on both input-symbol charts
- open missing input-symbol charts
- draw confirmed states
- draw invalidated double-hunt states
- draw main origin-to-destination line
- draw origin marker
- draw destination marker
- draw origin vertical
- draw destination vertical
- draw confirmation marker
- draw reference-cycle anchor
- draw hunter reference guide
- draw hunter current-extreme guide
- draw clean reference guide
- draw clean stop-reference guide
- draw clean comparison line
- draw text label

This prevents old `.set` files or previously attached EA inputs from keeping the geometry disabled.

### Strong main leg

The primary divergence leg is now drawn with a shadow plus a main line:

```text
shadow line: black, thicker
main line: signal color, thick
```

This makes the leg visible on gray, dark, light, and mixed chart backgrounds.

### Trend object hardening

Trend objects now explicitly set:

- `OBJPROP_RAY_LEFT = false`
- `OBJPROP_RAY_RIGHT = false`
- `OBJPROP_HIDDEN = false`
- `OBJPROP_TIMEFRAMES = OBJ_ALL_PERIODS`
- `OBJPROP_ZORDER = 1000`
- selectable object state
- back=false

### Minimum visual span

If the origin and destination timestamps collapse to the same value, the module pushes the destination forward by a safe visual span. This prevents a real line from becoming visually compressed into a single vertical pixel.

## What This Hotfix Does Not Change

- no trade
- no order
- no risk
- no target
- no stop placement
- no position management
- no statistical ranking
- no AI
- no CG filtering
- no strategy mutation

## Expected Result

After installing this hotfix, the chart should show more than text labels. For each confirmed or invalidated state, visible geometry should include:

- thick main divergence leg
- origin marker
- destination marker
- vertical origin line
- vertical destination line
- vertical confirmation line
- reference/current guide segments
- optional label

## Validation

Compile:

```text
mql5/Experts/IntermarketDivergenceExecution/EXP0017_CG_Visual_Ledger_Anatomy.mq5
```

Attach to one of the configured input-symbol charts. Confirm both configured symbol charts are open. When a final state appears, inspect Object List and search for prefix:

```text
EXP0017_P06_
```

You should see object names ending in:

- `origin_to_destination_*`
- `origin_to_destination_*_shadow`
- `origin_marker_*`
- `destination_marker_*`
- `origin_vertical_*`
- `destination_vertical_*`
- `confirmation_close_vertical_*`
- `reference_guide_*`
- `current_extreme_guide_*`
- `reference_cycle_anchor_*`
- `visual_label_*`
