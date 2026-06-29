# Flag Counting Phoenix — Level 19 Phase 4 Hook View Projection

## Purpose

Phase 4 extends the Level 19 State Gate from a closed-bar tracker plus Rally View projection into a full two-sided anatomy gate:

- Rally View reads the existing F1/F2/F3 anatomy.
- Hook View reads the existing Hook/ND branch anatomy.
- The dashboard displays both views per configured timeframe.
- The CSV export stores both Rally rows and Hook rows.

This phase is still read-only. It does not create, modify, filter, or reinterpret the locked Node, Hook/ND, Flag Body, Internal Count, F1, F2, or F3 engines.

## Hard boundary

The following layers remain locked and unchanged:

```text
Node Engine
Node Canonicalizer
Hook / ND Engine
Flag Body Engine
Internal Count Engine
F1 Lifecycle Engine
F2 Lifecycle Engine
F3 Lifecycle Engine
Ownership Engine
Canonicalization
Renderer
Validation
Release profiles
License gate
```

Phase 4 only runs the existing Phoenix anatomy pipeline per configured State Gate timeframe and projects the resulting `FP_HookBranch` rows into `FP_StateGateHookRow` rows.

## Conceptual meaning

The project does not add a separate Rally engine or Hook engine in Level 19.

```text
Rally View = existing F-counting output seen as the rally-side anatomy.
Hook View  = existing Hook/ND + node-count output seen as the hook-side anatomy.
```

That means the State Gate is the bridge from anatomy to future entry design, but it is not an entry engine. It stores and displays the state map needed before entry logic exists.

## Timeframe model

The State Gate still uses the three input timeframes:

```text
InpStateGateTf1 = PERIOD_M1
InpStateGateTf2 = PERIOD_M10
InpStateGateTf3 = PERIOD_H1
```

Each timeframe is processed independently from its own closed-bar candle stream. The dashboard does not fake M10/H1 state from the chart timeframe. For every configured timeframe, the canonical state is the last closed candle, `shift=1`.

## Hook View source

Hook View rows are built from the `FP_HookBranch` array returned by the existing locked detection pipeline:

```text
FP_DetectAllScales(..., tf_events, tf_hooks, ...)
```

Phase 4 reads these fields:

```text
branch_id
scale_L
direction
status
node_count
cycle_start_node
start_node
extreme_node
resolve_node
n1/n2/n3/n4
is_nd
side_kind
is_cycle_start_broken
nd_qualified
seeds_visible_f1
structural_id
visual_id
phase_id
chain_id
audit_id
source_L
source_mode
visible_main
hidden_reason
reason
```

No hook is rebuilt by Level 19. No Hook/ND branch is changed by Level 19.

## Projectable Hook rows

A Hook branch is projectable when:

```text
branch_id >= 0
node_count > 0
status is not invalidated
cycle_start is not broken
```

Visible hooks are displayed before hidden hooks, but hidden hooks are not automatically deleted from the State Gate. This follows the user requirement that the dashboard should show a broad state map across the available L-scale anatomy rather than only a single visible object.

## Sorting and display priority

For every timeframe, Hook rows are selected in this order:

```text
1. visible_main first
2. larger L scale first
3. larger node_count first
4. ND-qualified rows first
5. newer resolve_node index first
6. larger branch_id first
```

This gives the dashboard a large-to-small anatomy map, while keeping the most structurally important Hook/ND branches near the top.

The maximum rows per timeframe remains controlled by:

```text
InpStateGateMaxHookRowsPerTf
```

The global hard cap is:

```text
FP_STATE_GATE_MAX_HOOK_ROWS = 48
```

## Hook polarity

Phase 4 adds project-specific Hook polarity labels:

```text
FP_DIR_BULLISH → POSITIVE_HOOK_REVERSAL_UP
FP_DIR_BEARISH → NEGATIVE_HOOK_REVERSAL_DOWN
```

This matches the project language:

- Positive Hook means the semicircle ends downward and reversal pressure is upward.
- Negative Hook means the semicircle ends upward and reversal pressure is downward.

The polarity is a state label only. It is not an entry signal.

