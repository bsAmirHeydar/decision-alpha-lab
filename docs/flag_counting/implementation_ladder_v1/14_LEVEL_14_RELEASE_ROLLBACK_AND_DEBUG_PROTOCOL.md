# Phoenix Flag Counting Implementation Ladder V1

This document is part of the implementation ladder for the Phoenix Flag Counting engine. The ladder is intentionally layered so that lower layers become frozen foundations before higher layers are allowed to depend on them.

Global non-negotiables:

- All structural decisions use candle `high` and `low` only.
- `open`, `close`, candle body, candle color, volume, and indicators are not structural inputs.
- Equality is not a break. A level is broken only by a strict pass beyond it.
- The renderer is non-authoritative. It may only draw logical objects emitted by engines.
- Main-chart rendering and audit rendering are separate products.
- Every layer must expose enough audit fields to prove why an object exists.
- A higher layer may never silently repair a lower-layer defect.

# Level 14 — Release, Rollback, and Debug Protocol

## Purpose

Level 14 makes Phoenix operationally safe. It prevents losing time to stale MetaTrader `.ex5` files, stale chart objects, ambiguous debug states, and unclear Git rollback points.

Level 14 is not a market-structure layer.

It may:

```text
- select a runtime release/debug profile;
- force export, validation, render-off, or clean-main settings;
- request object cleanup by prefix;
- write a release manifest CSV;
- print FP_LEVEL14 / FP_LEVEL14_PRE audit logs;
- enforce a release gate from export/render/validation/canonical counters.
```

It may not:

```text
- create F1/F2/F3;
- create Hook/ND;
- mutate events or hooks;
- repair identity;
- repair hidden reasons;
- decide renderer visibility from geometry;
- change candle/node/body/internal/lifecycle/ownership/canonical rules.
```

## Implemented modules

```text
mql5/Include/FlagCountingPhoenix/FP_ReleaseTypes.mqh
mql5/Include/FlagCountingPhoenix/FP_ReleaseRules.mqh
mql5/Include/FlagCountingPhoenix/FP_ReleaseAudit.mqh
mql5/Include/FlagCountingPhoenix/FP_ReleaseEngine.mqh
```

## Runtime order

Level 14 wraps the existing pipeline:

```text
Load raw user inputs
-> Load Timebase / Engine / Export / Render / Validation configs
-> Level 14 applies selected runtime profile
-> Level 01 Timebase
-> Levels 02-11 Detection/Canonicalization
-> Level 11.5 Export
-> Level 12 Renderer
-> Level 13 Validation
-> Level 14 Final release gate + manifest
-> FP_SUMMARY
```

The profile is applied before the candle stream loads, so `debug_max` can also enable timebase samples.

## Release profiles

Input:

```mql5
InpReleaseProfile
```

Available profiles:

```text
FP_RELEASE_PROFILE_NORMAL
FP_RELEASE_PROFILE_CLEAN_MAIN
FP_RELEASE_PROFILE_AUDIT_EXPORT
FP_RELEASE_PROFILE_VALIDATION
FP_RELEASE_PROFILE_DEBUG_MAX
FP_RELEASE_PROFILE_RENDER_OFF
FP_RELEASE_PROFILE_SAFE_ROLLBACK
```

### normal

No overrides. This is the default operational profile.

### clean_main

For screenshots and visual inspection.

Enforces:

```text
strict ownership
strict canonical invariants
strict renderer visibility
canonical object names
prefix cleanup
clean labels
no parent/internal/origin/debug label noise
```

### audit_export

For logic inspection without chart trust.

Enforces:

```text
export enabled
visible_only=false
export samples enabled
renderer suppressed
```

Main value:

```text
Read CSV before trusting the chart.
```

### validation

For regression/baseline runs.

Enforces:

```text
export enabled
validation enabled
validation strict=true
render ok required
no render errors required
no canonical failures required
```

### debug_max

For deep investigation.

Enforces:

```text
timebase samples
node/identity/hook/body/internal/F1/F2/F3/ownership/canonical samples
export enabled
validation enabled in baseline mode
invalidated audit visible
unseeded hooks debug-visible
renderer strict visibility disabled
renderer detailed labels enabled
```

This mode is intentionally noisy.

### render_off

For CSV-only or headless audit.

Enforces:

```text
export enabled
renderer suppressed
validation does not require renderer ok
```

### safe_rollback

For compile/recover/cleanup when the chart is polluted or a patch is suspected broken.

Enforces:

```text
scan_hooks=false
scan_f1=false
scan_f2=false
scan_f3=false
export disabled
validation disabled
renderer suppressed
prefix cleanup requested
```

This is not a trading/research mode. It is a recovery mode.

## New EA inputs

```mql5
InpReleaseProfile
InpReleaseRunTag
InpReleaseFolder
InpReleaseWriteManifest
InpReleaseOverwriteLatest
InpReleaseStrictGate
InpReleaseRequireValidationOk
InpReleaseRequireExportOk
InpReleaseRequireRenderOk
InpReleaseRequireNoRenderErrors
InpReleaseRequireNoExportErrors
InpReleaseRequireNoCanonicalFailures
InpReleaseCleanObjectsForProfile
InpPrintReleaseSanity
InpPrintReleaseSamples
InpReleaseSampleLimit
```

