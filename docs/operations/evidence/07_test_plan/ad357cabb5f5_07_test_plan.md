# 07 - Test Plan

## 1. Purpose

The test plan ensures the STC SMT Cycles implementation follows the locked specification before any live trading.

Every test should be deterministic and should write expected vs actual values to a report.

## 2. Time and cycle tests

Test M assignment:

- 20:00 is M1.
- 01:59 is M1.
- 02:00 is gap.
- 02:59 is gap.
- 03:00 is M2.
- 08:59 is M2.
- 09:00 is gap.
- 09:29 is gap.
- 09:30 is M3.
- 15:29 is M3.
- 15:30 is hard close/reset.

Test W assignment for every W in M1, M2, and M3.

Test DST transition dates using New York time.

## 3. Check candle anchoring tests

For each check timeframe, verify aggregation starts at 20:00 New York.

Examples:

- 10m: 20:00-20:10.
- 10m: 21:20-21:30.
- 15m: 20:00-20:15.
- 3m: 20:00-20:03.

Verify that final check candles ending at M boundaries cannot enter.

## 4. W level tests

Build synthetic M1 data and verify W high/low:

- W high equals maximum high inside the W.
- W low equals minimum low inside the W.
- W completeness fails if either symbol is missing required data.
- W1 produces no signals.

## 5. Reference matrix tests

In W2, verify only W1 is eligible.

In W3, verify W2 and W1 are eligible.

In W4, verify W3, W2, and W1 are eligible.

Verify no current W self-reference.

Verify no cross-M reference.

Verify no previous STC day reference.

## 6. Hunt tests

High hunt:

- high above reference high => hunt.
- high equal to reference high => hunt.
- high below reference high => no hunt.

Low hunt:

- low below reference low => hunt.
- low equal to reference low => hunt.
- low above reference low => no hunt.

Verify no tolerance is applied.

## 7. SMT divergence tests

Case A: Symbol1 hunts high, Symbol2 does not.

- Expected: sell setup on Symbol2.

Case B: Symbol2 hunts high, Symbol1 does not.

- Expected: sell setup on Symbol1.

Case C: Symbol1 hunts low, Symbol2 does not.

- Expected: buy setup on Symbol2.

Case D: Symbol2 hunts low, Symbol1 does not.

- Expected: buy setup on Symbol1.

Case E: both hunt.

- Expected: no SMT.

Case F: neither hunts.

- Expected: no SMT.

## 8. Confirmation tests

Candidate forms inside a check candle and remains valid at close.

- Expected: confirmed.

Candidate forms but clean symbol hunts before close.

- Expected: invalidated, no entry.

Candidate confirms on final check candle ending at M boundary.

- Expected: expired, no entry.

Candidate confirms while Entry STC is OFF.

- Expected: audit-only, consumed, no delayed entry.

EA offline at exact entry time and restarted later.

- Expected: no delayed entry.

## 9. Reference selection tests

Create multiple valid references for the same side and clean symbol.

Verify selected reference is the one producing largest stop distance on the clean traded symbol.

Verify SL uses the selected reference of the traded symbol, not the hunted symbol.

## 10. Ambiguity tests

Buy and sell confirm in the same check candle.

- Expected: no trade, event discarded, no retry.

Same-direction multiple signals confirm.

- Expected: deterministic selection, max three trades per M, no duplicate same-symbol same-side trade in same check candle.

Same check candle after entry hits both SL and TP.

- Expected: trade outcome `AMBIGUOUS`.

## 11. Risk tests

Verify Final Reward 10 creates 10R TP.

Verify tick value is used when available.

Verify Contract Size fallback is used when tick value is unavailable.

Verify calculated theoretical volume.

Verify volume splitting when calculated volume is above broker maximum.

Verify skip when calculated volume is below broker minimum.

## 12. Hedging tests

Hedging OFF:

- First M trade buy locks M direction to buy.
- Sell signals inside same M are rejected.
- Next M can open sell.

Hedging ON:

- Buy and sell may occur in same M if not in same check candle.
- Max three trades per M still applies.
- Same-check-candle buy/sell ambiguity still creates no trade.

## 13. Partial tests

M1 trade remains open at 02:00.

- Expected: partial closes approximately 50%, rounded up.

M2 trade remains open at 09:00.

- Expected: partial closes approximately 50%, rounded up.

M3 trade remains open at 15:30.

- Expected: hard close, no partial.

Missed partial due to EA downtime.

- Expected: partial executes after restart if position still open and not previously partialed.

## 14. Hard close tests

At 15:30 New York, all magic-number STC positions close.

If close fails, retry every configured seconds.

If EA restarts after 15:30 with an old magic-number position still open, close at first opportunity.

Manual or other-magic positions are ignored.

## 15. Restart tests

Restart inside same STC day.

- Rebuild cycle state from current-day candles.
- Load consumed-signal journal.
- Detect open magic-number positions.
- Do not duplicate prior entries.
- Do delayed partial if due.
- Do delayed hard close if due.
- Do not enter missed signals.

## 16. Duplicate instance tests

Attach EA twice for same strategy ID and symbol pair.

- Expected: second instance blocked or passive.

Attach EA to a different symbol chart but same Symbol1/Symbol2 inputs.

- Expected: duplicate lock still applies.

## 17. Reporting tests

Verify creation of:

- Cycle audit file.
- Divergence audit file.
- Trade journal.
- Position management journal.
- Runtime summary.

Verify all rejected/no-trade reasons are explicitly reported.
