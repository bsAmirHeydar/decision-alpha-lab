# Phase 28 — Lifecycle Cleanup and Clustered Hook/Branch Label IDs

## Goal

Fix two operational issues in the minimal Hook semantic view:

1. stale Hook objects must be removed when the timeframe changes, the chart identity changes, or the expert is reattached;
2. branch-number labels must be readable, stacked deterministically below valleys and above peaks, and carry minimal Hook/branch identity.

## Cleanup behavior

The expert already had cleanup toggles, but Phase 28 hardens lifecycle cleanup by deleting the generic `DAL_HOOK_` namespace in addition to all configured Hook phase prefixes.

This handles stale objects from:

- timeframe changes;
- expert remove / reattach;
- recompilation;
- parameter changes;
- older Hook profile prefixes;
- changed input prefixes.

A runtime chart-identity guard was added:

```text
g_fp_runtime_chart_symbol
g_fp_runtime_chart_period
```

If the runtime symbol/period identity changes, the expert cleans all known Hook objects, resets the last-bar cache, redraws the chart, and runs the engine again.

## Label identity

Branch-number labels now optionally include compact identifiers:

```text
H<origin_node_id>B<branch_ordinal>:<node_number>
```

Example:

```text
H128B3:2
```

Meaning:

- `H128` = Hook context identified by origin boundary node id 128;
- `B3` = third visible branch/sequence inside that Hook context;
- `2` = node number inside that branch.

This keeps the labels minimal but makes it clear which Hook and branch each number belongs to.

## Label clustering

The previous label stacker keyed labels too narrowly by exact time/price, so nearby labels could still overlap.

Phase 28 replaces it with proximity clustering:

```text
InpHookPhase02LabelTimeClusterSeconds
InpHookPhase02LabelPriceClusterPoints
```

Defaults:

```text
InpHookPhase02LabelTimeClusterSeconds = 0
InpHookPhase02LabelPriceClusterPoints = 28
```

A zero time cluster means: use the current chart period seconds.

## Vertical placement

- low-side / positive Hook labels are placed below valleys;
- high-side / negative Hook labels are placed above peaks;
- labels in the same cluster are stacked farther away from price using `InpHookPhase02NodeLabelStackStepPoints`.

Minimal profile defaults were widened:

```text
InpHookPhase02NodeNumberOffsetPoints = 32
InpHookPhase02NodeLabelStackStepPoints = 20
```

## Rendering order

Hook envelope curves are drawn first, then branch-number labels are drawn afterward so labels stay readable above the gray curve layer.
