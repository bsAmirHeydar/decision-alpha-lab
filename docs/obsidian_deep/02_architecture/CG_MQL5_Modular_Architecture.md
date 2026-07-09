# CG MQL5 Modular Architecture

## Design principle

The EA should be an orchestration shell. Strategy logic should live in include modules.

## Proposed root

```text
mql5/Experts/IntermarketDivergenceCG/CG_IntermarketDivergence_EA.mq5
mql5/Include/IntermarketDivergenceCG/
```

## Module stack

```text
CG_Types
CG_Inputs
CG_Time
CG_CycleCalendar
CG_SymbolData
CG_ReferenceLevels
CG_Hunts
CG_Divergence
CG_SignalRegistry
CG_Drawing
CG_Risk
CG_TradeRouter
CG_PositionManager
CG_Audit
CG_Engine
```

## Pipeline

```text
OnTick
  -> manage scheduled exits
  -> detect new closed chart bar
  -> for each CG config
       -> build cycle context
       -> build previous-cycle reference levels
       -> evaluate touch-only hunts
       -> detect divergence asymmetry
       -> register signal key
       -> draw hunter-line if allowed
       -> trade clean symbol if allowed
```

## Non-negotiable architecture rule

Do not write 21 separate detection paths for 21 CGs. Build a config array and iterate.

