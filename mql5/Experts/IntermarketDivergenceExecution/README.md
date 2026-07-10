# Intermarket Divergence Execution Experts

This folder contains execution-oriented experts for intermarket divergence strategies.

## IMDEXEC001_STC_SMT_Cycles.mq5

`IMDEXEC001_STC_SMT_Cycles.mq5` is the STC SMT Cycles execution expert.

Current level:

- Level 01 skeleton
- Inputs and validation
- Common Files journals
- Timer runtime
- Duplicate instance lock
- No SMT detection
- No paper simulation
- No live orders

Compile this expert first before moving to the time/cycle engine level.

## STC SMT Hidden License Inputs

The STC SMT license is intentionally entered through neutral Cycle Model fields:

```text
InpCycleModelProfile
InpCycleOperatorMemo
InpCycleReferenceSeed
InpCycleDivergenceSeed
InpCycleExecutionSeed
InpCycleReleaseSeed
```

This build keeps the license hidden behind the neutral Cycle Model field names.

## EXP0017_CG_Raw_Execution_Backtest.mq5

Phase14 modular raw execution backtest for the EXP0017 cycle-group divergence stack.

Default profile:

- Strategy Tester transport only;
- protected/clean symbol execution;
- market entry after closed confirmation candle;
- stop behind the selected symbol confirmation candle;
- ATR(14) × 1.0 target by default, with optional fixed stop-risk multiple;
- fixed monetary risk sizing with maximum broker-valid volume under the risk cap;
- SELL stop spread adjustment enabled;
- hedging enabled by default and input-switchable;
- optional executed-CG divergence and entry/SL/TP drawings;
- only `cg_3m` enabled.


## One-shot execution invariant

`EXP0017_CG_Raw_Execution_Backtest.mq5` treats each divergence anatomy as one execution entitlement. Re-detection on later confirmation candles cannot create another order. The gate is mandatory and is reconstructed from closed-candle history during startup warmup.
