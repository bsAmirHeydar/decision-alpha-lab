# EXP0017 Phase 06 Hotfix009 — Non-Host Frontier Synchronization

This patch fixes the visual mismatch where the chart hosting the expert respected reference freshness, while the second configured symbol chart could still display stale or orphaned divergence legs.

## Root cause

Phase 05 calculated symbol-local frontier eligibility for both symbols, but Phase 06 only received the pair-level pass/fail result. The renderer then drew a package on both charts without retaining an explicit local freshness flag for the exact chart symbol.

A second defect existed at the rendering boundary: `ObjectDelete()` is asynchronous. The old one-pass cleanup accepted a queued delete as success without verifying that owned objects had actually disappeared from the non-host chart. Old `EXP0017_P06_` objects could therefore survive a rebuild.

## Changes

- Preserve side-specific frontier eligibility for symbol A and symbol B in `SCGCFinalSignal`.
- Refuse to draw a symbol-local leg unless that exact symbol reference is frontier-valid.
- Keep pair-level confirmation behavior unchanged.
- Replace one-pass object cleanup with bounded, verified cleanup on both configured charts.
- Bump the Phase 06 expert version from `1.08` to `1.09`.

## Install

Extract the patch at the repository root.

Compile:

```text
mql5/Experts/IntermarketDivergenceExecution/EXP0017_CG_Visual_Ledger_Anatomy.mq5
```

Then remove and reattach the expert on the host chart. Keep both configured charts open for visual validation.

The expert owns and cleans only objects whose name starts with:

```text
EXP0017_P06_
```

## Expected result

- A stale local reference cannot draw on either SPXUSD or NDXUSD.
- The non-host chart is rebuilt from the same accepted signal state as the host chart.
- Old owned lines from previous builds are removed before historical backfill is redrawn.
- No order, risk, target, outcome, ranking, or AI behavior changes.

## Rollback

Restore the four modified MQL5 files from Hotfix008 and compile expert version `1.08`.
