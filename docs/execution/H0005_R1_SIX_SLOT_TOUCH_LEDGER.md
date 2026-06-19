# H0005 Reversal Structural-Target-Capped Execution — Build 1.25

This document is the execution contract for `E0001_ReversalOneToOne.mq5`.

## Execution cadence

The strategy is evaluated once per closed candle by default:

- `InpRefreshSetupsOnNewBarOnly = true`
- `InpManageOrdersEveryTick = false`
- `InpUseClosedBarsOnly = true`

The current forming candle is excluded from structural/regime calculations so the touch zone is not mutated by the same candle that is about to trade it.

## Source of truth

Execution does not invent its own market logic. It reuses the hypothesis modules:

- M0001 builds node territories and node consumption/hunt state.
- M0002 builds the last completed branch outcome: reversal or continuation.
- E0001 only translates the active H0005 reversal state into pending limit orders.

## Regime input modes

`InpRegimeBasis` has two modes:

1. `E0001_REGIME_LAST_COMPLETED_BRANCH`
   - Trade only when the latest completed M0002 branch outcome is `REVERSAL_AFTER_EXIT`.

2. `E0001_REGIME_HUMAN_CONTEXT_COMBINED`
   - `InpHumanContextSignal = NEUTRAL`: use the latest completed M0002 branch.
   - `InpHumanContextSignal = REVERSAL`: explicitly gate execution as reversal while still using M0001/M0002 nodes.
   - `InpHumanContextSignal = CONTINUATION`: block reversal execution and delete managed pending orders.

## Node selection

When the effective regime is reversal:

- Choose the nearest LOW-node buy limits below the market.
- Choose the nearest HIGH-node sell limits above the market.
- Defaults:
  - `InpBuyLimitSlots = 3`
  - `InpSellLimitSlots = 3`
- Setting a slot input to `0` means unlimited for that side.

This keeps the next few possible reversals armed so a stop on the first order does not cause the next nearby touch to be missed.

## Spread-aware order geometry

For a LOW node:

```text
Buy Limit entry = zone_upper + spread
Stop            = zone_lower
Risk            = entry - stop
Fixed-R cap     = entry + Risk * InpRewardR
Opposite target = first HIGH-node touch edge in the profit path, i.e. that HIGH zone_lower
TP              = Opposite target by default; if InpUseFixedRExitIfCloser=true and Fixed-R cap is closer, use Fixed-R cap
```

For a HIGH node:

```text
Sell Limit entry = zone_lower
Stop             = zone_upper + spread
Risk             = stop - entry
Fixed-R cap      = entry - Risk * InpRewardR
Opposite target  = first LOW-node touch edge in the profit path, i.e. that LOW zone_upper
TP               = Opposite target by default; if InpUseFixedRExitIfCloser=true and Fixed-R cap is closer, use Fixed-R cap
```

Default TP is the first valid opposite-node touch in the profit path. `InpRewardR = 1.0` is a reference/cap input: it only becomes the exit if `InpUseFixedRExitIfCloser=true` and the fixed-R target is closer than the opposite touch. If `InpAllowOppositeTouchBelowRewardR=false`, setups whose opposite touch is below the configured R threshold are rejected. If no valid opposite-node target exists, the setup is rejected rather than falling back silently to fixed R.


## Trading-session filter

The time condition is strict. When enabled, the EA only creates, updates, or keeps managed pending limits inside the configured session:

```text
InpUseTradingSessionFilter = true
InpTradingSessionClock = E0001_SESSION_BROKER_TIME
InpTradingStartHour = 0
InpTradingStartMinute = 0
InpTradingEndHour = 23
InpTradingEndMinute = 59
InpDeletePendingsOutsideTradingSession = true
```

E0001 blocks new setup generation, order submission, order modification, and cached setup execution outside the configured session. If `InpDeletePendingsOutsideTradingSession` is true, managed pending orders are force-deleted outside the session regardless of stale-sync settings or near-market protection. Open positions are not force-closed.

Session logic supports normal intraday windows, for example `09:00 -> 17:00`, and overnight windows, for example `22:00 -> 02:00`. The start minute is inclusive and the end minute is exclusive, so `09:00 -> 17:00` means `09:00 <= time < 17:00`. Equal start/end bounds are treated as all-day trading to avoid an accidental no-trade trap.

## Reversal exit

If the effective regime is not reversal, E0001 deletes all managed pending orders for its magic/prefix. Open positions are not force-closed; they are left to their own SL/TP.

## Consumption

A structurally hunted/consumed node is retired by the M0001 module and is no longer used. Historical touches do not retire the node by themselves, because revisits are part of the H0005 execution hypothesis.

## Diagnostics

`DAL_E0001_CYCLE`, `DAL_E0001_LIMIT_ORDER`, `DAL_E0001_PENDING_UPDATE`, and `DAL_E0001_PENDING_DELETE` journal lines report:

- effective regime basis
- setup count
- new/modified/deleted orders
- skipped risk/geometry/touch-lock reasons
- raw zone edges
- spread-adjusted entry/stop/TP


## H0005 research report

Build 1.18 prints an execution-matched H5 research report from the same M0001/M0002 modules used by live execution.

Inputs:

```text
InpH5ReportEnabled = false
InpH5ReportEveryNClosedBars = 1
InpH5ReportMaxSamples = 300
InpH5ReportMaxBarsAfterEntry = 0
InpH5ReportPrintExamples = false
```

The report line is:

```text
DAL_E0001_H5_RESEARCH_REPORT
```

It reports two blocks of evidence.

### Directional memory

The report scans completed M0002 branch outcomes and prints:

```text
samples
reversalSamples
continuationSamples
transitions
directionMemoryHitPct
memoryVsRandomEdgePct
revToRev
revToCont
pRevAfterRevPct
contToCont
contToRev
pContAfterContPct
```

