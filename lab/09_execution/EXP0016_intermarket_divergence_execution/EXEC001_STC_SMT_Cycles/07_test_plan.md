# 07 - STC SMT Cycles Test Plan

## 1. Test philosophy

Do not trust aggregate backtest metrics until every rule has deterministic scenario tests.

The first test target is not profitability. It is logic correctness.

## 2. Time and cycle tests

### T001 - STC day boundary

Expected:

- New STC day starts at New York 20:00.
- End-of-day reset fires exactly at New York 15:30.

### T002 - M cycle detection

Expected active cycles:

| NY time | Expected |
| --- | --- |
| 20:30 | M1.W1 |
| 22:00 | M1.W2 |
| 23:30 | M1.W3 |
| 01:00 | M1.W4 |
| 03:30 | M2.W1 |
| 08:00 | M2.W4 |
| 10:00 | M3.W1 |
| 15:00 | M3.W4 |

### T003 - Gap handling

Times:

- 02:30.
- 09:15.

Expected behavior must match final spec decision.

## 3. W level tests

### T010 - W high/low construction

Given known bars inside each W:

- W high equals maximum high.
- W low equals minimum low.
- End time is exclusive.

### T011 - No previous-day leakage

After 15:30 reset:

- no W levels from the previous STC day remain usable.

## 4. SMT divergence tests

### T020 - Bullish SMT: Symbol1 hunts low only

Scenario:

- Symbol1 touches reference W low.
- Symbol2 does not touch reference W low.

Expected:

- bullish pending divergence;
- hunted symbol = Symbol1;
- clean symbol = Symbol2;
- intended trade = BUY Symbol2.

### T021 - Bullish SMT: Symbol2 hunts low only

Expected:

- intended trade = BUY Symbol1.

### T022 - Bearish SMT: Symbol1 hunts high only

Expected:

- intended trade = SELL Symbol2.

### T023 - Bearish SMT: Symbol2 hunts high only

Expected:

- intended trade = SELL Symbol1.

### T024 - Both symbols hunt same side before check close

Expected:

- pending divergence cancels;
- no entry.

### T025 - Neither symbol hunts

Expected:

- no divergence.

### T026 - Buy and sell divergence confirm simultaneously

Expected:

- no trade.

## 5. Confirmation tests

### T030 - Divergence still valid at check close

Expected:

- entry intent created immediately after check candle close.

### T031 - Divergence disappears before check close

Expected:

- no entry.

### T032 - Same divergence persists across later candles

Expected:

- only one entry.

## 6. M trade-limit tests

### T040 - Max 3 trades per M

Expected:

- trades 1, 2, 3 are allowed if rules pass;
- trade 4 is skipped.

### T041 - Hedging OFF direction lock

Expected:

- first M trade locks direction;
- opposite direction skipped;
- same direction allowed until max 3.

### T042 - Hedging ON

Expected:

- buy and sell both allowed;
- still max 3 per M.

## 7. Risk tests

### T050 - Stop-loss reference

Expected:

- BUY SL = selected reference W low.
- SELL SL = selected reference W high.
- no buffer.

### T051 - Closest W reference

If multiple references eligible:

- choose closest by time.

### T052 - Position sizing

Expected:

- volume follows risk percent, equity, contract size, and stop distance.
- no hard volume cap.

### T053 - Take-profit

Expected:

- TP calculated from Final Reward.
- TP not modified after entry.

## 8. Partial and reset tests

### T060 - Partial OFF

Expected:

- no partial close.

### T061 - Partial ON, not hit TP by W4 end

Expected:

- approximately 50% closed.
- trade marked partial-done.

### T062 - Volume 1.01

Expected:

- close 0.51.

### T063 - Volume 0.01

Expected:

- close full trade.

### T064 - End-of-day 15:30

Expected:

- all open trades closed;
- all state reset.

## 9. Regression tests before live

Before live trading is enabled:

- Run scenario tests.
- Run at least one full week on historical data with audit logs.
- Manually inspect every divergence/trade for one day.
- Verify no repeated entries for the same divergence.
- Verify no state leakage across 15:30 reset.
- Verify DST transition days.

