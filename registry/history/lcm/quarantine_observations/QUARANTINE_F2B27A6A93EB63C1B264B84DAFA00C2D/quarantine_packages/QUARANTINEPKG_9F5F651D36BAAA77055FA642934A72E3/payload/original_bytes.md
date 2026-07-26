# EXEC001 STC SMT Cycles — Implementation Plan

This document defines the staged implementation plan for `EXEC001_STC_SMT_Cycles`.

The goal is not to build one large monolithic Expert Advisor. The strategy must be implemented as a layered execution system where each layer can be tested, audited, and replaced independently.

This plan is based on the locked strategy specification, owner decisions, and the original STC Expert Advisor SRS.

---

## 1. Implementation Philosophy

The implementation must be deterministic, modular, and auditable.

The EA must not depend on the chart symbol or chart timeframe. It must operate only on `Symbol1` and `Symbol2`. All strategy decisions must be based only on the current STC trading day. A hard daily reset and hard close must occur at 15:30 New York time.

The strategy has three distinct runtime goals:

1. **Research Backtest** — reproduce signals, simulated entries, exits, partials, and journals without sending orders.
2. **Paper Live** — run on live data, draw and journal the same decisions, but do not place trades.
3. **Auto Trade** — execute real orders after the research and paper modes are validated.

The first implementation target is Research Backtest + Paper Live. Auto Trade must be added only after the full audit trail proves that the strategy state machine is correct.

---

## 2. Main Phases

### Phase 0 — Documentation and Contracts

Purpose: freeze the implementation contract before code.

Deliverables:

- locked strategy documents
- module boundary plan
- state machine plan
- data model and journal schemas
- implementation checklist
- deterministic test plan

No trading code should be started before this phase is complete.

Acceptance criteria:

- all strategy decisions are documented
- all remaining optional behaviors are marked as future knobs, not unresolved rules
- the build order is clear
- every code module has a defined responsibility

---

### Phase 1 — MQL5 Project Skeleton and Core Types

Purpose: create the minimal EA and include structure without strategy logic.

Main files:

- `mql5/Experts/IntermarketDivergenceExecution/IMDEXEC001_STC_SMT_Cycles.mq5`
- `mql5/Include/IntermarketDivergenceExecution/STC/DAL_STC_Types.mqh`
- `mql5/Include/IntermarketDivergenceExecution/STC/DAL_STC_Config.mqh`
- `mql5/Include/IntermarketDivergenceExecution/STC/DAL_STC_Enums.mqh`
- `mql5/Include/IntermarketDivergenceExecution/STC/DAL_STC_Utils.mqh`

Responsibilities:

- declare all inputs
- define enums and structs
- initialize runtime mode
- print build sanity information
- perform basic symbol validation
- create output folders
- create a clean timer-driven execution loop

This phase must not detect signals.

Acceptance criteria:

- EA compiles
- EA can be attached to any chart
- chart symbol has no effect on `Symbol1`/`Symbol2`
- `OnInit`, `OnDeinit`, `OnTimer`, and optional `OnTick` are stable
- build sanity log prints all major inputs

---

### Phase 2 — Time Engine and STC Trading Day Engine

Purpose: convert server time into New York time and classify the current STC trading day, M cycle, W cycle, gap, reset time, and entry eligibility.

Main files:

- `DAL_STC_Time.mqh`
- `DAL_STC_Cycles.mqh`

Responsibilities:

- broker server time to UTC conversion using user-provided broker UTC offset
- UTC to New York time conversion with DST support
- STC trading day detection
- M cycle detection
- W cycle detection
- no-entry gap detection
- final check candle blocking
- hard close window detection
- delayed hard close recovery flag

Locked rules:

- STC trading day starts at 20:00 New York and ends at 15:30 New York next day.
- No entry and no new signal detection are allowed in gaps.
- Open positions must still be managed in gaps.
- The final check candle of each M is not allowed to trigger entry.
- At 15:30 New York, hard close has priority over all other actions.

Acceptance criteria:

- every timestamp can be assigned to exactly one of: pre-day, M1, gap, M2, gap, M3, hard-close/reset, post-day
- M1, M2, and M3 boundaries are correct
- W1 through W4 boundaries are correct inside each M
- W1 is marked as non-signal-producing
- final check candle detection works for all supported candle check timeframes

---