This lets us see whether the market has real regime memory compared with a 50/50 random baseline.

### Fixed-R reversal outcome

For every completed reversal branch, the report builds the same near-node H5 setup model as the executor:

```text
3 nearest LOW-node buy limits below the closed-bar reference price
3 nearest HIGH-node sell limits above the closed-bar reference price
entry/SL/TP from the same spread-aware fixed-R geometry
```

Then it simulates pending-limit paths forward and prints:

```text
plannedTrades
buyPlanned
sellPlanned
filledTrades
unfilledTrades
fillRatePct
targetHits
stopHits
ambiguousSameBar
openAfterFill
targetHitPctFilled
targetHitPctPlanned
expectancyRConservative
profitFactorRConservative
sumRConservative
setupRejectSamples
simulationRejects
```

Same-bar TP+SL ambiguity is counted separately as `ambiguousSameBar` and is treated conservatively as a stop in `expectancyRConservative`, `profitFactorRConservative`, and `sumRConservative`.

This report is intentionally comparable with the EA journal: `plannedTrades` is the theoretical H5 opportunity set, while `DAL_E0001_CYCLE`, `DAL_E0001_LIMIT_ORDER`, and trade history show what the execution engine actually managed to plant and fill.


## Build 1.17 compile note

Build 1.17 splits the initialization sanity journal line into four smaller `Print()` calls. MQL5 has a practical argument-count limit for `Print`, and the build 1.16 one-line sanity report could fail compile with `wrong parameters count` on the init log call. The execution contract is unchanged.


## Build 1.18 strict time gate note

Build 1.18 makes the session gate strict for execution. Outside the configured time window, E0001 clears its setup cache, blocks all new order submission/modification, and force-deletes all managed pending limit orders when `InpDeletePendingsOutsideTradingSession=true`. This deletion path no longer depends on stale-sync inputs and does not protect near-market pending orders outside the session.

The configured session is interpreted as start-inclusive / end-exclusive: `start <= current_time < end`. Overnight windows are supported with the same rule. Equal start and end still mean all-day trading.


## Build 1.20 — strict touch/revisit ledger

This build keeps the H5 original-hypothesis report out of the execution EA. It only changes the execution ledger. A structural setup remains visible to the EA even when the current tick is already inside the touch zone, so the EA can lock that touch episode and avoid planting another limit until price exits the edge by `InpTouchRevisitResetBufferPoints` and later revisits it. Locked touch states are not pruned just because a node temporarily falls out of the 3+3 near-node cache, because that would allow duplicate limits inside the same touch.


## Build 1.21 — node-zone touch lock

This build fixes the duplicate same-node touch problem. The touch/revisit ledger is now keyed by structural `node_id + direction`, not only by the broker order comment. Once a node is touched or its limit is filled, that node-side is locked as an active touch episode. The EA will not plant or recreate another limit for the same node while price remains inside the same node zone.

Unlock/re-arm now requires a full zone exit, not just a small move away from the order entry:

- LOW-node buy lock re-arms only after `ask > zone_upper + InpTouchRevisitResetBufferPoints * point`.
- HIGH-node sell lock re-arms only after `bid < zone_lower - InpTouchRevisitResetBufferPoints * point`.

A move through the far side of the zone is treated as node consumption/hunt by the structural modules and is not considered a valid same-node revisit. This prevents repeated entries on the same node while the market is still in the original touch episode.

`InpAllowNodeRevisitRearm=true` keeps the original H5 revisit behavior: after a full exit, a later return can receive a new limit. Setting it to `false` makes a touched node lock forever after its first touch/fill within the test run.

## Build 1.24 TP policy

Build 1.24 changes the TP model for E0001 to first-opposite-node touch by default:

```text
TP = first opposite-node touch by default; optional InpUseFixedRExitIfCloser can exit at InpRewardR only if it is closer
```

This keeps the target aligned with the next structural opposing touch while preserving the 1R ceiling by default. For buys from LOW nodes, the opposing touch is the lower edge of the nearest active HIGH-node zone above entry. For sells from HIGH nodes, the opposing touch is the upper edge of the nearest active LOW-node zone below entry.


## Build 1.24 TP policy correction

Build 1.24 corrects the TP priority for both E0001 and E0002. The primary target is the first opposite-node touch. `InpUseFixedRExitIfCloser=false` by default, so `InpRewardR` does not cap TP unless explicitly enabled. When enabled, fixed-R can only close earlier than the opposite touch; it never extends TP beyond that structural target. `InpAllowOppositeTouchBelowRewardR=false` rejects trades whose first opposite-node touch is below the configured R reference instead of taking a sub-R target. Node touch/consume/revisit locking remains a separate execution ledger and is not part of TP selection.


## Build 1.25 speed pass

Build 1.25 does not change the H5 structural TP policy or node-zone touch/revisit ledger. It reduces tester load by making logs error-only by default, disabling the H5 execution-matched report by default in E0001, throttling outside-session pending purges to once per bar, and moving build/cycle diagnostics behind order/verbose logging. Use `InpLogMode=DAL_EXEC_LOG_ORDERS` or `DAL_EXEC_LOG_VERBOSE` only when diagnosing a specific run.


## Minimal input surface

Release 1.26 / E0002 1.04 hides diagnostic and engine-maintenance knobs from the Strategy Tester input panel. Public inputs are limited to symbol/timeframe/bars, core H5 structure (`InpL`, `InpZoneRatio`, `InpExitGap`, `InpConsumeMode`), regime source, trading-session window, risk/target policy, near-node slots, and node revisit settings. Heavy reports, verbose logs, pending-maintenance flags, market-catch switches, and speed/runtime controls are fixed internally for faster and cleaner tests.
