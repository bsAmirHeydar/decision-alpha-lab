# Phoenix Flag Counting Implementation Ladder V1

This document is part of the implementation ladder for the Phoenix Flag Counting engine.

# Level 11.5 — Raw Audit Export and Report Engine

## Purpose

Level 11.5 makes the engine auditable before the renderer becomes the primary inspection tool. Phoenix must be able to explain its structural decisions as data.

This level sits after semantic canonicalization and before renderer/layout work:

```text
Level 11 canonicalization
-> Level 11.5 raw audit export/report
-> Level 12 renderer
```

## Owned files

```text
mql5/Include/FlagCountingPhoenix/FP_Audit.mqh
mql5/Include/FlagCountingPhoenix/FP_Types.mqh       # only if audit fields are missing
mql5/Experts/FlagCounting/FlagCountingPhoenixExperiment.mq5 # only for input/output wiring
```

## Inputs

```text
FP_Node nodes[]
FP_HookBranch hooks[]
FP_FlagEvent raw_events[]
FP_FlagEvent visible_events[]
FP_DetectResult summary
FP_Config config
```

## Required output groups

At minimum, audit/report output must expose:

```text
raw_nodes
scaled_nodes
hook_branches
raw_events
visible_events
hidden_events
hidden_reason
sequence_transitions
canonical_winners
candidate_count
qualified_count
confirmed_count
invalidated_count
completed_count
locked_count
```

## Required fields per event

```text
event_id
sequence_id
parent_event_id
parent_sequence_id
chain_index
scale_L
direction
level
status
branch_kind
render_kind
origin_id / origin_time / origin_price
leg1_id / leg1_time / leg1_price
waist_id / waist_time / waist_price
leg2_id / leg2_time / leg2_price
confirm_id / confirm_time / confirm_price
invalid_id / invalid_time / invalid_price
flag_size
parent_flag_size
size_ratio
leg1_L
parent_leg1_L
from_phase_boundary
from_fail_open
visible_main
reason
```

## Required fields per Hook/ND branch

```text
branch_id
scale_L
direction
status
node_count
start_node
cycle_start_node
extreme_node
resolve_node
n1/n2/n3/n4
retrace_ratio
is_nd
reason
```

## Output forms

Target final output:

```text
CSV and/or JSON files under MQL5 Files/FlagCountingPhoenix/
```

Temporary acceptable output while export is being built:

```text
structured PrintFormat logs with stable field names
```

Temporary logs must use the same field names intended for CSV/JSON so that later export does not change the audit contract.

## Non-authority rule

Audit/export may not mutate event state, visibility, parent-child links, node identity, or renderer output. It only serializes decisions already made by lower layers.

## Acceptance tests

- Running with audit enabled emits raw event count and visible event count separately.
- Every hidden event has a non-empty `reason`.
- Every visible event has `visible_main=true`.
- A duplicate loser remains in raw events and is absent from visible events.
- A fail-open event is explicitly tagged.
- Renderer can be disabled while audit/export still works.
- Re-running the same range produces identical event order and IDs.

## Failure symptoms

- The only way to inspect a decision is by looking at the chart.
- Hidden structures disappear without a reason.
- Renderer settings change raw event counts.
- Audit logs use prose-only messages that cannot be parsed later.
- A child event exists without parent identity.

## Freeze criteria

Level 11.5 is frozen when a deterministic audit/report exists for at least one validation range and the renderer can be disabled without losing logical output.