### Phase 3 — Data Access and Check Candle Aggregation

Purpose: create a source-independent candle layer for both symbols and aggregate internal check candles from M1 data.

Main files:

- `DAL_STC_Series.mqh`
- `DAL_STC_CheckCandles.mqh`
- `DAL_STC_DataQuality.mqh`

Responsibilities:

- load candles for `Symbol1` and `Symbol2`
- build M1-based synthetic check candles for 1m, 3m, 5m, 10m, 15m, and 30m
- anchor check candles from 20:00 New York
- validate that both symbols have complete enough data
- reject trading when either symbol is missing required data
- write check candle audit rows

Locked rules:

- check candles are anchored from 20:00 New York.
- both symbols must have complete data for a valid SMT decision.
- if the market is closed or data is missing, no trade is allowed.
- the strategy can use any timeframe for W high/low construction because each W is a synthetic 90-minute candle; however, the implementation should prefer the most reliable available candle source.

Acceptance criteria:

- 3m and 10m candles are internally aggregated even if the broker does not provide native periods
- a check candle close event is detected exactly once
- missing-data days are journaled as no-trade days
- no duplicated check candle processing occurs after restart

---

### Phase 4 — W Level Builder and Cycle Audit

Purpose: build high/low levels for every W cycle on both symbols and persist them for audit.

Main files:

- `DAL_STC_WLevels.mqh`
- `DAL_STC_CycleAudit.mqh`

Responsibilities:

- build W1/W2/W3/W4 high and low for each M
- build levels separately for Symbol1 and Symbol2
- never share price levels between symbols
- store level quality and coverage
- write `stc_cycle_audit.csv`

Locked rules:

- each symbol has its own W levels
- the comparison is structural, not price-shared
- W1 produces no signal
- W2 may reference only W1
- W3 may reference only W2 and W1
- W4 may reference only W3, W2, and W1
- no W is compared with itself

Acceptance criteria:

- W level output matches manual chart inspection
- every W has symbol-specific high/low
- W reference matrix is deterministic
- no W1 signal can be produced

---

### Phase 5 — Hunt and SMT Candidate Engine

Purpose: detect raw SMT candidates before final confirmation.

Main files:

- `DAL_STC_Hunt.mqh`
- `DAL_STC_SMTDetector.mqh`
- `DAL_STC_ReferenceMatrix.mqh`

Responsibilities:

- evaluate high hunts and low hunts
- apply exact touch rules
- detect exactly-one-symbol-hunted conditions
- determine hunted symbol and clean symbol
- determine signal side
- create SMT candidate IDs
- write `stc_smt_candidates.csv`

Locked rules:

- high hunt is true when `high >= reference_high`
- low hunt is true when `low <= reference_low`
- no tolerance is used
- high-side SMT maps to SELL
- low-side SMT maps to BUY
- trade symbol is the clean non-hunted symbol
- if both symbols hunt the same reference side by the check candle close, there is no valid SMT

Acceptance criteria:

- candidate generation is reproducible
- candidate IDs prevent repeated trading of the same event
- candidates are linked to M, W, reference W, side, hunted symbol, and clean symbol

---

### Phase 6 — Confirmation, Ambiguity, and Signal Locking

Purpose: wait for check candle close, validate that the divergence still exists, and decide whether the candidate becomes a tradable signal.

Main files:

- `DAL_STC_Confirmation.mqh`
- `DAL_STC_SignalRegistry.mqh`

Responsibilities:

- process only closed check candles
- confirm still-valid SMT at check candle close
- block entries on final check candles of each M
- reject simultaneous buy and sell in the same check candle
- consume or discard signals according to locked owner rules
- prevent delayed entry when the EA was off at the exact entry time
- write `stc_signals.csv`

Locked rules:

- entry is allowed only immediately after the check candle close.
- if the EA is off at the entry moment, there is no late entry.
- if STC Entry is OFF, the signal is audited but not traded and cannot be traded later.
- if buy and sell confirm in the same check candle, both are forgotten and no trade is placed.
- if the final check candle of an M closes at or after the M end, no entry is allowed.

Acceptance criteria:

- every rejected signal has a reason code
- simultaneous buy/sell ambiguity never creates a trade
- Entry OFF never creates delayed entry
- restart does not re-enter old signals

---

### Phase 7 — Reference Selector and Risk Model

