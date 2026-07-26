# ENT-R03 — Normalized Interpretation

## Core Claim

A pending limit order remains alive only while the reasons that created that trade remain valid.

If the reasons are no longer valid, the pending limit must be deleted or canceled.

Recommended canonical rule:

```text
PendingLimitAlive ⇔ TradeReasonIntegrity is intact
```

This makes the pending order lifecycle structural rather than time-based.

## Pending Order as a Reason-Bound Object

A pending limit order is not an independent order floating in the market.

It is attached to a specific reason set.

Suggested object:

```text
PendingLimitIntent
```

It should be linked to:

```text
scenario_id
zone_id
entry_extreme_id
reference_node_id
destination_id
reason_set_id
execution_intent_id
```

The order remains valid only as long as this reason set remains valid.

## Trade Reason Set

The reasons for the trade may include:

```text
parent scenario
parent zone
entry-level Extreme Near Death
reference node
death boundary
destination / optionality
convexity profile
risk geometry
constraint set
```

The pending limit should maintain a `trade_reason_set`.

Each item can be tracked as:

```text
REASON_INTACT
REASON_WEAKENED
REASON_INVALIDATED
REASON_REPLACED
REASON_CONSUMED
```

## Reason Integrity

The main lifecycle metric is:

```text
trade_reason_integrity
```

Suggested interpretation:

```text
alive = core reasons intact
delete/cancel = core reasons invalidated
```

This is parallel to SCN-R04, where scenario life depends on constraint integrity.

ENT-R03 applies the same principle to pending orders.

## Structural Expiration Over Time Expiration

The user's answer implies that survival is based on whether the reasons remain alive.

Therefore, the first-class expiration type should be:

```text
STRUCTURAL_EXPIRATION
```

Not arbitrary time expiration.

Time expiration can exist later as an execution safety parameter, but it is not the core NDS rule.

Core NDS rule:

```text
pending order lives while its reasons live
```

## Cancel / Delete Policy

A pending limit should be deleted or canceled when any core reason that makes it tradeable is no longer valid.

Examples:

```text
parent scenario dies
parent zone is destroyed
entry-level Extreme Near Death is invalidated
reference node / death boundary is crossed
convexity disappears
reward path closes
risk geometry becomes non-convex
execution intent becomes unsafe
```

The cancellation reason should be recorded.

Suggested field:

```text
cancel_reason
```

## Missed Entry

The user did not define missed behavior explicitly in this answer.

Based on the core rule, "missed" should not be a separate discretionary decision unless the trade reasons remain valid but price moves away without fill.

Initial interpretation:

```text
MISSED = price moves away from the intended entry area without fill while the original reason was still valid at the time
```

But if reasons become invalid first, the state is not merely missed.

It is:

```text
CANCELED_BY_REASON_INVALIDATION
```

## Replace Policy

The user did not define replacement details explicitly.

Based on the answer, replacement should only be allowed if the old reasons are no longer the best expression, but a valid reason set still exists or a new reason set forms.

Possible interpretation:

```text
replace = delete old pending limit and create a new pending limit from an updated valid reason set
```

Replacement should not preserve a dead order.

It should create a new reason-bound intent.

## Pending Limit State Machine

Suggested states:

```text
PENDING_LIMIT_CREATED
PENDING_LIMIT_ALIVE
PENDING_LIMIT_REASON_INTACT
PENDING_LIMIT_REASON_WEAKENED
PENDING_LIMIT_CANCELED_BY_REASON_INVALIDATION
PENDING_LIMIT_DELETED
PENDING_LIMIT_MISSED
PENDING_LIMIT_REPLACED
PENDING_LIMIT_FILLED
PENDING_LIMIT_EXPIRED_STRUCTURALLY
```

## Important Distinction

A pending order can remain alive even if price has not filled it yet.

The deciding factor is not time or impatience.

The deciding factor is:

```text
Are the reasons for this trade still valid?
```

If yes, it remains.

If no, it is deleted.

## Machine-Readable Summary

```text
pending_limit_lifecycle = reason_integrity_based

if trade reasons remain valid:
    keep pending limit alive

if trade reasons become invalid:
    delete / cancel pending limit

primary expiration = structural expiration
time expiration = secondary execution safety parameter only
```

## Short Formal Statement

In NDS, a pending limit order remains alive only while the reasons that created that trade remain valid. The order is bound to its scenario, zone, entry-level Extreme, reference node, destination, convexity profile, and risk geometry. If those reasons remain intact, the pending order can stay alive. If the reasons are invalidated, the order must be deleted or canceled. This makes pending limit lifecycle a structural reason-integrity problem rather than an arbitrary time-expiration problem.
