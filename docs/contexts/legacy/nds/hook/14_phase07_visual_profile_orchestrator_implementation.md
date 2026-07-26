# 14 — NDS Hook Phase 07: Visual Profile Orchestrator

## Purpose

Phase 07 adds a central view-control layer for the Hook stack.

The previous phases are now structurally independent:

```text
Phase 01 => Node source adapter
Phase 02 => strict X-sequence / CycleHook object
Phase 03 => Y-axis opposite extremes
Phase 04 => ND / death / X-closure lifecycle
Phase 05 => Hook Type A/B/C classifier
Phase 06 => X/Y closure quality score
```

That modularity is correct, but it creates a chart-management problem: if all
phases draw at the same time, the chart becomes noisy and stale objects from a
previous view can remain visible after a profile switch.

Phase 07 solves that problem by adding a single **view-profile orchestrator**.
It does not build new Hook objects and it does not change the Rally/F-counting
logic. It only transforms the already existing Phase 01..Phase 06 configs before
those phases run.

## Non-execution boundary

Phase 07 is still diagnostics and visualization infrastructure only.

Forbidden in this phase:

```text
OrderSend
OrderCheck
CTrade
broker request construction
volume sizing
risk sizing
entry logic
exit logic
position management
live trading behavior
```

## New files

```text
mql5/Include/FlagCountingPhoenix/FP_HookPhase07Types.mqh
mql5/Include/FlagCountingPhoenix/FP_HookPhase07Rules.mqh
mql5/Include/FlagCountingPhoenix/FP_HookPhase07Visual.mqh
mql5/Include/FlagCountingPhoenix/FP_HookPhase07Export.mqh
mql5/Include/FlagCountingPhoenix/FP_HookPhase07Engine.mqh
```

## Central expert integration

The central expert now includes:

```cpp
#include "../../Include/FlagCountingPhoenix/FP_HookPhase07Engine.mqh"
```

and loads/applies the Phase 07 profile after Phase 01..Phase 06 configs are
loaded, but before the Hook phases execute:

```cpp
FP_HookPhase07Config hook_phase07_cfg;
FP_LoadHookPhase07Config(hook_phase07_cfg);

FP_HookPhase07Report hook_phase07_report;
FP_ApplyHookPhase07Profile(hook_phase07_cfg,
                           hook_phase01_cfg, hook_phase02_cfg, hook_phase03_cfg,
                           hook_phase04_cfg, hook_phase05_cfg, hook_phase06_cfg,
                           hook_phase07_report);
```

## Inputs

```text
InpHookPhase07Enabled
InpHookPhase07ViewProfile
InpHookPhase07RespectIndividualPhaseEnabled
InpHookPhase07ForceEnableRequiredPhases
InpHookPhase07ShowLabels
InpHookPhase07GlobalExportCsv
InpHookPhase07GlobalPrintSummary
InpHookPhase07GlobalPrintSamples
InpHookPhase07ExportProfileCsv
InpHookPhase07PrintSummary
InpHookPhase07CleanBeforeApply
InpHookPhase07CleanP01Objects
InpHookPhase07CleanP02Objects
InpHookPhase07CleanP03Objects
InpHookPhase07CleanP04Objects
InpHookPhase07CleanP05Objects
InpHookPhase07CleanP06Objects
InpHookPhase07CleanP07Objects
InpHookPhase07MaxNodesToDraw
InpHookPhase07MaxSequencesToDraw
InpHookPhase07SampleLimit
InpHookPhase07Folder
InpHookPhase07ObjectPrefix
```

Default behavior is intentionally conservative:

```text
InpNDSHookDisplayFamily = RALLY_ONLY
InpHookPhase07ViewProfile = KEEP_INPUTS
InpHookPhase07CleanBeforeApply = false
InpHookPhase07GlobalExportCsv = false
```

Therefore the existing Rally/F-counting mode remains unchanged unless the user
explicitly selects Hook display mode.

## View profiles

### KEEP_INPUTS

Leaves the Phase 01..Phase 06 drawing/export inputs exactly as the user set
them. Phase 07 still applies the shared display family and global draw budget.

Use this when debugging a very specific phase manually.

### RAW_NODES

Shows only the Hook node-source adapter.

```text
Phase 01 draw: on
Phase 02..06 draw: off
```

Use this when validating whether peaks/valleys from the central anatomy are
stable enough for Hook construction.

### SEQUENCE_XY

Shows the strict X-sequences and their opposite Y evidence.

```text
Phase 02 draw: origin, X nodes, X lines, death boundary
Phase 03 draw: Y extremes, Y lines, X references
Other phases draw: off
```

Use this when checking whether CycleHook anatomy exists before lifecycle and
classification logic are considered.

### LIFECYCLE

Shows the return-toward-origin layer:

```text
ND candidate
origin-return death boundary
X-closure threshold
X-closure event
```

Use this when validating alive / ND / dead / X-closed states.

### TYPE_QUALITY

Shows the final human-readable Hook classification and quality layer:

```text
Phase 05: Type A/B/C anchor and comparison evidence
Phase 06: X/Y closure quality score and projection evidence
```

Use this when the lower-level anatomy is already trusted and the chart should
focus on final structural interpretation.

### QUALITY_FOCUS

Shows only Phase 06 quality evidence.

```text
XY anchor
quality bucket
quality score
Y-step projection lines
```

Use this before training/audit when you want a clean surface containing only the
most compressed Hook structural score.

### FULL_DEBUG

Shows all phase layers.

Use this only for short visual smoke tests, because it can intentionally produce
a dense chart.

### AUDIT_EXPORT_ONLY

Turns drawing off and turns CSV export on for Phase 01..Phase 06.

Use this for data extraction and audit when the chart itself should stay clean.

## Stale object cleanup

Phase 07 can delete all previous Hook objects before applying a new view profile:

```text
InpHookPhase07CleanBeforeApply = true
```

Cleanup is prefix-based and individually controllable:

```text
InpHookPhase07CleanP01Objects
InpHookPhase07CleanP02Objects
InpHookPhase07CleanP03Objects
InpHookPhase07CleanP04Objects
InpHookPhase07CleanP05Objects
InpHookPhase07CleanP06Objects
InpHookPhase07CleanP07Objects
```

This is useful when switching from `FULL_DEBUG` to `QUALITY_FOCUS`, because a
phase that no longer draws should not leave old objects on the chart.

## CSV output

When enabled:

```text
InpHookPhase07ExportProfileCsv = true
```

Phase 07 writes:

```text
FlagCountingPhoenix\hook_phase07_view_profile.csv
```

The file records:

```text
schema_version
version
display_family
view_profile
p01..p06 enabled flags
p01..p06 draw flags
p01..p06 export flags
draw budgets
objects_deleted
status
reason
```

This is not a market-data export. It is a run-configuration audit row so that a
screenshot or CSV bundle can be traced back to the exact Hook view profile used.

## Acceptance checklist

```text
RALLY_ONLY remains unchanged.
HOOK_ONLY can show a clean Hook-only chart.
RALLY_AND_HOOK can show both layers without relying on shared object prefixes.
QUALITY_FOCUS hides lower-level debug clutter.
FULL_DEBUG can still show all evidence layers.
AUDIT_EXPORT_ONLY can write CSVs without drawing Hook objects.
Phase 07 does not add execution behavior.
```
