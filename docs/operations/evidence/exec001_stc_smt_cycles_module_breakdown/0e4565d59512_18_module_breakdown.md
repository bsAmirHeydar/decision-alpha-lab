# EXEC001 STC SMT Cycles — Module Breakdown

This document maps the strategy into concrete MQL5 modules.

The implementation must avoid a monolithic EA. Each module must have one clear responsibility and must be independently testable through logs, audit CSVs, or deterministic replay.

---

## 1. Expert Advisor Entry Point

### File

`mql5/Experts/IntermarketDivergenceExecution/IMDEXEC001_STC_SMT_Cycles.mq5`

### Responsibility

The EA entry point owns the lifecycle only:

- parse inputs
- initialize config
- initialize modules
- set timer
- route runtime events
- call the engine
- deinitialize cleanly

The EA file should not contain strategy logic.

### Main Functions

- `OnInit()`
- `OnDeinit()`
- `OnTimer()`
- optional `OnTick()` only as a wake-up mechanism

---

## 2. Types and Configuration

### Files

- `DAL_STC_Types.mqh`
- `DAL_STC_Enums.mqh`
- `DAL_STC_Config.mqh`

### Responsibility

Define all shared types.

Core structs:

- `STCConfig`
- `STCTimePoint`
- `STCTradingDay`
- `STCCycleContext`
- `STCWLevel`
- `STCCheckCandle`
- `STCHuntState`
- `STCSMTCandidate`
- `STCSignal`
- `STCTradePlan`
- `STCTradeState`
- `STCJournalRow`

Core enums:

- runtime mode
- M cycle ID
- W cycle ID
- side
- symbol role
- candidate status
- signal status
- trade status
- reject reason
- action type

---

## 3. Time Module

### File

`DAL_STC_Time.mqh`

### Responsibility

Convert server time to New York time and identify STC trading day boundaries.

Must support:

- broker UTC offset input
- New York DST conversion
- STC day start at 20:00 New York
- STC hard close/reset at 15:30 New York

The rest of the strategy must not use raw server time for decision logic.

---

## 4. Cycle Module

### File

`DAL_STC_Cycles.mqh`

### Responsibility

Classify a New York timestamp into:

- STC trading day
- M cycle
- W cycle
- no-entry gap
- hard-close/reset zone
- final-check-candle zone

This module owns the M/W schedule and no-entry gaps.

---

## 5. Series and Data Quality Module

### Files

- `DAL_STC_Series.mqh`
- `DAL_STC_DataQuality.mqh`

### Responsibility

Load candle data for both symbols and validate that the required data is complete.

Rules:

- if either symbol is missing required data, no SMT decision is allowed
- if the market is closed and data is missing, no trade is allowed
- chart symbol and chart timeframe are ignored

---

## 6. Check Candle Aggregator

### File

`DAL_STC_CheckCandles.mqh`

### Responsibility

Build internal check candles from M1 data.

Supported periods:

- 1m
- 3m
- 5m
- 10m
- 15m
- 30m

Anchor rule:

- all check candles are anchored from 20:00 New York for the current STC trading day

Output:

- closed check candle events
- check candle OHLC for both symbols
- audit row for each check candle

---

## 7. W Level Builder

### File

`DAL_STC_WLevels.mqh`

### Responsibility

Build symbol-specific W high/low levels.

Rules:

- Symbol1 has its own W levels
- Symbol2 has its own W levels
- levels are never shared across symbols
- W levels represent synthetic 90-minute candles
- W1 does not produce signals

---

## 8. Reference Matrix Module

### File

`DAL_STC_ReferenceMatrix.mqh`

### Responsibility

Return eligible reference W cycles for the current W.

Rules:

- W1: no references
- W2: W1
- W3: W2, W1
- W4: W3, W2, W1

No current W may reference itself.

---

## 9. Hunt Module

### File

`DAL_STC_Hunt.mqh`

### Responsibility

Evaluate whether a check candle touched a reference high or low.

Rules:

- high hunt: `high >= reference_high`
- low hunt: `low <= reference_low`
- equality counts as touch
- no tolerance
- close is not required

---

## 10. SMT Detector

### File

`DAL_STC_SMTDetector.mqh`

### Responsibility

Create raw SMT candidates when exactly one of the two symbols hunted a reference level.

