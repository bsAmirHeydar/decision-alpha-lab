# Flag Counting Level 19 — Phase 27A Compile Fix

## Purpose

Phase 27A fixes a compile error introduced in Phase 27.

## Error

```text
undeclared identifier 'FP_StateGateClampDouble'
```

## Cause

Phase 27 used `FP_StateGateClampDouble` inside the paper path smoothness score function, but that helper was not defined in the current State Gate rules module.

## Fix

Replace the undefined helper call with explicit local clamp logic:

```text
if score < 0.0  -> score = 0.0
if score > 100.0 -> score = 100.0
```

## Scope

This patch only changes the Phase 27 path quality smoothness score clamp.

It does not modify:

```text
Node Engine
Hook / ND Engine
Flag Body
Internal Count
F1 / F2 / F3
State Gate data model
paper lifecycle logic
paper performance logic
license logic
execution logic
```
