# Phase 46 — Canonical Hook Terminal and Cycle Alignment

## Status

Implementation step: **Step 4** of the canonical Hook doctrine.

## Problem

The Hook renderer needs two different terminal concepts:

1. A **structural terminal node** for Hook-after-Hook continuity.
2. A **visual terminal price/time** for the cycle arc endpoint.

Earlier iterations mixed these concepts or let the visual terminal scan too far into raw candle data. This caused cycle arcs to extend beyond the living Hook boundary or to stop at a node that did not represent the deepest/highest price actually seen by the Hook.

## Canon

### Positive Hook

A positive Hook terminates visually at:

```text
the lowest raw low reached after the crown while still above origin
```

The terminal may be a raw candle low and does not need to be a confirmed Phase01 valley node.

However, it must remain above the Hook origin. If price touches/crosses the origin, the terminal scan stops because the Hook has reached its death boundary.

### Negative Hook

A negative Hook terminates visually at:

```text
the highest raw high reached after the crown while still below origin
```

The terminal may be a raw candle high and does not need to be a confirmed Phase01 peak node.

However, it must remain below the Hook origin. If price touches/crosses the origin, the terminal scan stops because the Hook has reached its death boundary.

## Structural terminal vs visual terminal

### Structural terminal

Used for:

```text
Hook2.origin_node_id == Hook1.resolve_node_id
```

This keeps Hook-after-Hook continuity node-based and stable.

### Visual terminal

Used for:

```text
cycle arc endpoint
retracement geometry
near-death geometry
```

This may use raw candle price/time because the visual cycle should reflect what price actually saw.

## Boundary rule

Terminal scanning must stop at the first origin-boundary touch/cross.

For positive Hook:

```text
candidate low must stay above origin
```

For negative Hook:

```text
candidate high must stay below origin
```

If `death_on_boundary_touch = true`, equality is treated as boundary death.

## Implementation

Added:

```text
FP_HookP02RawTerminalCandidateInsideOriginBoundary(...)
```

Changed:

```text
FP_HookP02FindRawTerminalPriceExtreme(...)
```

It now receives:

```text
origin_price
touch_kills
```

and stops scanning as soon as raw price touches/crosses the Hook origin boundary.

## Non-goals

This step does not change:

- sequence construction
- seed ownership
- Hook-after-F3 validity
- Hook-after-Hook validity
- visible-set selection
- family rendering labels
- Zone logic
- execution logic
