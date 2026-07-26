# Level 11 — Paper Hard-Close Simulator and 15:30 End-of-Day Accounting

## Purpose

Level 11 adds the paper hard-close accounting layer for EXEC001 STC SMT Cycles. It does not place real broker orders and it does not close real positions. Its only purpose is to answer the question: for every paper trade that survived the earlier paper outcome and partial layers, what exactly remains open at 15:30 New York, and what paper action would the strategy take?

This level implements the locked owner rule that no STC trade may remain open after 15:30 New York. In the research/paper layer, this means that any paper volume still open at the 15:30 check-candle close is force-closed at the traded symbol's check-candle close price.

## Scope

Level 11 includes:

- 15:30 New York hard-close checkpoint detection.
- Delayed hard-close recovery if the EA was not running exactly at 15:30.
- Full-volume paper hard close when no partial happened.
- Remaining-volume paper hard close when W4 partial already reduced the position.
- No hard close if TP, SL, or ambiguous outcome occurred before 15:30.
- No hard close if the W4 partial fully consumed a tiny-volume paper trade.
- Dedicated hard-close audit CSV.

Level 11 intentionally excludes:

- Real broker position closing.
- Retry loops for live orders.
- Persistent journal reload.
- Chart drawing.
- Auto trade execution.

Those belong to later implementation levels.

## Locked rules implemented

The hard close time is exactly 15:30 New York, using the same New York/DST engine already built in Level 02. The relevant STC day is the day that started at 20:00 New York. Therefore, data before that STC day start is not used for signal decisions.

Hard close has priority over M3 partial. M3 W4 ends at 15:30, so M3 partial is disabled and the end-of-day close handles all remaining M3 paper volume.

For M1 and M2 trades, Level 11 first re-evaluates the Level 10 partial logic. If partial closed about 50% at the W4 end, Level 11 closes only the remaining paper volume at 15:30. If partial fully closed a small position, Level 11 records that no hard-close remainder exists.

If the EA was offline at 15:30 but restarted later before the next STC day begins, the hard-close simulator reconstructs the current STC day from candles and writes delayed hard-close audit rows.

## Algorithm

For each signal check that could have produced a valid paper entry before 15:30:

1. Rebuild the SMT candidate using the existing Level 06 logic.
2. Rebuild the Level 07 signal registry result.
3. Rebuild the Level 08 paper entry plan.
4. If no paper entry exists, write a no-paper-entry hard-close row.
5. Locate the hard-close check index, which is the check candle ending exactly at 15:30 New York.
6. If that check candle is not closed yet, do nothing.
7. Simulate the Level 09 outcome from entry through the 15:30 check candle.
8. If TP, SL, ambiguous outcome, rejection, or incomplete data occurred first, write no hard-close action.
9. If the trade is still open at 15:30, rebuild the Level 10 partial decision.
10. If partial fully closed the paper trade, write no hard-close remainder.
11. If partial partially closed it, force-close the remaining paper volume.
12. If no partial applies, force-close the full paper volume.
13. Use the traded symbol close of the 15:30 check candle as the paper hard-close price.
14. Record floating R and estimated paper PnL for the hard-close volume only.

## Output

Level 11 writes:

`stc_level11_hard_close_actions.csv`

Important columns:

- `hard_close_status`
- `pre_hard_outcome_status`
- `partial_status`
- `hard_close_due`
- `hard_close_recovered_late`
- `open_at_hard_close`
- `partial_applied_before_hard_close`
- `partial_full_close_before_hard_close`
- `hard_close_volume`
- `hard_close_price`
- `floating_r_at_hard_close`
- `hard_close_gross_pnl_money`
- `hard_close_net_pnl_money`

## Acceptance criteria

Level 11 is acceptable when:

- It compiles with all previous levels.
- It creates `stc_level11_hard_close_actions.csv` in Common Files.
- No real orders are placed.
- The hard close audit stays empty before the 15:30 check candle is closed.
- After 15:30, eligible paper trades produce hard-close audit rows.
- M1/M2 trades with partial close produce remaining-volume rows.
- M3 trades do not partial and close in full if still open at 15:30.
- Trades already resolved by TP, SL, or ambiguity do not receive forced hard-close rows.
