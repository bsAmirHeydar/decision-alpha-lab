# H0001 — Structural Node Territory Volatility

## Abstract

H0001 tests whether completed structural-node territory events generate materially higher relative volatility than length-matched random windows. The production MQL-native definition is intentionally event-based and avoids directional assumptions: a node event begins when price first touches a frozen node territory and completes only after the configured `exit_gap` number of fully-outside candles. The exit can occur on either side of the frozen territory.

## Algorithm

1. Detect confirmed structural highs and lows using the L-rule. A node becomes active only after the right-side confirmation window has closed.
2. Build a node territory from the node price and the current structural extreme. The territory is frozen at first touch.
3. Start the event when a candle intersects the frozen territory.
4. Continue the event while candles keep touching or intersecting the territory.
5. Complete the event after `exit_gap` consecutive candles are fully outside the frozen territory. A candle is fully outside if either its low is above the upper territory bound or its high is below the lower territory bound.
6. Exclude the final exit-gap candles from the RTV inside sample.
7. Compute event RTV as mean log-move inside the event divided by the equal-length baseline before entry.
8. Compare the event logRTV to deterministic, length-matched random windows with valid pre-entry baselines.

## Consumption lifecycle

The node consumption rule is input-driven. In `CONSUME_BY_TOUCH`, a completed touch event consumes the node. In `CONSUME_BY_HUNT`, a completed touch event only consumes the node if the node price was actually hunted/broken during the event; otherwise the node remains live and the next cycle can be recomputed. This is the same lifecycle used by H0002 and H0003.

## Validation stack

The official evidence stack includes random comparison, bootstrap confidence intervals, permutation checks, split stability, session/regime conditioning, hard matched nulls, placebo shifts, outlier stress, non-overlap filtering, cluster-robust day/week aggregation, block bootstrap, horizon decay, and random-vs-random negative control.

## Interpretation

H0001 is a market-structure volatility fact, not a trading strategy by itself. It says that completed node-territory events are volatility-producing regions relative to matched random windows. Strategy design must be a later layer built on top of this fact.
