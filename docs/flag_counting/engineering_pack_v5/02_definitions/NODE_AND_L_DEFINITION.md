# Node and L Definition

## Source of Truth

The Flag Counting engine must reuse the existing project node module.

Do not rewrite node logic locally inside Flag Counting unless the local implementation is a byte-for-byte or behavior-identical adapter of the project node logic.

## Raw Inputs

The structural inputs are:

```text
bar.time
bar.high
bar.low
```

The following are not structural inputs:

```text
bar.open
bar.close
bar body
bar color
bar direction
```

## L Definition

L is the minimum clearance count on both sides of a candidate high/low price.

```text
L = minimum candles left and right that must not reach candidate node price
```

For a High node candidate at price `P`:

```text
left side:  at least L candles before the candidate must have high < P
right side: at least L candles after the candidate must have high < P
```

For a Low node candidate at price `P`:

```text
left side:  at least L candles before the candidate must have low > P
right side: at least L candles after the candidate must have low > P
```

Equality is special and must follow existing project plateau handling.

## Equal Highs and Equal Lows

Equal highs/lows are treated as one plateau-style node.

High plateau:

```text
several adjacent or equivalent highs at the same price
=> one high node candidate
```

Low plateau:

```text
several adjacent or equivalent lows at the same price
=> one low node candidate
```

Important:

- equal-price bars inside or beside the plateau do not count as extra clearance;
- equality does not create multiple separate nodes;
- equality does not count as a break;
- the node must still receive at least L real non-reaching candles on each side.

## Node Stability

A confirmed node does not expire.

Later price can pass the node price, but the historical node remains valid. Passing a node may trigger a structural event, but it does not delete the node from history.

## Node Identity

Every node used by Flag Counting should expose or derive:

```text
node_id
symbol
timeframe
side: HIGH | LOW
L
price
primary time
plateau start time
plateau end time
source bar index / node index
```

If the project module already has an identity scheme, use it.

If it does not, construct deterministic identity from:

```text
symbol + timeframe + side + L + plateau_time_range + price
```

## Strict Pass Logic

A boundary is passed only with strict inequality.

Bullish upward pass:

```text
later high > boundary_price
```

Bullish downward pass:

```text
later low < boundary_price
```

Bearish downward pass:

```text
later low < boundary_price
```

Bearish upward pass:

```text
later high > boundary_price
```

Equality is not a pass.

## Tolerance

Default should be exact strict pass.

An optional input may exist:

```text
InpBoundaryEpsilonPoints = 0
```

But the default must preserve strict pass semantics.

## Node Views

The engine may request nodes at multiple L values.

Recommended abstraction:

```text
NodeProvider.get_nodes(symbol, timeframe, L)
```

The Flag Counting engine should not know how nodes are extracted internally. It only consumes nodes.

## Implementation Warning

Do not substitute generic zigzag pivots for project nodes unless they match the exact project L rule. A different pivot definition will change the entire model.
