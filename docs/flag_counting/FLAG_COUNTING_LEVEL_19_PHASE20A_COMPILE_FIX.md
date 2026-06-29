# Flag Counting Level 19 — Phase 20A Compile Fix

## Purpose

Phase 20A fixes a compile error introduced during Phase 20.

## Error

```text
undeclared identifier 'paper_portfolio_row_count'
undeclared identifier 'paper_portfolio_status'
...
```

## Cause

The paper portfolio aggregate fields are snapshot-level fields, but their reset assignments were accidentally inserted into `FP_ResetStateGateTimeframeState`.

`FP_StateGateTimeframeState` correctly does not own portfolio aggregate fields.

## Fix

Move the paper portfolio aggregate reset assignments to `FP_ResetStateGateSnapshot`.

The fix keeps the Phase 20 portfolio aggregate model intact and only corrects the type ownership boundary.

## Locked boundaries

This fix does not change:

```text
Node Engine
Hook / ND Engine
Flag Body
Internal Count
F1 / F2 / F3
Ownership / Canonicalization
Renderer
Validation
Release
License
```

It only fixes Phase 20 State Gate type reset ownership.
