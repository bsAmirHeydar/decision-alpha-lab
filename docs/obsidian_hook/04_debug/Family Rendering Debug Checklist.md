# Family Rendering Debug Checklist

Use this checklist when the correct Hooks are selected but the chart is hard to read.

## Inputs

```text
InpHookPhase02ShowOnlyValidHooks = true
InpHookPhase02ValidOnlyFallbackToStructural = false
InpHookPhase02ShowHookSequenceIdsInLabels = true
```

## Expected labels

- Hook after F3: `F3H ...`
- Hook-after-Hook child: `HH ...`
- Parent companion: `PARENT ...`
- Dual-family: `F3H+HH ...`

## Leakage checks

If an unqualified Hook appears without a family tag, inspect:

- selected indexes in `FP_HookP02SelectSequenceIndexes`
- parent expansion in `FP_HookP02ExpandSelectionWithHookAfterHookParents`
- same-origin expansion in `FP_HookP02ExpandSelectionWithSameHookGroupMembers`
- family tag derivation in `FP_HookP02CanonicalFamilyTag`

## Color checks

If all arcs have the same color in valid-only mode, inspect:

- `FP_HookP02CanonicalFamilyColor`
- `FP_HookP02DrawOriginGroupEnvelopes`
- `FP_HookP02DrawOneSequenceNumbers`

