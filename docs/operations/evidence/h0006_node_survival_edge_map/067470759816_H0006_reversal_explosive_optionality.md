# H0006 — Node Survival Edge Map

The current H0006 framing is not a win-rate hypothesis. It asks whether raw structural nodes that remain unbroken after a fixed number of candles become more edge-like decision levels.

The operational definition is:

- raw M0001 node is known at candle `k`
- from candle `k+1` forward, monitor whether price breaks the node price
- if it is not broken after 20 candles, mark it red
- if it is not broken after 50 candles, mark it green
- if it is not broken after 100 candles, mark it purple

This converts H6 from a generic optionality report into a chart-updating node survival map.

No M0002 samples are allowed. Nodes known on the same candle are simultaneous, not ordered.
