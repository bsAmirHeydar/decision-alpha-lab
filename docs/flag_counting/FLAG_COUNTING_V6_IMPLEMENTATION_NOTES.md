# Flag Counting V6 Implementation Notes

This patch adds a new implementation namespace: `FlagCountingV6`.

V6 is not a patch over the old scanner. It is a modular implementation intended to follow the engineering documentation pack:

1. L-rule node extraction from candle highs/lows.
2. Equal high/low plateau merge.
3. Alternating node view per L.
4. Two-leg flag body construction.
5. F1/F2/F3 post-flag state evaluation.
6. Backfilled F2/F3 child origins from the parent post-flag correction context.
7. Branch-based ND/Hook extraction.
8. Diagnostic renderer that only draws emitted logical objects.

## Compile target

```text
mql5/Experts/FlagCounting/FlagCountingV6Experiment.mq5
```

## Important implementation choices

### Node definition

The node engine follows the project L-rule:

- High/low only.
- Equal price is not a break.
- A node becomes confirmed when at least `L` candles on the right side do not reach beyond that price.
- Equal highs/lows are merged into a plateau node.
- The plateau stores a time interval and uses the latest equal touch as the drawing anchor.

### Flag body

A flag body is always:

```text
Origin -> Leg1 -> Waist -> Leg2
```

The body is the same for F1/F2/F3. The difference is only post-body behavior.

### F1

F1 is drawn after a two-leg body is complete.

F1 confirmation requires:

1. A post-flag internal `1/2` or more.
2. For the minimum `1/2`, the middle node between `1` and `2` must not break the F1 flag endpoint.
3. Then the F1 Leg2 endpoint must be strictly broken.

F1 invalidation before confirmation is the F1 waist.

### F2

F2 is authorized only after F1 confirmation, but its origin is backfilled from the deepest adverse correction after the F1 flag.

F2 must satisfy size relative to F1:

```text
F2.flag_size >= F1.flag_size * InpF2MinParentSizeRatio
```

F2 is not rejected while waiting for size. It can continue via Leg2 extension.

F2 invalidation is its own origin. If it dies, the parent F1 context remains alive.

### F3

F3 is authorized only after F2 confirmation, but its origin is backfilled from the deepest adverse correction after the F2 flag.

F3 completion uses an OR rule:

```text
F3.leg1_L >= ceil(0.80 * F2.leg1_L)
OR
F3.flag_size > 0.70 * F2.flag_size
```

F3 is not rejected while waiting for the OR rule. It can continue via Leg2 extension.

F3 locks when the first confirmed opposite F1 appears after F3 completion.

### ND / Hook

The ND/Hook engine is branch-based. It does not blindly label every sliding window.

ND is emitted when a hook branch has 3 or 4 adverse-side readable nodes. Two nodes are not ND.

The 50% rule is implemented as retracement from branch extreme toward branch start.

### Renderer

Renderer rules:

- Thin fixed line width by default.
- F body: straight line for `Origin -> Leg1`, smooth segmented curve for `Leg1 -> Waist -> Leg2`.
- ND/Hook: gray arc.
- Detailed labels by default: `F1 L8 Q23 status`.
- Origin label `O` shown by default.
- Internal numbers shown by default.
- Renderer does not create logical structures.

## Compile caveat

This patch was generated outside MetaEditor. The zip was built and tested, but a real MetaEditor compile must still be run locally. If MetaEditor reports a compile error, fix only the specific file and line; do not rewrite the logic again.
