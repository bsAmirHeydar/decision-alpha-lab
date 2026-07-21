# Hook Origin Lifecycle Fix Patch

## What this patch fixes

This patch prevents Phase 02 Hook candidates from being rendered when their
origin boundary was breached by raw candle high/low action before the terminal
node confirmation window completed.

## Core rule

```text
origin breach before terminal confirmation = non-hook candidate
```

## Changed behavior

Before:

```text
same-side node stream could miss raw origin breaches
semantic Hook arc could still draw
```

After:

```text
raw candle breach is checked through resolve_bar_index + scale_l
candidate is rejected before rendering
```

## Main files

```text
mql5/Include/FlagCountingPhoenix/FP_HookPhase02Rules.mqh
mql5/Include/FlagCountingPhoenix/FP_HookPhase02Types.mqh
mql5/Include/FlagCountingPhoenix/FP_HookPhase02Export.mqh
mql5/Experts/FlagCounting/FlagCountingPhoenixExperiment.mq5
```

## Documentation

```text
docs/nds_hook_architecture/44_phase32_raw_origin_breach_lifecycle_guard.md
docs/obsidian_hook/00_mocs/HOOK_LIFECYCLE_MOC.md
```
