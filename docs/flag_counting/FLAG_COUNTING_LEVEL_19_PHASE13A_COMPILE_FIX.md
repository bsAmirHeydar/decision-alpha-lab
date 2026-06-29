# Flag Counting Level 19 — Phase 13A Compile Fix

## Purpose

Phase 13A fixes a compile error introduced during Phase 13.

## Error

```text
struct member 'mtf_alignment_row_count' already defined
```

## Cause

`mtf_alignment_row_count` was accidentally declared twice inside `FP_StateGateTimeframeState`.

## Fix

Remove the duplicate declaration and keep the intended single per-timeframe field.

The separate snapshot-level `mtf_alignment_row_count` remains intact.

## Locked boundaries

This fix only touches the State Gate type shell and documentation.

It does not change:

- Node Engine
- Hook / ND Engine
- Flag Body
- Internal Count
- F1 / F2 / F3 lifecycle
- Ownership / Canonicalization
- Renderer
- Validation
- Release
- License
