# ND / Hook Definition

## General Definition

ND and Hook are one phase family in this contract.

They describe multi-node correction/cycle behavior using high/low nodes only.

ND/Hook is not based on candle close.

## Scope

ND/Hook can appear:

- after a flag body as post-flag correction;
- inside a larger active sequence;
- as a phase before F1;
- in overlapping contexts if separate logical contexts emit them.

All ND/Hook structures are displayed by default.

An input may restrict display to open sequence contexts:

```text
InpShowOnlyOpenSequenceND = false
```

## Numbered Nodes

ND/Hook numbering uses adverse-side nodes.

Bullish context:

```text
numbered nodes are lows
opposite nodes between them are highs
```

Bearish context:

```text
numbered nodes are highs
opposite nodes between them are lows
```

## Two Nodes

Two numbered adverse-side nodes are internal 1/2 only.

They are not ND.

```text
1/2 => internal numbering, no ND label
```

## Three or Four Nodes

Three or four numbered adverse-side nodes form ND/Hook if other requirements pass.

```text
1/2/3 => ND/Hook candidate
1/2/3/4 => ND/Hook candidate
```

These should receive both number labels and ND/Hook label.

## More Than Four Nodes

More than four numbered nodes are not allowed in final readable view.

If any hook branch has more than four numbered nodes, increase L and rebuild the view until every branch has four or fewer nodes.

The base context starts with L=2 for the source/anchor view, but readable output may use higher L.

## Branching

Hook counting is branchable.

There may be multiple `1` nodes that later share one `2`.

Bullish low example:

```text
low A appears -> candidate 1 branch A
higher low B appears -> candidate 1 branch B
later lower low C passes A and B -> can become 2 for both branches
later higher low D appears -> new candidate 1 branch D
```

A robust counting method is end-backward:

1. Start at a latest adverse node.
2. Walk backward through earlier adverse nodes.
3. Include earlier nodes that satisfy branch ordering.
4. Start a new branch when ordering breaks.
5. Reverse branch nodes chronologically for labeling.

## ND 50% Cycle Rule

Default ND acceptance requires retracement greater than 50% of the cycle.

Cycle:

```text
start node -> extreme node
```

Retracement:

```text
extreme node -> final node
```

Formula:

```text
cycle_size = abs(extreme.price - start.price)
retraced = abs(extreme.price - final.price)
ND passes when retraced > 0.50 * cycle_size
```

Equality is not enough.

Below-half-cycle ND can be allowed by input:

```text
InpAllowBelowHalfCycleND = false
```

Default is false.

## ND Rendering

ND/Hook is rendered as a gray semicircle/arc from start node to the point where ND formed.

No 50% line is drawn by default.

## ND and F Overlap

ND may overlap with F if both are emitted.

Renderer should draw both in a readable way, but the engine must keep their identities separate.
