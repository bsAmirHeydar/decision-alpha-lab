# BASE-04 — Normalized Interpretation

## Core Claim

The system must be ontology-pure.

Only the project's own concepts are allowed.

The complete ontology package is named:

```text
NDS
```

Everything outside NDS is forbidden by default.

## Allowed Concept Space

The allowed concept space includes only anatomy-native concepts such as:

```text
Hook
Rally
F-counting
Node-counting
Nodes
X-axis structure
Y-axis state
selected extreme
invalidation
destination
fractal context
scenario state
execution geometry derived from NDS
```

The exact list can expand only if the new concept is created inside NDS or translated fully into NDS language.

## Forbidden Concept Space

The following concept families are forbidden:

```text
classical indicators
ICT concepts
generic technical analysis
external trading systems
candle-pattern trading
indicator-driven triggers
generic trend/momentum/breakout language
time-of-day edges
day-of-week edges
artificial time-horizon labels
```

The system must not import these concepts directly.

## No Indicator Layer

Indicators are not allowed as decision inputs.

Forbidden examples:

```text
RSI
MACD
Moving Average crossovers
Bollinger Bands
Stochastic
ATR as a signal source
oscillator overbought/oversold logic
```

If a volatility or cost metric is ever needed for engineering, it must be explicitly treated as an execution/risk measurement and not as a signal concept.

## No ICT Layer

ICT concepts are not allowed as native concepts.

Forbidden examples:

```text
order block
fair value gap
liquidity sweep
breaker block
market structure shift
displacement
premium/discount
killzone
```

If any external idea appears useful, it must first be translated into NDS-native language and then revalidated.

It cannot enter the system under its original ontology.

## No Generic Technical Analysis Layer

The system must not use generic technical-analysis labels as reasons.

Forbidden examples:

```text
support/resistance as generic labels
trendline break
chart patterns
head and shoulders
double top/bottom
flag/pennant in the generic TA sense
confirmation candle
breakout confirmation
weakness/strength language outside NDS
```

Any useful observation must be rewritten as an NDS statement:

```text
Hook state
Rally state
F-count
Node state
fractal relation
invalidation geometry
destination state
execution geometry
```

## No Artificial Time-Horizon Labels

The system should not use artificial labels such as:

```text
will go up in 5 bars
will go down in 10 candles
20-bar forward return
session hour edge
weekday edge
time-of-day signal
```

Time may still exist as an ordering mechanism for backtesting and leakage prevention, but it must not become a decision concept unless a future NDS-native structural definition requires it.

## NDS Boundary Rule

The NDS boundary rule:

```text
If a concept cannot be expressed in NDS language, it cannot be used by the decision system.
```

This rule protects the system from ontology contamination.

## AI Relevance

AI must not learn from external concept families.

AI inputs must come from NDS-only features.

Allowed AI input families:

```text
Hook features
Rally features
F-counting features
Node-counting features
X-axis fields
Y-axis fields
fractal context fields
scenario fields
execution geometry fields
NDS-derived reason vectors
```

Forbidden AI input families:

```text
indicator features
ICT labels
generic TA labels
raw candle-pattern labels
time-of-day features
day-of-week features
artificial horizon labels
```

## Noise Rejection Consequence

The system should include an ontology gate before dataset creation.

Any feature or label should be rejected if it is not NDS-native.

Suggested gate:

```text
NDS_ONTOLOGY_GATE
```

Possible gate states:

```text
NDS_ALLOWED
NDS_TRANSLATION_REQUIRED
NDS_REJECTED
```

## Short Formal Statement

The project must remain NDS-pure. Only Hook, Rally, F-counting, Node-counting, and other NDS-native concepts may enter the system. Indicators, ICT, generic technical analysis, artificial time-horizon labels, and external trading ontologies are forbidden unless fully translated into NDS language and revalidated inside the project.
