<!-- CURRENT CANON NOTICE
This file remains the active semantic sequence contract for Phoenix, but it is subordinate to:

docs/contexts/legacy/flag_counting/FLAG_COUNTING_CURRENT_CANON.md

If this file conflicts with the current canon, the current canon wins.
-->

# Flag Counting Sequence Contract V4

This document is the canonical English contract for the Flag Counting experiment.
It replaces the earlier loose/sliding-window interpretation with a sequence-based, high/low-node-only state machine.

The goal of this contract is not to make the chart visually pleasing by approximation. The goal is to define the exact logical object that the code must detect, persist, invalidate, confirm, render, and audit.

---

## 1. Core Principle

The entire system is based on **high/low nodes only**.

The algorithm does not use candle open, candle close, candle body, candle color, or candle direction as structural inputs.

Close is not forbidden. It is simply irrelevant. If a candle happens to close beyond a level, that fact has no independent meaning for this model unless the high/low node geometry also satisfies the rule.

The structural universe is:

```text
High node
Low node
Node time
Node price
Node L
Node identity
```

A flag is not a candle pattern. A flag is a two-leg high/low-node structure.

---

## 2. Node Definition

Node definition must be copied from the existing project node module, not reinvented inside the Flag Counting detector.

The project-level definition is:

```text
L = the minimum number of candles on the left and on the right
    that must not reach the candidate node price
    for that high/low to qualify as a node.
```

For a High node:

```text
A candidate high price is a valid node if at least L candles to the left
and at least L candles to the right do not reach that high price.
```

For a Low node:

```text
A candidate low price is a valid node if at least L candles to the left
and at least L candles to the right do not reach that low price.
```

Nodes are extracted from candle highs and candle lows.

Equal highs and equal lows are treated as one plateau-style node according to the existing node module rules:

- equal highs are merged as one high node candidate;
- equal lows are merged as one low node candidate;
- equal-price bars immediately beside the plateau are not counted as extra left/right clearance;
- equality does not count as a break;
- the left/right clearance must be satisfied by bars that do not reach the node price.

A node does not expire. Once the required left/right clearance exists, the node remains a node. Later price action may break the node level, but that does not delete the historical node identity.

---

## 3. Equality, Hit, Break, and Pass

The model uses strict price pass logic.

Equality alone is ignored for structural hit/break decisions.

For a bullish boundary below price:

```text
hit/break = later low < boundary_price
not hit   = later low >= boundary_price
```

For a bearish boundary above price:

```text
hit/break = later high > boundary_price
not hit   = later high <= boundary_price
```

This is intentionally strict. A level must be passed, not merely touched at the same price.

An implementation may expose a tolerance input, but the default behavior must be strict pass logic:

```text
InpBoundaryEpsilonPoints = 0
```

---

## 4. Flag Body Definition

A flag is a two-leg object:

```text
Origin -> Leg1 -> Waist -> Leg2
```

For a bullish flag:

```text
Origin = Low node
Leg1   = highest High before correction
Waist  = lowest Low correction after Leg1 and before Leg2
Leg2   = High node that breaks/passes Leg1
```

For a bearish flag:

```text
Origin = High node
Leg1   = lowest Low before correction
Waist  = highest High correction after Leg1 and before Leg2
Leg2   = Low node that breaks/passes Leg1
```

The correction after Leg1 must not break the flag origin.

Bullish body validity:

```text
Waist must remain above Origin.
If Waist low < Origin low, the body is not a valid flag body.
```

Bearish body validity:

```text
Waist must remain below Origin.
If Waist high > Origin high, the body is not a valid flag body.
```

The flag body is not confirmed by itself. It only creates the post-flag context for F1/F2/F3-specific logic.

---

## 5. Leg1 and Waist Updating

Leg1 is not the first small high/low after the origin. Leg1 is the extreme before the correction.

Bullish:

```text
Origin low -> multiple highs may appear -> correction begins.
Leg1 = highest high before the correction.
```

Bearish:

```text
Origin high -> multiple lows may appear -> correction begins.
Leg1 = lowest low before the correction.
```

Waist must update continuously while correction is unfolding.

Bullish:

```text
After Leg1, every deeper correction low before Leg2 updates Waist.
Waist = deepest correction low before Leg2.
```

Bearish:

```text
After Leg1, every higher correction high before Leg2 updates Waist.
Waist = highest correction high before Leg2.
```

The renderer must use the true Waist as the curve control point. It must not use the first correction point if a deeper/higher correction appears later.

