# Dedup and Audit Algorithm

## Dedup Goal

Prevent exact duplicate emission while preserving all genuinely different sequences.

The engine must not merge near-duplicates for visual neatness.

## Identity Key

Use a full identity key:

```text
symbol
timeframe
direction
F level or Hook type
chain id
parent context id
origin node id/time/price
leg1 node id/time/price
waist node id/time/price
leg2 node id/time/price
readable L / node L
status class
```

For hook:

```text
hook context id
numbered node ids
start node
extreme node
final node
readable L
```

## Exact Duplicate

If full key matches an existing active/emitted object:

```text
update status/metadata if needed
but do not emit another chart geometry
```

## Distinct Sequence

If any field differs:

```text
emit distinct logical object
```

Even tiny time/price/context differences matter.

## Audit Events

Every transition should be auditable.

Recommended event fields:

```text
event_time
bar_time
node_time
symbol
timeframe
chain_id
object_id
event_type
old_status
new_status
reason_code
boundary_price
trigger_node_id
trigger_node_price
parent_id
context_id
```

## Reason Codes

Examples:

```text
PHASE_BOUNDARY_CREATED
F1_BODY_COMPLETED
F1_LEG2_EXTENDED
F1_INTERNAL_12_FOUND
F1_INVALIDATED_WAIST_PASSED
F1_CONFIRMED_LEG2_REPASS
F2_AUTHORIZED_BACKFILLED
F2_BODY_COMPLETED
F2_SIZE_WAITING
F2_SIZE_QUALIFIED
F2_INVALIDATED_ORIGIN_PASSED
F2_REBUILT_FROM_PARENT_CONTEXT
F2_WAIST_BREAK_BRANCH_CREATED
F2_CONFIRMED_LEG2_REPASS
F3_AUTHORIZED_BACKFILLED
F3_BODY_COMPLETED
F3_WAITING_OR_QUALIFICATION
F3_COMPLETED_OR_QUALIFIED
F3_EXTENDED
F3_LOCKED_BY_OPPOSITE_F1
HOOK_BRANCH_CREATED
ND_ACCEPTED_HALF_CYCLE
ND_REJECTED_BELOW_HALF
```

## Audit Before Rendering

Do not debug primarily from chart lines.

First verify audit sequence:

1. body creation;
2. context tracking;
3. hook branches;
4. child authorization;
5. invalidation/confirmation;
6. render model emission.

Only after audit is correct should renderer be judged.