Purpose: select the stop reference and compute entry, stop, target, theoretical volume, broker-aware volume, and final trade plan.

Main files:

- `DAL_STC_ReferenceSelector.mqh`
- `DAL_STC_Risk.mqh`
- `DAL_STC_TradePlan.mqh`

Responsibilities:

- choose the reference W that creates the largest stop distance for the clean traded symbol
- set SL on the clean/traded symbol reference W
- compute Final Reward as R multiple
- compute TP without transaction costs
- compute volume from equity, risk percent, stop distance, tick value, and contract size fallback
- read broker min/max/step volume limits
- split oversized volume if needed
- produce a trade plan object

Locked rules:

- SL belongs to the traded symbol, not the hunted symbol
- if several valid references exist, select the one that creates the largest stop distance on the clean traded symbol
- Final Reward 10 means 10R
- TP is calculated without spread, commission, or slippage
- tick value is preferred when available
- Contract Size fallback is shared
- EA does not impose an internal maximum volume, but broker constraints are respected
- if size exceeds broker max, split into multiple orders when Auto Trade is enabled

Acceptance criteria:

- risk distance is positive and valid
- TP/SL are on the correct side of entry
- theoretical volume and broker-normalized volume are both journaled
- split order plan is deterministic

---

### Phase 8 — Research and Paper Trade Simulator

Purpose: simulate trade lifecycle without real orders.

Main files:

- `DAL_STC_Simulator.mqh`
- `DAL_STC_Outcome.mqh`

Responsibilities:

- simulate entry at the open of the next check candle after confirmation
- manage SL/TP using the same check candle stream
- apply gap management
- mark ambiguous SL/TP same-candle outcomes as `AMBIGUOUS`
- simulate partial close at end of W4
- simulate delayed partial if runtime missed exact W4 end
- simulate hard close at 15:30 or delayed hard close recovery
- write `stc_trades.csv` and `stc_position_actions.csv`

Locked rules:

- backtest entry price is the open of the next check candle
- SL/TP are evaluated using the check candle stream
- if SL and TP are touched in the same candle, outcome is `AMBIGUOUS`
- delayed partial must be executed at the first available runtime opportunity
- M3 partial is disabled because hard close has priority
- hard close must close everything at 15:30, or as soon as possible if delayed

Acceptance criteria:

- simulated trade path is deterministic
- ambiguous outcomes are not forced into winner or loser categories
- partial actions happen once per trade
- no position remains open after the STC day hard close

---

### Phase 9 — Journaling, Persistence, and Restart Recovery

Purpose: make the EA restart-safe and audit-safe.

Main files:

- `DAL_STC_Journal.mqh`
- `DAL_STC_Persistence.mqh`
- `DAL_STC_RebuildState.mqh`

Responsibilities:

- write all audit CSV files
- persist consumed signals
- persist partial status
- persist trade IDs and magic-number ownership
- rebuild current day state after restart
- use current-day candles, daily journal, and magic-number positions
- prevent duplicate trades after restart

Locked rules:

- only data from the current STC trading day may affect strategy decisions
- current STC day state may be reconstructed after restart
- persistent daily journal is required to avoid duplicate entries
- EA manages only positions with its own magic number

Acceptance criteria:

- restarting the EA does not duplicate trades
- restarting after missed partial performs delayed partial
- restarting after missed hard close performs hard close immediately
- journal files are append-safe and machine-readable

---

### Phase 10 — Visualization Layer

Purpose: render the strategy state on chart for visual audit without affecting decisions.

Main files:

- `DAL_STC_Renderer.mqh`

Responsibilities:

- draw M and W zones
- draw W reference high/low levels
- draw hunt markers
- draw SMT markers
- draw confirmed/rejected signal markers
- draw entry, SL, TP, partial, hard close, and ambiguous outcome markers
- keep drawing object names short and deterministic
- clear only objects owned by this EA instance

Locked rules:

- drawing must never affect strategy logic
- drawing is audit-only
- no further owner clarification is required for drawing details

Acceptance criteria:

- chart can visually explain every trade and no-trade decision
- objects do not accumulate uncontrollably
- renderer does not break when chart symbol is not Symbol1 or Symbol2

---

### Phase 11 — Paper Live Mode

Purpose: run the same logic live without placing orders.

Main files:

- existing modules plus runtime mode integration

Responsibilities:

