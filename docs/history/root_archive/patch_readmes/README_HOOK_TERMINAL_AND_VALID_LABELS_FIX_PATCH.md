# Hook Terminal and Valid Labels Fix Patch

## Scope

This patch changes Hook Phase 02 terminal semantics and valid-only label visibility.

## Doctrine

A positive Hook does not end at an arbitrary compact sequence row. It ends at the lowest valley reached by the Hook's origin group. The negative mirror ends at the highest peak reached by its origin group.

In valid-only mode, the chart must not show labels from unqualified Hook groups. It should show sequence labels only for visible valid Hook groups, plus the immediate parent Hook group when a visible Hook is valid because it is Hook-2 after Hook-1.

## Code touched

- `mql5/Include/FlagCountingPhoenix/FP_HookPhase02Rules.mqh`
- `mql5/Include/FlagCountingPhoenix/FP_HookPhase02Visual.mqh`

## Documentation touched

- `docs/nds_hook_architecture/50_phase37_hook_terminal_and_valid_labels.md`
- `docs/obsidian_hook/02_policies/Positive Hook Terminal Is Lowest Valley.md`
- `docs/obsidian_hook/02_policies/Valid Only Means Valid Hook Labels Only.md`
- `docs/obsidian_hook/03_architecture/Phase 37 Hook Terminal and Valid Labels.md`
- `docs/obsidian_hook/04_debug/Valid Hook Label Leakage Checklist.md`