## Logs

Pre-run profile override log:

```text
FP_LEVEL14_PRE status=ok profile=<profile> overrides=<n> ...
```

Final gate log:

```text
FP_LEVEL14 status=ok|failed profile=<profile> gate=pass|fail ...
```

Summary counters:

```text
release_attempted
release_ok
release_gate_pass
release_gate_fail
release_overrides
release_files
release_errors
release_cleanup
release_export_forced
release_render_suppressed
release_validation_forced
release_rollback_safe
```

## Release manifest

If enabled:

```mql5
InpReleaseWriteManifest = true
```

Level 14 writes:

```text
MQL5/Files/FlagCountingPhoenix/latest_release.csv
```

unless overwrite-latest is disabled, in which case the run tag is used.

Manifest fields include:

```text
profile
run_tag
gate_passed
gate_blocking
overrides_applied
cleanup_requested
export_forced
render_suppressed
validation_forced
rollback_safe_mode
release check counts
event/hook counts
render/export/validation/canonical failure counters
override_log
reason
```

## Release gate

The gate is configured by:

```mql5
InpReleaseRequireValidationOk
InpReleaseRequireExportOk
InpReleaseRequireRenderOk
InpReleaseRequireNoRenderErrors
InpReleaseRequireNoExportErrors
InpReleaseRequireNoCanonicalFailures
InpReleaseStrictGate
```

Default behavior:

```text
Gate failures are reported but do not stop the EA.
```

If strict gate is enabled:

```text
FP_LEVEL14 status=failed when required release checks fail.
```

Level 14 does not roll back Git automatically. It gives deterministic evidence so the human rollback command is obvious.

## Standard apply block

```powershell
cd "C:\Users\ABN\AppData\Roaming\MetaQuotes\Terminal\4769098028DB821E4654DC6D5C533078\MQL5\Shared Projects\decision-alpha-lab"

git branch backup-before-<patch-name>

Expand-Archive -Path ".\<patch-name>.zip" `
  -DestinationPath "." `
  -Force

Remove-Item ".\<patch-name>.zip" -Force

Get-ChildItem -Recurse -Filter "FlagCountingPhoenixExperiment.ex5" |
  Remove-Item -Force -ErrorAction SilentlyContinue
```

## Standard chart cleanup

```text
1. Remove Expert from chart.
2. Press Ctrl+B.
3. Delete all objects with DAL_FCP_ prefix.
4. Recompile Expert.
5. Attach Expert again.
6. Reset inputs.
```

Or use:

```text
InpReleaseProfile = FP_RELEASE_PROFILE_SAFE_ROLLBACK
```

then attach/compile once to cleanup/suppress drawing.

## Debug order

When chart is wrong:

```text
1. Is the compiled .ex5 fresh?
2. Are old objects deleted?
3. Is InpReleaseProfile accidentally debug_max/render_off/safe_rollback?
4. Are inputs reset?
5. Does FP_LEVEL11 say canonical stream is ok?
6. Does latest_events.csv show visible events?
7. Does FP_LEVEL12 say renderer filtered or failed?
8. Does FP_LEVEL14 gate fail? Which requirement failed?
```

## Rollback options

### Safe revert after push

```bash
git revert HEAD
```

Use when shared history must be preserved.

### Exact reset to known good state

```bash
git reset --hard <GOOD_SHA>
git push --force-with-lease origin main
```

Use when you own the branch and want remote to match exactly.

### Restore selected files

```bash
git checkout <GOOD_SHA> -- mql5/Include/FlagCountingPhoenix/FP_Renderer.mqh
```

Use when only one layer must be restored.

## Failure triage examples

### Chart mostly gray

Likely failed layers:

```text
L04 Hook/ND emits too much
L11 Hook main/audit separation failed
L12 renderer draws audit hooks in main mode
L14 accidentally left debug_max enabled
```

### No colored flags

Likely failed layers:

```text
L05 flag body starved
L07 F1 root gating too strict
L10 sequence ownership hides roots
L11 canonicalization hides all winners
L14 render_off or safe_rollback profile enabled
```

### Too many same-direction F1s

Likely failed layers:

```text
L10 sequence ownership missing
L03 identity too weak
L11 canonicalization visual duplicate rules too weak
```

### F2/F3 too early

Likely failed layers:

```text
L08 F2 authorization wrong
L09 F3 authorization wrong
L06 internal count confirmation leaked
```

### Curves broken

Likely failed layers:

```text
L01 timebase uses timestamp interpolation
L12 renderer stale segment cleanup failed
```

## Freeze condition

Level 14 is frozen when:

```text
- every Phoenix run can print FP_LEVEL14;
- every release/debug profile is deterministic and documented;
- latest_release.csv can be written without renderer dependency;
- safe_rollback can suppress drawing and request prefix cleanup;
- release gate can fail loudly without changing market structure;
- apply/compile/cleanup/commit/rollback instructions exist for every patch.
```
