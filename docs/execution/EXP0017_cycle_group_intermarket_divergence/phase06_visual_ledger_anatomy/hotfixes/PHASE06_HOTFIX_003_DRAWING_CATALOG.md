# Phase 06 Hotfix003 — Complete Drawing Catalog

This document lists every visual object type currently available in the Phase 06 full visual language.

## 1. Main origin-to-destination divergence line

Object role:

```text
reference extreme -> current-cycle extreme
```

On hunter chart:

```text
hunter reference extreme -> hunter current extreme
```

On clean chart:

```text
clean reference extreme -> clean current extreme
```

Purpose:

```text
Show the exact leg that explains the intermarket divergence anatomy.
```

Input:

```text
InpDrawDivergenceOriginDestinationLine = true
```

## 2. Origin marker

Marks the origin of the visual leg.

Default meaning:

```text
reference-cycle high for SELL
reference-cycle low for BUY
```

Input:

```text
InpDrawOriginMarker = true
```

## 3. Destination marker

Marks the destination of the visual leg.

Default meaning:

```text
current-cycle high for SELL
current-cycle low for BUY
```

Input:

```text
InpDrawDestinationMarker = true
```

## 4. Origin vertical line

Vertical line through the origin time.

Input:

```text
InpDrawOriginVertical = true
```

## 5. Destination vertical line

Vertical line through the destination extreme time.

Input:

```text
InpDrawDestinationVertical = true
```

## 6. Confirmation close vertical line

Vertical line through the candle-close confirmation boundary.

Input:

```text
InpDrawConfirmationMarker = true
```

This line answers:

```text
When did this state become final under the closed-candle doctrine?
```

## 7. Reference-cycle anchor

Horizontal segment across the full reference-cycle time window at the reference price.

Input:

```text
InpDrawReferenceCycleAnchor = true
```

Purpose:

```text
Show which prior same-day cycle produced the reference.
```

## 8. Hunter reference guide

Horizontal guide at hunter reference price.

Input:

```text
InpDrawHunterReferenceGuide = true
```

## 9. Hunter current-extreme guide

Horizontal guide at hunter current-cycle extreme.

Input:

```text
InpDrawHunterCurrentExtremeGuide = true
```

## 10. Clean reference guide

Horizontal guide at clean reference price on the clean-symbol chart.

Input:

```text
InpDrawCleanReferenceGuide = true
```

## 11. Clean stop-reference guide

Horizontal guide at the clean symbol's future stop-reference preview.

Input:

```text
InpDrawCleanStopReferenceGuide = true
```

This is not an order and not a stop placement. It is visual metadata.

## 12. Clean comparison line

Symbol-local clean leg:

```text
clean reference extreme -> clean current extreme
```

Input:

```text
InpDrawCleanComparisonLine = true
```

Purpose:

```text
Show why the clean symbol remained clean at confirmation.
```

## 13. Visual label

Text object on the chart.

Input:

```text
InpDrawTextLabel = true
```

It includes:

```text
CG name
status
direction
role: HUNTER / CLEAN / DOUBLE_HUNT
symbol
reference cycle number
current cycle number
```

## 14. Tooltip metadata

Every major visual object receives a tooltip containing:

```text
phase
status
direction
side
CG
hunter symbol
clean symbol
reference cycle
origin time
origin price
destination time
destination price
note
```

## What is off by default?

Only the chart comment/panel is off:

```text
InpShowChartPanel = false
```

The visual drawing objects remain on.
