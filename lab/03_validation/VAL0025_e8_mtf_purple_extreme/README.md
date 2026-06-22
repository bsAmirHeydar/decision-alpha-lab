# VAL0025 — E0008 MTF Purple Extreme Validation

## Goal

Find whether multi-timeframe context can filter purple/source zones into tiny-stop high-R candidates.

## Main settings

```text
InpContextL = 2
InpExecutionL = 2
InpEntryMode = DAL_E0008_ENTRY_ALL_MODES
InpTradingEnabled = false
InpMinPotentialR = 50
```

## Test matrix

### A. No-future mode

```text
InpMinSourceSurvivalBars = 0
InpMinAlignedContexts = 2
InpRejectIfAnyContextConflicts = true
```

### B. Oracle purple mode

```text
InpMinSourceSurvivalBars = 500
InpEntryMode = DAL_E0008_ENTRY_ALL_MODES
InpTradingEnabled = false
```

### C. Micro tiny-stop mode

```text
InpEntryMode = DAL_E0008_ENTRY_MICRO_NODE_REVISIT
InpStopMode = DAL_E0008_STOP_MICRO_NODE
InpTargetMode = DAL_E0008_TARGET_CONTEXT_DESTINATION
InpMinPotentialR = 50
```

## What to inspect in the log

```text
DAL_E0008_PLAN
DAL_E0008_TRIGGER_REJECT
DAL_E0008_PLAN_REJECT
DAL_E0008_AUDIT
```

A good candidate should show:

```text
aligned >= required
R >= 50
microNode exists
entry close to micro extreme
target = context destination
```

## Important

Do not judge this by number of trades.  
The desired outcome is a small number of very asymmetric plans.
