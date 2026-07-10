# Phase 14 Backtest Operator Guide

## Compile target

```text
mql5/Experts/IntermarketDivergenceExecution/EXP0017_CG_Raw_Execution_Backtest.mq5
```

## Required baseline

Install Phase06 Hotfix011 before compiling Phase14. The executor imports the current confirmation and freshness modules.

## Recommended first test

```text
Expert: EXP0017_CG_Raw_Execution_Backtest
Host symbol: SPXUSD
Period: M1
Model: Every tick based on real ticks
Runtime: BACKTEST_ONLY
Symbol A: SPXUSD
Symbol B: NDXUSD
Trade leg: PROTECTED_SYMBOL
ATR period: 14
ATR multiplier: 1.0
Volume model: RISK_PERCENT_EQUITY
Risk: 1.0
cg_3m: true
all other CG switches: false
```

The default input requires a hedging test account so independent simultaneous positions retain separate SL/TP lifecycles. Disable that requirement only when netting aggregation is deliberately accepted.

## First-run behavior

The expert first reconstructs the current New York trading-day lifecycle from historical closed candles. No warmup order is sent. The Journal prints a warmup-complete line once both symbols have sufficient history.

## Audit output

Default file:

```text
EXP0017_Phase14_Raw_Execution_Audit.csv
```

The audit records accepted plans, rejected plans, paper decisions, broker attempts, retcodes, price geometry, ATR, volume, magic number, and tickets.

## Optimization sequence

Keep signal rules fixed while optimizing execution parameters. Start with:

1. ATR multiplier.
2. ATR period.
3. stop buffer points.
4. protected versus hunter execution leg.
5. confirmation timeframe.
6. individual CG enable switches.

Do not optimize freshness or divergence doctrine in the execution test; those are signal-authority parameters and require a separate research decision.
