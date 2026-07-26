# Phase 09 — Visual Smoke Test Harness Implementation

## Purpose

Phase 09 is the visual smoke-test harness for the NDS Hook stack.

It does not create a new Hook signal, does not classify trade direction, and does
not execute orders. Its only purpose is to verify that the selected Phase 07 view
profile is visually coherent after Phase 01 through Phase 08 have run.

The core question is:

```text
Does the current Hook view profile leave the expected chart evidence and audit evidence behind?
```

## Position in the Hook stack

```text
Phase 01 => node-source adapter
Phase 02 => X-sequence builder
Phase 03 => Y-axis opposite extremes
Phase 04 => ND/death/X-closure lifecycle
Phase 05 => Hook Type A/B/C classifier
Phase 06 => X/Y closure quality score
Phase 07 => visual profile orchestrator
Phase 08 => audit + CSV reconciliation
Phase 09 => visual smoke-test harness
```

Phase 09 is therefore a post-run inspector. It consumes the configs and runtime
reports of the previous phases. It does not rebuild sequences and it does not
mutate Phase 01 through Phase 08 logic.

## New modules

```text
mql5/Include/FlagCountingPhoenix/FP_HookPhase09Types.mqh
mql5/Include/FlagCountingPhoenix/FP_HookPhase09Rules.mqh
mql5/Include/FlagCountingPhoenix/FP_HookPhase09Visual.mqh
mql5/Include/FlagCountingPhoenix/FP_HookPhase09Export.mqh
mql5/Include/FlagCountingPhoenix/FP_HookPhase09Engine.mqh
```

## Central expert integration

Phase 09 is included in:

```text
mql5/Experts/FlagCounting/FlagCountingPhoenixExperiment.mq5
```

Runtime order:

```text
P01 -> P02 -> P03 -> P04 -> P05 -> P06 -> P08 -> P09
```

Phase 07 is still applied before the Hook phases run because it transforms the
visual configs for Phase 01 through Phase 06.

## Inputs

```text
InpHookPhase09Enabled
InpHookPhase09AllowRallyOnlySmoke
InpHookPhase09RequirePhase08Ok
InpHookPhase09RequireCurrentProfileCoverage
InpHookPhase09RequireObjectCensus
InpHookPhase09RequireDrawContractWhenRecordsExist
InpHookPhase09RequireAuditOnlyNoHookDraw
InpHookPhase09RequireNoPhaseFileErrors
InpHookPhase09RequirePanelWhenEnabled
InpHookPhase09DrawPanel
InpHookPhase09CleanObjectsBeforeDraw
InpHookPhase09ExportCsv
InpHookPhase09ExportScenariosCsv
InpHookPhase09ExportObjectCensusCsv
InpHookPhase09ExportFindingsCsv
InpHookPhase09PrintSummary
InpHookPhase09PrintSamples
InpHookPhase09MaxWarningsAllowed
InpHookPhase09SampleLimit
InpHookPhase09Folder
InpHookPhase09ObjectPrefix
InpHookPhase09PanelCorner
InpHookPhase09PanelX
InpHookPhase09PanelY
InpHookPhase09PanelFontSize
InpHookPhase09PanelOkColor
InpHookPhase09PanelWarningColor
InpHookPhase09PanelBlockerColor
InpHookPhase09PanelTextColor
```

Default behavior is conservative:

```text
InpNDSHookDisplayFamily = RALLY_ONLY
InpHookPhase09AllowRallyOnlySmoke = false
InpHookPhase09DrawPanel = false
InpHookPhase09ExportCsv = false
```

Therefore existing Rally/F-counting behavior remains unchanged by default.

## Checks

### 1. Phase 08 audit dependency

If enabled, Phase 09 requires Phase 08 to be OK.

```text
PHASE08_AUDIT_OK
```

This prevents a clean-looking chart from being trusted when the runtime audit is
already blocked.

### 2. Object census by Hook prefix

Phase 09 counts chart objects by the object prefix of each Hook phase:

```text
P01 => DAL_HOOK_P01_
P02 => DAL_HOOK_P02_
P03 => DAL_HOOK_P03_
P04 => DAL_HOOK_P04_
P05 => DAL_HOOK_P05_
P06 => DAL_HOOK_P06_
P07 => DAL_HOOK_P07_
P08 => DAL_HOOK_P08_
P09 => DAL_HOOK_P09_
```

The object census answers:

```text
Which phase actually left visible chart evidence?
```

### 3. Current profile coverage

Phase 09 maps the selected Phase 07 view profile to expected smoke scenarios:

```text
RAW_NODES        => P01 node-source objects
SEQUENCE_XY      => P02/P03 X/Y sequence objects
LIFECYCLE        => P04 ND/death/X-closure objects
TYPE_QUALITY     => P05/P06 type + quality objects
QUALITY_FOCUS    => P06 quality objects
FULL_DEBUG       => P01..P06 visual surfaces
AUDIT_EXPORT_ONLY=> no required P01..P06 visual objects
```

### 4. Draw contract when records exist

If a phase has records and its draw surface is enabled, Phase 09 expects at
least one chart object for that phase.

This catches broken visual paths where internal reports say records exist but
nothing appears on chart.

### 5. Audit-only no-draw contract

When Phase 07 profile is `AUDIT_EXPORT_ONLY`, Phase 09 checks that stale P01
through P06 chart objects are not misleading the visual audit.

If stale objects are detected, the recommendation is to run with:

```text
InpHookPhase07CleanBeforeApply = true
```

### 6. Phase file-error health

Phase 09 also checks file errors from Phase 01 through Phase 08 so a visual
smoke pass is not accepted while export surfaces are failing.

## Optional panel

Phase 09 can draw a single status panel object:

```text
DAL_HOOK_P09_SMOKE_STATUS
```

The panel is disabled by default. When enabled, it summarizes:

```text
status
view profile
scenario pass count
Hook object count
blocker count
warning count
```

## CSV outputs

If enabled:

```text
hook_phase09_smoke_summary.csv
hook_phase09_smoke_scenarios.csv
hook_phase09_object_census.csv
hook_phase09_smoke_findings.csv
```

These files are designed to be joined with Phase 08 audit outputs before the
Hook stack is frozen as a training input.

## Non-execution boundary

Phase 09 must not contain:

```text
OrderSend
OrderCheck
CTrade
position sizing
volume sizing
broker requests
live trading behavior
```

It is a visual and audit harness only.

## Acceptance checklist

```text
RALLY_ONLY remains unchanged by default
HOOK_ONLY can run smoke without touching Rally rendering
RALLY_AND_HOOK can count Hook visual objects separately by prefix
AUDIT_EXPORT_ONLY can detect stale chart objects
selected Phase 07 profile has expected visual coverage
Phase 08 audit blockers block Phase 09 smoke pass
CSV outputs are optional and disabled by default
no execution path is introduced
```
