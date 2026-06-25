# EXP0013 Astro Dashboard V5 - Pro Clean Layout

This patch is focused on making the dashboard noticeably more professional and easier to read.

## Main visual changes

- removed extra clutter from the header
- removed the old crowded toggle cluster
- simplified the cockpit to the most useful cards
- switched the display heat scale to:
  - low = red
  - mid = yellow
  - high = green
- improved spacing between rows and cards
- replaced the oversized bottom panel with a compact oscillator board

## Cockpit mode

Shows:
- Path Quality
- Micro M1
- Macro Background
- Raw Axes
- Diagnostics

## Focus mode

Shows a larger version of the selected section:
- Path
- Micro
- Regime
- Macro
- Raw

## Compact oscillator

The lower block is no longer a huge stretched history area.
It is now a compact recent-history board that shows:
- metric name
- current value
- current mini bar
- short sparkline history

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
- RELOAD

## Goal of this version

This version is meant to be visually cleaner while still keeping all major astro states available.
