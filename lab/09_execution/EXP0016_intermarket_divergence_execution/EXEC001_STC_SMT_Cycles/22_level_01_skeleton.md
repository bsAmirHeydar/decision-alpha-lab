# EXEC001 STC SMT Cycles — Level 01 Skeleton Implementation

This document describes the first implementation level for `EXEC001_STC_SMT_Cycles`.

Level 01 is intentionally not a strategy engine yet. It is the safe foundation that all later STC modules will plug into.

## Level 01 Goal

The goal of Level 01 is to create a compileable MQL5 expert advisor shell with the exact STC inputs, the first shared data structures, output journaling, timer runtime, and duplicate-instance protection.

It must not detect SMT divergence. It must not build W levels. It must not open orders. It must not partial close. It must not hard close. Those behaviors belong to later levels.

## Files Added

MQL5 expert:

- `mql5/Experts/IntermarketDivergenceExecution/IMDEXEC001_STC_SMT_Cycles.mq5`

MQL5 includes:

- `mql5/Include/IntermarketDivergenceExecution/STC/DAL_STC_Enums.mqh`
- `mql5/Include/IntermarketDivergenceExecution/STC/DAL_STC_Types.mqh`
- `mql5/Include/IntermarketDivergenceExecution/STC/DAL_STC_Config.mqh`
- `mql5/Include/IntermarketDivergenceExecution/STC/DAL_STC_Utils.mqh`
- `mql5/Include/IntermarketDivergenceExecution/STC/DAL_STC_Journal.mqh`
- `mql5/Include/IntermarketDivergenceExecution/STC/DAL_STC_Engine.mqh`

## Runtime Modes

Level 01 exposes the future runtime modes but does not yet change behavior based on them:

- `RESEARCH_BACKTEST`
- `PAPER_LIVE`
- `AUTO_TRADE`

The important design rule is that `AUTO_TRADE` exists as a configuration value only. Level 01 never places orders.

## Input Groups

### Runtime

- `InpRuntimeMode`
- `InpRunId`
- `InpTimerSeconds`
- `InpWriteHeartbeat`
- `InpHeartbeatSeconds`
- `InpOutputRootCommon`

### Symbols

- `InpSymbol1`
- `InpSymbol2`
- `InpStrictSymbolValidation`

`Symbol1` and `Symbol2` are both data symbols and execution symbols for this strategy. There is no separate data/execution mapping in the locked STC design.

### Strategy Switches

- `InpEntrySTC`
- `InpPartial`
- `InpHedging`
- `InpEnableDrawing`

Level 01 stores and journals these switches, but no strategy action is performed yet.

### Risk Inputs

- `InpFinalRewardR`
- `InpRiskPercent`
- `InpCandleCheck`
- `InpContractSize`
- `InpBrokerUtcOffsetHours`
- `InpMagicNumber`

These inputs are present now so later levels do not need to break the user-facing interface.

### Reporting Costs

- `InpUseBrokerCostsForReporting`
- `InpFallbackSpreadPoints`
- `InpFallbackCommissionPerLot`

Costs are report-only in the locked STC design. TP is calculated from raw R distance, not cost-adjusted R.

### Safety

- `InpUseDuplicateInstanceLock`
- `InpInstanceLockStaleSeconds`
- `InpHardCloseRetrySeconds`

Hard close retry is only stored in Level 01. The actual hard-close engine is deferred.

## Validation Rules Implemented

Level 01 validates:

- `StrategyId` is not empty.
- `RunId` is not empty.
- `Symbol1` is not empty.
- `Symbol2` is not empty.
- `Symbol1 != Symbol2`.
- `FinalRewardR > 0`.
- `RiskPercent > 0`.
- `ContractSize > 0`.
- `MagicNumber > 0`.
- `OutputRootCommon` is not empty.
- `CandleCheck` is one of 1m, 3m, 5m, 10m, 15m, 30m.

Symbol selection is attempted for both symbols. If `InpStrictSymbolValidation=false`, missing broker symbols are recorded as warnings instead of failing initialization. This keeps the EA attachable while the user is still preparing broker symbol names.

## Duplicate Instance Lock

Level 01 creates a terminal global variable lock based on:

- account login
- terminal build
- strategy id
- symbol pair
- magic number

The lock prevents two active copies of the same strategy/symbol/magic profile from running at once.

If a previous lock is older than `InpInstanceLockStaleSeconds`, the new instance may take over.

## Common Files Output

Level 01 writes under:

`InpOutputRootCommon`

Default:

`dal/stc/EXEC001_STC_SMT_Cycles`

Generated files:

- `stc_level01_build_sanity.csv`
- `stc_level01_runtime_events.csv`

## Build Sanity CSV

The build sanity file records:

- strategy id
- module level
- build version
- build scope
- locked contract
- terminal common data path
- account login
- terminal build
- runtime mode
- symbols
- all key inputs
- locked rule summary
- validation warnings

This gives an immediate audit trail after compiling and attaching the EA.

## Runtime Events CSV

The runtime events file records:

- `INIT`
- `HEARTBEAT`
- `DEINIT`

Later levels will append cycle events, SMT candidates, signals, trade simulations, partial actions, and hard-close actions into separate journals.

## Locked Rules Logged But Not Yet Executed

Level 01 prints and journals the locked STC contract:

- equality counts as touch
- no hunt tolerance
- New York trading day from 20:00 to 15:30
- no entry and no detection in M gaps
- W1 produces no signal
- W2 references W1
- W3 references W2 and W1
- W4 references W3, W2 and W1
- structural comparison per symbol
- high SMT maps to sell on the clean symbol
- low SMT maps to buy on the clean symbol
- backtest entry is next check-candle open
- final check candle of each M cannot trigger entry
- reference selector uses largest stop on the clean traded symbol
- simultaneous buy and sell are forgotten with no trade
- Entry OFF is audit-only and never creates delayed entry
- order failure consumes the signal but does not increment the trade counter
- max three trades per M across the pair
- hard close at 15:30 New York applies only to the EA magic number
- auto-trade is disabled in Level 01

## Acceptance Criteria

Level 01 is accepted when:

1. The EA compiles.
2. The include tree compiles.
3. The EA can be attached to any chart.
4. Chart symbol does not affect configuration.
5. It selects only `Symbol1` and `Symbol2`.
6. It creates the Common Files output folder.
7. It writes the build sanity CSV.
8. It appends INIT, HEARTBEAT, and DEINIT events.
9. It prevents duplicate active instances when the lock is enabled.
10. It does not open, close, modify, or simulate any trades.

## Next Level

Level 02 will implement the time engine:

- broker server time to UTC
- UTC to New York time
- STC trading day identity
- M1/M2/M3 detection
- W1/W2/W3/W4 detection
- no-entry/no-detection gaps
- final check-candle gating
- hard-close time detection only, without closing trades yet
