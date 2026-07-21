# Hook Validity Lite Patch

## Purpose

The previous valid-Hook implementation became too restrictive. It mixed three different concerns:

- sequence construction,
- family validity,
- semantic near-death readiness.

That made the production view too sparse and made debugging difficult. This patch separates those concerns.

## New doctrine

A Hook can be displayed as valid when it satisfies one of two family rules:

1. **Immediate Hook After Opposing F3**
   - an F3 is completed or locked;
   - the next structural Hook after it qualifies only if it is in the opposite direction;
   - the F3 does not validate every later Hook.

2. **Hook After Hook**
   - the second Hook starts exactly from the structural terminal node of the previous Hook;
   - the parent Hook may be displayed as a companion, but it is not independently promoted.

## Practical visibility defaults

The valid-only view no longer requires near-death readiness by default:

```text
InpHookPhase02ValidOnlyRequireNearDeath = false
```

F3-to-Hook validity no longer requires exact scale matching by default:

```text
InpHookPhase02ValidF3RequireSameScale = false
```

These can be turned on when a stricter research/audit view is needed.

## Changed files

```text
mql5/Experts/FlagCounting/FlagCountingPhoenixExperiment.mq5
mql5/Include/FlagCountingPhoenix/FP_HookPhase02Types.mqh
mql5/Include/FlagCountingPhoenix/FP_HookPhase02Rules.mqh
mql5/Include/FlagCountingPhoenix/FP_HookPhase02Engine.mqh
mql5/Include/FlagCountingPhoenix/FP_HookPhase02Visual.mqh
mql5/Include/FlagCountingPhoenix/FP_HookPhase02Export.mqh
```

## Documentation

```text
docs/nds_hook_architecture/52_phase39_practical_valid_hook_determination.md
docs/obsidian_hook/00_mocs/HOOK_VALIDITY_CORE_MOC.md
docs/obsidian_hook/01_concepts/Practical Valid Hook.md
docs/obsidian_hook/02_policies/Valid Hook Determination Policy.md
docs/obsidian_hook/03_architecture/Phase 39 Practical Valid Hook Filter.md
docs/obsidian_hook/04_debug/Valid Hook Too Few Debug Checklist.md
```