## Current node state

For every projected Hook row, the State Gate stores:

```text
current_node_number = hook.node_count
```

The dashboard label uses:

```text
NODE_3_CONFIRMED
NODE_4_CONFIRMED
```

The row also adds context tags:

```text
ND / HOOK
VISIBLE / HIDDEN
SEEDS_VISIBLE_F1 when true
CYCLE_BOUNDARY=<node id>
RESOLVE=<node id>
```

This answers the dashboard question:

```text
In this timeframe and this L-scale Hook sequence, what is the latest confirmed node state?
```

## Latest high and low node inside the Hook row

For every projected Hook row, Phase 4 scans the branch's own known anatomy nodes:

```text
cycle_start_node
start_node
n1
n2
n3
n4
extreme_node
resolve_node
```

Then it stores the latest high and latest low by `index_anchor`:

```text
latest_high_node_id
latest_high_node_price
latest_low_node_id
latest_low_node_price
```

This is not a new node-counting rule. It is a read-only projection of already-existing nodes inside the Hook branch.

## Dashboard behavior

Phase 4 keeps the dashboard in the upper-right chart corner by default:

```text
InpStateGatePanelCorner = CORNER_RIGHT_UPPER
InpStateGatePanelX      = 16
InpStateGatePanelY      = 24
```

The panel remains minimizable.

The expanded panel now shows, for each configured timeframe:

```text
closed-bar tracker row
latest established Rally summary
probable next Rally summary
top Hook summary
up to two Rally row labels
up to two Hook row labels
```

The full Hook list is written to CSV. The panel is intentionally compact so it remains readable on the chart.

## CSV outputs

Phase 4 continues to write:

```text
MQL5/Files/FlagCountingPhoenix/latest_state_gate_summary.csv
MQL5/Files/FlagCountingPhoenix/latest_state_gate_rally.csv
MQL5/Files/FlagCountingPhoenix/latest_state_gate_hooks.csv
MQL5/Files/FlagCountingPhoenix/latest_state_gate_manifest.csv
```

`latest_state_gate_hooks.csv` now contains real projected Hook rows instead of Phase 3 placeholders.

Hook CSV columns:

```text
symbol
slot
timeframe
closed_bar_time
closed_bar_close
status
source_hook_id
sequence_id
scale_L
direction
polarity
current_node_number
latest_high_node_id
latest_high_node_price
latest_low_node_id
latest_low_node_price
position_label
source_id
label
```

## Manifest state

The manifest now reports:

```text
projection_state = phase4_rally_and_hook_projected
```

## Audit behavior

The runtime audit still emits:

```text
FP_LEVEL19_STATE_GATE
FP_LEVEL19_STATE_GATE_SAMPLE
FP_LEVEL19_STATE_GATE_TIMER
```

The counts now include real Hook row counts.

## What Phase 4 is not

Phase 4 is not an entry model.

It does not output:

```text
buy
sell
entry_allowed
entry_forbidden
stop
final target
risk/reward
```

Those belong to later phases after the State Gate map is stable.

## Acceptance criteria

Phase 4 is accepted when:

```text
1. The EA compiles.
2. The Level 19 panel appears in the upper-right chart corner by default.
3. The panel can be minimized and restored.
4. Each configured timeframe is tracked only by closed candles.
5. Rally View still shows Phase 3 projected F-state rows.
6. Hook View shows projected Hook/ND rows from existing FP_HookBranch output.
7. Hook rows include polarity, L scale, current node number, latest high node, and latest low node.
8. latest_state_gate_hooks.csv contains real projected Hook rows.
9. latest_state_gate_manifest.csv reports phase4_rally_and_hook_projected.
10. No locked Node, Hook/ND, F-counting, ownership, renderer, validation, release, or license logic is modified.
```

## Next phase

The next natural phase is panel and export polish:

```text
Phase 5: State Gate Dashboard Polish + Debug Usability
```

Possible Phase 5 work:

```text
- row color modes by timeframe
- row filtering controls
- compact/detail toggle
- more readable ID modes
- optional CSV row limits
- screenshot-friendly panel geometry
- object count hardening
```
