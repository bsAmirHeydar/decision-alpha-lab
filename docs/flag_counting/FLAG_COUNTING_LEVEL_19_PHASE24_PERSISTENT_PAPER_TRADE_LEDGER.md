# Flag Counting Level 19 — Phase 24 Persistent Paper Trade Ledger

## Purpose

Phase 24 adds a persistent paper trade identity ledger above the Phase 23 Dry-Run Decision Policy layer.

This phase still does **not** send real orders.

It turns dry-run-allowed policy rows into stable paper trade records with deterministic paper trade IDs.

## Hard safety contract

```text
real execution = disabled
persistent paper trade ledger only
no broker orders
no tickets
no position state
```

## New CSV

Phase 24 writes:

```text
MQL5/Files/FlagCountingPhoenix/latest_state_gate_persistent_paper_trades.csv
```

## New input

```text
InpStateGateExportPersistentPaperTradesCsv = true
```

## New per-timeframe fields

Each State Gate timeframe state now stores:

```text
persistent_paper_trade_row_count
persistent_paper_trade_status
persistent_paper_trade_key
persistent_paper_trade_id
persistent_paper_trade_lifecycle_status
persistent_paper_trade_direction
persistent_paper_trade_type
persistent_paper_trade_entry_price
persistent_paper_trade_invalidation_price
persistent_paper_trade_destination_price
persistent_paper_trade_policy_status
persistent_paper_trade_execution_status
persistent_paper_trade_notes
```

## Snapshot-level fields

The State Gate snapshot now stores:

```text
persistent_paper_trade_row_count
persistent_paper_trade_status
persistent_paper_trade_key
persistent_paper_trade_total_rows
persistent_paper_trade_registered_rows
persistent_paper_trade_blocked_rows
persistent_paper_trade_open_like_rows
persistent_paper_trade_policy_allowed_rows
persistent_paper_trade_distribution
persistent_paper_trade_execution_status
persistent_paper_trade_notes
```

## Trade status examples

```text
PERSISTENT_PAPER_TRADE_REGISTERED_DRY_RUN_ONLY
PERSISTENT_PAPER_TRADE_BLOCKED_BY_POLICY
PERSISTENT_PAPER_TRADE_BLOCKED_NO_ENTRY_PRICE
PERSISTENT_PAPER_TRADE_BLOCKED_NO_CLOSED_BAR
```

## Lifecycle status examples

```text
PAPER_TRADE_LIFECYCLE_REGISTERED_WAITING_FOR_FUTURE_TRACKING
PAPER_TRADE_LIFECYCLE_BLOCKED_BY_POLICY
PAPER_TRADE_LIFECYCLE_BLOCKED_NO_ENTRY_PRICE
PAPER_TRADE_LIFECYCLE_BLOCKED
```

## Persistent ID

The paper trade ID is deterministic and contains:

```text
symbol
timeframe
closed bar time
source policy key
entry price
```

This makes the row stable enough for later lifecycle tracking.

## Design boundary

Phase 24 does not create broker orders, live tickets, or position state.

It only creates a paper trade identity layer for future persistent paper lifecycle simulation.

## Execution safety

Every Phase 24 row keeps:

```text
execution_status = REAL_EXECUTION_DISABLED_PHASE24_PERSISTENT_PAPER_ONLY
trade_mode       = PERSISTENT_PAPER_DRY_RUN_ONLY
```

## Locked boundaries

Phase 24 does not modify:

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

It only reads paper policy, decision, ledger, and geometry context.

## Next natural phase

The next phase can be:

```text
Phase 25 — Persistent Paper Trade Lifecycle Engine
```

That phase should still be non-executable and should track the persistent paper trade state across future closed bars.
