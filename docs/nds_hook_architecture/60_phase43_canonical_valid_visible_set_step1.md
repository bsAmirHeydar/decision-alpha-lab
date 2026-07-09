# Phase 43 — Canonical Valid Visible Set, Step 1

## Intent

This phase is the first code-alignment step after the Hook validity canon.

The goal is not to rebuild Hook detection. The goal is to make production rendering respect the valid-visible-set doctrine.

## Doctrine

Hook counting remains complete.

Production rendering is filtered.

When `InpHookPhase02ShowOnlyValidHooks = true`, the chart may show only:

1. Hook After Opposing F3.
2. Hook-2 After Hook-1.
3. Hook-1 only as the parent companion of visible Hook-2.

No other Hook cycles, node labels, or sequence labels may be drawn.

## Previous failure mode

The renderer could select a valid Hook and then expand into every same-origin structural branch. This made valid-only mode visually equivalent to structural-debug mode.

It also allowed structural fallback to re-populate the chart when valid selection returned zero results.

## Step 1 implementation

A new helper was added:

```text
FP_HookP02SequenceIsProductionValidHook(sequence)
```

It returns true only when:

```text
sequence.valid_after_opposing_f3 == true
or
sequence.valid_after_hook == true
```

Parent companion expansion remains available only for Hook-after-Hook children.

Same-origin group expansion is disabled in this phase. This prevents invalid sibling labels from leaking into production view.

Structural fallback is disabled in production valid-only mode.

## Non-goals

This phase does not change:

- Hook sequence counting.
- F3-to-Hook matching.
- Hook-after-Hook terminal matching.
- Raw terminal semantics.
- F-counting.
- Rally logic.
- Zone logic.
- execution or risk.

Those belong to later implementation phases.
