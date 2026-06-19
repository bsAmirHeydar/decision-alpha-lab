# M0001 Node Marker Precision and Bridge Performance Fix

## Node marker

The Python node price is the truth. The visual marker must point exactly to it.

Wingdings arrow glyphs in MT5 can have confusing visual centers/anchors. To avoid
glyph-anchor ambiguity, the default node marker is now a custom two-segment
chevron:

- HIGH node: red `V` marker, exact vertex at node high, wings above the candle
- LOW node: green `^` marker, exact vertex at node low, wings below the candle

Inputs:

```text
InpNodeMarkerStyle = 1
InpNodeChevronWingPoints = 70.0
InpNodeChevronWingBars = 0.28
InpNodeChevronWidth = 2
```

The exact chevron vertex is the Python node price.

## Performance

The bridge previously rewrote the runtime config on every timer cycle. That can
cause Python to recompute the same candle stream repeatedly.

Now the timer does not rewrite config unless explicitly requested:

```text
InpBridgeTimerConfigPulse = false
```

Normal flow:

```text
OnInit / input change -> write config
OnTick new bar        -> export candles + write config
Python watcher        -> recompute only when inputs/candles change
```
