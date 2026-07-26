# Phase 10 — Hook v1 Freeze + Training Contract

## Purpose

Phase 10 is the final modular Hook phase for the current NDS architecture pass.
It does **not** create a new Hook signal. It freezes the runtime contract that
makes Hook output safe to use as downstream training input.

The rule is:

```text
Hook v1 can only become training material after:
Phase 06 quality records exist
+ Phase 08 audit reconciles
+ Phase 09 visual smoke passes
+ Phase 10 contract checks pass
```

This phase is a gate, not a strategy.

---

## First input requirement

The central expert now exposes the display-family selector as the **first visible
input**:

```mql5
input FP_NDSHookDisplayFamily InpNDSHookDisplayFamily = FP_NDS_HOOK_DISPLAY_RALLY_ONLY;
```

Available values:

```text
FP_NDS_HOOK_DISPLAY_RALLY_ONLY
FP_NDS_HOOK_DISPLAY_HOOK_ONLY
FP_NDS_HOOK_DISPLAY_RALLY_AND_HOOK
```

Expected behavior:

```text
RALLY_ONLY      => legacy Rally / F-counting display only
HOOK_ONLY       => suppress Rally/F drawing and show Hook phases only
RALLY_AND_HOOK  => draw Rally/F-counting and Hook layers together
```

The default remains `RALLY_ONLY` to preserve old behavior.

---

## Added files

```text
mql5/Include/FlagCountingPhoenix/FP_HookPhase10Types.mqh
mql5/Include/FlagCountingPhoenix/FP_HookPhase10Rules.mqh
mql5/Include/FlagCountingPhoenix/FP_HookPhase10Visual.mqh
mql5/Include/FlagCountingPhoenix/FP_HookPhase10Export.mqh
mql5/Include/FlagCountingPhoenix/FP_HookPhase10Engine.mqh
```

Documentation overlay:

```text
docs/contexts/legacy/nds/hook/17_phase10_freeze_training_contract_implementation.md
docs/contexts/legacy/nds/hook/hook_phase10_manifest.json
```

---

## Phase 10 is no-draw

`FP_HookPhase10Visual.mqh` intentionally does not draw Hook structure.

Reason:

```text
Phase 10 is the freeze/training contract.
It must not add chart objects that could be mistaken for Hook evidence.
```

All Phase 10 artifacts are CSV/log contracts.

---

## Freeze modes

```mql5
enum FP_HookPhase10FreezeMode
{
   FP_HOOK_P10_FREEZE_OBSERVE_ONLY       = 0,
   FP_HOOK_P10_FREEZE_V1_CANDIDATE       = 1,
   FP_HOOK_P10_FREEZE_TRAINING_READY     = 2,
   FP_HOOK_P10_FREEZE_STRICT_LOCK        = 3
};
```

### OBSERVE_ONLY

Use when inspecting the contract without asserting readiness.

### V1_CANDIDATE

Default. Runs the contract checks but does not imply permanent lock.

### TRAINING_READY

Use when preparing Hook output for downstream training datasets.

### STRICT_LOCK

Requires clean audit, clean smoke, visible Hook display family, Hook records,
quality records, and no upstream file errors.

---

## Main inputs

```mql5
input bool   InpHookPhase10Enabled = true;
input FP_HookPhase10FreezeMode InpHookPhase10FreezeMode = FP_HOOK_P10_FREEZE_V1_CANDIDATE;
input bool   InpHookPhase10AllowRallyOnlyFreeze = false;
input bool   InpHookPhase10RequirePhase08Ok = true;
input bool   InpHookPhase10RequirePhase09Ok = true;
input bool   InpHookPhase10RequireHookRecords = true;
input bool   InpHookPhase10RequireXYQualityRecords = true;
input bool   InpHookPhase10RequireHighQualityRecords = false;
input bool   InpHookPhase10RequireViewProfileNotKeepInputs = false;
input bool   InpHookPhase10RequireExportContract = false;
input bool   InpHookPhase10RequireNoFileErrors = true;
```

Conservative defaults:

```text
RALLY_ONLY skips Phase 10 unless explicitly allowed.
CSV export is disabled by default.
High/elite quality presence is optional until thresholds are calibrated.
```

---

## Contract checks

Phase 10 emits explicit contract rows:

```text
DISPLAY_FAMILY_VISIBLE_FIRST_INPUT
PHASE08_AUDIT_RECONCILED
PHASE09_VISUAL_SMOKE_RECONCILED
HOOK_RECORDS_EXIST
XY_QUALITY_RECORDS_EXIST
HIGH_OR_ELITE_QUALITY_AVAILABLE
VIEW_PROFILE_EXPLICIT
NO_UPSTREAM_FILE_ERRORS
P10_EXPORT_CONTRACT_ENABLED
STRICT_LOCK_GATE
```

The central concept:

```text
freeze_ready = required checks pass
             + warning limit is not exceeded
             + Phase 10 export has no file errors
```

---

## Training schema contract

Phase 10 defines the first stable Hook-v1 training schema. It is not the dataset
itself. It is the column contract that downstream exporters/trainers must obey.

Examples:

```text
contract_id
schema_version
symbol
period
display_family
view_profile
direction
scale
sequence_id
origin_time
origin_price
x0_time
x0_price
x1_time
x1_price
x2_time
x2_price
x3_time
x3_price
y_state
xy_state
hook_type
quality_bucket
quality_score
x_strength
y_strength
type_strength
lifecycle_strength
dead_by_origin_return
anchor_time
anchor_price
record_reason
```

This creates a stable bridge from visual Hook anatomy to future AI/training
layers.

---

## CSV outputs

When `InpHookPhase10ExportCsv = true`, Phase 10 writes:

```text
hook_phase10_freeze_summary.csv
hook_phase10_contract_checks.csv
hook_phase10_training_schema.csv
hook_phase10_freeze_manifest.csv
```

Default folder:

```text
FlagCountingPhoenix
```

---

## Runtime integration

The central expert now includes:

```mql5
#include "../../Include/FlagCountingPhoenix/FP_HookPhase10Engine.mqh"
```

Phase 10 is loaded after Phase 09 config:

```mql5
FP_HookPhase10Config hook_phase10_cfg;
FP_LoadHookPhase10Config(hook_phase10_cfg);
```

Phase 10 runs after Phase 09:

```mql5
FP_RunHookPhase10(_Symbol, _Period,
                  hook_phase07_cfg, hook_phase10_cfg,
                  hook_phase06_report, hook_phase08_report, hook_phase09_report,
                  hook_phase10_report);
```

---

## Safety boundary

Phase 10 preserves the non-execution boundary:

```text
no OrderSend
no OrderCheck
no CTrade
no broker request
no position sizing
no risk sizing
no live execution behavior
```

---

## Acceptance checklist

A successful Phase 10 pass means:

```text
InpNDSHookDisplayFamily is the first visible input.
RALLY_ONLY remains the default.
HOOK_ONLY suppresses Rally/F drawing and allows Hook-only inspection.
RALLY_AND_HOOK allows combined inspection.
Phase 08 audit state is visible in the contract.
Phase 09 smoke state is visible in the contract.
Phase 06 quality counts are visible in the contract.
Training schema columns are emitted when export is enabled.
Freeze manifest is emitted when export is enabled.
No execution code was introduced.
```
