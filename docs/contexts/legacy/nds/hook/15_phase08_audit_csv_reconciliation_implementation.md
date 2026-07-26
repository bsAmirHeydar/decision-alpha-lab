# 15 — Hook Phase 08 Implementation: Audit + CSV Reconciliation

## Phase Goal

Phase 08 adds the audit reconciliation layer for the modular NDS Hook stack.

The goal is not to create a new Hook signal. The goal is to answer one question:

```text
Does the Hook chart view, phase configuration, runtime report chain, and CSV output agree?
```

This phase is the bridge between visual engineering and later training readiness.

## Position in the Hook Pipeline

Phase 08 runs after:

```text
Phase 01 => node source adapter
Phase 02 => CycleHook / strict X-sequence builder
Phase 03 => Y-axis opposite extremes
Phase 04 => ND / death / X-closure lifecycle
Phase 05 => Hook Type A/B/C classifier
Phase 06 => X/Y closure quality scoring
Phase 07 => visual profile orchestrator
```

Phase 08 consumes the reports/configs of those phases and writes audit outputs.

It does not rebuild Hook objects and does not draw chart objects.

## Added Files

```text
mql5/Include/FlagCountingPhoenix/FP_HookPhase08Types.mqh
mql5/Include/FlagCountingPhoenix/FP_HookPhase08Rules.mqh
mql5/Include/FlagCountingPhoenix/FP_HookPhase08Visual.mqh
mql5/Include/FlagCountingPhoenix/FP_HookPhase08Export.mqh
mql5/Include/FlagCountingPhoenix/FP_HookPhase08Engine.mqh
```

Documentation:

```text
docs/contexts/legacy/nds/hook/15_phase08_audit_csv_reconciliation_implementation.md
docs/contexts/legacy/nds/hook/hook_phase08_manifest.json
```

## New Expert Inputs

```text
InpHookPhase08Enabled
InpHookPhase08AllowRallyOnlyAudit
InpHookPhase08ExportCsv
InpHookPhase08ExportPhaseMatrixCsv
InpHookPhase08ExportIntegrityCsv
InpHookPhase08PrintSummary
InpHookPhase08PrintSamples
InpHookPhase08RequireRuntimeReportOk
InpHookPhase08RequirePhaseChainAlignment
InpHookPhase08RequireUniqueObjectPrefixes
InpHookPhase08RequireNonnegativeCounts
InpHookPhase08RequireAuditExportProfileAlignment
InpHookPhase08RequireNoFileErrors
InpHookPhase08RequireP06RecordsForQualityAudit
InpHookPhase08MaxWarningsAllowed
InpHookPhase08SampleLimit
InpHookPhase08Folder
InpHookPhase08ObjectPrefix
```

Safe defaults:

```text
InpHookPhase08Enabled = true
InpHookPhase08AllowRallyOnlyAudit = false
InpHookPhase08ExportCsv = false
InpHookPhase08PrintSummary = false
InpHookPhase08PrintSamples = false
```

So in default `RALLY_ONLY` mode, this phase skips itself and Rally/F-counting remains protected.

## Audit Checks

### 1. Runtime Report OK

For every enabled Hook phase:

```text
attempted == true
ok == true
```

If not, Phase 08 emits a blocker.

### 2. Phase Chain Alignment

Phase 08 verifies that downstream phases saw the same upstream universe:

```text
P03.phase02_sequences_seen == P02.sequences_total
P04.phase03_records_seen   == P03.records_total
P05.phase04_records_seen   == P04.records_total
P06.phase05_records_seen   == P05.records_total
```

This protects the dataset from silent desynchronization.

### 3. Unique Object Prefixes

Every Hook phase must have a unique chart object prefix:

```text
P01 != P02 != P03 != P04 != P05 != P06 != P07 != P08
```

This prevents cleanup logic from deleting another phase's objects.

### 4. Nonnegative Counters

Runtime counters must never be negative:

```text
records
positive / negative counts
files_written
file_errors
objects_created
objects_deleted
drawn counts
```

Negative counters indicate corrupted report accounting.

### 5. Export/File Error Check

If a phase has export enabled, Phase 08 requires:

```text
file_errors == 0
```

### 6. Audit Profile Alignment

If Phase 07 is set to:

```text
AUDIT_EXPORT_ONLY
```

then at least one export surface should be enabled. Otherwise the profile is logically empty.

### 7. Optional Phase 06 Record Requirement

Optional input:

```text
InpHookPhase08RequireP06RecordsForQualityAudit
```

When enabled, Phase 08 warns if Phase 06 produced no quality records.

This is useful before preparing Hook features for training.

## CSV Outputs

When `InpHookPhase08ExportCsv = true`, Phase 08 can write:

```text
hook_phase08_audit_summary.csv
hook_phase08_phase_matrix.csv
hook_phase08_integrity_checks.csv
```

### Summary CSV

One-row run manifest containing:

```text
schema_version
version
symbol
period
display_family
view_profile
status
ok
reason
phase counts
finding counts
chain/prefix/runtime/export failure counts
Phase 06 quality snapshot
file counters
```

### Phase Matrix CSV

One row per Hook phase:

```text
phase
cfg_enabled
attempted
ok
status
reason
export_enabled
files_written
file_errors
records_seen
positive_seen
negative_seen
objects_created
objects_deleted
drawn_seen
```

### Integrity Checks CSV

One row per audit finding:

```text
check_code
severity
passed
phase
evidence
recommendation
```

## Status Model

Phase 08 produces:

```text
HOOK_P08_SKIPPED
HOOK_P08_OK
HOOK_P08_BLOCKED
HOOK_P08_WARNINGS_EXCEEDED
HOOK_P08_FILE_ERROR
```

A clean audit requires:

```text
blocker_count == 0
warning_count <= InpHookPhase08MaxWarningsAllowed
file_errors == 0
```

## Why This Phase Matters

Before training, the Hook dataset must be reproducible.

A visual label on chart is not enough. The system needs proof that:

```text
what was drawn
what was classified
what was scored
what was exported
what the runtime reports counted
```

are the same object universe.

Phase 08 creates that proof layer.

## Acceptance Checklist

```text
RALLY_ONLY remains unchanged by default
HOOK_ONLY can run Phase 08 audit
RALLY_AND_HOOK can run Phase 08 audit
Phase 08 writes no chart objects
Phase 08 sends no broker requests
Phase 08 does not mutate Hook classification
Phase 08 reports chain mismatch as blocker
Phase 08 reports duplicate object prefixes as blocker
Phase 08 reports export file errors as blocker
CSV phase matrix agrees with runtime reports
CSV integrity checks explain failures with evidence and recommendation
```

## No Execution Boundary

Phase 08 does not add:

```text
OrderSend
OrderCheck
CTrade
broker requests
risk sizing
volume sizing
live trading behavior
```
