# Level 18 — Real Hard Close Finalizer

## Purpose

Level 18 turns the 15:30 New York hard-close rule into a dedicated real broker finalizer.
It does not change the STC signal logic, SMT detection, reference selection, paper simulator, real auto-entry router, or real partial close manager.
Its only job is to make sure that, after the STC trading day ends, no remaining real broker position owned by this strategy instance is left open.

The finalizer is magic-only. It manages only positions whose symbol is Symbol1 or Symbol2 and whose magic number equals the configured STC magic number.
Manual positions, foreign-magic positions, and non-pair symbols are never closed by this module.

## Locked Strategy Rule Covered

The STC SRS requires all open STC trades to be closed at 15:30 New York, without exception. The owner clarified that if the hard close was missed because the EA was offline, the hard close must be performed at the first later opportunity.

Level 18 implements that as a retrying broker-side finalizer.

## Safety Defaults

Real hard close finalization is disabled by default.

The finalizer can only send real close requests when the following gates are satisfied:

- `InpEnableBrokerPositionManager = true`
- `InpEnableRealHardCloseFinalizer = true`
- runtime mode is `STC_MODE_AUTO_TRADE`
- or runtime mode is `STC_MODE_PAPER_LIVE` and `InpAllowRealHardCloseFinalizerInPaperLive = true`
- New York time is at or after 15:30 for the current STC trading day
- the position is on Symbol1 or Symbol2
- the position magic number matches `InpMagicNumber`
- the per-position attempt cap has not been reached

## Position Eligibility

A position is eligible for the real hard close finalizer only if all of these are true:

- `POSITION_SYMBOL == Symbol1 || POSITION_SYMBOL == Symbol2`
- `POSITION_MAGIC == InpMagicNumber`
- `snap.hard_close_due == true`
- transport is explicitly enabled

The module never closes:

- manual positions
- positions with a different magic number
- positions on unrelated symbols
- foreign pair-symbol positions

Foreign pair-symbol positions are audit-only when `InpAuditForeignPairPositions = true`.

## Retry Model

Level 18 is intentionally more aggressive than the earlier Level 15 safety close layer.

The finalizer scans on `InpRealHardCloseFinalizerScanSeconds`.
If hard close is due, it attempts close retries on `InpRealHardCloseFinalizerRetrySeconds`.

Each position identifier gets a persistent attempt counter under Common Files:

`dal/stc/EXEC001_STC_SMT_Cycles/real_hard_close_attempts/<stc_day_id>/attempts_<position_identifier>.marker`

The counter prevents infinite silent looping. The cap is controlled by:

`InpRealHardCloseFinalizerMaxAttemptsPerPosition`

If the cap is reached, the module stops sending close requests for that position and writes an explicit manual-review audit row.

## Verification After Close Attempt

After sending a close request, the module immediately checks whether the same ticket is still visible and still belongs to this strategy.

Possible outcomes:

- `REAL_HARD_CLOSE_CONFIRMED_CLOSED`
- `REAL_HARD_CLOSE_SENT_BUT_POSITION_STILL_OPEN`
- `REAL_HARD_CLOSE_FAILED`
- `BLOCKED_TRANSPORT_DISABLED`
- `BLOCKED_MAX_ATTEMPTS_REACHED`
- `SKIPPED_NOT_MANAGED_MAGIC_POSITION`
- `NO_REMAINING_MANAGED_POSITIONS`

If a position remains visible after a seemingly successful trade API call, the finalizer will retry on the next due scan.

## Audit Output

The module writes:

`stc_level18_real_hard_close_finalizer.csv`

The file includes:

- STC day id
- runtime mode
- ticket
- position identifier
- symbol
- magic
- position type
- open time
- open time in New York
- volume
- open price
- current price
- SL
- TP
- floating profit
- hard close due flag
- transport allowed flag
- action allowed flag
- action attempted flag
- action success flag
- attempt count before
- attempt count after
- max attempts
- deviation
- trade result retcode
- trade result comment
- whether the position remained after attempt
- remaining managed positions after scan
- status
- rule note

## Relationship to Prior Layers

Level 15 introduced safe broker position scanning and optional hard close.
Level 17 introduced real partial close at W4 for M1 and M2.
Level 18 is the final end-of-day authority.

Partial close never has priority over hard close after 15:30. If a position remains after 15:30, the hard close finalizer owns it.

## What Level 18 Still Does Not Do

Level 18 does not add a new signal.
Level 18 does not alter SMT detection.
Level 18 does not alter paper results.
Level 18 does not alter real entry sizing.
Level 18 does not close foreign positions.
Level 18 does not manage manual trades.

## Acceptance Criteria

The level is accepted when:

1. The EA compiles.
2. The new real hard-close finalizer inputs appear in the EA input panel.
3. In default settings, no real close request is sent.
4. After 15:30 New York, matching magic-number positions are audited.
5. With the finalizer explicitly enabled in AUTO_TRADE mode, eligible positions receive real close attempts.
6. Foreign/manual positions are audited but never closed.
7. Retry rows are written until no managed positions remain or the per-position attempt cap is reached.
8. Restarting the EA does not reset the per-position attempt counter for the same STC day.
