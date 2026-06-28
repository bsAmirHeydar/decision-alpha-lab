# 06 - MQL5 Architecture Plan

## 1. Goal

Build the STC SMT Cycles strategy as an execution module without hard-coding it into the generic intermarket divergence detector.

## 2. Proposed MQL5 folder layout

```text
mql5/Experts/IntermarketDivergenceExecution/
  IMDEXEC001_STC_SMT_Cycles.mq5

mql5/Include/IntermarketDivergenceExecution/STC/
  DAL_STC_Types.mqh
  DAL_STC_Time.mqh
  DAL_STC_Cycles.mqh
  DAL_STC_Levels.mqh
  DAL_STC_SMTDetector.mqh
  DAL_STC_Confirmation.mqh
  DAL_STC_Risk.mqh
  DAL_STC_PositionManager.mqh
  DAL_STC_Journal.mqh
```

## 3. Shared dependency candidates

The module should reuse, not duplicate:

```text
IntermarketDivergence series loading
external CSV/CME bridge inputs
timeframe-independent bar access
journal/file helpers
position sizing helpers when generalized
```

## 4. Main EA inputs

```mql5
input string InpSymbol1 = "SPXUSD";
input string InpSymbol2 = "NDXUSD";
input bool   InpEntrySTC = true;
input bool   InpPartial = true;
input bool   InpHedging = false;
input double InpFinalReward = 10.0;
input double InpRiskPercent = 0.5;
input int    InpCandleCheckMinutes = 5;
input double InpContractSize = 10.0;
input int    InpBrokerUtcOffsetHours = 0;
input int    InpTimerSeconds = 5;
```

Additional implementation-safety inputs:

```mql5
input bool   InpReportOnly = true;
input bool   InpAllowLiveTrading = false;
input int    InpMagicNumber = 16001;
input string InpOutputFolder = "imd/EXP0016/STC";
input ENUM_STC_REFERENCE_MATRIX_MODE InpReferenceMatrixMode = STC_REF_PREVIOUS_ONLY;
```

## 5. Time module

Responsibilities:

- Convert broker time to UTC.
- Convert UTC to New York time.
- Handle DST.
- Return current STC day ID.
- Return active M/W cycle.
- Detect 15:30 reset event.
- Detect W4-end partial checkpoints.

## 6. Cycle module

Responsibilities:

- Define M and W schedules.
- Build W high/low for each symbol.
- Track current W and prior W levels.
- Enforce same-M reference rules.
- Keep no prior-day levels after reset.

## 7. SMT detector module

Responsibilities:

- Evaluate reference W high/low hunts.
- Create pending SMT records.
- Prevent duplicate divergence IDs.
- Resolve hunted symbol and clean symbol.
- Resolve side: BUY/SELL.
- Detect simultaneous buy/sell conflict.

## 8. Confirmation module

Responsibilities:

- Schedule check-candle close time.
- Revalidate divergence at check close.
- Confirm or cancel pending divergence.
- Create entry intent.

## 9. Execution module

Responsibilities:

- Enforce `Entry STC`.
- Enforce max 3 trades per M.
- Enforce hedging/direction-lock rules.
- Select entry symbol.
- Calculate SL/TP/volume.
- Either journal paper trade or send order.

## 10. Position manager

Responsibilities:

- Manage partial close at W4 end.
- Close all at STC end-of-day 15:30.
- Keep managing existing positions even when `Entry STC` is OFF.
- Track each trade's M, W, divergence ID, and partial status.

## 11. Journal module

Output files:

```text
stc_signals.csv
stc_trades.csv
stc_daily_reset.csv
stc_cycle_audit.csv
stc_pending_divergences.csv
```

## 12. Runtime model

The EA should be chart independent:

- Use `OnTimer` for cycle and confirmation checks.
- Use selected lower timeframe data internally, independent of chart timeframe.
- Optionally refresh on `OnTick`, but never depend on chart ticks alone.

## 13. Build stages

### Stage A - Document-only

Done in this patch.

### Stage B - Research/paper EA

- No live order sending.
- Full signal audit.
- Paper trade journal.

### Stage C - Backtest-compatible executor

- MQL5 tester-safe simulation.
- Intrabar assumptions explicit.

### Stage D - Live executor

- Real orders only when explicitly enabled.
- Magic-number isolation.
- Safety checks around symbol specs.

