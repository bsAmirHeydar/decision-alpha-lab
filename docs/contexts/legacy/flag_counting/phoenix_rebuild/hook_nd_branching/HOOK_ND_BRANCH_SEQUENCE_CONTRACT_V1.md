# Hook / ND Branch-Sequence Contract V1

## 1. Purpose

This document defines the exact Hook / ND logic for the Flag Counting Phoenix engine.

The previous failure mode was that ND was treated as a raw marker produced from local 3-node or 4-node windows. That is incorrect. A valid Hook / ND is a structured phase container. It is built from same-side nodes, can contain multiple internal branch sequences, and must be normalized by the project `L` rule so that no internal branch sequence exceeds four counted nodes.

The Hook / ND engine is part of the phase-boundary layer. It helps decide where an F1 root can start and explains ranges where the market is not yet expressing a clean F1/F2/F3 chain. It is not merely a visual annotation.

## 2. Terminology

### 2.1 Node

A node is the project-defined high/low swing node.

`L` means the number of candles on the left and right side that must not reach the node price for that price to be accepted as a node.

Nodes are derived only from candle high and candle low.

The following are explicitly irrelevant for Hook / ND logic:

- candle open
- candle close
- candle body
- candle color
- candle direction

Equal high or equal low plateaus are treated as a single structural node according to the project node engine. Equality is not a break. A level must be strictly crossed to count as crossed.

### 2.2 Same-side nodes

Hook / ND branch sequences are built from same-side nodes.

For a low-side Hook, same-side nodes are low nodes.

For a high-side Hook, same-side nodes are high nodes.

Opposite-side nodes can be useful for visual context and cycle extremes, but the internal Hook branch count is based on same-side nodes.

### 2.3 Low-side Hook

A low-side Hook is built from low nodes.

In a low-side Hook, the current or rightmost low node is the active node under evaluation. It may be confirmed or still forming, depending on the configured mode. The engine walks backward through previous low nodes with the same current `L` until it reaches a lower low. That lower low is the Hook floor and the Hook origin boundary.

The low-side Hook region is the span from the Hook floor to the active low node.

### 2.4 High-side Hook

A high-side Hook is the exact mirror of a low-side Hook.

It is built from high nodes. The engine walks backward through previous high nodes until it reaches a higher high. That higher high is the Hook ceiling and the Hook origin boundary.

The high-side Hook region is the span from the Hook ceiling to the active high node.

### 2.5 Hook origin boundary

The Hook origin boundary is the first same-side node found by walking backward from the active node that breaks the current same-side local sequence.

For low-side Hook:

- active node = rightmost low under evaluation
- walk backward over previous lows
- stop at the first previous low whose price is strictly lower than the active low price
- that lower low is the Hook floor / origin boundary

For high-side Hook:

- active node = rightmost high under evaluation
- walk backward over previous highs
- stop at the first previous high whose price is strictly higher than the active high price
- that higher high is the Hook ceiling / origin boundary

The boundary node is not itself counted as internal node `1`, `2`, `3`, or `4`. It is the start boundary of the Hook context.

### 2.6 Internal branch sequence

An internal branch sequence is a same-side sequence inside a Hook region. A single Hook can have many internal branch sequences.

The number of branch sequences is unlimited.

The number of counted same-side nodes inside one branch sequence must be between one and four after adaptive L normalization.

Only branch sequences with exactly three or exactly four counted nodes can make the Hook qualify as ND.

A branch with one or two counted nodes can exist, can be rendered in debug mode, and can be used as a developing Hook state, but it is not ND by itself.

### 2.7 ND

ND is a Hook state, not a separate raw pattern.

A Hook becomes ND when, after adaptive L normalization:

1. the Hook contains at least one internal branch sequence with exactly three or exactly four counted same-side nodes;
2. no internal branch sequence has more than four counted same-side nodes;
3. the qualified branch satisfies the configured cycle retracement rule.

### 2.8 Cycle retracement rule

The default ND threshold is 50% cycle retracement.

The 50% line is not drawn by default.

For a low-side Hook:

- cycle start = Hook floor / branch start boundary
- cycle extreme = highest opposite-side excursion reached after the Hook floor and before or during the branch formation
- final branch node = latest counted low in the branch
- retracement is measured from the extreme back toward the Hook floor side
- if the final branch node has retraced more than 50% of the cycle range, the branch passes the default ND retracement condition

For a high-side Hook, the rule is mirrored.

The input layer may allow below-50% Hooks for research, but the default semantic ND definition uses above-50% retracement.

## 3. Core invariants

### 3.1 Hook is a container

A Hook is a container of branch sequences. It is not a single branch and not a single node label.

### 3.2 Branch count is not capped

The number of internal branch sequences can be any positive number.

### 3.3 Branch length is capped

The number of counted nodes inside each internal branch sequence is capped at four after adaptive L normalization.

### 3.4 Adaptive L is applied to the Hook context

If even one internal branch sequence contains more than four counted nodes, the engine must increase `L` and rebuild the entire Hook context. It must not merely delete the fifth node. It must not truncate the branch. It must not accept a five-node branch as ND.

### 3.5 Hook / ND uses same-side structure

For low-side Hook, internal branch counts are built from lows.

For high-side Hook, internal branch counts are built from highs.

Opposite nodes are not counted as internal branch numbers, but they can define cycle extremes and rendering curvature.

### 3.6 Rightmost node may be provisional

The active node under evaluation can be still forming when the engine is configured to include pending nodes. This is useful for live visualization. Semantic confirmed reports should distinguish pending-based Hooks from confirmed-node Hooks.

### 3.7 Strict crossing

