# VAL0026 — E0009 Release 112 Validation

## Default intended behavior

```text
Macro: H4 nearest valid 4-node chain
Setup: M15 latest 4 same-type nodes only
Entry: M1 limit touch on hook extreme
Exit: H4 structural TP, 3-node pattern
Micro filter: off by default
Hunted hooks: rejected by default
Hook candidates: 0 = all eligible hooks
```

## Macro examples

```text
High1 > High2 > High3 > High4 -> SELL
Low1  < Low2  < Low3  < Low4  -> BUY
```

`1` is closest to live.

## Setup examples

Setup only checks latest nodes:

```text
latest 4 highs rising -> SELL setup
latest 4 lows falling -> BUY setup
```

Older valid chains are ignored at setup level.

## Backtest comparison

Test these separately:

```text
InpUseMacroModeFilter = true / false
InpRequireSetupAgreesWithMacro = true / false
InpMaxHookCandidatesPerBar = 0 / 1 / 3
InpRejectHuntedM1Hook = true / false
InpUseMicroOnlyFilter = false / true
```
