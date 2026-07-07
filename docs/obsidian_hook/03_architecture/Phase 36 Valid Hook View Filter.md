# Phase 36 — Valid Hook View Filter

## Pipeline

```text
Hook Phase 02 sequences
→ validity annotation
→ valid-family selection
→ Hook-after-Hook parent expansion
→ production renderer
```

## Why Parent Expansion Exists

A Hook-after-Hook child is not readable without its immediate parent. Therefore, valid-only mode must include the parent Hook when the child Hook is selected.

This does not turn the parent into a valid independent Hook.

## Renderer Helpers

- `FP_HookP02SequencePassesBaseDrawFilter`
- `FP_HookP02SequencePassesDrawFilter`
- `FP_HookP02ExpandSelectionWithHookAfterHookParents`
- `FP_HookP02SortSelectedIndexesBySequenceId`

## Expected Behavior

With valid-only mode enabled:

```text
Hook After Opposing F3       -> shown
Hook After Hook child        -> shown
Hook After Hook parent       -> shown as companion
Unqualified standalone Hook  -> hidden
```
