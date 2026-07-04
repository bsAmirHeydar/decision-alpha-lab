# 08 — Hook Phase 01 Implementation: Node Source Adapter

## Scope

This phase adds the first modular Hook/CycleHook implementation layer to the central expert.

It does not implement full Hook sequences yet.

It implements:

```text
NDS display family input
Hook-only / Rally-only / Rally-and-Hook mode boundary
strict peak/valley node source adapter
multi-scale Hook node extraction
Hook Phase 01 chart markers
Hook Phase 01 CSV audit
```

## Display Family

New input:

```text
InpNDSHookDisplayFamily
```

Values:

```text
FP_NDS_HOOK_DISPLAY_RALLY_ONLY
FP_NDS_HOOK_DISPLAY_HOOK_ONLY
FP_NDS_HOOK_DISPLAY_RALLY_AND_HOOK
```

Default:

```text
FP_NDS_HOOK_DISPLAY_RALLY_ONLY
```

This preserves existing Rally/F-counting behavior by default.

## Phase 01 Meaning

Phase 01 is not the full Hook algorithm.

It is the Node Source Adapter for Hook.

It answers:

```text
Which strict peaks and valleys are available per L scale?
Can Hook logic receive a stable node stream?
Can we visually inspect Hook node candidates without changing Rally/F-counting?
```

## Strict Node Rules

Peak:

```text
center high > all highs within L bars on both sides
```

Valley:

```text
center low < all lows within L bars on both sides
```

Equal highs/lows are rejected.

Minimum L is forced to 2 for this layer.

## New Modules

```text
mql5/Include/FlagCountingPhoenix/FP_HookPhase01Types.mqh
mql5/Include/FlagCountingPhoenix/FP_HookPhase01Rules.mqh
mql5/Include/FlagCountingPhoenix/FP_HookPhase01Visual.mqh
mql5/Include/FlagCountingPhoenix/FP_HookPhase01Export.mqh
mql5/Include/FlagCountingPhoenix/FP_HookPhase01Engine.mqh
```

## New CSV Outputs

Enabled with:

```text
InpHookPhase01ExportCsv = true
```

Outputs:

```text
hook_phase01_nodes.csv
hook_phase01_summary.csv
```

## New Chart Objects

Object prefix:

```text
InpHookPhase01ObjectPrefix = "DAL_HOOK_P01_"
```

Markers:

```text
PEAK
VALLEY
L value label
```

## Acceptance Criteria

Rally-only mode:

```text
Existing F-counting behavior remains unchanged.
Hook Phase 01 is skipped.
```

Hook-only mode:

```text
Rally/F labels are suppressed.
Hook Phase 01 peak/valley node candidates are drawn.
```

Rally-and-Hook mode:

```text
Existing Rally/F-counting remains visible.
Hook Phase 01 node candidates are also drawn under their own prefix.
```

## No Execution Boundary

This phase does not add:

```text
OrderSend
OrderCheck
CTrade
broker requests
real execution
risk sizing
volume sizing
position management
```
