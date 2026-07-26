# E0007 — Purple Source Extreme Executor Template

E0007 is the first execution template for the idea that came from the purple-zone screenshots:

> Purple is not the signal. Purple is the context.  
> The trade is the local source/revisit/extreme trigger that appears after the zone proves it is not dead.

The screenshots were generated with `L=2`, so E0007 defaults to:

```text
InpSourceL = 2
InpZoneRatio = 0.90
```

## Why this is a template, not the final executor

The purple zones are an outcome map. A purple box means a zone eventually survived long enough. In live trading, we do not know that at the moment of first touch.

So E0007 supports two different research modes:

### 1. No-future/live-style source mode

```text
InpMinSourceSurvivalBars = 0
```

The EA does not require the future 500-bar survival label. It only asks whether the first touch:

- was confirmed,
- did not hunt the node,
- created enough first reaction,
- and can now be traded on the next revisit or secondary-node zone.

### 2. Oracle purple research mode

```text
InpMinSourceSurvivalBars = 500
```

This is not a live-valid execution mode. It is for reverse-engineering: "what if we only studied zones that later became purple-class zones?"

Use it to compare entry modes, not to claim a no-future edge.

## Entry modes

```text
DAL_E0007_ENTRY_FIRST_TOUCH_CONTEXT
DAL_E0007_ENTRY_SOURCE_SECOND_REVISIT
DAL_E0007_ENTRY_SECONDARY_NODE_ZONE
DAL_E0007_ENTRY_EARLY_LADDER_STEP
DAL_E0007_ENTRY_ALL_MODES
```

### SOURCE_SECOND_REVISIT

This is the main idea:

```text
first touch proves the zone is alive
first reaction confirms source behavior
the next revisit is traded
```

### SECONDARY_NODE_ZONE

This uses the same-side internal node that was created during the first touch/base window.

For a bullish source:

```text
LOW purple/source touch
internal LOW created during the base
next revisit to that secondary LOW zone is traded
stop behind the secondary LOW
```

For a bearish source:

```text
HIGH purple/source touch
internal HIGH created during the base
next revisit to that secondary HIGH zone is traded
SELL stop includes spread
```

### EARLY_LADDER_STEP

This is a placeholder execution family for continuation steps after a source rally starts. It currently uses the same candidate construction and is meant for comparing early ladder behavior.

## Stop modes

```text
DAL_E0007_STOP_ORIGIN_ZONE_BACK
DAL_E0007_STOP_ORIGIN_NODE
DAL_E0007_STOP_SECONDARY_NODE
DAL_E0007_STOP_MICRO_EXTREME
```

For SELL trades, stop includes spread.

## Destination/R filter

E0007 is built around asymmetric reward:

```text
R_potential = abs(destination - entry) / abs(entry - stop)
```

Default:

```text
InpUseDestinationRFilter = true
InpMinPotentialR = 40
```

The first destination implementation is intentionally simple: recent opposite-side extremes. This is a template. Later the destination map should be replaced by the full hook/open-count destination engine.

## Exit modes

```text
DAL_E0007_TARGET_NONE
DAL_E0007_TARGET_FIXED_R
DAL_E0007_TARGET_NTH_OPPOSITE_INTERNAL_NODE
```

Default:

```text
InpTargetMode = DAL_E0007_TARGET_NTH_OPPOSITE_INTERNAL_NODE
InpOppositeNodeTPCount = 3
```

For BUY positions, TP is moved to the N-th valid internal HIGH after entry.  
For SELL positions, TP is moved to the N-th valid internal LOW after entry.

## Recommended initial tests

### Test A — no-future source revisit

```text
InpMinSourceSurvivalBars = 0
InpEntryMode = DAL_E0007_ENTRY_SOURCE_SECOND_REVISIT
InpStopMode = DAL_E0007_STOP_SECONDARY_NODE
InpTargetMode = DAL_E0007_TARGET_NTH_OPPOSITE_INTERNAL_NODE
InpMinPotentialR = 40
```

### Test B — secondary-node entry

```text
InpMinSourceSurvivalBars = 0
InpEntryMode = DAL_E0007_ENTRY_SECONDARY_NODE_ZONE
InpStopMode = DAL_E0007_STOP_SECONDARY_NODE
InpMinPotentialR = 40
```

### Test C — oracle purple research

```text
InpMinSourceSurvivalBars = 500
InpEntryMode = DAL_E0007_ENTRY_ALL_MODES
InpTradingEnabled = false
InpPrintLogs = true
```

This prints plans only and lets us compare which entry mode would have selected the purple-class source zones.

## What is not final yet

This release does not claim to solve context.

The current HTF context input is present only as a placeholder. The correct future direction is:

```text
M0007_FractalContextReporter
→ source role map
→ open destination map
→ micro extreme trigger
→ E0007 execution
```

E0007 is the execution skeleton for testing entry modes around the source/purple behavior.


## Release 101 compile fix

Fixed the E0007 field-name mismatch:

```text
pricing.opposite_node_count      // wrong
pricing.opposite_node_tp_count   // correct
```

No execution logic changed.
