# 07 — MQL5 Modular Architecture Plan

## 1. Objective

The expert must be written as a modular system, not a monolithic EA.

The EA file should coordinate modules. Detection, time conversion, cycle building, risk, drawing, and trade management must be separated.

## 2. Proposed expert name

```text
mql5/Experts/IntermarketDivergenceCG/CG_IntermarketDivergence_EA.mq5
```

This path deliberately avoids existing previous expert paths.

## 3. Proposed include path

```text
mql5/Include/IntermarketDivergenceCG/
```

## 4. File breakdown

```text
mql5/Include/IntermarketDivergenceCG/CG_Types.mqh
mql5/Include/IntermarketDivergenceCG/CG_Inputs.mqh
mql5/Include/IntermarketDivergenceCG/CG_Time.mqh
mql5/Include/IntermarketDivergenceCG/CG_CycleCalendar.mqh
mql5/Include/IntermarketDivergenceCG/CG_SymbolData.mqh
mql5/Include/IntermarketDivergenceCG/CG_ReferenceLevels.mqh
mql5/Include/IntermarketDivergenceCG/CG_Hunts.mqh
mql5/Include/IntermarketDivergenceCG/CG_Divergence.mqh
mql5/Include/IntermarketDivergenceCG/CG_SignalRegistry.mqh
mql5/Include/IntermarketDivergenceCG/CG_Drawing.mqh
mql5/Include/IntermarketDivergenceCG/CG_Risk.mqh
mql5/Include/IntermarketDivergenceCG/CG_TradeRouter.mqh
mql5/Include/IntermarketDivergenceCG/CG_PositionManager.mqh
mql5/Include/IntermarketDivergenceCG/CG_Audit.mqh
mql5/Include/IntermarketDivergenceCG/CG_Engine.mqh
```

## 5. Module responsibilities

### 5.1 `CG_Types.mqh`

Defines shared enums and structs.

Required types:

```cpp
enum CG_DivergenceSide
{
   CG_SIDE_NONE = 0,
   CG_SIDE_BUY,
   CG_SIDE_SELL,
   CG_SIDE_CONFLICT
};

struct CG_Config;
struct CG_CycleContext;
struct CG_ReferenceLevels;
struct CG_HuntState;
struct CG_DivergenceEvent;
struct CG_PositionPlan;
```

### 5.2 `CG_Inputs.mqh`

Maps raw MQL5 inputs into `CG_Config configs[]`.

Responsibilities:

- build all 21 CG configs;
- validate symbol inputs;
- validate time offsets;
- validate risk input;
- expose helper functions for lookup by CG name.

### 5.3 `CG_Time.mqh`

Converts broker time to New York time and back.

Responsibilities:

- broker to UTC;
- UTC to NY;
- NY to broker;
- trading-day key;
- day-start/day-end computation.

No other module should do timezone math directly.

### 5.4 `CG_CycleCalendar.mqh`

Builds cycle context for a given CG duration and time.

Responsibilities:

- inside-day check;
- current cycle index;
- current cycle start/end;
- previous cycle start/end;
- incomplete final cycle handling.

### 5.5 `CG_SymbolData.mqh`

Handles OHLC access for both symbols.

Responsibilities:

- ensure symbol selected;
- copy rates for Symbol A/B;
- detect new closed chart bar;
- map confirmation bar times across both symbols;
- handle missing data safely.

### 5.6 `CG_ReferenceLevels.mqh`

Builds reference high/low for each symbol over the reference cycle window.

Responsibilities:

- find bars whose time intervals belong to reference cycle;
- compute high/low for Symbol A;
- compute high/low for Symbol B;
- mark reference as invalid if data is incomplete.

### 5.7 `CG_Hunts.mqh`

Evaluates touch-only hunt rules.

Responsibilities:

- high hunt inclusive `>=`;
- low hunt inclusive `<=`;
- first touch detection time on hunter symbol;
- no close-break logic;
- no tolerance unless later added as optional input.

### 5.8 `CG_Divergence.mqh`

