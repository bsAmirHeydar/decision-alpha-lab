# M0001 Consumed Extreme History

## Rule

When a node is consumed, its expansion extreme is no longer a live variable.
However, the final node-to-extreme link should remain visible as history.

## Behavior

Active node:

```text
extreme line = node -> current live expansion extreme
```

Consumed node:

```text
extreme line = node -> final expansion extreme at/ before consume
```

The line does not extend or update after the consume candle.

## Input

```text
InpShowConsumedExtremeHistory = true
```

Set to `false` to hide consumed-node extreme links entirely.

## Logic vs visual

This is not only a drawing rule. The audit-state engine already stops scanning
the node once it is consumed, so the stored `expansion_extreme` is frozen at the
final meaningful point. The visual layer now keeps that frozen final link on the
chart for audit.

Version: `1.24`.
