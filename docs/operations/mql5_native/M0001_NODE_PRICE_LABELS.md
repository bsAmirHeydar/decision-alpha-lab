# M0001 Node Price Labels

## Change

`InpShowNodePrices` no longer draws full-chart horizontal lines.

It now draws a local text label near the node marker:

- HIGH node: price text above the red chevron
- LOW node: price text below the green chevron

This keeps the chart clean while still showing the exact node price.

## Inputs

```text
InpShowNodePrices = true
InpNodePriceTextGapPoints = 35.0
InpNodePriceTextFontSize = 8
```

The old full-chart line behavior is still available separately:

```text
InpShowNodePriceLines = true
```

Default:

```text
InpShowNodePriceLines = false
```

## Reason

Full horizontal node-price lines create visual noise and can make structural
inspection harder on M1/M5 charts. Local labels keep the chart readable and make
each node's exact price obvious.
