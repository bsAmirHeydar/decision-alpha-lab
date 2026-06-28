# Phoenix Flag Counting Implementation Ladder V1

This document is part of the implementation ladder for the Phoenix Flag Counting engine.

# Level 13 — Validation Suite / Acceptance Matrix

## Purpose

Level 13 turns Phoenix from a visually inspected overlay into a repeatable validation target.

It runs after:

```text
Level 11 canonicalization
-> Level 11.5 raw audit export/report
-> Level 12 renderer
-> Level 13 validation harness
```

The validation layer is read-only. It must never mutate events, hooks, visibility, identity, ownership, canonical state, export files from Level 11.5, or chart objects from Level 12.

## Active modules

```text
mql5/Include/FlagCountingPhoenix/FP_ValidationTypes.mqh
mql5/Include/FlagCountingPhoenix/FP_ValidationRules.mqh
mql5/Include/FlagCountingPhoenix/FP_ValidationAudit.mqh
mql5/Include/FlagCountingPhoenix/FP_ValidationEngine.mqh
```

The EA wiring lives in:

```text
mql5/Experts/FlagCounting/FlagCountingPhoenixExperiment.mq5
```

## Validation modes

### Baseline mode

Default when validation is enabled:

```text
InpValidationBaselineMode = true
```

Unset expected ranges are reported as `WARN baseline_required` and the actual values are written to `latest_validation.csv`. This is how a new broker/range creates its first baseline.

### Regression mode

After accepting a baseline, fill the expected min/max inputs. For exact expected values, set min and max to the same number.

Example:

```text
InpValidationExpectedMinVisibleEvents = 14
InpValidationExpectedMaxVisibleEvents = 14
```

If a patch intentionally changes a count, update the case report and explain why.

## EA controls

```text
InpValidationEnabled = false
InpValidationCaseId = "manual"
InpValidationSuiteTag = "phoenix_level13"
InpValidationFolder = "FlagCountingPhoenix"
InpValidationWriteCsv = true
InpValidationOverwriteLatest = true
InpValidationStrict = true
InpValidationBaselineMode = true
InpValidationRequireExportOk = false
InpValidationRequireRenderOk = true
InpValidationRequireNoCanonicalFailures = true
InpValidationRequireNoRenderErrors = true
InpValidationRequireNoExportErrors = false
```

Expected range inputs exist for:

```text
bars
scales
raw_nodes
canonical_nodes
hooks
nd
events
visible_events
hidden_events
f1
f2
f3
locked_f3
```

A value of `-1` means unbounded.

## Output

When enabled, Level 13 writes:

```text
MQL5/Files/FlagCountingPhoenix/latest_validation.csv
```

unless `InpValidationOverwriteLatest=false`, in which case the case id is used in the file name.

The terminal sanity log is:

```text
FP_LEVEL13
```

`FP_SUMMARY` also includes:

```text
validation_attempted
validation_ok
validation_checks
validation_pass
validation_fail
validation_warn
validation_skipped
validation_file_errors
```

## Built-in invariant checks

Level 13 always checks:

```text
visible + hidden == event count
hidden events have hidden_reason
visible events do not carry stale hidden_reason
visible F2/F3 children have visible parents
visible canonical_id is unique
canonical invariant failures are zero when required
renderer errors are zero when required
export errors are zero when required
```

Expected-count checks are added only when the corresponding range input is set.

## Validation case registry

The active registry is:

```text
docs/flag_counting/VALIDATION_CASE_REGISTRY.md
```

Artifacts should be stored under:

```text
lab/03_experiments/EXP_flag_counting/validation_cases/
```

## Mandatory case families

```text
FC-GC-001 node plateau/equality
FC-GC-002 Hook/ND branch size
FC-GC-003 flag body strict break
FC-GC-004 F1 internal confirmation
FC-GC-005 F2 backfill/size
FC-GC-006 F3 OR completion/lock
FC-GC-007 sequence ownership/canonical hiding
FC-GC-008 renderer independence
FC-GC-009 gap/index curve stability
FC-GC-010 full Phoenix smoke range
```

## Freeze condition

Level 13 is frozen when:

- `FP_LEVEL13 ok=true` on all baselined mandatory cases;
- every frozen level has at least one positive and one negative case;
- validation CSV, events CSV, hooks CSV, summary CSV, manifest CSV, screenshot, and case report are archived;
- expected counts are baselined from MT5 data, not guessed from documentation.
