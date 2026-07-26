# Flag Counting Level 19 — Phase 11 Entry Bridge Readiness

## Purpose

Phase 11 is the first formal bridge from the State Gate anatomy map toward future entry design.

It still does **not** create trade signals.

The purpose is to store decision-neutral readiness fields that tell the next layer whether the current closed-bar anatomy is ready to be used for extreme mapping, X-invalidation mapping, X-destination mapping, and optionality geometry.

## What Phase 11 adds

Phase 11 adds per-timeframe fields to the State Gate contract:

```text
entry_bridge_readiness
entry_bridge_key
candidate_extreme_status
candidate_extreme_key
candidate_extreme_source
candidate_direction
candidate_scale_context
x_invalidation_status
x_invalidation_key
x_destination_status
x_destination_key
optionality_status
optionality_key
```

These fields are stored in the `FP_StateGateTimeframeState` object.

## Important boundary

These fields are **not** trade decisions.

Phase 11 must not produce:

```text
buy
sell
entry_allowed
entry_direction
entry_price
stop_loss
take_profit
target
order_type
```

The only purpose is to prepare a clean bridge object.

## Readiness labels

The main readiness field can produce labels such as:

```text
ENTRY_BRIDGE_READY_FOR_EXTREME_MAPPING_NO_DECISION
ENTRY_BRIDGE_RALLY_ONLY_NEEDS_HOOK_CONTEXT_NO_DECISION
ENTRY_BRIDGE_HOOK_ONLY_NEEDS_RALLY_CONTEXT_NO_DECISION
ENTRY_BRIDGE_NOT_READY_NO_PROJECTED_ANATOMY
ENTRY_BRIDGE_BLOCKED_NO_CLOSED_BAR
```

## Candidate extreme labels

The candidate extreme field is still context-only:

```text
CANDIDATE_EXTREME_FROM_HOOK_CONTEXT_NO_PRICE
CANDIDATE_EXTREME_FROM_RALLY_CONTEXT_NO_PRICE
CANDIDATE_EXTREME_NOT_AVAILABLE
CANDIDATE_EXTREME_BLOCKED_NO_CLOSED_BAR
```

This means Phase 11 identifies the *source context* for future extreme selection, but it does not yet select an executable price.

## X and Optionality placeholders

The X geometry fields are intentionally placeholders:

```text
X_INVALIDATION_PENDING_GEOMETRY_NO_PRICE
X_DESTINATION_PENDING_GEOMETRY_NO_PRICE
OPTIONALITY_PENDING_X_GEOMETRY_NO_R
```

This keeps the boundary clean:

- Phase 11 stores readiness.
- Later phases map actual X-invalidation.
- Later phases map actual X-destination.
- Later phases compute potential R / optionality.

## New export

Phase 11 adds:

```text
InpStateGateExportEntryBridgeCsv = true
```

and writes:

```text
MQL5/Files/FlagCountingPhoenix/latest_state_gate_entry_bridge.csv
```

This file is the primary output for the next implementation phase.

## Locked engines

Phase 11 does not modify:

- Node Engine
- Hook / ND Engine
- Flag Body
- Internal Count
- F1 Lifecycle
- F2 Lifecycle
- F3 Lifecycle
- Ownership / Canonicalization
- Renderer
- Validation
- Release
- License

It only reads State Gate projection outputs and extends the contract layer.

## Next phase

The next natural phase is:

```text
Phase 12 — Extreme Candidate Map
```

That phase should start converting the context-only candidate fields into a structured map of candidate extremes, still without orders.
