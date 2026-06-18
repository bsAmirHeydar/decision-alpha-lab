# M0001 Node Visibility Diagnostics

## Purpose

This adds an on-chart diagnostic summary to separate three different questions:

1. Is data limited?
2. Are structural nodes being computed?
3. Are visual caps hiding some computed nodes?

## New input

```text
InpShowNodeVisibilityDebug = true
```

## Summary fields

The summary now shows:

```text
bars=<data bars>
nodes=<computed structural nodes>
audit=<computed node audit states>
node_draw=all/N or latest K/N
audit_draw=all/N or latest K/N
last_node=HIGH/LOW id=<id> idx=<bar index> t=<node time> p=<node price> active=<active_from>
```

## Interpretation

If `nodes` is large and `last_node` is recent, the detector is not capped.

If `nodes` is large but `node_draw=latest 2/N`, the cap is visual only.

If `last_node` is far behind the current chart time, the L-rule detector has not
confirmed a newer structural node yet for the current `InpL`.

## Important

`InpBars` remains the data cap:

```text
InpBars = 0 -> all tester/history bars
InpBars = 2 -> only 2 data bars
```

Visual caps are separate:

```text
InpMaxNodesToDraw = 2 -> latest 2 visual nodes only
```

## Version

`M0001_LiveVisualLab.mq5` version: `1.27`.
