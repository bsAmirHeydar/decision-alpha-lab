# Phase 21 — Cycle Arc Ends at the Directional Extreme

## Goal

Make the cycle semicircle match the intended Hook anatomy:

- the cycle arc starts at the Hook origin
- the arc spans toward the semicircle crown
- the arc endpoint lands where the cycle actually saw its directional extreme
- for a positive Hook, that endpoint is the **lowest valley seen by the cycle**
- for a negative Hook, that endpoint is the **highest peak seen by the cycle**

## Problem in previous versions

The cycle arc ended at the **last visible X** (`X1`, `X2`, `X3`, or `X4`).
That was acceptable for generic debugging, but it did not match the intended interpretation of the Hook cycle.

## New arc endpoint mode

A new Phase 02 setting was added:

```text
FP_HookPhase02CycleArcEndMode
```

Modes:

- `FP_HOOK_P02_CYCLE_ARC_END_LAST_VISIBLE_X`
- `FP_HOOK_P02_CYCLE_ARC_END_DIRECTIONAL_EXTREME`

## Directional extreme behavior

When `DIRECTIONAL_EXTREME` is active:

- **Positive** Hook: choose the lowest price among `X1..X4`
- **Negative** Hook: choose the highest price among `X1..X4`
- if two points have the same extreme price, prefer the later one in time

The cycle semicircle then spans from `origin` to that extreme point.

## Minimal profile default

`FP_HOOK_P07_VIEW_MINIMAL_ALL_HOOKS` now forces:

```text
p02.cycle_arc_end_mode = FP_HOOK_P02_CYCLE_ARC_END_DIRECTIONAL_EXTREME;
```

So the arc-only minimal view now follows the actual cycle low/high rather than simply ending at the latest visible X.
