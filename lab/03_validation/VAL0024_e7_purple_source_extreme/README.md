# VAL0024 — E0007 Purple Source Extreme Execution Validation

## Purpose

Validate the new E0007 execution template against the purple-zone examples.

The core hypothesis:

```text
Not every purple zone is tradable.
Tradable candidates are source / source-revisit / early ladder zones with open destination and tiny stop.
```

## Required chart/test setup

The screenshots were generated with:

```text
L = 2
```

So start with:

```text
InpSourceL = 2
InpZoneRatio = 0.90
```

## Test matrix

### A. Source second revisit

```text
InpMinSourceSurvivalBars = 0
InpEntryMode = DAL_E0007_ENTRY_SOURCE_SECOND_REVISIT
InpStopMode = DAL_E0007_STOP_SECONDARY_NODE
InpMinFirstReactionR = 2
InpMinPotentialR = 40
```

### B. Secondary-node zone

```text
InpEntryMode = DAL_E0007_ENTRY_SECONDARY_NODE_ZONE
InpStopMode = DAL_E0007_STOP_SECONDARY_NODE
```

### C. Oracle purple research

```text
InpMinSourceSurvivalBars = 500
InpEntryMode = DAL_E0007_ENTRY_ALL_MODES
InpTradingEnabled = false
InpPrintLogs = true
```

This mode is not live-valid. It is for reverse-engineering the purple atlas.

## Metrics to record

For every run record:

```text
candidates
sent/planned
rejected
entry mode
stop mode
firstReactionR
potentialR
TP modified/waiting/rejected
```

The first goal is not profit. The first goal is to see whether the executor selects the same family of zones seen in the screenshots.
