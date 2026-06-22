# E0008 — MTF Purple Extreme Executor

E0008 is the execution template that matches the user objective more directly than E0007:

> We do not want every purple zone.  
> We want purple/source zones that sit inside the correct higher-timeframe context and give a tiny local stop with 50R/100R path potential.

## Architecture

```text
Big Context TFs  → direction + destination
Local Context TF → where in the path to hunt the extreme
Execution TF     → tiny-stop trigger
R Filter         → reject unless destination/risk is extreme
```

Default stack:

```text
Context TF1 = H1
Context TF2 = M15
Context TF3 = H4 optional
Local TF    = M15
ExecutionTF = chart timeframe
L           = 2
```

The default `L=2` is intentional because the purple screenshots were generated with L=2.

## What counts as context

Each context timeframe builds M0001 node/zone events and searches for a source-like event:

```text
first touch confirmed
first touch did not hunt the node
first reaction after touch >= InpMinFirstReactionR
optional survival >= InpMinSourceSurvivalBars
destination exists in recent extremes
```

This is not yet a full human-grade hook engine, but it is the first testable proxy:

```text
purple/source behavior + open destination
```

## Live mode vs oracle purple research

```text
InpMinSourceSurvivalBars = 0
```

No future survival label is required.

```text
InpMinSourceSurvivalBars = 500
```

Oracle/research mode: only zones that already survived 500 bars are used.  
This is for reverse engineering and must not be treated as live-valid.

## Entry modes

```text
DAL_E0008_ENTRY_MICRO_NODE_REVISIT
DAL_E0008_ENTRY_LOCAL_SOURCE_REVISIT
DAL_E0008_ENTRY_LOCAL_SECONDARY_NODE
DAL_E0008_ENTRY_EARLY_LADDER_STEP
DAL_E0008_ENTRY_ALL_MODES
```

### MICRO_NODE_REVISIT

Uses the latest same-side execution-timeframe node after the local source.

For BUY:

```text
latest LOW node after local source
entry = node zone upper + spread
SL = micro LOW / selected stop
```

For SELL:

```text
latest HIGH node after local source
entry = node zone lower
SL = high-side anchor + spread
```

### LOCAL_SOURCE_REVISIT

Uses the local context source zone directly.

### LOCAL_SECONDARY_NODE

Finds a same-side node inside the first source touch/base window and uses its zone.

### EARLY_LADDER_STEP

Uses the same micro-node trigger but is separated for test reporting because early ladder behavior is different from source reversal behavior.

## Stop modes

```text
DAL_E0008_STOP_MICRO_NODE
DAL_E0008_STOP_LOCAL_SOURCE_ZONE_BACK
DAL_E0008_STOP_LOCAL_SOURCE_NODE
DAL_E0008_STOP_SECONDARY_NODE
```

SELL stops always include spread.

## Target modes

```text
DAL_E0008_TARGET_CONTEXT_DESTINATION
DAL_E0008_TARGET_FIXED_R
DAL_E0008_TARGET_NTH_OPPOSITE_NODE
DAL_E0008_TARGET_NONE
```

Default:

```text
InpTargetMode = DAL_E0008_TARGET_CONTEXT_DESTINATION
InpMinPotentialR = 50
```

This is the important change from E0007.  
The target is the higher-timeframe destination, not a small local exit.  
This is what makes 50R/100R tests possible.

## Suggested tests

### Test 1 — plan-only all modes

```text
InpTradingEnabled = false
InpEntryMode = DAL_E0008_ENTRY_ALL_MODES
InpMinPotentialR = 50
InpMinAlignedContexts = 2
InpRejectIfAnyContextConflicts = true
```

### Test 2 — micro-node tiny stop

```text
InpEntryMode = DAL_E0008_ENTRY_MICRO_NODE_REVISIT
InpStopMode = DAL_E0008_STOP_MICRO_NODE
InpTargetMode = DAL_E0008_TARGET_CONTEXT_DESTINATION
```

### Test 3 — oracle purple source

```text
InpMinSourceSurvivalBars = 500
InpTradingEnabled = false
InpEntryMode = DAL_E0008_ENTRY_ALL_MODES
```

Use this only to compare which entry family catches the same purple winners seen in the screenshots.

## What this release still does not claim

This is not the final brain.

It adds MTF direction/destination/context and micro extreme triggers, but the true next modules should be:

```text
M0007_FractalHookContextReporter
M0008_OpenCountDestinationMap
M0009_PurpleRoleAtlas
```

E0008 is the testable execution shell for the current purple-source idea.


## Release 101 — performance scheduler

E0008 now runs on the execution timeframe candle only. The default execution timeframe is M1:

```text
InpExecutionTF = PERIOD_M1
```

No tick-by-tick structural rebuild is done. `OnTick()` only checks whether a new execution candle has opened.

### Cached context maps

Higher-timeframe context maps are cached and refreshed only when their own timeframe opens a new candle:

```text
InpCacheContextMaps = true
InpUpdateContextOnlyOnItsOwnNewBar = true
```

This means H1 context is not rebuilt on every M1 candle. It is rebuilt on the next H1 candle, or when forced.

### Separate bar budgets

```text
InpContextBarsPerTF = 1800
InpLocalBars = 1200
InpExecutionBars = 700
```

The execution map is the only map rebuilt every execution candle, and it uses the smallest bar budget.

### Force refresh

```text
InpForceContextRefreshEveryExecBars = 0
```

`0` means off. Set this to a value like `200` if a periodic full refresh is needed.

### Logging

Skip/reject logs are off by default:

```text
InpPrintSkipLogs = false
```

Plan logs remain separately controllable:

```text
InpPrintPlanLogs = true
```

### Cross-timeframe index fix

Micro triggers no longer compare an M1 node index with an M15/H1 context index. They now use event/node times, so the local-context source and the execution-timeframe trigger are aligned by time, not by incompatible bar indexes.