Converts hunt states into divergence events.

Responsibilities:

- high-side asymmetry -> sell event;
- low-side asymmetry -> buy event;
- identify hunter and clean symbols;
- assign stop reference level;
- assign scheduled exit time;
- flag conflicts.

### 5.9 `CG_SignalRegistry.mqh`

Prevents duplicate signals and keeps same-day event memory.

Responsibilities:

- build signal key;
- check if signal already processed;
- reset memory at new trading day;
- keep event list for audit/drawing/trade modules.

### 5.10 `CG_Drawing.mqh`

Draws confirmed divergence lines.

Responsibilities:

- object naming;
- line creation;
- color per CG;
- duplicate drawing prevention;
- avoid wrong-symbol price scale drawing unless chart symbol equals hunter.

### 5.11 `CG_Risk.mqh`

Calculates volume from 1% equity risk.

Responsibilities:

- risk money calculation;
- stop distance validation;
- tick size/value calculation;
- volume normalization;
- min/max/step compliance.

### 5.12 `CG_TradeRouter.mqh`

Sends market orders.

Responsibilities:

- trade permission checks;
- buy/sell order construction;
- SL placement;
- magic number;
- slippage;
- error logging.

### 5.13 `CG_PositionManager.mqh`

Manages time-based exits.

Responsibilities:

- track scheduled cycle-end exits;
- close positions at scheduled exit;
- recover missed closes after restart;
- manage only EXP0017 magic number.

### 5.14 `CG_Audit.mqh`

Writes structured logs.

Responsibilities:

- signal logs;
- trade attempt logs;
- rejected signal logs;
- data error logs;
- position close logs.

### 5.15 `CG_Engine.mqh`

The orchestrator.

Responsibilities:

```text
OnInit:
    build configs
    validate environment
    initialize modules

OnTick:
    update position manager
    detect new closed bar
    if no new closed bar: return
    for each CG config:
        build cycle context
        build reference levels
        evaluate hunts
        build divergence event
        register signal
        draw if enabled
        trade if enabled
```

## 6. EA file responsibilities

The `.mq5` file should contain only:

```cpp
#property metadata
input declarations
#include statements
CG_Engine engine;
OnInit()
OnDeinit()
OnTick()
```

No heavy strategy logic should be placed in the EA file.

## 7. Recommended build order

### Phase 1 — Documentation and interfaces

- finalize types;
- finalize input names;
- finalize cycle calendar;
- finalize event schema.

### Phase 2 — Non-trading detector

- build time module;
- build cycle module;
- build reference levels;
- build divergence detector;
- print/log events only.

### Phase 3 — Drawing

- draw hunter reference lines;
- verify symbol scale behavior;
- prevent duplicate objects.

### Phase 4 — Paper/audit

- log hypothetical entries;
- compute risk and scheduled exit without sending orders.

### Phase 5 — Live trade router

- send trades when enabled;
- manage cycle-end exits;
- add robust error handling.

## 8. Isolation from earlier experts

The first code implementation should not import:

```text
IntermarketDivergenceExecution/STC
FlagCounting
NDS
Astro
Hook
```

It may use only generic common utilities if they are clean, but the preferred first implementation is standalone include files.

## 9. Future extension points

The architecture should allow adding:

- all-previous-cycles reference mode;
- selected N previous cycles;
- different target policies;
- per-CG risk percent;
- per-CG max trades;
- draw-on-both-symbol-charts mode;
- conflict handling modes;
- close-break hunt variants;
- tolerance inputs;
- session filters.

These should be added as new modules or config fields, not by rewriting the detector core.

## Implemented Phase 14 execution architecture

The Phase14 backtest executor is implemented under:

```text
mql5/Experts/IntermarketDivergenceExecution/EXP0017_CG_Raw_Execution_Backtest.mq5
mql5/Include/IntermarketDivergenceExecution/CG/Execution/
```

The implemented dependency map and extension seams are documented in [[phase14_raw_execution_backtest/PHASE14_MODULE_ARCHITECTURE]].