Equality does not count as a break.

For low-side Hook, a lower low must be strictly lower.

For high-side Hook, a higher high must be strictly higher.

### 3.8 Renderer is non-authoritative

The renderer must never invent Hook branches. It may only draw Hook objects emitted by the Hook engine.

## 4. Low-side Hook branch logic

This section defines the low-side version. The high-side version is the exact mirror.

Let same-side lows be ordered from old to new:

```text
L0, L1, L2, ..., Ln
```

Let the active rightmost low be:

```text
Ln
```

Using Python-like reverse references:

```text
-1 = Ln
-2 = L(n-1)
-3 = L(n-2)
...
```

### 4.1 Find the Hook floor

Starting from `-1`, walk backward through low nodes of the same `L`.

Stop at the first low node whose price is strictly below the active low price.

That node is the Hook floor.

The Hook floor is the start boundary of the Hook.

The internal branch search happens between the Hook floor and the active low.

### 4.2 Build internal branches from the right side

Internal branches are discovered from the active side backward and then labeled old-to-new.

The engine starts with the active low `-1`. It examines older lows.

A previous low can join the current branch if it is above the current branch reference level according to the low-side Hook rule.

When a lower low is found, it splits or resolves the current branch context and becomes a boundary for the next branch construction pass.

This creates multiple branch sequences inside one Hook.

### 4.3 Numbering direction

Even though discovery starts from the right side, labels are assigned from old to new inside each branch.

For a branch with three counted lows:

```text
oldest counted low  -> 1
middle counted low  -> 2
newest counted low  -> 3
```

For a branch with four counted lows:

```text
oldest counted low  -> 1
next counted low    -> 2
next counted low    -> 3
newest counted low  -> 4
```

The Hook floor is not numbered as `1`; it is the origin boundary.

### 4.4 Multiple branch sequences

A single Hook may contain many branch sequences.

The branches are ordered from old to new by their first counted node time.

A node can participate in more than one branch if it naturally resolves or connects several branch paths. The implementation should preserve distinct branch identities when their node lists differ.

### 4.5 Valid ND branch

A branch is ND-qualified only if its counted length is 3 or 4 and it passes the cycle retracement threshold.

A branch of length 2 is not ND.

A branch of length 5 forces adaptive L escalation.

## 5. High-side Hook branch logic

High-side Hook is a mirror of low-side Hook.

Replace lows with highs.

Replace lower-low boundary with higher-high boundary.

Replace upward/downward comparisons accordingly.

For high-side Hook:

- active node = rightmost high
- Hook ceiling = first older high strictly above the active high
- branch internal counted nodes are high nodes inside the Hook region
- branch numbering is still old-to-new
- ND-qualified branch length is still exactly 3 or 4
- if any branch length exceeds 4, increase L and rebuild

## 6. Adaptive L normalization

Adaptive L normalization is mandatory.

The engine must not accept a Hook context where any branch contains more than four counted same-side nodes.

Algorithm:

1. Start with the requested base L, usually `L=2`.
2. Build same-side nodes for that L.
3. Build Hook context and all internal branches.
4. Compute maximum branch length.
5. If maximum branch length is greater than 4, increase L and rebuild from step 2.
6. Repeat until maximum branch length is less than or equal to 4 or until the configured maximum L is reached.

If maximum L is reached and a branch still has more than 4 counted nodes, the Hook is marked as unresolved for semantic ND and may be emitted only in audit mode.

## 7. Hook state classification

A Hook context can be classified as:

### 7.1 Developing Hook

At least one branch exists, but no branch has length 3 or 4.

Usually this means branch length is 1 or 2.

This is not ND.

### 7.2 ND Hook

At least one branch has length 3 or 4 and passes the cycle retracement threshold.

### 7.3 Overextended Hook

At least one branch exceeds four nodes before adaptive L normalization.

This is not accepted as final. The engine must increase L and rebuild.

### 7.4 Unresolved Hook

The engine cannot reduce all branches to four or fewer nodes within the configured L range.

This should be visible in audit, not as a clean ND marker.

## 8. Relationship to F1 roots

Hook / ND is one allowed source of F1 phase boundaries.

For a bullish F1 after a low-side Hook:

- F1 origin should come from the lowest low node inside the Hook context / Hook floor boundary, depending on the selected phase boundary mode.
- It must not start from an arbitrary mid-leg point.

For a bearish F1 after a high-side Hook:

- F1 origin should come from the highest high node inside the Hook context / Hook ceiling boundary.

Fail-open F1 root creation can be kept as a research fallback, but it must be clearly tagged as fallback and should not be confused with Hook-owned semantic F1 roots.

## 9. Rendering contract summary

A Hook / ND should be rendered as:

- gray arc / semicircle from Hook origin boundary to Hook resolution point;
- branch numbers `1/2/3/4` on counted same-side branch nodes when enabled;
- `ND` label only when a 3-node or 4-node branch is ND-qualified;
- optional debug label showing branch id, L, node count, retracement percentage, and pending/confirmed status.

Raw 1-node or 2-node developing Hooks must not be mislabeled as ND.

## 10. Implementation risks

The main risks are:

1. treating every 3-node or 4-node sliding window as ND;
2. ignoring multiple internal branch sequences inside one Hook;
3. accepting a 5-node branch instead of escalating L;
4. counting opposite-side nodes as Hook branch numbers;
5. drawing ND labels for developing 1-node or 2-node Hooks;
6. allowing the renderer to invent branch labels not emitted by the Hook engine;
7. failing to distinguish pending-node Hook from confirmed-node Hook.

The Phoenix implementation must explicitly guard against all of these.