---

## 6. The Three F Levels

F1, F2, and F3 are all flags at the body level.

They are different because of what must happen **after** the two-leg flag body.

```text
Flag body = Origin -> Leg1 -> Waist -> Leg2
F-level   = post-flag behavior and sequence role
```

The canonical sequence in one structural chain is:

```text
F1 -> F2 -> F3
```

After F1, the next valid flag in that chain is F2, not another F1.

After F2, the next valid flag in that chain is F3, not another F1.

F3 is terminal for that chain.

---

## 7. Sequence Ownership

Flag Counting is sequence-based, not sliding-window-based.

The detector must not treat every alternating 4-node window as a standalone F1.

A chain owns its phase context.

Within one active chain:

```text
F1 is searched first.
After F1 confirms, F2 is searched from the post-F1 correction context.
After F2 confirms, F3 is searched from the post-F2 correction context.
After F3 completes/locks, the chain ends.
```

If a direction already has an active F1 or F2 chain, the engine must not start arbitrary new F1 chains in the middle of the same directional move. The active larger chain is still doing work.

A new same-direction chain may begin only after a genuine phase boundary, such as:

- an ND/Hook boundary;
- the end/lock of an opposite sequence;
- a confirmed opposite F1 that terminates a previous F3 extension;
- another explicitly owned phase boundary.

This prevents the old error where lines started from the middle of an ongoing move without a meaningful origin.

---

## 8. F1 Start

F1 must not begin from the middle of an already active move.

F1 may start from:

1. the terminal extreme of a valid ND/Hook phase;
2. the end of an opposite sequence phase;
3. the first confirmed opposite F1 that locks a prior F3 extension and starts a new opposite chain.

Bullish F1 origin should be the lowest relevant low at the phase boundary.

Bearish F1 origin should be the highest relevant high at the phase boundary.

The concern is simple:

```text
No movement should be structurally idle.
No F1 should be invented in the middle of a move only because a local 4-node window exists.
```

---

## 9. F1 Body and Display Maturity

For F1, the main chart should show it only after the probable flag body has been hit/completed:

```text
Origin -> Leg1 -> Waist -> Leg2
```

Before Leg2 exists, it is only an impulse/correction seed and should not be drawn as a flag on the main chart.

Candidate F1 bodies may be shown after Leg2 exists, with a candidate/live color distinct from confirmed F1.

Rejected F1 bodies must not remain on the main chart.

---

## 10. F1 Post-Flag Logic

After an F1 body exists, F1 is not confirmed immediately.

F1 must produce internal correction numbering after Leg2.

For bullish F1:

```text
After F1 Leg2, the correction-side numbered nodes are lows.
1 = first adverse low
2 = later adverse low that passes below 1
Between 1 and 2 there must be an opposite high.
That opposite high must not pass above the F1 Leg2 high before the minimum 1/2 structure exists.
```

For bearish F1:

```text
After F1 Leg2, the correction-side numbered nodes are highs.
1 = first adverse high
2 = later adverse high that passes above 1
Between 1 and 2 there must be an opposite low.
That opposite low must not pass below the F1 Leg2 low before the minimum 1/2 structure exists.
```

F1 confirmation:

```text
F1 confirms when:
  the F1 flag body exists,
  internal 1/2 or more exists after Leg2,
  F1 Waist has not been passed before confirmation,
  and price later passes F1 Leg2 again.
```

Bullish:

```text
F1 confirms when a later high > F1 Leg2 high.
```

Bearish:

```text
F1 confirms when a later low < F1 Leg2 low.
```

F1 invalidation before confirmation:

```text
F1 invalidates if price passes F1 Waist before confirmation.
```

Bullish:

```text
later low < F1 Waist low => F1 invalid
```

Bearish:

```text
later high > F1 Waist high => F1 invalid
```

---

## 11. F1 Leg2 Extension Rule

If F1 has formed its two-leg flag body but has not yet produced the minimum internal 1/2 structure, then a new break beyond Leg2 is not a new flag.

It is still part of F1 Leg2 extension.

Bullish:

```text
If price exceeds the current F1 Leg2 before valid post-flag 1/2 exists,
then the new high becomes the extended F1 Leg2.
The earlier Leg2 high is ignored as final Leg2.
```

Bearish:

```text
If price falls below the current F1 Leg2 before valid post-flag 1/2 exists,
then the new low becomes the extended F1 Leg2.
The earlier Leg2 low is ignored as final Leg2.
```

