# Level 11.5 — Raw Audit Export / Report Engine

## Purpose

Level 11.5 makes the Phoenix engine auditable as data before Level 12 renderer/layout work. The chart is useful, but it is not proof. The export layer serializes the final Level 11 canonical stream into stable CSV files so hidden structures, losing candidates, parent links, lifecycle states, and canonical decisions can be inspected outside MetaTrader.

Pipeline position:

```text
Level 11 canonicalization
-> Level 11.5 raw audit export/report
-> Level 12 renderer and labels
```

## Active files

```text
mql5/Include/FlagCountingPhoenix/FP_ExportTypes.mqh
mql5/Include/FlagCountingPhoenix/FP_ExportRows.mqh
mql5/Include/FlagCountingPhoenix/FP_ExportEngine.mqh
mql5/Experts/FlagCounting/FlagCountingPhoenixExperiment.mq5
mql5/Include/FlagCountingPhoenix/FP_Types.mqh       # export counters only
mql5/Include/FlagCountingPhoenix/FP_Audit.mqh       # summary counters only
```

## Authority boundary

Level 11.5 is read-only.

It may:

```text
serialize events
serialize hooks
serialize summary counters
serialize manifest metadata
print FP_LEVEL11_5 sanity/sample logs
```

It may not:

```text
create events
hide events
repair events
repair hooks
assign identity
change parent links
change chart object visibility
change renderer output
change sequence ownership
```

## Inputs

```text
canonical FP_FlagEvent events[] after Level 11
canonical FP_HookBranch hooks[] after final Hook seed pass
FP_DetectResult result
FP_Config engine_cfg
FP_ExportConfig export_cfg
symbol / timeframe / bars / scale_count
```

## Inputs added to EA

```text
InpExportAuditFiles = false
InpExportFolder = "FlagCountingPhoenix"
InpExportRunTag = ""
InpExportVisibleOnly = false
InpExportEventsCsv = true
InpExportHooksCsv = true
InpExportSummaryCsv = true
InpExportManifestCsv = true
InpExportOverwriteLatest = true
InpExportMaxEvents = 0
InpExportMaxHooks = 0
InpPrintExportSanity = true
InpPrintExportSamples = false
InpExportSampleLimit = 5
```

## Output path

Default output folder:

```text
MQL5/Files/FlagCountingPhoenix/
```

Default overwrite mode:

```text
latest_events.csv
latest_hooks.csv
latest_summary.csv
latest_manifest.csv
```

Validation mode may set:

```text
InpExportOverwriteLatest = false
InpExportRunTag = "GOLD_M1_2026_01_01_2026_06_28_level11_5"
```

## Event CSV contract

`events.csv` exports both visible and hidden events by default. Each row includes:

```text
run metadata
canonical id
structural id
visual id
phase id
chain id
audit id
sequence and parent ids
level / direction / status
visibility and hidden_reason
source mode / fail-open / phase-boundary tags
body id / body status / body reason
internal pack id / count / valid12 / reason
F1 lifecycle status and F2 authorization
F2 lifecycle status, size gate, F3 authorization
F3 lifecycle status, OR gate, lock evidence
ownership state and phase owner
canonical state, rank, conflict group, invariant flags
Origin / Leg1 / Waist / Leg2 / Confirm / Invalid / ExtensionEnd node columns
final reason
```

This is intentionally wide. The goal is debugability, not compactness.

## Hook CSV contract

`hooks.csv` exports both visible and hidden Hook/ND contexts by default. Each row includes:

```text
branch id
scale_L
direction
status
node count
side kind
is_nd / nd_qualified
seeds_visible_f1
visible_main / hidden_reason
retrace ratio
max branch length
cycle-start broken flag
identity fields
start / cycle_start / extreme / resolve / n1 / n2 / n3 / n4 node columns
reason
```

## Summary CSV contract

`summary.csv` is a one-row aggregate view with core counters:

```text
raw nodes
canonical nodes
hooks
NDs
events
visible / hidden events
F1/F2/F3 totals
confirmed F1/F2
completed / locked F3
canonical invariant failures
post-canonical duplicate conflicts
parent missing after canonicalization
export counters
```

## Manifest CSV contract

`manifest.csv` is key/value metadata:

```text
run_id
export_time
symbol
timeframe
bars
scale_count
identity_generation_pass
identity_config_hash
visible_only
events_file
hooks_file
summary_file
events_written
hooks_written
files_written_before_manifest
file_errors_before_manifest
```

## Sanity log

When enabled, terminal output includes:

```text
FP_LEVEL11_5 attempted=... ok=... run_id=... files=... errors=... events_written=... hooks_written=...
```

`FP_SUMMARY` also includes export counters so export failures are visible in the normal run summary.

## Acceptance tests

- With `InpExportAuditFiles=false`, no files are written and engine behavior is unchanged.
- With export enabled, `events.csv`, `hooks.csv`, `summary.csv`, and `manifest.csv` are created under `MQL5/Files/FlagCountingPhoenix/`.
- `events.csv` contains hidden events unless `InpExportVisibleOnly=true`.
- Every hidden exported event carries `hidden_reason`.
- Renderer settings do not change exported event count.
- Re-running the same range with the same inputs and `InpExportRunTag` produces stable event order and IDs.
- The renderer can be disabled while Level 11.5 still exports the logical stream.

## Freeze criteria

Level 11.5 is frozen when a validation range can be inspected entirely from exported CSV files without looking at chart objects.
