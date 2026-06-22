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

## Release 104 compile fix

Compile target remains:

```text
mql5/Experts/DecisionAlphaLab/Execution/E0009_HTF123M1HookCounterExecutor.mq5
```

This release only fixes the stale `one_order_per_hook` assignment and initializes local 123 detector node variables.

## Release 105 root no-trade test

Use the new defaults first:

```text
InpTradingEnabled = true
InpOrderMode = DAL_E0009_ORDER_MARKET_ON_CONFIRM
InpRejectHuntedM1Hook = false
InpMaxPendingPerSide = 0
InpMaxPositionsPerSide = 0
InpHTF123MaxAgeBars = 0
InpPrintRejectLogs = true
```

If still no trades, read the audit:

```text
no_closed_htf_123        -> HTF has no 3 rising highs / 3 falling lows
hookSeen = 0             -> no M1 hook of the needed side exists
hookAfterTimeReject high -> no hook after the HTF 123 close
hookBuilt > 0 but sent=0 -> order/risk/cap/duplicate issue
duplicateSkip high       -> same hook was already used
```

## Release 106 micro filter test

Start with:

```text
InpUseMicroOnlyFilter = true
InpMaxHookRiskToHTFAmplitude = 0.08
InpMicroAvgRangeBars = 80
InpMaxHookRiskToM1AvgRange = 3.0
InpMaxHookRiskPoints = 0
```

Tighter test:

```text
InpMaxHookRiskToHTFAmplitude = 0.04
InpMaxHookRiskToM1AvgRange = 2.0
```

Looser test:

```text
InpMaxHookRiskToHTFAmplitude = 0.12
InpMaxHookRiskToM1AvgRange = 4.0
```

Interpretation:

```text
hookMicroReject high + no trades      -> filter too tight
hookMicroReject low + equity leakage  -> filter too loose
```

## Release 107 compile fix

Compile target remains:

```text
mql5/Experts/DecisionAlphaLab/Execution/E0009_HTF123M1HookCounterExecutor.mq5
```

Audit output is now split across `AUDIT_A`, `AUDIT_B`, and `AUDIT_C`.

## Release 108 hook ledger test

Recommended comparison:

### Old behavior proxy

```text
InpOneTradePerHookForever = false
```

### Corrected one-hook-one-trade behavior

```text
InpOneTradePerHookForever = true
```

Expected effects:

```text
Total Trades should drop sharply.
duplicateSkip should rise.
Equity leakage should drop if repeated stale hooks were the main leak.
If profit collapses entirely, the previous result was mostly repeat exposure on the same hook.
```
