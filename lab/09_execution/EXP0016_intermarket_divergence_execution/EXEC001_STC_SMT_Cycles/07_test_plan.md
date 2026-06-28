# 07 - Test Plan

## Goal

The test plan verifies that the STC SMT Cycles strategy matches the locked SRS and owner clarifications before live execution is implemented.

## Time and cycle tests

1. Verify New York DST conversion.
2. Verify trading day assignment from 20:00 to 15:30.
3. Verify M1: 20:00 -> 02:00.
4. Verify no new entry during 02:00 -> 03:00 gap.
5. Verify M2: 03:00 -> 09:00.
6. Verify no new entry during 09:00 -> 09:30 gap.
7. Verify M3: 09:30 -> 15:30.
8. Verify hard close at 15:30.
9. Verify W boundaries for all M cycles.
10. Verify W high/low aggregation from lower timeframe candles.

## Reference matrix tests

1. W1 produces no signal.
2. W2 can use only W1.
3. W3 can use W2 and W1.
4. W4 can use W3, W2, and W1.
5. Current W is never used as its own reference.
6. References from previous M are not allowed.
7. References from previous trading day are not allowed.

## Hunt tests

1. High touch by Symbol1 only creates raw high-side divergence.
2. High touch by Symbol2 only creates raw high-side divergence.
3. Low touch by Symbol1 only creates raw low-side divergence.
4. Low touch by Symbol2 only creates raw low-side divergence.
5. Both symbols touching the same side before check close invalidates divergence.
6. No tolerance is applied.
7. No close beyond level is required.

## Confirmation tests

1. Raw divergence mid-check-candle confirms at same check-candle close if still valid.
2. Raw divergence invalidates if clean symbol hunts before check close.
3. Confirmation after M end is cancelled.
4. Last check candle of M cannot create a new entry.
5. Same divergence does not re-enter on later check candles.

## Direction and trade-symbol tests

1. Symbol1 high hunt and Symbol2 clean -> sell Symbol2.
2. Symbol2 high hunt and Symbol1 clean -> sell Symbol1.
3. Symbol1 low hunt and Symbol2 clean -> buy Symbol2.
4. Symbol2 low hunt and Symbol1 clean -> buy Symbol1.

## Simultaneous signal tests

1. Buy and sell confirmed in same check candle -> no trade.
2. Buy then sell in separate check candles with hedging OFF -> second trade blocked if direction differs.
3. Buy then sell in separate check candles with hedging ON -> both allowed subject to max trade count.

## Max trade tests

1. Max three trades per M across both symbols.
2. Counter increments only after successful position open.
3. Failed order does not increment counter.
4. Counter resets at the next M.
5. Counter resets at daily reset.

## Stop-loss tests

1. Buy SL uses selected reference W low of trade symbol.
2. Sell SL uses selected reference W high of trade symbol.
3. No buffer is added.
4. Closest-by-time reference mode chooses W3 over W2/W1 when current W is W4 and all are eligible.
5. Optional smallest-stop mode chooses the smallest valid stop distance.

## TP and risk tests

1. Final Reward = 10 creates 10R TP.
2. Volume uses risk percent and equity.
3. Tick value is used if available.
4. Contract Size input is used if tick value is unavailable.
5. Theoretical volume is not capped by strategy logic.
6. Live volume respects broker min/max/step.
7. Raw and net results are both recorded when costs are enabled.

## Partial tests

1. M1 trades are checked at 02:00.
2. M2 trades are checked at 09:00.
3. M3 trades are closed at 15:30 by daily hard close.
4. Partial is applied even if trade is in loss.
5. Volume 1.01 with 0.01 step closes 0.51.
6. Volume 0.01 closes fully.
7. Each trade is partially closed at most once.
8. M1 trade is not partially closed again in M2.

## Daily reset tests

1. All open STC positions close at 15:30.
2. All counters reset.
3. All divergence records clear.
4. All partial states clear.
5. Previous-day data does not affect next trading day.
6. EA restart inside current day can rebuild from current-day data.
7. EA restart after 15:30 closes old managed positions if any remain.

## Missing data and holidays

1. Missing required symbol data -> no trade.
2. Closed market -> no trade.
3. No synthetic candle construction if source bars are missing.

## Clarification pass 2 test cases

Add the following deterministic test cases before implementation is accepted:

1. Equality touch:
   - high exactly equals reference high -> high hunt true.
   - low exactly equals reference low -> low hunt true.

2. Check-candle anchor:
   - 10m candles align from 20:00 NY.
   - 3m candles align from 20:00 NY.

3. Final M candle:
   - a signal confirmed at 02:00, 09:00, or 15:30 produces no new entry.

4. Multiple references:
   - W4 has W1/W2/W3 candidates; selected reference is the one producing the largest stop distance for the clean symbol.

5. Simultaneous buy/sell:
   - buy and sell confirmed in same check candle -> no trade and no delayed entry.

6. Entry OFF:
   - signal confirms while Entry OFF -> audit only, no later entry.

7. Offline at entry:
   - EA misses intended entry time -> no late entry.

8. Order failure:
   - signal confirms, order fails -> signal consumed, trade counter unchanged.

9. Hedging per M:
   - M1 direction lock does not affect M2 direction lock.

10. Missed partial:
    - EA offline at M1 W4 end -> partial executes at first later opportunity.

11. Missed hard close:
    - EA offline at 15:30 -> hard close executes at first later opportunity and retries until closed.

12. Missing data:
    - either symbol missing data -> no trade, audit reason recorded.

13. Duplicate EA instance:
    - second instance on same pair cannot execute trades.

14. Magic number:
    - EA ignores manual positions and other-strategy positions.

15. Ambiguous SL/TP:
    - one backtest candle hits both SL and TP -> AMBIGUOUS result.