This extension continues until the minimum internal 1/2 structure appears or the F1 invalidation boundary is passed.

---

## 12. Internal Numbering and Hook Branching

Internal numbering is based on adverse-side nodes after a flag body.

For bullish post-flag correction:

```text
Numbered nodes are lows.
2 must pass below 1.
3 and 4 may also appear as additional hook/ND sequence nodes.
Opposite highs must exist between consecutive numbered lows.
```

For bearish post-flag correction:

```text
Numbered nodes are highs.
2 must pass above 1.
3 and 4 may also appear as additional hook/ND sequence nodes.
Opposite lows must exist between consecutive numbered highs.
```

Numbering is multi-dimensional and branchable.

There may be multiple `1` nodes that later share one `2`.

Example, bullish lows:

```text
A low appears: candidate 1.
A higher low appears: it can also be candidate 1 in another branch.
A later lower low passes both: it can become 2 for both branches.
If a later higher low appears again, it may become a new 1 branch.
```

A robust way to count hooks is from the end backward:

1. Start from the latest adverse-side node.
2. Walk backward through prior adverse-side nodes.
3. In a bullish correction, prior lows above the current lower low belong to the same descending hook branch.
4. In a bearish correction, prior highs below the current higher high belong to the same ascending hook branch.
5. If the required ordering is not satisfied, start a new hook branch.
6. After building branches backward, number each branch chronologically from old to new.

If any hook branch has more than four numbered adverse nodes, increase L until the maximum node count in every hook branch is four or fewer.

No hook/ND sequence should have more than four numbered adverse nodes in the final readable view.

---

## 13. Internal 3/4 and ND Label

If post-flag correction has exactly two numbered adverse-side nodes, it is internal 1/2 only. It is not ND.

If the correction has exactly three or four numbered adverse-side nodes after valid compression/scaling, it is also an ND/Hook.

Therefore:

```text
2 nodes => internal numbering only, no ND label
3 nodes => internal 1/2/3 plus ND label
4 nodes => internal 1/2/3/4 plus ND label
>4 nodes => raise L until <=4
```

If F1 already has valid 1/2 and later creates 3/4 instead of immediately confirming, the additional nodes must be counted.

For F1, the special middle-node restriction applies only to forming the minimum 1/2 without prematurely passing the flag end. After valid 1/2 exists, if price passes Leg2, F1 confirms; if price instead continues into 3/4, those nodes are counted as hook/ND continuation.

---

## 14. F2 Authorization and Backfill

F2 is not allowed before F1 confirms.

However, F2 origin is backfilled from the correction context that existed after the F1 flag body.

This means:

```text
F1 confirms in the present,
but F2 origin may be in the past,
inside the post-F1 correction region.
```

The same break that confirms F1 may also serve as part of the initial F2 development, depending on node structure.

The engine should store post-flag correction metadata for each F-level so the next F can be built deterministically.

For a bullish F1:

```text
F2 Origin = lowest low after F1 Leg2 and before/around F1 confirmation context.
```

For a bearish F1:

```text
F2 Origin = highest high after F1 Leg2 and before/around F1 confirmation context.
```

This is the deepest/farthest adverse correction after the F1 flag.

It is not arbitrary. It is not necessarily the last correction node. It is the deepest adverse correction node in the owned post-F1 correction context.

---

## 15. F2 Size Requirement

F2 is compared to F1 by flag size only.

No same-scale L compatibility is required for F2 by default.

Flag size:

```text
flag_size = abs(Leg2.price - Origin.price)
```

F2 qualification:

```text
F2 flag_size >= F1 flag_size
```

If a candidate F2 has not yet reached that size, it is not rejected. It remains a candidate and may extend Leg2 until the size requirement is satisfied.

A candidate is rejected only if its own invalidation rule is triggered.

---

## 16. F2 Invalidation and Continuity

F2 invalidation is different from F1 invalidation.

F2 invalidates only if the origin/start of its first leg is passed.

Bullish F2:

```text
later low < F2 Origin low => candidate F2 dies
```

Bearish F2:

```text
later high > F2 Origin high => candidate F2 dies
```

If F2 dies, it means that body was not actually F2.

The parent F1 remains alive if F1 itself is still valid/owned.

The engine must continue searching for F2 from the same post-F1 correction context:

```text
keep F1 context alive
keep post-F1 correction region alive
recompute/deepen the adverse correction extreme as needed
do not reuse the dead F2 body identity
build a new candidate F2 from the owned context
```

