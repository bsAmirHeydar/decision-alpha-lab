# Node Engine Algorithm

## Source

Use existing project node logic.

Flag Counting should call it as a dependency.

## Required Interface

Recommended adapter:

```text
GetNodes(symbol, timeframe, L, start_time, end_time) -> Node[]
```

Node fields:

```text
id
side
L
time
price
bar_index
plateau_start_time
plateau_end_time
```

## Extraction Semantics

For candidate high plateau at price P:

1. Merge equal highs into one candidate.
2. Do not count equal adjacent highs as clearance.
3. Require at least L candles left with high < P.
4. Require at least L candles right with high < P.
5. Emit high node.

For candidate low plateau at price P:

1. Merge equal lows into one candidate.
2. Do not count equal adjacent lows as clearance.
3. Require at least L candles left with low > P.
4. Require at least L candles right with low > P.
5. Emit low node.

## Ordering

Nodes should be sorted by:

```text
time ascending
if same time, deterministic side/order rule from project module
```

## Multi-L Views

The engine may request several L values.

Example:

```text
L = 2, 3, 5, 8, 13, ...
```

Hook readability may increase L dynamically.

## No Expiration

Do not delete old nodes because later price passed them.

Historical nodes remain part of identity and audit.

## Break Function

Use helper functions:

```text
PassAbove(price, boundary) = price > boundary + epsilon
PassBelow(price, boundary) = price < boundary - epsilon
```

Default:

```text
epsilon = 0
```

Equality returns false.

## Adapter Tests

Minimum tests:

1. Equal high plateau becomes one node.
2. Equal low plateau becomes one node.
3. Equal neighboring bar does not count as clearance.
4. Node remains after later pass.
5. Equality does not trigger pass.
6. High/low nodes match legacy project outputs.
