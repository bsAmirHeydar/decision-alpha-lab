# Flag Counting Level 20 — Entry Bridge / X-Y Anchor Join

## Purpose

Level 20 is the first layer after the completed Level 19 observation suite.

Level 19 observes state, transitions, stability, regimes, and completion.

Level 20 creates a read-only bridge from that observed Y-axis state to X-axis structural anchors.

This is not execution.

This is not paper trading.

This is not a broker request.

## Hard boundary

Level 20 does not modify:

```text
FP_Renderer.mqh
FP_RenderRules.mqh
FP_RenderTypes.mqh
F / Hook / Node detection logic
curve drawing logic
line drawing logic
RTV / zone objects
chart objects
license logic
execution logic
```

It remains:

```text
CSV-only
read-only
panel off
print silent by default
no order
no paper order
no real execution
```

## New output

```text
MQL5/Files/FlagCountingPhoenix/state_gate_level20_entry_bridge.csv
```

## New inputs

```text
InpLevel20EntryBridgeEnabled = true
InpLevel20EntryBridgeExportCsv = true
InpLevel20EntryBridgePrintSummary = false
InpLevel20EntryBridgePreferLatestVisibleEvent = true
InpLevel20EntryBridgeAllowHookFallback = true
InpLevel20EntryBridgeMinRR = 1.0
InpLevel20EntryBridgeFolder = "FlagCountingPhoenix"
```

## What Level 20 produces

The Entry Bridge creates one current research row containing:

```text
source kind
source id
source level
source L
direction hint
Y-state label
Y-context label
entry anchor
invalidation anchor
destination anchor
current close
risk distance
reward distance
RR-like value
readiness status
block reason
execution status
```

## Y-axis source

The preferred Y-axis source is the latest visible Flag Counting event:

```text
F1
F2
F3
```

If no visible event is usable, Level 20 can fall back to the latest visible Hook / ND context.

This fallback is controlled by:

```text
InpLevel20EntryBridgeAllowHookFallback
```

## X-axis anchors

For event sources, Level 20 derives anchors as follows:

```text
entry anchor:
  event waist
  else event leg2
  else event origin fallback

invalidation anchor:
  event invalid
  else event origin fallback

destination anchor:
  event confirm
  else event leg1 fallback
  else event extension fallback
```

For Hook / ND fallback sources:

```text
entry anchor:
  hook extreme

invalidation anchor:
  hook start
  else hook cycle start

destination anchor:
  hook resolve
```

These are research anchors only.

They are not orders.

## Readiness statuses

Level 20 can output:

```text
ENTRY_RESEARCH_READY_NO_ORDER
ENTRY_BRIDGE_BLOCKED_TIMEBASE
ENTRY_BRIDGE_BLOCKED_RENDER_HEALTH
ENTRY_BRIDGE_BLOCKED_VALIDATION_HEALTH
ENTRY_BRIDGE_BLOCKED_NO_SOURCE
ENTRY_BRIDGE_BLOCKED_NO_DIRECTION
ENTRY_BRIDGE_BLOCKED_NO_ENTRY_ANCHOR
ENTRY_BRIDGE_BLOCKED_NO_INVALIDATION_ANCHOR
ENTRY_BRIDGE_BLOCKED_NO_DESTINATION_ANCHOR
ENTRY_BRIDGE_BLOCKED_ZERO_RISK_DISTANCE
ENTRY_BRIDGE_BLOCKED_ZERO_REWARD_DISTANCE
ENTRY_BRIDGE_BLOCKED_BAD_RR
```

## RR-like calculation

```text
risk_distance = abs(entry_anchor - invalidation_anchor)
reward_distance = abs(destination_anchor - entry_anchor)
rr_like = reward_distance / risk_distance
```

The minimum allowed research RR is controlled by:

```text
InpLevel20EntryBridgeMinRR
```

Default:

```text
1.0
```

## Execution status

Every row explicitly stays non-executable:

```text
REAL_EXECUTION_DISABLED_LEVEL20_ENTRY_BRIDGE_ONLY
```

## Why this layer matters

Level 19 tells us what the state is.

Level 20 answers the next necessary question:

```text
Given the current state, do we even have a usable entry / invalidation / destination anchor set?
```

This is the bridge from observation to paper intent, but it still does not create an intent or send any request.

## Next correct layer

After Level 20, the next layer should be:

```text
Level 21 — Paper Intent
```

Level 21 can convert an Entry Bridge row into a paper intent only if Level 20 says:

```text
ENTRY_RESEARCH_READY_NO_ORDER
```
