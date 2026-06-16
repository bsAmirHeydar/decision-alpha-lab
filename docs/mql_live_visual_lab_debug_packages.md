# M0001 Visual Debug Packages

The MT5 expert is visual-only. All rows come from the Python visual contract.

Manual visual toggles default to `false`. Use `InpViewPreset` to turn on a complete inspection package, or keep `InpViewPreset = 0` and enable individual layers manually.

## Presets

```text
0  Custom manual toggles
1  Structural Node Audit
2  Territory Construction Audit
3  Event Entry Exit Audit
4  Baseline vs Inside Sample Audit
5  RTV Formula Audit
6  Hunt Validation Audit
7  Live/Open Event Audit
8  Candle Classification Audit
9  State Machine Audit
10 Focused Event Inspector
11 Multi Event Overview
12 Full Research Lab
```

## Recommended validation order

```text
1  Structural Node Audit
2  Territory Construction Audit
3  Event Entry Exit Audit
4  Baseline vs Inside Sample Audit
5  RTV Formula Audit
6  Hunt Validation Audit
10 Focused Event Inspector
```

## Package 1 — Structural Node Audit

Shows:

```text
NODE
NODE_PRICE
ACTIVE_FROM
CONFIRMATION_WINDOW
```

Question answered:

```text
Was the node confirmed only after L bars, and did the event logic start only after active_from?
```

## Package 2 — Territory Construction Audit

Shows:

```text
NODE_PRICE
EXPANSION_EXTREME
TERRITORY
RTV_LABEL
```

Question answered:

```text
Was the territory built from node_price and expansion_extreme correctly?
```

## Package 3 — Event Entry Exit Audit

Shows:

```text
EVENT
ENTRY
EXIT
```

Question answered:

```text
Did the event start on the first wick intersection and close through exit_gap logic?
```

## Package 4 — Baseline vs Inside Sample Audit

Shows:

```text
BEFORE_SAMPLE
INSIDE_SAMPLE
OUTSIDE_ACTIVE
```

Question answered:

```text
Were mean_before and mean_inside calculated from the correct candles?
```

## Package 5 — RTV Formula Audit

Shows:

```text
RTV_LABEL
RTV_FORMULA
EVENT_INFO
```

Question answered:

```text
Does RTV equal mean_inside / mean_before for this event?
```

## Package 6 — Hunt Validation Audit

Shows:

```text
NODE_PRICE
HUNT
EVENT
```

Question answered:

```text
Did the hunt marker appear on the first candle that breached node_price?
```

## Package 10 — Focused Event Inspector

Shows the cleanest inspection view for a selected event:

```text
TERRITORY
EVENT
ENTRY
EXIT
BEFORE_SAMPLE
INSIDE_SAMPLE
RTV_LABEL
RTV_FORMULA
HUNT
EVENT_INFO
```

Use filters:

```text
InpFocusNodeId
InpFocusRevisitId
InpOnlyHunted
InpOnlyStrongRtv
InpMinRtv
InpMaxRtv
```
