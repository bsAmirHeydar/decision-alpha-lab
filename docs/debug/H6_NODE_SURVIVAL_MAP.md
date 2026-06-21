# H6 Node Survival Map

This release redefines H0006 as a chart-facing no-sample node survival map.

A raw M0001 node becomes an edge-candidate level if, after its known-time candle, the market does not break that node price within the configured survival horizons.

Default horizons:

- 20 candles: red
- 50 candles: green
- 100 candles: purple

Contract:

- raw M0001 nodes only
- no M0002 branch samples
- no branch sample ordering
- no internal ordering among nodes known on the same candle
- node survival is measured only after known-time
- chart objects are deleted and redrawn using the `DAL_H6_NODE_` prefix

Break definition:

- high node breaks when a later candle high reaches `node_price + break_buffer`
- low node breaks when a later candle low reaches `node_price - break_buffer`

Touch definition is reported separately:

- high node touched when high reaches `node_price - touch_buffer`
- low node touched when low reaches `node_price + touch_buffer`

The key report lines are:

- `DAL_H0006_NODE_SURVIVAL_AUDIT`
- `DAL_H0006_NODE_SURVIVAL_H20`
- `DAL_H0006_NODE_SURVIVAL_H50`
- `DAL_H0006_NODE_SURVIVAL_H100`
- `DAL_H0006_NODE_CHART_UPDATE`

Interpretation:

- high survival percentage means many nodes are not broken after that horizon
- high detached percentage means the market did not even return close enough to touch the node
- purple nodes are the strongest survival stage because they remained unbroken for 100 candles
