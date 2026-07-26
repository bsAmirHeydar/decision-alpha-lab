# Phase 06 Hotfix005 — Historical Visual Backfill

## Problem

The visual layer was effectively live-only. After attaching the EA, new labels and drawings could appear, but earlier confirmed or invalidated divergence states were not rebuilt and placed on historical bars. This made the chart look as if the visual language started only at the moment of attachment.

## Required Behavior

When the EA is attached, it must scan a configurable historical window and rebuild Phase 01 through Phase 05 anatomy at each historical closed-candle boundary. Any confirmed or invalidated final state found during that scan must be drawn at its historical origin and destination.

## New Behavior

The engine now performs a one-time historical visual backfill before the normal live pulse. The scan uses the configured confirmation timeframe, collects prior closed candles, processes them oldest-to-newest, and calls the same drawing module used for live events.

## Core Inputs

| Input | Default | Purpose |
|---|---:|---|
| `InpEnableHistoricalVisualBackfill` | `true` | Enables one-time historical drawing scan on attach. |
| `InpHistoricalBackfillLookbackTradingDays` | `2` | Approximate lookback window for closed-candle observations. |
| `InpHistoricalBackfillMaxClosedCandles` | `600` | Hard cap to protect performance. |
| `InpHistoricalBackfillWriteLedger` | `false` | Keeps historical drawing separate from CSV ledger by default. |
| `InpHistoricalBackfillPrintSummary` | `true` | Prints scan summary after backfill completes. |
| `InpKeepFirstVisualForSameSignalId` | `true` | Keeps the first visual position for a signal instead of allowing later candles in the same cycle to drag the drawing forward. |

## Oldest-To-Newest Rule

Historical observations are processed from oldest to newest. This is critical because the first closed candle that confirms a given signal must own the visual position. Later closed candles inside the same current cycle can still reproduce the same signal id, but they must not relocate the line.

## First Visual Lock

When `InpKeepFirstVisualForSameSignalId = true`, the drawing module checks whether the primary origin-to-destination line already exists for the signal id and symbol-local chart. If it exists, the module does not redraw that package. This prevents historical and live rescans from moving established divergence geometry forward.

## Ledger Boundary

Historical ledger writing is off by default. The purpose of this hotfix is chart audit backfill. If historical ledger rows are needed, `InpHistoricalBackfillWriteLedger` can be enabled, but duplicate guards should stay on.

## Strategy Integrity

This hotfix does not change divergence logic. It only changes when the same already-defined visual audit process is applied.
