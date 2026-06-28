# Phoenix Sequence Ownership Repair V4

## Failure that this patch addresses

The previous Phoenix repairs improved individual components, but they still left the main chart as a candidate enumeration layer.  Hook/ND roots, raw fail-open roots, and multiple L-scales could all emit independent F1 roots in the middle of the same directional phase.  This violated the sequence contract:

```text
F1 -> F2 -> F3
```

Within one active directional phase, a later same-direction F1 is not allowed to become a new main-chart chain merely because a local Hook/ND or a lower-L body exists.  The active chain is still doing work.

## Root cause

The engine was doing the following:

1. Build Hook-derived roots.
2. Optionally build fail-open roots.
3. Build F1/F2/F3 chains from every root.
4. Try to clean the chart with duplicate-body canonicalization.

That is not a true state machine.  Duplicate cleanup only removes nearly identical bodies.  It cannot decide ownership when two F1 roots are different geometrically but belong to the same active directional phase.

## Correct contract

The main chart must be a sequence-state view, not a sliding-window dump.

- Hook/ND may authorize a phase boundary.
- Raw fail-open may be used as recovery while Hook coverage is being researched.
- But after a same-direction F1 root is accepted for a phase, later same-direction F1 roots must be hidden unless an opposite completed/locked F3 resets the phase.
- If several candidate roots compete inside the same phase, the main chart keeps the chain with higher semantic maturity, not necessarily the earliest or largest L umbrella.

## Implemented repair

This patch adds strict main-chart ownership:

```text
InpStrictMainChartOwnership = true
```

For each direction, visible F1 roots are processed in chronological order.  If a new same-direction F1 appears before an opposite completed/locked F3 reset, it competes with the current root.  The engine keeps the chain with the stronger maturity score and hides the losing root together with its descendants.

Maturity score prefers:

1. chains that have advanced to F3;
2. chains that have advanced to confirmed F2;
3. confirmed F1 roots;
4. Hook/phase-boundary roots over fail-open roots;
5. local lower-L roots over high-L umbrellas when semantic maturity is otherwise close.

This is not renderer logic.  It is sequence ownership logic applied before rendering.

## Label discipline

The main chart must not show audit labels by accident.  This patch adds:

```text
InpForceCleanMainChartLabels = true
```

When detailed labels are off, Hook count labels, parent IDs, origin labels, and internal labels are forced off at the renderer call boundary.  To audit internal labels, explicitly enable `InpDetailedLabels`.

## What this patch does not change

- Node extraction remains high/low only.
- Equality remains non-breaking.
- Hook branch extraction remains bounded and same-side.
- F2 is still authorized only after confirmed F1.
- F3 is still authorized only after confirmed F2.
- Renderer still draws only emitted events and hooks.
