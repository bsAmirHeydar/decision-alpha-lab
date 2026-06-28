# EXEC001 STC SMT Cycles — First Implementation Patch Scope

This document defines the exact scope of the first code patch.

The first patch must create a stable execution shell only. It must not implement SMT logic.

---

## 1. Objective

Create a compilable MQL5 Expert Advisor and include structure that can host the STC SMT Cycles engine.

The first patch should prove that the project structure, inputs, timer loop, symbol handling, runtime modes, output folder setup, and build sanity logs are stable.

---

## 2. Files to Add

### Expert

`mql5/Experts/IntermarketDivergenceExecution/IMDEXEC001_STC_SMT_Cycles.mq5`

### Include Directory

`mql5/Include/IntermarketDivergenceExecution/STC/`

### Include Files

- `DAL_STC_Enums.mqh`
- `DAL_STC_Types.mqh`
- `DAL_STC_Config.mqh`
- `DAL_STC_Utils.mqh`
- `DAL_STC_Journal.mqh` minimal stub
- `DAL_STC_Engine.mqh` minimal no-op engine

---

## 3. Inputs to Add

Core inputs:

- `InpSymbol1`
- `InpSymbol2`
- `InpRuntimeMode`
- `InpEntrySTC`
- `InpPartial`
- `InpHedging`
- `InpFinalReward`
- `InpRiskPercent`
- `InpCandleCheckMinutes`
- `InpContractSize`
- `InpBrokerUtcOffsetHours`
- `InpMagicNumber`
- `InpTimerSeconds`
- `InpEnableDrawing`
- `InpEnableCsvJournal`
- `InpHardCloseRetrySeconds`

Optional reporting inputs:

- `InpOutputSubfolder`
- `InpBuildTag`
- `InpVerboseLogs`

---

## 4. Runtime Modes

The first patch should define but not fully implement:

- `STC_RUNTIME_RESEARCH_BACKTEST`
- `STC_RUNTIME_PAPER_LIVE`
- `STC_RUNTIME_AUTO_TRADE`

Only no-op behavior is required in the first patch.

---

## 5. Build Sanity Log

On initialization the EA must print:

- strategy ID
- build tag
- runtime mode
- Symbol1
- Symbol2
- Entry STC state
- Partial state
- Hedging state
- Final Reward
- Risk Percent
- Candle Check minutes
- Contract Size
- Broker UTC offset
- Magic Number
- output folder

---

## 6. Validation Logic

The first patch must validate:

- Symbol1 is not empty
- Symbol2 is not empty
- Symbol1 and Symbol2 are not identical
- symbols can be selected with `SymbolSelect`
- Candle Check is one of 1, 3, 5, 10, 15, 30
- Final Reward is positive
- Risk Percent is positive
- Contract Size is positive
- Timer seconds are positive

If validation fails, `OnInit()` must return `INIT_FAILED` with a clear log message.

---

## 7. Timer Loop

The first patch should implement a timer loop that calls a no-op engine method.

The no-op engine should log heartbeat only when verbose logs are enabled.

---

## 8. Output Folders

The first patch should create or verify output folders for:

- journals
- state
- reports

It does not need to write full strategy CSVs yet.

---

## 9. What This Patch Must Not Do

The first patch must not:

- detect W cycles
- detect SMT
- open trades
- simulate trades
- draw strategy objects except optional build label
- write final trade journals
- implement partial close
- implement hard close

---

## 10. Acceptance Criteria

The patch is accepted only if:

- it compiles with zero errors
- it attaches to any chart
- it uses only Symbol1 and Symbol2 for validation
- it prints a complete build sanity log
- it can run a timer loop without errors
- it creates output folders
- it has no trading capability yet

