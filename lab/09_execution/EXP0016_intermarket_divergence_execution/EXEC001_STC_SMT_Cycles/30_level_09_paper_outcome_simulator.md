# Level 09 — Paper Outcome Simulator and Trade Journal

Level 09 extends EXEC001 STC SMT Cycles from a no-order paper-entry planner into an audit-only paper outcome simulator.

This level still does not send real orders, does not manage real positions, does not execute partial closes, does not execute hard closes, and does not draw chart objects. Its purpose is to transform Level 08 paper-entry plans into deterministic paper trade outcomes using the closed check-candle stream.

## Scope

Level 09 adds:

1. a paper outcome module,
2. a new paper outcome CSV journal,
3. SL/TP path scanning after each paper entry,
4. AMBIGUOUS classification when SL and TP are both touched in the same check candle,
5. gross and net reporting fields,
6. open-unresolved reporting when no exit is known yet,
7. dedicated outcome counters so outcome simulation does not mutate the Level 08 paper-entry journal counters.

## Locked strategy rules implemented in this level

The implementation follows the locked owner decisions:

- the paper entry price is the open of the next check candle after confirmation;
- SL is the selected reference W price on the traded clean symbol;
- TP is derived from Final Reward R and raw price risk distance;
- costs do not change TP or SL;
- spread and commission are reporting fields only;
- if both SL and TP are touched in the same check candle, the outcome is AMBIGUOUS;
- no fake intrabar ordering is invented;
- both-symbol data completeness is still required;
- no real orders are sent;
- partial close and hard-close accounting are deferred to later levels.

## Outcome algorithm

For each signal check index that could already have an entry open:

1. Rebuild the same SMT candidate logic from the previous levels.
2. Rebuild the same signal and paper-entry plan using an isolated outcome counter state.
3. If multiple same-direction candidates are valid for different clean symbols, simulate one paper outcome row for each planned paper entry, while still respecting max-three-per-M and the M direction lock.
4. If the paper entry is not planned, write a no-outcome row.
5. If the paper entry is planned, scan closed check candles from the entry check onward.
6. For BUY:
   - TP is hit when check high is greater than or equal to TP.
   - SL is hit when check low is less than or equal to SL.
7. For SELL:
   - TP is hit when check low is less than or equal to TP.
   - SL is hit when check high is greater than or equal to SL.
8. If both are hit in the same check candle, classify the trade as AMBIGUOUS.
9. If only TP is hit, classify as TP_HIT.
10. If only SL is hit, classify as SL_HIT.
11. If no closed check candle resolves the trade yet, classify as OPEN_UNRESOLVED.

## Why AMBIGUOUS exists

The strategy is checked on synthetic check candles. Without a lower-timeframe path inside that check candle, the engine cannot know whether SL or TP was touched first when both are inside the same candle range.

The owner decision was not to force an artificial path. Therefore Level 09 records the outcome as AMBIGUOUS and leaves it available for later research filtering.

## Output file

The new file is:

```text
Common Files/dal/stc/EXEC001_STC_SMT_Cycles/stc_level09_paper_outcomes.csv
```

Main fields:

- signal_check_index
- entry_check_index
- exit_check_index
- last_checked_index
- outcome_status
- paper_status
- signal_id
- paper_trade_id
- direction
- trade_symbol
- entry_price
- stop_price
- take_profit_price
- exit_price
- last_checked_close
- risk_distance_price
- reward_distance_price
- final_reward_r
- paper_order_volume
- risk_money
- gross_pnl_money
- estimated_cost_money
- net_pnl_money
- realized_r_gross
- realized_r_net
- floating_r_at_last_check
- status
- rule_note

## Outcome statuses

### TP_HIT

The paper trade reached final TP first according to the closed check-candle stream.

### SL_HIT

The paper trade reached SL first according to the closed check-candle stream.

### AMBIGUOUS_SL_TP_SAME_CHECK

Both SL and TP were touched inside the same check candle. The engine does not guess the order.

### OPEN_UNRESOLVED

The trade is still open according to available closed check candles.

### NO_PAPER_ENTRY

No paper entry existed for that signal check.

### REJECTED_DATA_INCOMPLETE

Outcome scanning stopped because the pair data was incomplete.

## Cost reporting

The raw TP and SL geometry is not changed by costs.

Costs are estimated only for net reporting:

- spread is read from the check candle / broker fields when available;
- fallback spread is used when broker-derived spread is not available;
- commission per lot is recorded from the fallback reporting input;
- gross R is based only on price geometry;
- net R subtracts the estimated cost from gross PnL.

## Non-scope

Level 09 does not yet implement:

- partial close at W4 end;
- delayed partial recovery;
- hard close at 15:30 New York;
- delayed hard-close recovery;
- real position management;
- restart persistence from existing journals;
- chart visualization;
- auto trading.

Those are intentionally left for later levels.

## Acceptance criteria

Level 09 is accepted when:

1. the EA compiles;
2. all previous level CSVs still write;
3. `stc_level09_paper_outcomes.csv` is created;
4. planned paper entries produce outcome rows;
5. BUY TP/SL logic uses high/low correctly;
6. SELL TP/SL logic uses high/low correctly;
7. same-check SL+TP becomes AMBIGUOUS;
8. unresolved trades remain OPEN_UNRESOLVED;
9. no real order is sent.
