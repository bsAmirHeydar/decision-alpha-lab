# Phase 27 — Lifecycle-Aligned Confirmed Near-Death Hook Visibility

## Problem

The Phase 26 rebuild aligned the branch builder with the Hook/ND branch documentation, but the semantic renderer was still too permissive:

- a Hook could still visually span across its own floor/ceiling boundary;
- unconfirmed final nodes could still produce visible structure;
- arcs could be drawn before the last same-side node was confirmed in the Near-Death area;
- the renderer was still allowed to infer an end point from counted nodes instead of the confirmed lifecycle resolve node.

This contradicts the lifecycle rule:

> If the Hook floor/ceiling is touched or penetrated, the Hook is failed/dead.
> If the final node is confirmed in Near-Death, draw only to that node.
> If it is not confirmed, do not draw the Hook in semantic view.

## Rules added

### 1. Boundary failure kills visibility

For a low-side / positive Hook:

```text
boundary = Hook floor
touch/breach = same-side low <= boundary price
```

For a high-side / negative Hook:

```text
boundary = Hook ceiling
touch/breach = same-side high >= boundary price
```

When `death_on_boundary_touch` is enabled, equality also kills the Hook. This matches the practical visual rule that the start of the Hook must not be hit again.

### 2. Confirmed resolve node required

The semantic renderer now requires:

```text
resolve_confirmed = true
```

for the branch resolve/final node.

### 3. Near-Death retracement required

The branch must have a confirmed resolve node that retraces toward the Hook floor/ceiling side by at least:

```text
near_death_retrace_threshold = 0.50
```

If not, the branch stays out of semantic Hook rendering.

### 4. Arc endpoint is the confirmed Near-Death resolve node

The grouped Hook envelope no longer chooses an arbitrary counted node after the crown. It only chooses confirmed Near-Death resolve nodes from render-eligible branches.

## New inputs

```text
InpHookPhase02RequireConfirmedResolveNode
InpHookPhase02DeathOnBoundaryTouch
InpHookPhase02RequireNearDeathForSemanticArc
InpHookPhase02NearDeathRetraceThreshold
```

## New sequence audit fields

```text
resolve_node_id
resolve_time
resolve_price
resolve_confirmed
retracement_ratio
near_death_confirmed
hook_failed
failure_node_id
failure_time
failure_price
render_eligible
visibility_reason
```

## Remaining architecture note

This patch fixes lifecycle gating and visibility. It does not implement the full adaptive-L rebuild when a branch exceeds four counted nodes; that remains a separate engine-level phase.
