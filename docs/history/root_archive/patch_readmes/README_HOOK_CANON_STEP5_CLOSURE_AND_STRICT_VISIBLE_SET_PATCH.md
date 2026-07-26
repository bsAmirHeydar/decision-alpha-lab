# README — Hook Canon Step 5 Closure and Strict Visible Set Patch

## Purpose

This patch fixes the precise failure seen on the chart: many structural Hook sequence labels were still visible while `InpHookPhase02ShowOnlyValidHooks=true`.

The source was not the label painter itself; it was the visible-set expansion layer. After a valid sequence was selected, the renderer expanded that selection to every same-origin sibling sequence. That made valid-only behave like “valid origin group plus all its branches”, while the user canon says “only valid Hook details”.

## Canon corrections

### 1. Valid-only is not origin-group expansion

Allowed visible rows:

- `F3H`: Hook After Opposing F3;
- `HH`: Hook-2 After Hook-1;
- `PARENT`: Hook-1 only when it is the required parent companion of a visible HH child.

Forbidden in production valid-only:

- raw structural Hook candidates;
- same-origin sibling branches;
- sequence labels from unqualified Hooks;
- node labels from unqualified Hooks;
- structural fallback.

### 2. Hook closure is terminal-node confirmation

A Hook candidate is not a closed Hook until its last same-side terminal node is confirmed by the swing-node confirmation window.

If price touches or crosses the Hook origin before that terminal node is confirmed, the candidate was never a Hook and must not be treated as valid or visible.

If a newer same-side terminal node appears before origin death, the candidate may continue into that newer terminal. Otherwise, after the terminal node is confirmed, the Hook is closed.

### 3. Terminal is a confirmed node, not a raw wick

Positive Hook terminal: the lowest confirmed valley still above origin.

Negative Hook terminal: the highest confirmed peak still below origin.

Raw candles can be used later for diagnostics, but not for production Hook terminal ownership or valid-only cycle endpoints.

## Files changed

- `mql5/Include/FlagCountingPhoenix/FP_HookPhase02Visual.mqh`
- `mql5/Include/FlagCountingPhoenix/FP_HookPhase02Rules.mqh`
- `docs/nds_hook_architecture/64_phase47_hook_closure_and_strict_visible_set.md`
- Obsidian notes under `docs/obsidian_hook/`

## Expected chart behavior

With:

```text
InpHookPhase02ShowOnlyValidHooks = true
InpHookPhase02ValidOnlyFallbackToStructural = false
```

The chart should show only:

- valid cycle arcs;
- node/sequence labels belonging to those valid Hook rows;
- parent companion details only for valid Hook-after-Hook chains.

If there is no canonical valid Hook in the visible scan window, the chart should draw no Hook Phase02 objects.
