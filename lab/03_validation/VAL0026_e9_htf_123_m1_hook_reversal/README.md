# VAL0026 — E0009 HTF 123 M1 Hook Counter Validation

## Purpose

Test the simplified rule:

```text
HTF 3 higher highs / 3 lower lows closed → enter counter-direction on every M1 hook
```

## Test matrix

### A. Fixed 50R

```text
InpHTFTimeframe = PERIOD_M15
InpExecutionTF = PERIOD_M1
InpExitMode = DAL_E0009_EXIT_FIXED_R
InpFixedR = 50
InpTradingEnabled = false
```

### B. Fixed 100R

```text
InpFixedR = 100
```

### C. HTF point-2 target

```text
InpExitMode = DAL_E0009_EXIT_HTF_POINT_2
```

### D. Both directions for sanity only

```text
InpCounterMode = DAL_E0009_COUNTER_BOTH_FOR_TEST
```

This ignores the counter-direction rule and prints both BUY/SELL hook plans for comparison.

## Release 101 definition

HTF 123 now means:

```text
last 3 confirmed HIGH nodes are rising -> SELL M1 HIGH hooks
last 3 confirmed LOW nodes are falling -> BUY M1 LOW hooks
```

## Release 102 TP test

Main exit test:

```text
InpExitMode = DAL_E0009_EXIT_HTF_THIRD_OPPOSITE_SWING
InpHTFTpSwingCount = 3
```

Expected behavior:

```text
BUY  -> TP is moved to 3rd confirmed HTF HIGH after entry
SELL -> TP is moved to 3rd confirmed HTF LOW after entry
```

## Release 103 no-trade diagnostic test

First run plan-only:

```text
InpTradingEnabled = false
InpOrderMode = DAL_E0009_ORDER_AUTO
InpMaxHookCandidatesPerBar = 6
InpPrintRejectLogs = true
InpRejectHuntedM1Hook = true
```

If `hookHuntedReject` is high, test:

```text
InpRejectHuntedM1Hook = false
```

If `geometryReject` is high, test:

```text
InpOrderMode = DAL_E0009_ORDER_AUTO
```

If `sentOrPlan` is positive but no real trades are sent:

```text
InpTradingEnabled = true
```
