# 12 - State Machines

## 1. Strategy day state

States:

- `BEFORE_STC_DAY`
- `ACTIVE_DAY`
- `HARD_CLOSE_DUE`
- `HARD_CLOSE_RECOVERY`
- `DAY_RESET_DONE`

Transitions:

- At 20:00 New York, enter `ACTIVE_DAY`.
- At 15:30 New York, enter `HARD_CLOSE_DUE`.
- If all STC positions close successfully, enter `DAY_RESET_DONE`.
- If any close fails or EA restarts after 15:30 with open STC positions, enter `HARD_CLOSE_RECOVERY`.
- After successful recovery, reset state for next day.

## 2. M state

States:

- `NOT_STARTED`
- `ACTIVE`
- `GAP_AFTER_M`
- `ENDED`

M state carries:

- M ID.
- Trade count.
- Direction lock.
- Opened trade IDs.
- Partial due time.

On M start:

- Trade count = 0.
- Direction lock = none.

On first opened trade when Hedging OFF:

- Direction lock = trade side.

On M end:

- No more entries allowed.
- Partial may become due for M1/M2.
- M3 hands control to hard close.

## 3. W state

States:

- `BUILDING`
- `COMPLETED`
- `REFERENCE_ELIGIBLE`
- `CURRENT_W`

W1 never signals.

W2/W3/W4 can be current W for candidate detection.

A completed W can be a reference if it is inside the same M and allowed by the reference matrix.

## 4. Candidate state

States:

- `FORMED`
- `WAITING_CHECK_CLOSE`
- `INVALIDATED_BEFORE_CLOSE`
- `CONFIRMED`
- `DISCARDED_AMBIGUOUS`
- `EXPIRED_FINAL_CHECK`
- `CONSUMED_AUDIT_ONLY`
- `CONSUMED_ORDER_FAILED`
- `ENTERED`

Transitions:

- Candidate forms when exactly one symbol hunts.
- Candidate waits until check candle closes.
- Candidate invalidates if clean symbol hunts before close.
- Candidate expires if confirmation happens on final check candle of M.
- Candidate discards if buy and sell confirm in same check candle.
- Candidate becomes audit-only if Entry STC OFF.
- Candidate becomes entered if order succeeds.
- Candidate is consumed if order fails.

## 5. Trade state

States:

- `PLANNED`
- `ORDER_SENT`
- `OPEN`
- `PARTIAL_DONE`
- `TP_HIT`
- `SL_HIT`
- `AMBIGUOUS_SL_TP`
- `HARD_CLOSED`
- `ORDER_FAILED`
- `CLOSED_MANUALLY_OR_EXTERNAL`

Transitions:

- Confirmed signal creates `PLANNED` trade.
- Execution sends order.
- Successful order moves to `OPEN`.
- TP hit moves to `TP_HIT`.
- SL hit moves to `SL_HIT`.
- Both hit in same check candle moves to `AMBIGUOUS_SL_TP`.
- Partial close marks `PARTIAL_DONE` but trade can remain open.
- Hard close moves to `HARD_CLOSED`.

## 6. Partial state

States:

- `NOT_DUE`
- `DUE`
- `DONE`
- `MISSED_DUE_TO_DOWNTIME`
- `RECOVERED`
- `NOT_APPLICABLE`

Rules:

- M1 and M2 trades become partial-eligible at W4 end.
- M3 trades are `NOT_APPLICABLE` for partial because hard close dominates.
- A missed partial is performed later if the position remains open and has not been partialed.

## 7. Hard-close state

States:

- `NOT_DUE`
- `DUE`
- `CLOSE_SENT`
- `RETRY_WAIT`
- `COMPLETE`

Rules:

- Hard close is due at 15:30 New York.
- It applies only to this strategy magic number.
- It retries every configured seconds until complete.
- Entry STC OFF does not disable hard close.
