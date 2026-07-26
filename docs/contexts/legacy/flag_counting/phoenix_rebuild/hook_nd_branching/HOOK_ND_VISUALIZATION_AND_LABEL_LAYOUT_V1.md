# Hook / ND Visualization and Label Layout V1

## 1. Purpose

This document defines how Hook / ND structures and Flag Counting labels must be rendered on the chart.

The main visual failures observed so far were:

1. labels overlap and become unreadable;
2. ND labels are drawn for raw/developing structures that are not true ND;
3. multiple branch states are dumped directly on the main chart;
4. Hook arcs do not clearly show which branch or Hook context they belong to.

This contract separates semantic rendering from debug rendering.

## 2. Rendering principles

### 2.1 Renderer is not a detector

The renderer must not create Hook, ND, F1, F2, or F3 structures.

It only draws events emitted by the engine.

### 2.2 Semantic view versus audit view

Semantic view is the default chart view.

It should show:

- confirmed and active structures;
- meaningful developing structures;
- ND branches only when they satisfy the ND contract;
- clean labels.

Audit view can show:

- raw branches;
- developing 1-node and 2-node Hook branches;
- below-threshold Hooks;
- superseded states;
- detailed node ids.

Audit view must be explicitly enabled.

## 3. Hook / ND visual objects

### 3.1 Hook arc

A Hook / ND arc should be drawn as a gray semicircle-like curve.

For low-side Hook:

- arc start = Hook floor / origin boundary
- arc end = branch resolve node or active node
- arc belly/control = cycle extreme or a smooth midpoint derived from the cycle extreme

For high-side Hook:

- arc start = Hook ceiling / origin boundary
- arc end = branch resolve node or active node
- arc belly/control = cycle extreme or a smooth midpoint derived from the cycle extreme

### 3.2 ND label

The label `ND` is drawn only when a branch is ND-qualified.

ND-qualified means:

- branch count is exactly 3 or 4;
- no branch in the Hook context exceeds four nodes after adaptive L;
- branch passes the configured retracement rule, unless below-threshold display is explicitly enabled.

### 3.3 Branch number labels

When enabled, branch numbers are drawn on counted same-side nodes.

Labels are old-to-new inside the branch:

```text
1, 2, 3, 4
```

For low-side Hook, labels are attached to lows.

For high-side Hook, labels are attached to highs.

### 3.4 Developing branches

A 1-node or 2-node branch is not ND.

In semantic view, developing branches may be hidden or shown as small muted hook markers depending on input settings.

In audit view, developing branches can be shown with detailed status.

## 4. Label layout contract

### 4.1 Labels must be stacked

Labels must not be placed independently with random offsets.

The renderer must first collect label candidates into clusters, then assign deterministic lanes.

### 4.2 Label clusters

A label cluster is formed by proximity in time and price.

Inputs:

```text
InpLabelTimeClusterBars
InpLabelPriceClusterPoints
InpLabelLaneSpacingPoints
InpMaxLabelsPerCluster
```

Two labels belong to the same cluster when:

```text
abs(label.bar_index - cluster.anchor_bar_index) <= InpLabelTimeClusterBars
and
abs(label.price - cluster.anchor_price) <= InpLabelPriceClusterPoints * _Point
```

### 4.3 Peak labels

Labels attached to highs / peaks should stack above the peak.

Closest-to-price label should be assigned lane 0.

Lane price:

```text
price = anchor_price + lane_index * lane_spacing
```

### 4.4 Valley labels

Labels attached to lows / valleys should stack below the valley.

Closest-to-price label should be assigned lane 0.

Lane price:

```text
price = anchor_price - lane_index * lane_spacing
```

### 4.5 Deterministic lane priority

Within a cluster, label priority should be deterministic.

Default priority from closest to price outward:

1. older sequence first;
2. higher semantic importance;
3. locked / confirmed before live / candidate;
4. F3 before F2 before F1 before ND / Hook debug;
5. lower branch index before higher branch index;
6. lower node id as final tie-break.

This implements the requirement that older structures remain closer to price.

### 4.6 Avoiding text walls

If too many labels exist in one cluster, semantic view should collapse labels into a summary.

Example:

```text
F1 x4, F2 x2, ND x3
```

Full details remain available in audit logs.

Input:

```text
InpCollapseDenseLabelClusters = true
InpDenseClusterLabelLimit = 8
```

## 5. Detailed labels

Semantic label examples:

```text
F1 L8 Q120 confirmed
F2 L13 Q121 P120 live_body
F3 L21 Q122 P121 locked
ND L5 H44 B3
```

Debug label examples:

```text
F2 L13 Q121 P120 O=501 L1=509 W=514 L2=530 sz=1.23xF1
ND L5 H44 B3 nodes=[102,108,115] retrace=0.62 pending=false
```

## 6. Visual colors

The color family should still encode direction and status.

Hook / ND should use gray by default.

Branch numbers may use muted gray or branch-specific color shades in audit mode.

All body lines remain thin by default.

## 7. Duplicate visual geometry

If several structures share exactly the same visual geometry, semantic view should render one geometry and combine labels when possible.

Exact same geometry means same node identity for all defining points, not merely similar prices.

For Hooks:

```text
same boundary_node_id
same resolve_node_id
same counted_node_ids[]
same side
```

For Flags:

```text
same origin_node_id
same leg1_node_id
same waist_node_id
same leg2_node_id
same level
same direction
```

## 8. Required inputs

Recommended visualization inputs:

```text
InpDrawHooks = true
InpDrawNDOnly = false
InpDrawHookDevelopingBranches = false
InpDrawHookBranchNumbers = true
InpDrawHookDebugLabels = false
InpCollapseDenseLabelClusters = true
InpDenseClusterLabelLimit = 8
InpLabelTimeClusterBars = 4
InpLabelPriceClusterPoints = 160
InpLabelLaneSpacingPoints = 120
InpMaxLabelsPerCluster = 12
InpDetailedLabels = true
InpShowParentIds = true
```

## 9. Acceptance criteria

The rendering is acceptable only if:

1. labels in the same area are vertically stacked and readable;
2. ND is not shown for 1-node or 2-node developing branches;
3. Hook arcs have clear start and end points;
4. branch numbers are attached to the counted same-side nodes;
5. dense clusters can be collapsed without losing audit details;
6. renderer never draws structures not emitted by the logic engine.
