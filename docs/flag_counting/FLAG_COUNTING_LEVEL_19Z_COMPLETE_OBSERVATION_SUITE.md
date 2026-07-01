# Flag Counting Level 19Z — Complete Observation Suite

## Purpose

Level 19Z completes Level 19 as a read-only observation layer.

The goal is to finish Level 19 without pushing into entry, paper trading, broker requests, or real execution.

Level 19Z adds the final diagnostic outputs needed before Level 20 Entry Bridge.

## Hard boundary

Level 19Z does not modify:

```text
FP_Renderer.mqh
FP_RenderRules.mqh
FP_RenderTypes.mqh
F / Hook / Node drawing logic
curves
lines
RTV / zone objects
object cleanup behavior
license logic
execution logic
```

It remains:

```text
read-only
CSV-only by default
panel off by default
print silent by default
no execution
```

## Previous Level 19 outputs

Level 19 keeps all previous outputs:

```text
latest_state_gate_level19.csv
state_gate_level19_closed_bar_ledger.csv
state_gate_level19_state_delta.csv
state_gate_level19_transition_events.csv
```

## New Level 19Z outputs

Level 19Z adds:

```text
state_gate_level19_transition_summary.csv
state_gate_level19_transition_stability.csv
state_gate_level19_regime_labels.csv
state_gate_level19_completion.csv
```

## New inputs

```text
InpLevel19StateGateExportTransitionSummaryCsv = true
InpLevel19StateGateExportTransitionStabilityCsv = true
InpLevel19StateGateExportRegimeLabelCsv = true
InpLevel19StateGateExportCompletionCsv = true
```

## Transition Summary

The transition summary is overwritten on each run and stores accumulated counts since the EA instance started:

```text
total transition rows
baseline rows
no-change rows
health rows
major rows
structural rows
minor rows
F1 expansion rows
F2 expansion rows
F3 expansion rows
F-count contraction rows
ND change rows
Hook change rows
visibility change rows
event count change rows
latest visible event change rows
latest visible hook change rows
state key change rows
dominant transition family
dominant severity
```

## Transition Stability

The transition stability file appends one row per closed-bar transition and tracks:

```text
current transition family
current transition severity
previous transition family
current streak
stability status
stability quality
bias hint
action hint
```

It can classify persistence as:

```text
STABILITY_SINGLE_OR_RESET
STABILITY_REPEAT
STABILITY_STABLE
STABILITY_PERSISTENT
```

## Regime Labels

Regime labels are diagnostic only.

Examples:

```text
REGIME_F3_STRUCTURAL_EXPANSION
REGIME_F2_STRUCTURAL_EXPANSION
REGIME_F1_STRUCTURAL_EXPANSION
REGIME_F_COUNT_CONTRACTION
REGIME_ND_REBUILD
REGIME_HOOK_REBUILD
REGIME_VISIBILITY_RESHUFFLE
REGIME_STABLE_NO_CHANGE
REGIME_HEALTH_REVIEW
REGIME_OBSERVE_ONLY_UNCLASSIFIED
```

## Completion Snapshot

The completion file tells whether Level 19 is ready to hand off to Level 20:

```text
LEVEL19_COMPLETE_READY_FOR_LEVEL20_ENTRY_BRIDGE
LEVEL19_COMPLETE_BLOCKED_TIMEBASE
LEVEL19_COMPLETE_RENDER_HEALTH_REVIEW
LEVEL19_COMPLETE_VALIDATION_HEALTH_REVIEW
LEVEL19_COMPLETE_EMPTY_STATE_OBSERVED
```

The normal next step when ready is:

```text
NEXT_LEVEL_20_ENTRY_BRIDGE_XY_ANCHOR_JOIN
```

## What Level 19 is now responsible for

Level 19 now owns:

```text
state snapshot
closed-bar state history
closed-bar delta history
transition event classification
transition summary
transition stability
regime labels
Level 19 completion status
```

## What Level 19 must not own

Level 19 must not own:

```text
entry anchors
stop anchors
target anchors
RR calculation
paper orders
broker requests
real execution
risk sizing
```

Those belong to Level 20 and later.

## Final Level 19 conclusion

Level 19 is now complete as an observation and diagnostic layer.

The next correct layer is:

```text
Level 20 — Entry Bridge / X-Y Anchor Join
```

Level 20 should connect the Level 19 Y-axis state/transition/regime context to X-axis structural anchors:

```text
entry anchor
invalidation anchor
destination anchor
```

without sending orders.
