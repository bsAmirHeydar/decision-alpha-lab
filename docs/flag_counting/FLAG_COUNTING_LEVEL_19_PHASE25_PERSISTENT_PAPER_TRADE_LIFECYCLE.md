# Flag Counting Level 19 — Phase 25 Persistent Paper Trade Lifecycle Engine

## Purpose

Phase 25 adds a lifecycle engine above the Phase 24 Persistent Paper Trade Ledger.

This phase still does **not** send real orders.

It takes persistent paper trade rows and evaluates their current paper lifecycle using the latest closed candle close only.

## Hard safety contract

```text
real execution = disabled
persistent paper trade lifecycle only
no broker orders
no tickets
no position state
```

## New CSV

Phase 25 writes:

```text
MQL5/Files/FlagCountingPhoenix/latest_state_gate_persistent_paper_trade_lifecycle.csv
```

## New input

```text
InpStateGateExportPersistentPaperTradeLifecycleCsv = true
```

## New per-timeframe fields

Each State Gate timeframe state now stores:

```text
persistent_paper_trade_lifecycle_row_count
persistent_paper_trade_lifecycle_engine_status
persistent_paper_trade_lifecycle_key
persistent_paper_trade_lifecycle_trade_id
persistent_paper_trade_lifecycle_path_state
persistent_paper_trade_lifecycle_terminal_status
persistent_paper_trade_lifecycle_entry_touch_status
persistent_paper_trade_lifecycle_invalidation_touch_status
persistent_paper_trade_lifecycle_destination_touch_status
persistent_paper_trade_lifecycle_execution_status
persistent_paper_trade_lifecycle_notes
```

## Snapshot aggregate fields

The snapshot now stores:

```text
persistent_paper_trade_lifecycle_row_count
persistent_paper_trade_lifecycle_status
persistent_paper_trade_lifecycle_key
persistent_paper_trade_lifecycle_total_rows
persistent_paper_trade_lifecycle_pending_entry_rows
persistent_paper_trade_lifecycle_open_rows
persistent_paper_trade_lifecycle_destination_rows
persistent_paper_trade_lifecycle_invalidation_rows
persistent_paper_trade_lifecycle_ambiguous_rows
persistent_paper_trade_lifecycle_blocked_rows
persistent_paper_trade_lifecycle_distribution
persistent_paper_trade_lifecycle_execution_status
persistent_paper_trade_lifecycle_notes
```

## Lifecycle states

Phase 25 can classify persistent paper trades as:

```text
PAPER_TRADE_LIFECYCLE_PENDING_ENTRY_NO_EXECUTION
PAPER_TRADE_LIFECYCLE_OPEN_NO_EXECUTION
PAPER_TRADE_LIFECYCLE_HIT_DESTINATION_NO_EXECUTION
PAPER_TRADE_LIFECYCLE_HIT_INVALIDATION_NO_EXECUTION
PAPER_TRADE_LIFECYCLE_AMBIGUOUS_CLOSE_ONLY_NO_EXECUTION
PAPER_TRADE_LIFECYCLE_BLOCKED_NO_EXECUTION
PAPER_TRADE_LIFECYCLE_UNKNOWN_NO_EXECUTION
```

## Terminal states

```text
PAPER_TRADE_TERMINAL_PENDING_ENTRY
PAPER_TRADE_TERMINAL_OPEN
PAPER_TRADE_TERMINAL_HIT_DESTINATION
PAPER_TRADE_TERMINAL_HIT_INVALIDATION
PAPER_TRADE_TERMINAL_AMBIGUOUS
PAPER_TRADE_TERMINAL_BLOCKED
PAPER_TRADE_TERMINAL_UNKNOWN
```

## Path states

```text
PAPER_TRADE_PATH_BLOCKED_NOT_REGISTERED
PAPER_TRADE_PATH_BLOCKED_NO_ENTRY_PRICE
PAPER_TRADE_PATH_PENDING_ENTRY
PAPER_TRADE_PATH_OPEN_AFTER_ENTRY_CLOSE_ONLY
PAPER_TRADE_PATH_HIT_DESTINATION_CLOSE_ONLY
PAPER_TRADE_PATH_HIT_INVALIDATION_CLOSE_ONLY
PAPER_TRADE_PATH_AMBIGUOUS_DESTINATION_AND_INVALIDATION_SAME_CLOSE
```

## Evaluation method

Phase 25 remains close-only:

```text
latest closed candle close
```

It does not use intrabar high/low yet.

For BUY-like paper trade directions:

```text
entry/invalidation touch: close <= anchor
destination touch:        close >= anchor
```

For SELL-like paper trade directions:

```text
entry/invalidation touch: close >= anchor
destination touch:        close <= anchor
```

## R-equivalent

When a non-zero invalidation distance exists, the engine computes:

```text
risk = abs(entry_price - invalidation_price)
R    = signed_delta / risk
```

If invalidation distance is unavailable, R stays pending.

## Execution safety

Every Phase 25 row keeps:

```text
execution_status = REAL_EXECUTION_DISABLED_PHASE25_PAPER_TRADE_LIFECYCLE_ONLY
```

No order is opened, modified, deleted, closed, or sent.

## Locked boundaries

Phase 25 does not modify:

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

It only reads persistent paper trade rows and writes paper lifecycle diagnostics.

## Next natural phase

The next phase can be:

```text
Phase 26 — Paper Performance Report
```

That phase should aggregate closed/open paper lifecycle rows into performance metrics such as win rate, expectancy, average R, distribution, and drawdown-equivalent, still without enabling real execution.
