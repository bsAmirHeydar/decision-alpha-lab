# 06 - MQL5 Architecture Plan

## Design goal

The STC SMT Cycles implementation should be modular enough to support later related divergence/cycle strategies without hardcoding all logic into one EA.

This document describes the planned MQL5 architecture for EXEC001 only, while keeping common components reusable.

## Proposed folder structure

Expert:

- `mql5/Experts/IntermarketDivergenceExecution/IMDEXEC001_STC_SMT_Cycles.mq5`

Includes:

- `mql5/Include/IntermarketDivergenceExecution/Core/`
- `mql5/Include/IntermarketDivergenceExecution/STC/`

Strategy documentation:

- `lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/`

## Core modules

### Time module

Responsibilities:

- convert broker/server time to UTC;
- convert UTC to New York time;
- handle New York DST;
- assign bars/ticks to STC trading day;
- detect M cycle, W cycle, gaps, partial times, and daily close.

### Synthetic candle module

Responsibilities:

- build W synthetic 90-minute candles;
- build check candles from lower timeframe data;
- support non-standard check periods: 3m and 10m;
- maintain per-symbol high/low state.

### Cycle state module

Responsibilities:

- maintain current trading day state;
- maintain M counters;
- maintain W high/low records;
- clear state at daily reset;
- rebuild same-day state after restart.

### SMT divergence module

Responsibilities:

- evaluate eligible W references;
- detect touch-only hunts;
- confirm divergence at check-candle close;
- detect invalidation by clean-symbol hunt;
- prevent duplicate entry for the same divergence;
- handle simultaneous buy/sell no-trade rule.

### Reference selection module

Responsibilities:

- choose closest eligible W by time;
- optionally choose smallest-stop reference in research mode;
- return the selected trade-symbol stop anchor.

### Entry gate module

Responsibilities:

- enforce STC Entry ON/OFF;
- enforce no-entry gaps;
- enforce final-check-candle rule;
- enforce max three trades per M;
- enforce hedging direction lock;
- enforce simultaneous signal no-trade.

### Risk module

Responsibilities:

- calculate SL and TP;
- calculate risk money;
- use tick value if available;
- fall back to Contract Size input;
- normalize volume to broker min/max/step for live;
- record theoretical vs executed volume.

### Position management module

Responsibilities:

- place market orders;
- track STC-managed positions by magic/comment;
- handle TP/SL via broker orders where possible;
- perform W4 partial close;
- hard-close all positions at 15:30 New York;
- recover active positions after restart.

### Journal module

Responsibilities:

- write confirmed signals;
- write skipped signals with reason;
- write opened trades;
- write partial closes;
- write final close/reset events;
- write raw and net PnL fields.

## Suggested strategy inputs

- `InpSymbol1`
- `InpSymbol2`
- `InpEnableSTCEntry`
- `InpEnablePartial`
- `InpEnableHedging`
- `InpFinalRewardR`
- `InpRiskPercent`
- `InpCheckCandleMinutes`
- `InpContractSize`
- `InpBrokerUtcOffsetHours`
- `InpReferenceSelectionMode`
- `InpSpreadPointsForReport`
- `InpSlippagePointsForReport`
- `InpCommissionPerLotForReport`
- `InpMagicNumber`
- `InpReportPrefix`

## Reference selection enum

- `STC_REF_CLOSEST_BY_TIME`
- `STC_REF_SMALLEST_STOP_DISTANCE`

Default should be closest by time.

## Event IDs

The divergence event ID should include:

- strategy code;
- trading day;
- M id;
- current W id;
- reference W id;
- side;
- hunted symbol;
- trade symbol;
- check close time.

This prevents duplicate entries and supports deterministic audit.

## Execution phases

### Phase 1 - Research/paper engine

- no live auto order;
- signal and trade simulation;
- CSV reports;
- deterministic tests.

### Phase 2 - Live management engine

- live signal detection;
- market orders;
- position sizing;
- partial close;
- hard close;
- restart recovery.

### Phase 3 - Multi-strategy router

- shared core modules;
- independent strategy ON/OFF;
- shared risk and position accounting;
- conflict management between related strategies.

## Clarification pass 2 implementation requirements

The implementation must include:

- internal check-candle aggregation anchored at 20:00 New York;
- no-entry logic for any check candle closing at or after active M end;
- equality-based touch operators with no tolerance;
- reference selection by largest stop distance on the clean/traded symbol;
- persistent daily journal/state reconstruction;
- magic-number-only position management;
- global instance lock by strategy id and symbol pair;
- missed partial processing at first later opportunity;
- missed hard-close processing at first later opportunity with retry every few seconds;
- ambiguous SL/TP outcome category;
- broker-volume splitting for above-max requested volume where practical;
- chart drawing for cycle regions, reference levels, hunt markers, confirmations, entry/SL/TP, partials, and reset markers.