Rules:

- high SMT means sell bias
- low SMT means buy bias
- trade symbol is the clean symbol
- comparison is structural, not price-shared
- each candidate gets a deterministic ID

---

## 11. Reference Selector

### File

`DAL_STC_ReferenceSelector.mqh`

### Responsibility

If multiple reference W candidates exist, select the one that gives the largest stop distance on the clean/traded symbol.

This selected reference is used for both:

- the final signal identity
- the stop-loss level

---

## 12. Confirmation Module

### File

`DAL_STC_Confirmation.mqh`

### Responsibility

Convert raw candidates into accepted or rejected signals at check candle close.

Rules:

- divergence must still be valid at close
- entry is allowed only immediately after close
- no entry on final check candle of M
- simultaneous buy/sell in same check candle means no trade and forget the event
- Entry OFF means audit only, no delayed trade
- downtime at entry time means no late entry

---

## 13. Signal Registry

### File

`DAL_STC_SignalRegistry.mqh`

### Responsibility

Prevent duplicate entries.

It stores:

- consumed signals
- skipped signals
- order-failed signals
- ambiguous signals
- Entry-OFF signals

Restart must reload registry state from the daily journal.

---

## 14. Risk and Trade Plan Module

### Files

- `DAL_STC_Risk.mqh`
- `DAL_STC_TradePlan.mqh`

### Responsibility

Build executable trade plans.

Rules:

- entry price in backtest is next check candle open
- SL comes from selected reference W on trade symbol
- Final Reward is R multiple
- Final Reward 10 means 10R
- TP ignores transaction costs
- tick value preferred
- shared Contract Size fallback
- broker min/max/step respected
- oversized volume may be split

---

## 15. Position Manager

### File

`DAL_STC_PositionManager.mqh`

### Responsibility

Manage simulated or real positions depending on runtime mode.

Rules:

- manage only positions with this EA's magic number
- no position remains after hard close recovery
- partial occurs once per trade
- delayed partial is allowed and required
- M3 partial is disabled because hard close dominates
- hard close retries every configured interval until done

---

## 16. Simulator

### Files

- `DAL_STC_Simulator.mqh`
- `DAL_STC_Outcome.mqh`

### Responsibility

Manage research/paper trade lifecycle without real orders.

Rules:

- outcome uses check candle stream
- same-candle SL and TP touch produces `AMBIGUOUS`
- gross and net metrics are recorded separately
- spread/commission/slippage come from data or broker when available

---

## 17. Order Module

### File

`DAL_STC_Orders.mqh`

### Responsibility

Auto Trade only.

Rules:

- place market order immediately after valid confirmation
- no delayed entry
- order failure consumes the signal but does not increment trade counter
- order split is allowed when volume exceeds broker max
- all order actions are journaled

---

## 18. Journal Module

### File

`DAL_STC_Journal.mqh`

### Responsibility

Write all CSV outputs.

Required journals:

- `stc_cycle_audit.csv`
- `stc_check_candles.csv`
- `stc_smt_candidates.csv`
- `stc_signals.csv`
- `stc_trades.csv`
- `stc_position_actions.csv`
- `stc_daily_summary.csv`

---

## 19. Persistence Module

### Files

- `DAL_STC_Persistence.mqh`
- `DAL_STC_RebuildState.mqh`

### Responsibility

Make the EA restart-safe.

State is rebuilt from:

- current STC day candle history
- daily journal files
- account positions with the EA magic number

---

## 20. Renderer

### File

`DAL_STC_Renderer.mqh`

### Responsibility

Draw audit visuals.

Drawing is not part of strategy logic.

---

## 21. Instance Lock

### File

`DAL_STC_InstanceLock.mqh`

### Responsibility

Prevent duplicate EA instances for the same strategy and symbol pair.

Lock key:

- strategy ID
- Symbol1
- Symbol2
- magic number

---

## 22. Engine Orchestrator

### File

`DAL_STC_Engine.mqh`

### Responsibility

Coordinate all modules.

The engine owns the main processing order:

1. update time context
2. enforce hard close if required
3. update data/check candle state
4. update W levels
5. process closed check candle
6. detect candidates
7. confirm signals
8. create trade plans
9. simulate or execute trades
10. manage open trades
11. write journals
12. update drawings

