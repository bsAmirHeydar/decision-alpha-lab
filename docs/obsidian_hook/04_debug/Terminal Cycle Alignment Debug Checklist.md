# Terminal Cycle Alignment Debug Checklist

Use this when a Hook cycle arc ends too early or too late.

## Check 1 — direction

Positive Hook should end at the lowest raw low after crown while still above origin.

Negative Hook should end at the highest raw high after crown while still below origin.

## Check 2 — boundary

If price touches/crosses origin, the cycle must not extend beyond that bar.

## Check 3 — structural continuity

Hook-after-Hook should still use structural node ids:

```text
Hook2.origin_node_id == Hook1.resolve_node_id
```

Do not use raw terminal time/price for chain ownership.

## Check 4 — valid-only view

If valid-only is enabled, only visible valid Hook origin groups and their required parent companions should draw arcs and labels.
