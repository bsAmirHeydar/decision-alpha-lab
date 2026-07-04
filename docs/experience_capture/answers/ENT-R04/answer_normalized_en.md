# ENT-R04 — Normalized Interpretation

## Core Claim

After a limit entry is filled, the reason set that created the trade must become locked to the active position.

As long as that position remains open, the system must not open a duplicate trade using the same reasons.

Recommended canonical rule:

```text
If Position is open for ReasonSet R:
    block new duplicate entry for ReasonSet R
```

This creates a `PositionReasonLock`.

## Scenario-to-Position Transition

Before fill, the system has:

```text
ScenarioThread
ZoneOpportunity
EntryLevelExtreme
ExecutionIntent
PendingLimitIntent
```

After fill, the filled intent becomes:

```text
PositionThread
```

The scenario does not necessarily disappear. It can remain as the parent analytical object, but the active risk and trade management should move into a position object.

Suggested relationship:

```text
ScenarioThread → ExecutionIntent → FillEvent → PositionThread
```

The `PositionThread` should preserve lineage:

```text
scenario_id
zone_id
entry_extreme_id
reason_set_id
execution_intent_id
pending_limit_id
fill_id
position_id
```

## Duplicate Trade Block

The most important rule in this answer is:

```text
Do not take another duplicate trade with the same reasons while the original trade is open.
```

This prevents repeated entries from the same structural logic while the first trade has not completed.

Suggested object:

```text
PositionReasonLock
```

Fields:

```text
reason_set_id
position_id
is_locked
lock_start_time
lock_end_time
unlock_reason
```

If a new candidate has the same reason set while the position is still open:

```text
entry_permission = BLOCKED_DUPLICATE_REASON
```

## Same Reasons vs New Reasons

The duplicate block applies to the same reasons.

It does not necessarily block all new trades.

A new trade may be allowed if it is based on a genuinely different reason set.

This requires reason-set identity comparison.

Suggested levels:

```text
same_reason_set
overlapping_reason_set
new_reason_set
opposite_reason_set
hedge_reason_set
```

Only `same_reason_set` is clearly blocked by this answer.

Overlapping or new reason sets remain open questions for future risk policy.

## PositionThread

A filled trade should be tracked as a position object, not merely as a scenario state.

Suggested object:

```text
PositionThread
```

It should contain:

```text
position_id
reason_set_id
scenario_id
zone_id
entry_extreme_id
entry_price
stop_price
destination_set
exit_plan
position_state
```

The scenario can still update in the background, but the position should have its own lifecycle.

## Multi-Exit Logic

Exit can happen in several places.

The user states:

```text
Exit can be in several places based on our own logics.
```

This means exit should not be reduced to one fixed TP.

Exits may be based on:

```text
destination logic
multi-destination logic
partial exit logic
position management logic
structural completion
risk reduction logic
tail / runner logic
```

The exact exit rules remain a destination/position-management topic, but ENT-R04 establishes that multiple exits are allowed.

Suggested object:

```text
MultiExitPlan
```

Possible exit states:

```text
EXIT_PENDING
PARTIAL_EXIT_1_DONE
PARTIAL_EXIT_2_DONE
RUNNER_ACTIVE
FINAL_EXIT_DONE
POSITION_COMPLETED
```

## Hedge Separation

Hedging is not part of this same position transition logic.

The user explicitly states that hedge is separate because it has separate entry logics.

Therefore:

```text
hedge entry must require its own entry logic
```

A hedge should not be created automatically just because an opposite scenario appears or because an existing position is open.

Suggested rule:

```text
Hedge is a separate EntryIntent family.
```

It should have its own:

```text
scenario
zone
entry_extreme
reason_set
risk budget
validation
```

## Opposite Scenario Handling

If an opposite scenario appears while a position is open, that does not automatically mean hedge.

Based on this answer:

```text
opposite scenario ≠ automatic hedge
```

A hedge can only be considered if the hedge logic itself produces a valid entry reason set.

This keeps hedging from contaminating the main position lifecycle.

## Split Orders and Logical Position

ENT-R02 established that max-lot orders can be split into multiple trades.

ENT-R04 implies that if those split trades come from the same reasons, they should be treated as one logical position group.

Suggested object:

```text
LogicalPositionBucket
```

Fields:

```text
logical_position_id
reason_set_id
child_order_ids
child_position_ids
aggregate_volume
aggregate_risk
aggregate_exit_state
```

This prevents split orders from being mistaken for duplicate new opportunities.

## Position Completion

A position should remain tied to its reason set until it is closed.

Unlocking condition:

```text
position fully closed
position invalidated and exited
position completed by exit plan
manual/forced close recorded
```

Only after unlocking can the same reason set potentially be eligible again, depending on future rules.

## Machine-Readable Summary

```text
after fill:
    create PositionThread
    lock reason_set_id to open position
    block duplicate entries with same reasons
    allow exits at multiple NDS-defined locations
    treat hedge as separate entry logic
    do not auto-hedge from opposite scenario alone
```

## Short Formal Statement

After a limit entry is filled, the trade becomes an active PositionThread linked to the same scenario, zone, entry extreme, and reason set that created it. While that position is open, the system must not take another duplicate trade with the same reasons. The reason set is locked to the open position until the position is closed or completed. Exits can occur in multiple places according to NDS exit and destination logic. Hedging is a separate topic because it requires separate entry logic and should not be automatically triggered by the existence of an active position or an opposite scenario.
