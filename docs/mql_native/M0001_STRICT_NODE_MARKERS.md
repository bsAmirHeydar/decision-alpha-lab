# M0001 Strict Node Markers

## Change

M0001 node visualization is now strict arrow-only.

The visual layer no longer draws chevron wing segments for nodes and no longer
draws full-chart horizontal node price lines.

The only node objects are:

```text
OBJ_ARROW  = node marker
OBJ_TEXT   = optional local node price label
```

## Why

Chevron markers are implemented as `OBJ_TREND` segments. On dense M1 charts they
look like high/low tracing lines around candles. This is visually noisy and makes
node inspection harder.

## Inputs

```text
InpShowNodePrices = true
InpShowNodePriceLines = false
InpNodeMarkerStyle = 0  # retained but ignored; strict arrow mode is forced
```

## Price labels

When `InpShowNodePrices=true`:

- HIGH node price is written above the red down arrow
- LOW node price is written below the green up arrow

## Warning fix

Arrow marker anchor typing now uses `ENUM_ARROW_ANCHOR`, not `ENUM_ANCHOR_POINT`,
so MetaEditor should no longer warn about implicit enum conversion.
