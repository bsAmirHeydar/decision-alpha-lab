# ND / Hook Branching Explained

## Why Hook Counting Is Branchable

Post-flag correction is not always a simple sequence:

```text
1 -> 2
```

There can be multiple possible `1` nodes, and one later `2` can validate more than one earlier `1`.

This is why hook logic cannot be a single linear counter.

## Bullish Example

In a bullish post-flag correction, numbered nodes are lows.

Imagine these lows appear:

```text
L1 at 100
L2 at 103
L3 at 99
L4 at 104
```

L1 can be a `1`.

L2, being higher, can also be a new `1` in another branch.

L3 passes below both L1 and L2. Therefore L3 can serve as `2` for both branches.

L4 is higher again and can become a new `1` branch.

The structure is not one counter. It is multiple hook branches.

## End-Backward Counting

A practical way to count is from the latest adverse node backward.

For bullish lows:

1. Start from a current low.
2. Move backward through previous lows.
3. A prior higher low belongs to the same descending branch.
4. If ordering breaks, create or switch branch.
5. After branch construction, label from old to new.

For bearish highs:

1. Start from current high.
2. Move backward through previous highs.
3. A prior lower high belongs to the same ascending branch.
4. If ordering breaks, create or switch branch.
5. Label from old to new.

## Why L Must Increase

If any branch contains more than four numbered adverse nodes, the view is too fine.

The engine must increase L and rebuild the hook branches until the maximum branch length is four or fewer.

This is not random simplification. It is structural rescaling.

## ND Qualification

Two nodes are only internal numbering.

Three or four nodes are ND/Hook if the retracement condition passes.

The retracement condition uses the cycle:

```text
start -> extreme -> final
```

ND passes if:

```text
abs(extreme - final) > 0.5 * abs(extreme - start)
```

This is based on high/low nodes only.

## Why ND Can Overlap F

ND is not a replacement for F. It is a phase description.

If a post-flag correction creates a valid F confirmation path and also has a 3/4-node hook, both can exist.

The chart should show both, but the engine must keep separate identities.

## Why We Do Not Draw the 50% Line

The 50% level is an acceptance condition, not a visual object.

Drawing the level adds clutter and can imply that the line is a trading level. The intended display is a gray arc/semicircle from hook start to ND formation point.
