# Strict Valid Hook View Fix — Start Here

This patch closes the remaining leak in valid-only Hook rendering.

The previous valid-only input filtered Phase 02 semantic sequences, but raw/core Hook rendering and later diagnostic Hook phases could still draw unqualified Hook objects. In addition, the Opposing-F3 validity assignment was too broad: one old opposing F3 could validate every later Hook in the opposite direction.

This patch makes valid-only mode strict:

- raw/core Hook renderer is suppressed when `InpHookPhase02ShowOnlyValidHooks = true`
- Phase 01 raw nodes are hidden in valid-only mode
- Phase 03-06 diagnostic overlays are hidden in valid-only mode
- stale Hook objects are deleted before the valid Phase 02 redraw
- only Phase 02 valid Hook families own the production valid Hook view
- Opposing-F3 validity is bounded to the first Hook after each completed/locked opposing F3
- Hook-after-Hook still shows the immediate parent companion when the second Hook is visible

Production setting:

```text
InpHookPhase02ShowOnlyValidHooks = true
InpHookPhase02SeedUsedNodesCannotRestart = true
InpHookPhase02RejectRawOriginBreachBeforeTerminalConfirmation = true
```
