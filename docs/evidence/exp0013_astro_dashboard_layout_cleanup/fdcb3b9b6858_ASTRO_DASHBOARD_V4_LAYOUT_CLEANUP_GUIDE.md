# EXP0013 Astro Dashboard V4 - Layout Cleanup

This patch focuses specifically on visual cleanup and readability.

## What was fixed

The previous interactive cockpit was functionally better, but visually it still had these problems:

- cards were too narrow
- value text and labels could collide
- header controls were too crowded
- diagnostics mixed into the same visual density as analytical cards
- oscillator rows were too compressed

## V4 layout improvements

### 1) Cleaner header

The header is now split into clearer lines:

- title
- research/runtime line
- symbol / timeframe / mode line
- row status line
- broker/utc line
- thesis/help line

Buttons are now placed in two dedicated rows on the right side, instead of colliding with title text.

### 2) Better card spacing

Cards now use a wider structure with separate columns for:

- metric name
- numeric value
- bucket label
- progress bar

This makes them much easier to scan.

### 3) Clearer diagnostics

Diagnostics now live in their own larger dedicated card.
This keeps troubleshooting readable when the row is exact / fallback / missing.

### 4) Cleaner oscillator

The oscillator now uses:

- wider historical area
- clearer metric label/value area
- dedicated mini-bar zone
- more vertical row spacing

## View modes

### Cockpit mode

Shows the multi-card dashboard.

### Focus mode

Shows one selected section larger, plus diagnostics.

## Buttons

Top row:

- COCKPIT
- PATH
- MICRO
- REGIME
- MACRO
- RAW

Second row:

- TEXT ON/OFF
- OSC ON/OFF
- PTH
- MIC
- REG
- MAC
- RAW
- RELOAD

## Notes

This is still a research UI, not a trade executor.
It is meant to answer:

```text
How clean, noisy, smooth, or dirty is the path context for the market direction I already have?
```
