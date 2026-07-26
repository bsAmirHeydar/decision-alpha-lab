# EXT-06 — Normalized Interpretation

## Core Claim

Node penetration is a hard invalidation event.

If price passes even one point beyond the cycle-origin node, the validity of that node as an Extreme anchor is finished.

This means there is no tolerance for penetration of the cycle-origin node.

## Hard Rule

Suggested hard rule:

```text
IF price crosses beyond the cycle-origin node by at least 1 point
THEN the Extreme anchor node is invalidated.
```

Formal state:

```text
NODE_VALIDITY = INVALIDATED
EXTREME_VALIDITY = DEAD
```

This is not a soft signal.

It is a structural invalidation.

## Small Penetration Is Not Treated as a Stop-Hunt

For this specific rule, a small penetration is not treated as a valid stop-hunt that preserves the original node.

The answer implies:

```text
one-point penetration = structural death
```

Therefore, the system should not reinterpret a penetrated cycle-origin node as still valid just because price returned quickly.

## No Buffer Around the Cycle-Origin Node

The answer does not allow a buffer for the cycle-origin node.

There may be execution buffers for broker stop placement or spread handling, but the structural node validity itself is binary.

Suggested distinction:

```text
structural invalidation = no buffer
broker stop placement = may include execution buffer
```

So the structural record should mark the node invalid as soon as the node is crossed.

## Before Fill vs After Fill

The user's answer implies that penetration invalidates the node regardless of whether the limit entry was filled before or after the penetration.

However, the system should still record the sequence because it matters for execution analysis.

Possible cases:

```text
PENETRATION_BEFORE_FILL
PENETRATION_AFTER_FILL
FILL_AND_IMMEDIATE_PENETRATION
STOP_HIT_THEN_REVERSE
```

Even if all of them invalidate the original node structurally, they have different execution-learning implications.

## Impact on Extreme

Since Extreme is built around the near-death zone of a cycle-origin node, node penetration means the cycle has died.

Therefore:

```text
Extreme is no longer alive as the same Extreme.
```

If price later reverses, that may create a new structure or a new scenario, but it should not keep the old Extreme anchor alive.

## Relationship to EXT-01

EXT-01 defined Extreme as near-death of a cycle.

EXT-06 defines the death boundary.

Together:

```text
Near death = valid Extreme zone before node death.
Node crossed by even one point = cycle death confirmed.
```

This makes the Extreme concept crisp:

```text
trade near death,
but do not pretend death has not happened after penetration.
```

## Dataset Consequence

Future Extreme datasets must track exact node penetration.

Required fields:

```text
anchor_node_price
cycle_origin_node_price
node_penetrated
node_penetration_points
node_penetration_before_fill
node_penetration_after_fill
extreme_invalidated_by_penetration
```

## Execution Consequence

If a pending Extreme order exists and the anchor node is penetrated before fill:

```text
cancel the pending order
mark the Extreme as invalidated
```

If an Extreme entry is already filled and the node is penetrated:

```text
the structural stop/invalidation has occurred
mark the trade as invalidated
```

If price penetrates and then reverses:

```text
log STOP_HIT_THEN_REVERSE or PENETRATION_THEN_REVERSAL
do not keep the old node valid
use the event to evaluate stop geometry and Extreme width
```

## AI Relevance

AI should not learn to keep the same anchor node alive after penetration.

This is a hard rule.

AI may learn from penetration outcomes, but only as post-event analysis.

Allowed AI tasks:

```text
analyze how often one-point invalidation is followed by reversal
evaluate whether entry width was too tight
evaluate whether stop placement is too fragile
suggest new policy for future Extreme width
```

Forbidden AI task:

```text
declare a penetrated cycle-origin node still valid
```

## Short Formal Statement

For an Extreme anchor based on a cycle-origin node, any penetration beyond the node, even by one point, ends the validity of that node. Quick return does not preserve the original node. The old Extreme is structurally dead, although the penetration-then-reversal event should be recorded for execution and policy learning.
