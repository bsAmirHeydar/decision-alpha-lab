# EXP0013 Astro Dashboard V6 - Cleanup and Spacing Fix

This patch addresses two specific problems from the previous versions:

## 1) Old panels were not being cleared

### Problem
When the expert refreshed, changed mode, or was reloaded, some previous panels stayed on the chart.
That created duplicates such as:
- old focus cards still visible
- old cockpit cards staying behind
- old oscillator fragments remaining

### Fix
This version now does two levels of cleanup:

- full cleanup on `OnInit`
- full cleanup on `OnDeinit`
- full cleanup at the start of every render cycle

It also removes objects from older EXP0013 astro prefixes, so legacy panels from previous dashboard versions are cleared too.

## 2) Text and numbers were still too crowded

### Problem
The previous layout still had:
- labels too close to values
- values too close to state labels
- bars too close to text
- bottom oscillator overly wide and visually noisy

### Fix
This version improves spacing by:
- increasing metric-row spacing
- separating columns into:
  - label
  - value
  - state bucket
  - bar
- widening the focus card and cockpit cards
- shrinking the bottom oscillator into a more compact recent-history block

## Color logic
This version uses the requested scale:

- low = red
- mid = yellow
- high = green

## Modes
### Cockpit
Shows:
- Path Quality
- Micro M1
- Macro Background
- Raw Axes
- Diagnostics

### Focus
Shows one larger selected section:
- Path
- Micro
- Regime
- Macro
- Raw

## Notes
Because the dashboard now does full object cleanup before redrawing, it prioritizes a clean and correct screen state over retaining old objects.
That is intentional to eliminate ghost panels and duplicated sections.
