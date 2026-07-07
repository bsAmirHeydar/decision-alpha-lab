# README — Valid Hook View Filter Patch

## Purpose

The Hook layer can generate many structurally detected Hook candidates. The production view should not show every candidate. It should show only the Hook families that are valid under the current Alpha Lab doctrine:

- Hook After Opposing F3
- Hook After Hook

The only non-valid-family Hook allowed into the production drawing layer is the immediate parent Hook of a visible Hook-after-Hook pair.

## Visibility Doctrine

```text
Visible in valid-only mode:
1. Hook After Opposing F3
2. Hook After Hook
3. Parent Hook of a visible Hook After Hook pair
```

```text
Hidden in valid-only mode:
- standalone unqualified Hook candidates
- hook-like fractal noise
- valid/renderable Hooks that are not in a valid family
- first Hooks that are not followed by a valid second Hook
```

## Input

The default was changed to:

```mql5
InpHookPhase02ShowOnlyValidHooks = true
```

Set it to `false` only for audit/debug mode.

## Files Changed

```text
mql5/Experts/FlagCounting/FlagCountingPhoenixExperiment.mq5
mql5/Include/FlagCountingPhoenix/FP_HookPhase02Visual.mqh
```

## Documentation Added

```text
docs/nds_hook_architecture/49_phase36_valid_hook_view_filter.md
docs/obsidian_hook/02_policies/Valid Hook View Filter.md
docs/obsidian_hook/03_architecture/Phase 36 Valid Hook View Filter.md
docs/obsidian_hook/04_debug/Valid Hook View Debug Checklist.md
```
