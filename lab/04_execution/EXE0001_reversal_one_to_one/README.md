# EXE0001 — H0005 Reversal Fixed-R Executor

Build: `1.18`

Purpose: execute the H0005 reversal branch as pending limit orders, not market chasing.

## Contract

On each closed candle:

1. Load bars from the configured symbol/timeframe.
2. Exclude the current forming candle by default.
3. Detect structural nodes through the existing L-rule/M0001 modules.
4. Compute M0001 events and the latest completed M0002 branch sample.
5. Resolve the effective regime:
   - last completed branch only, or
   - last branch combined with explicit human context input.
6. If reversal:
   - place/update nearest LOW-node buy limits below market;
   - place/update nearest HIGH-node sell limits above market.
7. If continuation/non-reversal:
   - delete managed pending orders.

## Defaults

```text
InpRegimeBasis = E0001_REGIME_LAST_COMPLETED_BRANCH
InpHumanContextSignal = E0001_HUMAN_CONTEXT_NEUTRAL
InpUseClosedBarsOnly = true
InpBuyLimitSlots = 3
InpSellLimitSlots = 3
InpRewardR = 1.0
InpRefreshSetupsOnNewBarOnly = true
InpManageOrdersEveryTick = false
InpAllowOppositeTrades = true
InpMaxSimultaneousTrades = -1
```

## Geometry

LOW node buy:

```text
entry = zone_upper + spread
SL    = zone_lower
TP    = entry + (entry - SL) * InpRewardR
```

HIGH node sell:

```text
entry = zone_lower
SL    = zone_upper + spread
TP    = entry - (SL - entry) * InpRewardR
```

## Optional time filter

```text
InpUseTradingSessionFilter = true
InpTradingSessionClock = E0001_SESSION_BROKER_TIME
InpTradingStartHour = 0
InpTradingStartMinute = 0
InpTradingEndHour = 23
InpTradingEndMinute = 59
InpDeletePendingsOutsideTradingSession = true
```

New H5 reversal setup generation and pending-order management only run inside the configured session. Outside the session, managed pending orders are force-deleted by default, independent of stale-sync protection; existing positions remain managed by their SL/TP.


## H5 comparison report

Build 1.18 adds `DAL_E0001_H5_RESEARCH_REPORT` journal output. It is enabled by default and uses the same bars, L-rule nodes, M0001 events, and M0002 completed branch samples as execution.

Main fields:

```text
directionMemoryHitPct
memoryVsRandomEdgePct
pRevAfterRevPct
plannedTrades
filledTrades
targetHits
stopHits
targetHitPctFilled
expectancyRConservative
profitFactorRConservative
```

Use this beside the EA order logs to answer: did the raw H5 reversal fixed-R model produce enough 1R reversals, and did execution capture the same opportunities?


## Build 1.20 — strict touch/revisit ledger

This build keeps the H5 original-hypothesis report out of the execution EA. It only changes the execution ledger. A structural setup remains visible to the EA even when the current tick is already inside the touch zone, so the EA can lock that touch episode and avoid planting another limit until price exits the edge by `InpTouchRevisitResetBufferPoints` and later revisits it. Locked touch states are not pruned just because a node temporarily falls out of the 3+3 near-node cache, because that would allow duplicate limits inside the same touch.


### Build 1.21 node-zone lock note

The H5 executor now locks touch state by structural node (`node_id + direction`) and by the touched zone boundaries. A node does not receive a second pending limit while price remains in the same zone episode. Re-arm requires a full exit beyond the zone edge plus `InpTouchRevisitResetBufferPoints`; optional `InpAllowNodeRevisitRearm=false` disables same-node revisits entirely.


## TP policy

TP defaults to the first opposite-node touch. If `InpUseFixedRExitIfCloser=true`, the fixed-R target from `InpRewardR` may be used only when it is closer than that opposite touch. If `InpAllowOppositeTouchBelowRewardR=false`, setups whose opposite touch is below the configured R threshold are skipped.


## Build 1.25 performance defaults

Execution behavior is unchanged, but the EA is quieter and faster by default: `InpLogMode=DAL_EXEC_LOG_ERRORS`, `InpH5ReportEnabled=false`, outside-session pending purges are throttled to once per bar, and build/cycle diagnostics require order/verbose logging.


## Minimal input surface

Release 1.26 / E0002 1.04 hides diagnostic and engine-maintenance knobs from the Strategy Tester input panel. Public inputs are limited to symbol/timeframe/bars, core H5 structure (`InpL`, `InpZoneRatio`, `InpExitGap`, `InpConsumeMode`), regime source, trading-session window, risk/target policy, near-node slots, and node revisit settings. Heavy reports, verbose logs, pending-maintenance flags, market-catch switches, and speed/runtime controls are fixed internally for faster and cleaner tests.
