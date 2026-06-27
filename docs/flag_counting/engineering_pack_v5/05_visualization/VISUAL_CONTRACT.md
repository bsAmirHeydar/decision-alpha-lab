# Visual Contract

## Rendering Inputs

Renderer receives render model objects:

```text
RenderFlagBody
RenderOriginMarker
RenderFLabel
RenderInternalNumberLabel
RenderHookArc
RenderStatusPanelItem
```

It does not receive raw bars to infer structures.

## Flag Body Rendering

A flag body uses two visual pieces:

```text
Origin -> Leg1: straight thin line
Leg1 -> Waist -> Leg2: smooth arc through true Waist
```

All flag lines are thin by default.

Do not make larger scale lines thick by default. Use label and shade, not width.

## Smooth Arc Requirement

The curve must not look like broken angular trendlines.

Implementation options:

- polyline sampled from quadratic Bezier through Waist;
- arc-like curve with enough sample points;
- platform curve object if available and stable.

Minimum visual rule:

```text
The curve must visibly pass through the true Waist.
```

The curve does not need to follow every candle. It must show body logic.

## ND / Hook Rendering

ND/Hook uses gray arc/semicircle.

```text
from hook start node
to ND formation/final node
```

Do not draw the 50% line by default.

## Origin Marker

Show `O` by default during research.

Input:

```text
InpShowOriginLabels = true
```

## Labels

Research default uses detailed labels:

```text
F1 L8 Q23
F2 L8 Q23
F3 L8 Q23
ND L8 H17
1
2
3
4
O
```

`Q` can be sequence/chain id. `H` can be hook id.

## Colors

Use semantic color families:

```text
Bullish candidate
Bullish confirmed
Bearish candidate
Bearish confirmed
F3 completed/locked
ND/Hook gray
Invalid/rejected hidden by default
```

Within a semantic family, use shade variation for different sequence ids.

Do not use huge line width differences.

## Main Chart Defaults

```text
Draw all emitted sequences = true
Draw rejected = false
Draw ND hooks = true
Draw origin labels = true
Draw detailed labels = true
Fixed line width = 1
Use sequence shade variation = true
```

## Fidelity Rule

If a line appears, it must be traceable to a logical object id.

Object tooltip or label should make this possible.
