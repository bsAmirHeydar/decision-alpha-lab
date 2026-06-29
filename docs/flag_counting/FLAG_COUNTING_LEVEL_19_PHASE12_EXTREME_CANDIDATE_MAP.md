# Flag Counting Level 19 — Phase 12 Extreme Candidate Map

## Purpose

Phase 12 adds the first real map from State Gate context toward X-axis candidate extremes.

This is still **not an entry system**.

Phase 12 does not produce:

```text
buy
sell
entry_allowed
entry_price
stop_loss
take_profit
order_type
```

It only maps candidate extremes from the already-projected State Gate anatomy.

## What Phase 12 adds

Phase 12 introduces an Extreme Candidate Map above the read-only Rally and Hook projections.

For each configured timeframe, the State Gate now stores:

```text
extreme_candidate_row_count
extreme_map_status
extreme_map_key
primary_extreme_source
primary_extreme_direction
primary_extreme_side
primary_extreme_role
primary_extreme_price_status
primary_extreme_price
primary_extreme_node_id
primary_extreme_scale_L
extreme_map_notes
```

## New CSV

Phase 12 writes:

```text
MQL5/Files/FlagCountingPhoenix/latest_state_gate_extreme_candidates.csv
```

This file is the main Phase 12 output.

It contains one row per mapped candidate context.

## Candidate sources

The candidate map can read from two existing State Gate sources:

```text
HOOK_VIEW
RALLY_VIEW
```

### Hook candidate rows

Hook rows can map to an actual high/low node context because the Hook View already contains latest high/low node fields.

The current rule is:

```text
POSITIVE_HOOK_REVERSAL_UP   -> LOW_EXTREME
NEGATIVE_HOOK_REVERSAL_DOWN -> HIGH_EXTREME
```

If polarity is not explicit, the direction is used as a fallback:

```text
BULLISH -> LOW_EXTREME
BEARISH -> HIGH_EXTREME
```

The mapped row stores:

```text
side
node_id
price
price_status
scale_L
source_hook_id
polarity
direction
```

### Rally candidate rows

Rally rows provide context, but they do not yet provide a final X-extreme price.

Therefore Rally-derived rows are exported with:

```text
side         = RALLY_CONTEXT_SIDE_PENDING
node_id      = -1
price        = 0
price_status = RALLY_CONTEXT_NO_EXTREME_PRICE
```

This is intentional. The Rally context remains useful, but the exact X geometry is for later phases.

## Status labels

Examples:

```text
EXTREME_MAP_READY_CONTEXT_ONLY_NO_DECISION
EXTREME_MAP_BLOCKED_NO_CLOSED_BAR
EXTREME_MAP_NOT_READY_NO_PROJECTED_ANATOMY
EXTREME_CANDIDATE_MAPPED_FROM_HOOK_NO_DECISION
EXTREME_CANDIDATE_CONTEXT_FROM_RALLY_NO_DECISION
EXTREME_PRICE_FROM_HOOK_NODE_CONTEXT_ONLY
RALLY_CONTEXT_NO_EXTREME_PRICE
```

All labels are explicitly decision-neutral.

## Updated outputs

Phase 12 extends these outputs:

```text
latest_state_gate_summary.csv
latest_state_gate_contract.csv
latest_state_gate_panel.csv
latest_state_gate_panel_lines.csv
latest_state_gate_entry_bridge.csv
latest_state_gate_manifest.csv
```

and adds:

```text
latest_state_gate_extreme_candidates.csv
```

## Inputs

New inputs:

```text
InpStateGateMaxExtremeCandidatesPerTf = 8
InpStateGateExportExtremeCandidatesCsv = true
```

## Locked boundaries

Phase 12 does not modify:

```text
Node Engine
Hook / ND Engine
Flag Body
Internal Count
F1 Lifecycle
F2 Lifecycle
F3 Lifecycle
Ownership / Canonicalization
Renderer
Validation
Release
License
```

It only consumes projected State Gate rows.

## Why this matters

The project needs to move from pure anatomy toward possible future entry geometry, but without jumping directly to trade decisions.

Phase 12 creates the missing intermediate layer:

```text
Rally / Hook State
        ↓
Extreme Candidate Map
        ↓
future X-invalidation / X-destination geometry
        ↓
future optionality
        ↓
future entry decision
```

## Next natural phase

The next phase is:

```text
Phase 13 — Multi-Timeframe Alignment Map
```

That phase should compare M1 / M10 / H1 candidate contexts and explain whether lower-timeframe extremes are meaningful inside the higher-timeframe state.
