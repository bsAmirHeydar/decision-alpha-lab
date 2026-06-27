# Engineering Contract: Phoenix Flag Counting

## Node contract

A node is extracted from high/low data only. `L` is the number of candles on each side that must not reach the node price. Equal highs/lows are collapsed into one plateau node. The anchor time is the last equal touch of the plateau.

Equality is never a break. For a bullish boundary, price must move strictly below the boundary to break it. For a bearish boundary, price must move strictly above the boundary to break it.

## Flag body contract

A flag body is the invariant object:

```text
Origin -> Leg1 -> Waist -> Leg2
```

Bullish:

- Origin is a low node.
- Leg1 is the highest high before the correction.
- Waist is the deepest correction low after Leg1 that does not break Origin.
- Leg2 is the high that breaks Leg1.

Bearish is symmetric.

## F1 contract

F1 is displayed after the two-leg body exists. F1 confirms only after a valid internal 1/2 or more forms after Leg2 and price then breaks Leg2 again before F1 Waist is broken.

F1 invalidation before confirmation is the Waist.

## F2 contract

F2 is authorized only after F1 confirmation. Its origin is backfilled from the deepest adverse correction after F1 Leg2 and before F1 confirmation. F2 must compare by size to F1. If it has not reached the size condition, it is not rejected; it remains a candidate until extension or invalidation.

F2 invalidates at its own Origin, not at its Waist. Waist-break can be an internal branch.

## F3 contract

F3 is authorized only after F2 confirmation. Its origin is backfilled from the deepest adverse correction after F2 Leg2 and before F2 confirmation. F3 completes by its body when the documented OR condition is satisfied:

1. `F3.leg1_L >= ceil(0.80 * F2.leg1_L)`, or
2. `F3.flag_size > 0.70 * F2.flag_size`.

F3 is locked by the first opposite confirmed F1 after F3 completion.

## Hook/ND contract

ND/Hook is branch-based. It is not blind chart decoration. A branch must have 3 or 4 readable nodes. Two nodes are not ND. The branch is ND when its final node has returned more than the configured retracement threshold from the branch extreme toward the start.

Phoenix currently implements readable 3/4-node alternating branch detection at each L view. If strict semantic gating produces no roots, keep fail-open enabled until Hook/ND coverage is validated.

## Renderer contract

Renderer cannot invent structure. It only draws `FP_FlagEvent` and `FP_HookBranch` objects emitted by the engine.
