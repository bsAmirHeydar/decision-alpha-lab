# Phase 06 Visual Language Specification

## Objective

Phase 06 defines how EXP0017 displays its confirmed and invalidated divergence states on the chart.

The visual layer exists for audit, debugging, and strategy-architect review. It is not a signal-quality model and not a trade recommendation layer.

## Visual objects

For each eligible Phase 05 final state, Phase 06 can draw:

- A horizontal trend line at the hunter reference price.
- A vertical reference-cycle anchor.
- A vertical confirmation marker at the closed-candle confirmation boundary.
- A text label containing CG name, status, direction, hunter symbol, clean symbol, and reference cycle number.

## Drawing anchor doctrine

The current Phase 06 implementation draws from the **reference-cycle anchor** to the confirmation candle.

This is deliberate. Earlier phases store the reference cycle and reference price, but they do not yet store the exact M1 timestamp of the high/low wick inside the reference cycle. The exact wick-time anchor can be promoted in a later refinement when the reference field stores extreme timestamps.

## Chart-symbol caveat

MT5 chart objects use the current chart price scale. When the chart symbol is not the hunter symbol, a hunter-symbol price may not line up visually with the chart scale.

For this reason Phase 06 includes:

- `InpDrawOnlyWhenChartIsHunterSymbol`

When enabled, the expert draws only signals whose hunter symbol equals the current chart symbol.

## Object prefix

All objects use the prefix:

```text
EXP0017_P06_
```

This lets the expert clear its own objects without deleting other drawings.
