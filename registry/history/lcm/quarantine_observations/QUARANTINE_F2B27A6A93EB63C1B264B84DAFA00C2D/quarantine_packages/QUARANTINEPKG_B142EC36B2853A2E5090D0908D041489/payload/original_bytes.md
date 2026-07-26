# Level 10 — Paper Partial Close Simulator and W4 Management

## Scope

Level 10 adds the first paper position-management layer after the Level 09 paper outcome simulator.
It does not place real orders, does not modify broker positions, and does not perform hard-close accounting yet.
Its only new responsibility is to decide what would happen at the end of W4 for open paper trades.

The locked STC rule is:

- If Partial is OFF, no partial action is taken.
- If Partial is ON, at the end of W4 of the same M, every trade opened in that M is checked.
- If the trade has already reached TP, SL, or an ambiguous SL/TP state before or at the W4 checkpoint, no partial action is taken.
- If the trade is still open at the W4 checkpoint, about 50% of the volume is closed.
- The 50% close volume is rounded upward to the broker volume step.
- If rounding consumes the whole position, the paper action is a full close by small volume.
- M3 partial is disabled because the M3 W4 endpoint is also the 15:30 New York hard-close boundary.
- If the EA was offline at the exact W4 endpoint, the partial is still recovered later from the current-day history and journal process.

## Inputs added

- `InpWritePartialAudit`
- `InpMaxPartialBackfillOnInit`
- `InpMaxPartialCatchupPerPulse`

These are audit controls only. They do not change strategy logic.

## New output

`stc_level10_partial_actions.csv`

This journal records one row per processed paper signal/check. The important fields are:

- `partial_status`
- `paper_status`
- `pre_partial_outcome_status`
- `partial_due_check_index`
- `partial_due_ny`
- `partial_due_server`
- `paper_order_volume`
- `broker_volume_step`
- `close_volume`
- `remaining_volume`
- `close_volume_ratio`
- `floating_r_at_partial`
- `status`
- `rule_note`

## Algorithm

1. Rebuild the same deterministic paper entry that Level 08 created.
2. Identify the M cycle of the paper signal.
3. Determine the W4 endpoint of that M.
4. Convert the W4 endpoint into the final check-candle index of that M.
5. If the final W4 checkpoint has not closed yet, the partial action is not due.
6. If the M is M3, record `SKIPPED_M3_HARD_CLOSE` because hard close owns the 15:30 boundary.
7. Simulate Level 09 outcome from entry until the W4 checkpoint only.
8. If the trade is no longer open by the W4 checkpoint, record `NOT_OPEN_AT_W4_END`.
9. If the trade is still open, calculate the partial close volume:
   - raw half volume = paper volume × 0.50
   - close volume = ceil(raw half volume / broker step) × broker step
10. If close volume is equal to or greater than the full paper volume, record `FULL_CLOSE_BY_SMALL_VOLUME`.
11. Otherwise, record `PARTIAL_CLOSE` and the remaining volume.

## Examples

If paper volume is `1.01` and broker step is `0.01`:

- raw half = `0.505`
- rounded upward = `0.51`
- remaining = `0.50`

If paper volume is `0.01` and broker step is `0.01`:

- raw half = `0.005`
- rounded upward = `0.01`
- remaining = `0.00`
- status = `FULL_CLOSE_BY_SMALL_VOLUME`

## What is still deferred

- Hard-close accounting at 15:30 New York.
- Delayed hard-close recovery.
- Persistent journal reload after restart.
- Chart visualization.
- Real broker order partial close.
- Real broker hard close.
