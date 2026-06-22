# E0009 — Reversal Macro / Latest Setup / Hook Executor

Release 112 aligns E0009 with the intended reversal logic.

## Layer 1 — Macro mode

Default:

```text
InpMacroModeTF = PERIOD_H4
InpMacroModeNodeCount = 4
InpMacroModeMaxAgeBars = 0
```

Index convention:

```text
1 = nearest confirmed same-type node to live
4 = farthest node in the 4-node chain
```

Macro scans backwards from live and finds the nearest valid same-type chain.

```text
High1 > High2 > High3 > High4  -> macro mode SELL
Low1  < Low2  < Low3  < Low4   -> macro mode BUY
```

This is reversal logic: rising highs define a sell-reversal context; falling lows define a buy-reversal context.

## Layer 2 — Middle setup

Default:

```text
InpSetupTF = PERIOD_M15
InpSetupNodeCount = 4
InpSetupMaxAgeBars = 0
```

Setup does **not** scan older chains. It only checks the latest N highs and latest N lows.

```text
latest 4 highs rising toward live  -> SELL setup
latest 4 lows falling toward live   -> BUY setup
```

If `InpRequireSetupAgreesWithMacro=true`, macro and setup must point to the same trade direction.

## Layer 3 — M1 hook entry

Default:

```text
InpExecutionTF = PERIOD_M1
InpRejectHuntedM1Hook = true
InpMaxHookCandidatesPerBar = 0
InpOrderMode = DAL_E0009_ORDER_LIMIT_REVISIT
```

`InpMaxHookCandidatesPerBar = 0` means scan all eligible hooks.

Entry is a limit touch on the hook extreme:

```text
BUY  on LOW hook  -> buy limit at hook low, SL behind the low node
SELL on HIGH hook -> sell limit at hook high, SL behind the high node
```

`InpRejectHuntedM1Hook=true` means consumed/hunted hooks are not allowed back into the game.

## Layer 4 — Micro filter

Default:

```text
InpUseMicroOnlyFilter = false
```

The filter is available but disabled by default.

## Layer 5 — Exit

Default:

```text
InpExitMode = DAL_E0009_EXIT_TF_MONOTONIC_PATTERN
InpExitTF = PERIOD_H4
InpExitNodeCount = 3
InpUseCurrentExitPatternAsInitialTP = false
```

Exit does not depend on entry time or entry price.

```text
BUY  -> when exit TF has 3 rising highs, TP = newest high
SELL -> when exit TF has 3 falling lows, TP = newest low
```

The EA continuously syncs TP for open positions when the structural exit condition exists.
