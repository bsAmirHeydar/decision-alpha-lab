# EXP_flag_counting

Unified experiment for fractal flag counting.

## Purpose

This experiment turns F-counting into a reusable market-structure grammar:

```text
ND / Hook -> F1 -> F2 -> F3 -> ...
```

The goal is not to draw every local candidate. The goal is to maintain parallel F-counting sequences across several swing scales and render only useful body geometry and tiny labels.

## Final working assumptions

- F-counting is fractal.
- Multiple sequences can run in parallel.
- Multiple swing scales can produce valid structures at the same time.
- F1 is the root level.
- F2 starts from the parent F1 internal `2`.
- F3 starts from the parent F2 internal `2`.
- After F1, the continuation of that sequence is F2.
- After F2, the continuation of that sequence is F3.
- The child may be delayed, extended, and live/pending for a long time.
- A sequence is not deleted just because the next child is not immediately complete.

## F-level rules

### F1

```text
origin -> leg1 -> waist -> leg2
confirmed = Leg2 rebreak before waist break
invalidated = waist break before Leg2 rebreak
```

The F1 waist must stay between origin and leg1.

### F2

```text
origin = parent F1 internal 2
confirmed = own Leg2 rebreak before origin break
invalidated = own origin break before Leg2 rebreak
```

F2 may break its own waist. If the waist-break branch is used:

```text
1 = waist
2 = node that breaks waist
```

### F3

```text
origin = parent F2 internal 2
confirmed = own Leg2 rebreak before origin break
invalidated = own origin break before Leg2 rebreak
```

F3 uses the same continuation-level rules as F2.

## Size symmetry

Continuation bodies are required by default to be at least the size of their parent:

```text
child_size >= parent_size * InpChildMinParentSizeRatio
size = abs(Leg2.price - Origin.price)
```

## Multi-scale settings

```text
InpUseMultiScale = true
InpSwingL = 3
InpSwingL2 = 5
InpSwingL3 = 8
InpSwingL4 = 13
InpSwingL5 = 21
InpSwingL6 = 0
```

## Rendering

The chart renderer is intentionally minimal:

```text
origin -> leg1 = straight line
leg1 -> waist -> leg2 = curve
F1/F2/F3 = tiny text
1/2 = tiny numeric labels only
```

No line is drawn from Leg2 to `1`, `2`, or confirmation.

## ND / Hook roadmap

ND is the hook/cycle-close phase that is not hunted. It does not require a strict 90% retracement; the key is that the local cycle closes and then movement begins. The current patch documents ND and keeps the experiment ready for it, but explicit ND partitioning and ND drawing are not yet fully implemented.

## Debugging

Use `FC_EVENT` fields:

```text
scaleL, chain, step, level, direction, status, branch, sizeRatio
```

When the chart looks wrong, first isolate one scale and one direction, then inspect `chain` and `step` ordering.
