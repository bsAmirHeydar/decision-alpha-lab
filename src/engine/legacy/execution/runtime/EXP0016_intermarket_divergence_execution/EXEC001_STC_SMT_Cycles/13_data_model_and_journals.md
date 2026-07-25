# 13 - Data Model and Journals

## 1. Goals

The strategy must be restart-safe, auditable, and testable.

Every important decision should produce a record. The engine should be able to answer why it entered, why it skipped, why it rejected, and how it calculated SL/TP/volume.

## 2. Core records

### STC day record

Fields:

- `stc_day_id`
- `ny_start_time`
- `ny_end_time`
- `hard_close_time`
- `symbol1`
- `symbol2`
- `broker_utc_offset`
- `check_candle_tf`
- `entry_stc_enabled`
- `partial_enabled`
- `hedging_enabled`

### M cycle record

Fields:

- `stc_day_id`
- `m_id`
- `start_time_ny`
- `end_time_ny`
- `trade_count`
- `direction_lock`
- `partial_due_time`
- `status`

### W cycle record

Fields:

- `stc_day_id`
- `m_id`
- `w_id`
- `symbol`
- `start_time_ny`
- `end_time_ny`
- `open`
- `high`
- `low`
- `close`
- `data_complete`
- `missing_bar_count`

### Check candle record

Fields:

- `stc_day_id`
- `check_close_time_ny`
- `check_start_time_ny`
- `check_tf`
- `m_id`
- `w_id`
- `is_final_check_candle_of_m`
- `symbol1_ohlc`
- `symbol2_ohlc`
- `data_complete`

### SMT candidate record

Fields:

- `candidate_id`
- `stc_day_id`
- `m_id`
- `current_w_id`
- `check_close_time_ny`
- `side`
- `reference_side`
- `hunted_symbol`
- `clean_symbol`
- `trade_symbol`
- `selected_reference_w`
- `selected_reference_price`
- `selection_reason`
- `symbol1_hunted`
- `symbol2_hunted`
- `candidate_status`
- `reject_reason`

### Trade intent record

Fields:

- `intent_id`
- `candidate_id`
- `entry_mode`
- `planned_entry_time`
- `planned_entry_price`
- `sl_price`
- `tp_price`
- `risk_points`
- `final_reward_r`
- `risk_percent`
- `risk_money`
- `theoretical_volume`
- `broker_volume`
- `order_split_count`
- `intent_status`

### Trade journal record

Fields:

- `trade_id`
- `intent_id`
- `ticket`
- `symbol`
- `side`
- `entry_time`
- `entry_price`
- `sl_price`
- `tp_price`
- `volume`
- `partial_done`
- `partial_time`
- `exit_time`
- `exit_price`
- `exit_reason`
- `gross_r`
- `gross_money`
- `net_money`
- `commission`
- `spread_cost`
- `slippage_cost`

## 3. CSV outputs

### `stc_cycle_audit.csv`

One row per symbol per W.

Purpose: prove that M/W construction is correct.

### `stc_check_candles.csv`

One row per check candle.

Purpose: prove check-candle anchoring, final-candle rule, and data completeness.

### `stc_smt_candidates.csv`

One row per candidate/reference evaluation.

Purpose: prove why SMT existed or did not exist.

### `stc_signals.csv`

One row per confirmed/discarded/consumed signal.

Purpose: track tradable signal lifecycle.

### `stc_trades.csv`

One row per opened or planned trade.

Purpose: track execution, risk, volume, exits, partial, and outcomes.

### `stc_position_actions.csv`

One row per partial, close, failed close, retry, or recovery action.

Purpose: audit position management.

### `stc_daily_summary.csv`

One row per STC trading day.

Purpose: high-level performance and behavior summary.

## 4. Persistent state files

The EA should persist:

- Consumed signal IDs.
- Open trade IDs created by this strategy.
- Partial flags by ticket/trade ID.
- M trade counters.
- Direction lock by M.
- Last completed check candle time.
- Hard-close recovery status.

## 5. Restart reconstruction

On restart:

1. Determine current STC day.
2. Load current-day persistent state files.
3. Rebuild W levels from current-day candles.
4. Rebuild check-candle context.
5. Read magic-number positions from account.
6. Link positions to trade journal records when possible.
7. Do not enter missed signals.
8. Do delayed partial if due.
9. Do hard-close recovery if due.

## 6. Event IDs

Use stable deterministic IDs.

Candidate ID should include:

- strategy_id
- stc_day_id
- m_id
- current_w_id
- check_close_time
- side
- hunted_symbol
- clean_symbol
- selected_reference_w

Trade ID should include candidate ID plus entry attempt index or broker ticket.

## 7. Rejection reasons

Recommended rejection reason enum:

- `W1_NO_SIGNAL`
- `GAP_NO_ENTRY`
- `FINAL_CHECK_CANDLE_NO_ENTRY`
- `DATA_INCOMPLETE`
- `NO_SMT_BOTH_HUNTED`
- `NO_SMT_NEITHER_HUNTED`
- `CLEAN_SYMBOL_HUNTED_BEFORE_CLOSE`
- `AMBIGUOUS_BUY_SELL_DISCARDED`
- `ENTRY_STC_OFF_AUDIT_ONLY`
- `DUPLICATE_SIGNAL_CONSUMED`
- `M_TRADE_LIMIT_REACHED`
- `DIRECTION_LOCK_REJECTED`
- `VOLUME_BELOW_BROKER_MIN`
- `ORDER_FAILED_SIGNAL_CONSUMED`
- `EA_OFFLINE_AT_ENTRY_NO_DELAYED_ENTRY`
