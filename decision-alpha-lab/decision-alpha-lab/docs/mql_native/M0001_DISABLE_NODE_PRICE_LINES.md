# M0001 Disable Node Price Lines

## Change

Full-chart horizontal node price lines are now hard-disabled.

Even if `InpShowNodePriceLines` is accidentally left `true` in an old MT5 input
set, the Expert forces:

```text
visual.show_node_price_lines = false
```

and the visual module no longer calls `DAL_DrawHLine()` for node prices.

## Correct way to show node prices

Use local text labels:

```text
InpShowNodePrices = true
```

This draws:

- HIGH node price above the high-node arrow
- LOW node price below the low-node arrow

## Reason

Full horizontal lines create heavy chart noise and make node inspection harder.
M0001 visual validation should show local node information, not permanent full-chart
levels for every node.