The search for F2 is not abandoned while F1 remains the active parent context.

---

## 17. F2 Post-Flag Logic and Waist-Break Branch

F2 confirms when it produces internal 1/2 or more after its flag body and then passes its Leg2 again.

Unlike F1, F2 may break its own Waist after the body without invalidating, as long as the F2 Origin is not passed.

In an F2 waist-break branch:

```text
1 = F2 Waist
2 = node that passes F2 Waist
```

The same hook/ND branch rules may continue into 3/4 if additional valid nodes appear.

F2 confirmation:

```text
F2 confirms when:
  F2 body exists,
  F2 size requirement is satisfied,
  internal 1/2 or waist-break branch exists,
  F2 Origin has not been passed,
  and price later passes F2 Leg2 again.
```

---

## 18. F3 Authorization and Backfill

F3 is not allowed before F2 confirms.

Like F2, F3 origin is backfilled from the correction context after the F2 flag body.

For bullish F2:

```text
F3 Origin = lowest low after F2 Leg2 in the owned post-F2 correction context.
```

For bearish F2:

```text
F3 Origin = highest high after F2 Leg2 in the owned post-F2 correction context.
```

F3 starts from the deepest/farthest adverse correction after the F2 flag.

---

## 19. F3 Completion and Same-Scale Qualification

F3 is terminal. It does not need post-flag internal 1/2 to become F3.

F3 requires a two-leg flag body:

```text
Origin -> Leg1 -> Waist -> Leg2
```

But F3 must be compatible with the F2 scale/size by an OR condition.

F3 same-scale qualification passes if either condition is true:

```text
Condition A:
  F3 Leg1 endpoint node L >= 0.80 * F2 Leg1 endpoint node L

OR

Condition B:
  F3 flag_size >= 0.70 * F2 flag_size
```

This is an OR, not an AND.

If F3 initially forms but does not yet satisfy either condition, it is not rejected. It remains a candidate and may continue extending until one condition is satisfied, unless its origin invalidation logic makes it impossible.

When the F3 body exists and at least one same-scale qualification condition passes, F3 is completed.

---

## 20. F3 Extension and Lock

After F3 is completed, the rest of the movement in the same direction is considered F3 extension.

The sequence is not immediately closed by a simple pullback.

F3 extension continues until the first confirmed F1 in the opposite direction is detected.

Important:

```text
The first confirmed opposite F1 locks F3.
It is the first by detection/confirmation time, not necessarily the smallest body.
```

When F3 locks:

1. the old F1->F2->F3 sequence is closed;
2. the F3 geometry/extension remains on the chart unless hidden by input;
3. the confirmed opposite F1 becomes the start of its own independent opposite sequence.

A locked F3 must not be deleted even if the market later fully reverses through the old structure. F3 has already completed its job.

---

## 21. Persistence of Confirmed F1/F2

F3 locked structures are always persistent.

For confirmed F1 and F2, persistence after later boundary violation must be controlled by input.

Default behavior:

```text
InpKeepConfirmedF1F2AfterBoundaryBreak = false
```

With the default behavior, confirmed F1/F2 may be removed from the main chart if their later relevant boundary is passed, while their audit record may remain.

Optional behavior:

```text
InpKeepConfirmedF1F2AfterBoundaryBreak = true
```

With this option, confirmed F1/F2 remain historically visible even after later boundary violations.

This input exists because the research workflow may require both views:

- clean current-state view;
- full historical audit view.

---

## 22. ND / Hook Definition

ND and Hook are the same phase family in this contract.

ND/Hook is defined by numbered hook sequences, not by candle close.

A valid ND/Hook sequence must have:

```text
3 or 4 numbered adverse-side nodes
```

Two nodes are not ND.

More than four nodes are not allowed in the final readable view. If any hook branch has more than four nodes, L must be increased until all branches have four or fewer nodes.

The anchor/source node of the hook context begins at the base node view, normally L=2. The view may increase L for readability, but the context must preserve the original anchor identity.

---

## 23. ND 50% Cycle Rule

Default ND acceptance requires a retracement greater than 50% of the cycle.

No 50% line is drawn by default.

The cycle is defined from the start node to the extreme node of the ND/Hook move.

```text
cycle_size = abs(extreme_price - start_price)
retraced   = abs(extreme_price - final_node_price)
ND passes  = retraced > 0.50 * cycle_size
```

