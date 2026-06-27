# Sequence Identity Definition

## Why Identity Matters

Earlier visual failures came from orphan lines and indistinguishable candidates. Every structure must be traceable.

A drawn flag must answer:

```text
Which chain owns me?
Which level am I?
Which nodes define me?
What is my parent?
What state am I in?
Why am I still alive?
```

## Chain Identity

Recommended chain fields:

```text
chain_id
symbol
timeframe
direction
root_phase_boundary_id
root_origin_node_id
active_L_context
creation_time
status
```

## F Object Identity

Recommended F object fields:

```text
f_id
chain_id
f_level: 1|2|3
direction
status
origin_node_id
leg1_node_id
waist_node_id
leg2_node_id
flag_size
parent_f_id
post_flag_context_id
qualification_state
confirmation_time
completion_time
lock_time
```

## Post-Flag Context Identity

Recommended fields:

```text
context_id
parent_f_id
start_after_leg2_node_id
adverse_side
tracked_nodes
hook_branch_ids
deepest_adverse_node_id
confirmation_break_node_id
```

## Hook Branch Identity

Recommended fields:

```text
hook_id
owning_context_id
direction_context
adverse_side
start_node_id
extreme_node_id
final_node_id
readable_L
numbered_node_ids[1..4]
is_nd
half_cycle_passed
```

## Duplicate Rule

All different structures should be visible.

A duplicate exists only when complete identity is the same.

Compare:

```text
symbol
timeframe
direction
F level
chain id / parent context
origin time + price + node id
leg1 time + price + node id
waist time + price + node id
leg2 time + price + node id
post-flag context id
readable L / node L identity
```

If any item differs, it is a distinct sequence.

## Near-Duplicates

Near duplicates are not duplicates.

Examples that must remain distinct:

- same price but different time;
- same time but different L identity;
- same body but different parent context;
- visually close but different waist;
- same origin/leg1 but different Leg2 extension;
- same geometry but different sequence role.

## Exact Same Geometry with Different L

If every geometry node time/price is identical but only L metadata differs, the safest research behavior is:

```text
keep separate logical identities
render with either separate labels or combined multi-L label if explicitly enabled
```

Default for research should not silently merge. Merging may hide a logic error.

A later visualization input may allow:

```text
InpMergeExactGeometryDifferentLForDisplay = false
```

Default false.

## Dead Candidate Identity

When a candidate dies, its identity is closed. It must not be reused.

If parent context continues and a new candidate is built from the same context, the new candidate receives a new identity.

This is critical for F2:

```text
F2 candidate dies by origin pass.
F1 context remains.
New F2 candidate can be built from the same post-F1 correction context.
But the old F2 body identity is not resurrected.
```
