# M0001 Hard Clean Visual

## Problem

The chart still showed red/blue lines tracking candle highs/lows. These lines were
not part of the desired node output.

Desired node output:

```text
HIGH node: red arrow + price text above it
LOW node : green arrow + price text below it
```

No high/low trace lines, no chevron wings, no indicator traces.

## Fix

The Expert now has hard cleanup controls:

```text
InpPurgeTraceLines = true
InpPurgeMainWindowIndicators = true
```

`InpPurgeTraceLines` deletes trend/channel style chart objects on every redraw.
`InpPurgeMainWindowIndicators` removes main-window indicators on init, useful when
ZigZag-style traces remained attached to the chart.

## Price label spacing

Node price labels now use separate gaps:

```text
InpHighNodePriceTextGapPoints = 120
InpLowNodePriceTextGapPoints = 120
InpNodePriceTextFontSize = 9
```

This moves high labels higher and low labels lower for readability.

## Version

`M0001_LiveVisualLab.mq5` version: `1.15`.
