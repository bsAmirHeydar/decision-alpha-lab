# Flag Counting Level 19 — Phase 24A Compile Fix

## Purpose

Phase 24A fixes a compile error introduced during Phase 24.

## Error

```text
struct member 'persistent_paper_trade_row_count' already defined
identifier 'persistent_paper_trade_row_count' already used
```

## Cause

`persistent_paper_trade_row_count` was declared twice inside `FP_StateGateTimeframeState`.

One per-timeframe declaration is required, and one snapshot-level declaration is required. The duplicate per-timeframe declaration was invalid.

## Fix

Remove the extra per-timeframe declaration and keep:

```text
FP_StateGateTimeframeState::persistent_paper_trade_row_count
FP_StateGateSnapshot::persistent_paper_trade_row_count
```

Both reset paths remain valid:

```text
FP_ResetStateGateTimeframeState
FP_ResetStateGateSnapshot
```

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

It only fixes Phase 24 type ownership.
