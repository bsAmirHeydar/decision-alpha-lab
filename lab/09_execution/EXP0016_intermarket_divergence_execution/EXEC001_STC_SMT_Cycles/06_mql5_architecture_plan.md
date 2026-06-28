# 06 - MQL5 Architecture Plan

## 1. Design goal

The implementation must be modular. The STC strategy should not be a single large EA with hidden state. It should be built from reusable modules that can later support other SMT/cycle-divergence strategies.

## 2. Proposed folder structure

MQL5 experts:

- `mql5/Experts/IntermarketDivergenceExecution/IMDEXEC001_STC_SMT_Cycles.mq5`

MQL5 include modules:

- `mql5/Include/IntermarketDivergenceExecution/Core/`
- `mql5/Include/IntermarketDivergenceExecution/STC/`

STC modules:

- `DAL_STC_Types.mqh`
- `DAL_STC_Time.mqh`
- `DAL_STC_Cycles.mqh`
- `DAL_STC_CheckCandles.mqh`
- `DAL_STC_WLevels.mqh`
- `DAL_STC_SMTDetector.mqh`
- `DAL_STC_Confirmation.mqh`
- `DAL_STC_ReferenceSelector.mqh`
- `DAL_STC_Risk.mqh`
- `DAL_STC_PositionManager.mqh`
- `DAL_STC_StateJournal.mqh`
- `DAL_STC_TradeJournal.mqh`
- `DAL_STC_Renderer.mqh`
- `DAL_STC_InstanceLock.mqh`

## 3. Core modules

Shared core modules should include:

- Broker symbol info reader.
- Tick value and volume step utilities.
- Position lookup by magic number.
- CSV writer.
- Time conversion utility.
- Atomic file writer.
- Chart object prefix cleaner.
- Common drawing helpers.

## 4. STC EA responsibilities

The EA should:

1. Load inputs.
2. Acquire duplicate-instance lock.
3. Initialize time/cycle configuration.
4. Load current-day data for Symbol1 and Symbol2.
5. Reconstruct state from current-day candles, journals, and magic-number positions.
6. Run the scheduler on new check-candle closes.
7. Detect SMT candidates.
8. Confirm signals.
9. Route signals to research, paper, or auto-trade execution mode.
10. Manage positions, partials, SL/TP outcomes, and hard close.
11. Write audit and trade journals.
12. Draw chart overlays.

## 5. Scheduler algorithm

OnTimer or OnTick should call a scheduler. The scheduler must not depend on chart timeframe.

Scheduler steps:

1. Get current server time.
2. Convert to UTC and New York time.
3. Determine STC day and cycle context.
4. If new check candle closed, run signal logic.
5. Always run position management.
6. Always run hard-close recovery if needed.
7. Always run delayed partial recovery if needed.
8. Update drawings.

## 6. Time engine

The time engine must expose:

- `GetStcTradingDayId()`
- `GetMContext()`
- `GetWContext()`
- `IsGap()`
- `IsFinalCheckCandleOfM()`
- `GetNextCheckCandleOpen()`
- `IsHardCloseDue()`
- `ConvertServerToNewYork()`

## 7. Cycle engine

The cycle engine builds:

- M cycle records.
- W cycle records.
- W high/low per symbol.
- Completeness flags.
- Eligible reference lists.

The engine must reject W references if either symbol has incomplete data.

## 8. Check candle engine

The check-candle engine aggregates candles anchored from 20:00 New York.

It must support 1m, 3m, 5m, 10m, 15m, and 30m check candles.

It must expose the completed check candle for both symbols at the same close time.

If either symbol is missing the check candle, the signal engine must skip and log `DATA_INCOMPLETE`.

## 9. SMT detector

The detector receives:

- Current M/W context.
- Completed check candle for Symbol1.
- Completed check candle for Symbol2.
- Eligible references for Symbol1 and Symbol2.

It returns candidate objects with:

- Side.
- Hunted symbol.
- Clean symbol.
- Candidate references.
- Selected reference.
- Formation/check close time.
- Rejection reason if rejected.

## 10. Confirmation and filter pipeline

The confirmation pipeline applies filters in this order:

1. In active M, not gap.
2. Current W is not W1.
3. Check candle is not final for M.
4. Data complete for both symbols.
5. Exactly one symbol hunted.
6. Buy/sell ambiguity filter.
7. Reference selection by largest stop.
8. Duplicate signal filter.
9. Entry STC filter.
10. M trade counter filter.
11. Hedging direction lock filter.
12. Runtime mode routing.

## 11. Risk module

The risk module computes:

- Entry price.
- SL.
- TP.
- R distance.
- Theoretical volume.
- Broker-normalized volume.
- Order split plan if volume exceeds broker maximum.
- Skip reason if volume below broker minimum.

## 12. Position manager

The position manager handles:

- Open STC positions by magic number.
- SL/TP outcome in research mode.
- Real broker order monitoring in live mode.
- Partial close at W4 end for M1 and M2.
- Delayed partial recovery.
- Hard close at 15:30.
- Hard-close retry.

## 13. Persistence

The EA must write daily state files so restart does not create duplicate trades.

Minimum files:

- Consumed signal journal.
- Candidate/divergence audit.
- Trade journal.
- Position management journal.
- Runtime state snapshot.

The journal must be keyed by STC trading day.

## 14. Drawing layer

The renderer must be optional but should be enabled by default in research/paper mode.

Drawing must use a strategy-specific object prefix and must be safe to clean without affecting other chart objects.

Drawing must not alter strategy state.

## 15. Duplicate instance lock

A lock key should include:

- Strategy ID.
- Symbol1.
- Symbol2.
- Magic number.

If another active instance holds the lock, the EA should refuse to run or enter passive display-only mode.