- process check candle close in real time
- emit signals
- draw and journal everything
- simulate trade management as paper trades
- perform delayed partial/hard-close logic in paper state

Acceptance criteria:

- paper live matches research backtest behavior on the same data
- no real order is placed
- signal timing is exact
- downtime behavior follows the locked rules

---

### Phase 12 — Auto Trade Mode

Purpose: place and manage real orders after all previous layers pass.

Main files:

- `DAL_STC_Orders.mqh`
- `DAL_STC_PositionManager.mqh`

Responsibilities:

- place market orders immediately after valid confirmation close
- apply SL and TP
- split orders if volume exceeds broker max
- manage only own magic-number positions
- retry hard close every configured interval until positions are closed
- perform partial close at W4 end or delayed partial if missed
- journal all order results

Acceptance criteria:

- no trade is placed outside valid entry moments
- no delayed entry occurs after downtime
- positions with other magic numbers are ignored
- hard close retry loop is safe and bounded by configuration
- every order result is journaled

---

## 3. Recommended Build Order

The safe implementation order is:

1. Core Types and Inputs
2. Time Engine
3. Cycle Engine
4. Check Candle Aggregator
5. W Level Builder
6. Cycle Audit CSV
7. Hunt Detector
8. SMT Candidate Engine
9. Confirmation Engine
10. Signal Registry
11. Reference Selector
12. Risk and Trade Plan
13. Research Simulator
14. Journal Writer
15. Restart Persistence
16. Renderer
17. Paper Live
18. Auto Trade

Auto Trade should not start before steps 1 through 16 compile and produce valid audit outputs.

---

## 4. Patch Sequence

The implementation should be delivered in small patches.

### Patch A — Skeleton and Core Types

Adds EA shell, inputs, enums, structs, and build sanity logs.

No strategy decision logic.

### Patch B — Time and Cycle Engine

Adds New York time, STC day, M/W classification, gaps, and final check candle blocking.

### Patch C — Data and Check Candle Engine

Adds Symbol1/Symbol2 series loading, M1-based check candle aggregation, data completeness, and check candle audit.

### Patch D — W Level Builder

Adds symbol-specific W high/low construction and cycle audit journal.

### Patch E — SMT Candidate Engine

Adds reference matrix, hunt detection, SMT candidate formation, and candidate audit.

### Patch F — Confirmation and Signal Registry

Adds check candle close confirmation, simultaneous buy/sell rejection, Entry OFF behavior, and signal uniqueness.

### Patch G — Trade Plan and Risk

Adds reference selection by largest stop, SL/TP, R multiple, volume calculation, tick value, contract size fallback, broker limits, and split plan.

### Patch H — Research Simulator and Journals

Adds paper trade lifecycle, partial, hard close, ambiguous outcomes, and full journals.

### Patch I — Persistence and Restart Recovery

Adds journal restore, magic-number position restore, duplicate signal protection, delayed partial, delayed hard close.

### Patch J — Visualization

Adds audit drawings.

### Patch K — Paper Live Mode

Adds live timer integration without real orders.

### Patch L — Auto Trade Mode

Adds real orders, partial close, hard close retry, and broker-aware execution.

---

## 5. Non-Negotiable Implementation Gates

The EA must not advance to the next phase until the previous phase satisfies its gate.

### Gate 1 — Compile Gate

Every patch must compile with zero errors.

### Gate 2 — Determinism Gate

The same historical data must produce the same CSV outputs on repeated runs.

### Gate 3 — Time Gate

All M/W assignments must match the documented New York schedule.

### Gate 4 — No Duplicate Gate

The same divergence cannot be traded twice.

### Gate 5 — Restart Gate

Restart must not create duplicate entries and must recover delayed partial/hard close behavior.

### Gate 6 — No Late Entry Gate

If the EA was off at the valid entry time, it must not enter later.

### Gate 7 — Hard Close Gate

No EA-owned position may remain open after the daily hard close recovery logic has run.

### Gate 8 — Journal Gate

Every accepted, rejected, skipped, ambiguous, partial, closed, or failed action must have a journal reason.

---

## 6. First Code Patch Scope

The first implementation patch should be intentionally small.

It should implement:

- EA shell
- all user inputs
- enums and structs
- runtime mode
- symbol validation
- timer loop
- build sanity log
- output folder creation
- no trading
- no signal detection

This creates a stable base for the rest of the system.

