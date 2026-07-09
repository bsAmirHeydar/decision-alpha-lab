# Hook Canon Step 2 — Validity Determination Patch

## Purpose

The previous step filtered rendering, but the renderer can only be correct if the validity flags are correct. This patch aligns Phase 02 validity annotation with the canonical Hook doctrine.

## Canonical Rules

### 1. Hook After Opposing F3

A Hook is valid after F3 only when:

- the F3 is completed or locked;
- the Hook direction opposes the F3 direction;
- the Hook starts from a terminal endpoint of that F3;
- the selected Hook is the earliest structural Hook satisfying that terminal-start condition for the F3.

A historical F3 must not validate arbitrary later Hooks.

### 2. Hook After Hook

Hook-2 is valid after Hook-1 only when:

- Hook-1 has closed its own sequence/cycle structurally;
- Hook-2 and Hook-1 are the same genus, implemented as the same Hook direction;
- Hook-2 starts from Hook-1's structural terminal node;
- terminal node continuity uses `resolve_node_id`, while raw terminal price/time remains a rendering concern.

Hook-1 is not promoted into an independently valid Hook by this rule. It remains a required parent companion for rendering Hook-2.

## Code Changed

- `mql5/Include/FlagCountingPhoenix/FP_HookPhase02Rules.mqh`
- `mql5/Include/FlagCountingPhoenix/FP_HookPhase02Types.mqh`
- `mql5/Experts/FlagCounting/FlagCountingPhoenixExperiment.mq5`

## Documentation Added

- `docs/nds_hook_architecture/61_phase44_canonical_validity_determination_step2.md`
- `docs/obsidian_hook/02_policies/Canonical Hook Validity Determination.md`
- `docs/obsidian_hook/03_architecture/Phase 44 Canonical Validity Determination.md`
- `docs/obsidian_hook/04_debug/Canonical Validity Determination Debug Checklist.md`

## Recommended Inputs

```text
InpHookPhase02ShowOnlyValidHooks = true
InpHookPhase02ValidOnlyFallbackToStructural = false
InpHookPhase02ValidOnlyRequireNearDeath = false
InpHookPhase02ValidF3RequireSameScale = false
InpHookPhase02ValidF3RequireOppositeDirection = true
InpHookPhase02SeedUsedNodesCannotRestart = true
InpHookPhase02RejectRawOriginBreachBeforeTerminalConfirmation = true
```
