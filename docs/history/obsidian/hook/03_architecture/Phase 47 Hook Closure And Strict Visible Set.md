# Phase 47 Hook Closure And Strict Visible Set

## Code-level intent

Phase 47 changes two specific areas:

1. Visual selection: no same-origin expansion in valid-only mode.
2. Rule layer: no raw wick/candle terminal promotion in production Hook Phase02.

## Visual selection

The function `FP_HookP02ExpandSelectionWithSameHookGroupMembers` is intentionally no-op.

The only expansion still allowed is `FP_HookP02ExpandSelectionWithHookAfterHookParents`.

## Rules layer

`FP_HookP02BuildSequencesWithRates` preserves the structural terminals produced by `FP_HookP02BuildSequences`.

The raw-terminal helper functions remain available for future research diagnostics but are not applied to production terminal ownership.

## Result

With valid-only enabled, displayed labels should match the canonical family rows exactly.
