# M0001 Clean Arrow Markers

## Change

The default node marker is now a clean `OBJ_ARROW`, not a two-segment chevron.

This removes the red/green diagonal wing lines that visually tracked around candle
highs/lows and made the chart noisy.

## Inputs

```text
InpNodeMarkerStyle = 0
InpNodeArrowWidth = 2
```

Optional old chevron mode remains available:

```text
InpNodeMarkerStyle = 1
```

## Node price labels

`InpShowNodePrices=true` draws a simple local text label:

- HIGH node: price text above the high-node arrow
- LOW node: price text below the low-node arrow

Full horizontal price lines are still disabled by default:

```text
InpShowNodePriceLines = false
```

Use `InpNodePriceTextGapPoints` and `InpNodePriceTextFontSize` to tune readability.
