# Phase 35 — Hook Root Compile API Compatibility

## Problem

The Hook root rebuild moved the production sequence model to the seed-owned Phase 02 builder. Some later Hook phases still used the earlier rate-aware Phase 02 entrypoint.

## Doctrine

A later Hook phase should be able to rebuild Phase 02 without depending on a missing symbol. Phase 02 must keep a stable public API while its internal sequence logic evolves.

## Repair

`FP_HookP02BuildSequencesWithRates(...)` is restored as a compatibility wrapper and forwards to `FP_HookP02BuildSequences(...)`.

## Scope

This is an API compatibility repair, not a trading-logic change.