Equality is not enough. It must pass the 50% level.

A research input may allow below-50 ND detection:

```text
InpAllowBelowHalfCycleND = false
```

Default remains false.

---

## 24. ND Scope and Display

Default behavior:

```text
Show all ND/Hook structures.
```

ND/Hook structures may overlap with F structures. Both may be displayed if both are logically emitted by the engine.

However, an input should allow restricting ND display to active/open sequence contexts:

```text
InpShowOnlyOpenSequenceND = false
```

When false, all detected ND/Hook structures are drawn.

When true, ND/Hook display is limited to contexts where the owning sequence is still open and has not yet completed F3.

ND/Hook should be rendered as a gray semicircle/arc from the start node to the point where the ND formed. It should not use a 50% line.

---

## 25. Candidate, Confirmed, Invalidated, Locked

The engine must explicitly distinguish structure status.

Recommended statuses:

```text
SEED
CANDIDATE
LIVE_BODY
POST_FLAG_COUNTING
CONFIRMED
COMPLETED
LOCKED
INVALIDATED
REJECTED
```

Main chart rules:

```text
SEED:
  F1 seed hidden.
  F2/F3 seed may be shown to reveal stage.

CANDIDATE/LIVE:
  shown with candidate color/shade.

CONFIRMED:
  shown with confirmed color/shade.

COMPLETED F3:
  shown as terminal/extension-capable.

LOCKED F3:
  remains visible unless explicitly hidden by input.

INVALIDATED/REJECTED:
  hidden from main chart by default.
  may remain in logs/audit tables.
```

For F1, display starts after the probable flag body has been hit/completed.

For F2 and F3, display may begin earlier from the probable Leg1 seed so the research chart shows which stage the chain is in.

---

## 26. Duplicate and Multi-Sequence Identity

All genuinely different sequences must be visible.

Even a tiny difference in time, price, node identity, L, parent, or sequence context makes it a different structure.

A duplicate exists only if the complete identity is the same:

```text
same symbol
same timeframe
same direction
same F level
same scale/node L identity
same parent chain id
same origin time and price
same leg1 time and price
same waist time and price
same leg2 time and price
same post-flag context identity
```

If any of those differ, it is a distinct sequence.

The renderer must not merge distinct sequences merely because they look close.

---

## 27. Rendering Contract

The renderer must never invent structure.

It may only draw structures emitted by the sequence engine.

The renderer is a visualization of backend logic, not a replacement for logic.

Flag rendering:

```text
Origin -> Leg1: straight thin line
Leg1 -> Waist -> Leg2: smooth semicircle/arc through the true Waist
```

ND/Hook rendering:

```text
gray semicircle/arc from hook start node to the point where ND/Hook formed
no 50% line by default
```

All lines should be thin and same width by default.

Sequence differentiation should come from shades within the same direction/status color family, not from large line-width changes.

Labels should use detailed option C by default during research:

```text
F1 L8 Q23
F2 L8 Q23
F3 L8 Q23
ND L8 H17
O
1
2
3
4
```

`O` should be shown at origin by default during debugging, with an input to hide it later.

---

## 28. Open Implementation Inputs

Recommended inputs from this contract:

```text
InpBoundaryEpsilonPoints = 0
InpKeepConfirmedF1F2AfterBoundaryBreak = false
InpAllowBelowHalfCycleND = false
InpShowOnlyOpenSequenceND = false
InpShowOriginLabels = true
InpShowDetailedLevelLabels = true
InpDrawNDHooks = true
InpDrawAllSequences = true
InpDrawRejected = false
InpF3Leg1LRatio = 0.80
InpF3FlagSizeRatio = 0.70
```

---

## 29. Non-Negotiable Anti-Regression Rules

The following old errors must not return:

1. Do not create F1 from every alternating 4-node window.
2. Do not start a flag from the middle of a move without a phase boundary.
3. Do not draw orphan lines whose origin is not owned by a sequence.
4. Do not use open/close/body/color in F or ND logic.
5. Do not treat equality as a break.
6. Do not use first correction point as Waist if a deeper/higher correction appears later.
7. Do not kill the parent chain when a child candidate dies.
8. Do not abandon F2 search when a candidate F2 dies; continue from the F1 post-flag context.
9. Do not reject F2/F3 only because they have not yet reached size/scale qualification; allow extension.
10. Do not erase locked F3 structures.
11. Do not let renderer heuristics draw structures that the sequence engine did not emit.
