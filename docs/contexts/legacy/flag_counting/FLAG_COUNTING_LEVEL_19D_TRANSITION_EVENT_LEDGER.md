# Flag Counting Level 19D — Closed-Bar Transition Event Ledger

## Purpose

Level 19D adds a transition-event ledger on top of Level 19C.

Level 19C measures numeric deltas between closed-bar states.

Level 19D classifies those deltas into transition families and severities.

This layer is still read-only and diagnostic-only.

## New output

Level 19D keeps the previous Level 19 outputs:

```text
MQL5/Files/FlagCountingPhoenix/latest_state_gate_level19.csv
MQL5/Files/FlagCountingPhoenix/state_gate_level19_closed_bar_ledger.csv
MQL5/Files/FlagCountingPhoenix/state_gate_level19_state_delta.csv
```

and adds:

```text
MQL5/Files/FlagCountingPhoenix/state_gate_level19_transition_events.csv
```

## New input

```text
InpLevel19StateGateExportTransitionEventCsv = true
```

## Transition families

The layer can classify transitions as:

```text
TRANSITION_BASELINE_FIRST_ROW
TRANSITION_RENDER_HEALTH_CHANGE
TRANSITION_VALIDATION_HEALTH_CHANGE
TRANSITION_F3_EXPANSION
TRANSITION_F2_EXPANSION
TRANSITION_F1_EXPANSION
TRANSITION_F_COUNT_CONTRACTION
TRANSITION_ND_COUNT_CHANGE
TRANSITION_HOOK_COUNT_CHANGE
TRANSITION_VISIBILITY_CHANGE
TRANSITION_EVENT_COUNT_CHANGE
TRANSITION_LATEST_VISIBLE_EVENT_CHANGED
TRANSITION_LATEST_VISIBLE_HOOK_CHANGED
TRANSITION_STATE_KEY_CHANGED
TRANSITION_NO_CHANGE
```

## Transition severities

```text
TRANSITION_SEVERITY_BASELINE
TRANSITION_SEVERITY_HEALTH
TRANSITION_SEVERITY_MAJOR
TRANSITION_SEVERITY_STRUCTURAL
TRANSITION_SEVERITY_MINOR
TRANSITION_SEVERITY_NONE
```

## Bias hints

The row includes a non-executable bias hint based only on the latest visible event/hook direction:

```text
BIAS_HINT_LATEST_VISIBLE_EVENT_BULLISH
BIAS_HINT_LATEST_VISIBLE_EVENT_BEARISH
BIAS_HINT_LATEST_VISIBLE_HOOK_BULLISH
BIAS_HINT_LATEST_VISIBLE_HOOK_BEARISH
BIAS_HINT_NEUTRAL_OR_UNKNOWN
BIAS_HINT_BASELINE_NO_PRIOR_STATE
```

These are diagnostic labels only.

They are not trade signals.

## Action hints

The row also includes an observe-only action hint:

```text
ACTION_HINT_REVIEW_REPORTS_ONLY_NO_EXECUTION
ACTION_HINT_MAJOR_STRUCTURAL_TRANSITION_OBSERVE_ONLY
ACTION_HINT_STRUCTURAL_TRANSITION_OBSERVE_ONLY
ACTION_HINT_MINOR_STATE_UPDATE_OBSERVE_ONLY
ACTION_HINT_NO_CHANGE
ACTION_HINT_BASELINE_OR_UNKNOWN_NO_EXECUTION
```

## Duplicate behavior

The transition-event ledger writes at most one row per closed-bar time while the EA instance is running.

Repeated ticks on the same closed bar are skipped in memory.

## Hard no-touch boundary

Level 19D does not modify:

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

## Panel and print behavior

The Level 19 panel remains disabled by default:

```text
InpLevel19StateGatePanelEnabled = false
```

Prints remain disabled by default.

## Why this layer matters

Level 19B stores closed-bar state history.

Level 19C measures numeric state changes.

Level 19D converts those changes into classified transition events, which later research layers can group, filter, and compare without touching chart visuals or execution.
