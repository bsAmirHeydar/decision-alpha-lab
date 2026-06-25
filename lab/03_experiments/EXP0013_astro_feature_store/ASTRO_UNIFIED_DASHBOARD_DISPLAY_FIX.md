# EXP0013 Astro Unified Dashboard EA - Display and Update Fix

This patch improves the dashboard rendering quality and removes the visible cut/blink effect.

## What was wrong before

The previous version used a full `DeleteByPrefix()` redraw on every render cycle.
That caused:

- visible flicker / cut-and-return effect
- unstable live updates
- overlapping oscillator content because all metrics were drawn into one shared cloud
- long source-path text that pushed layout out of shape

## What changed

### 1) No more full delete on every refresh

The dashboard now updates objects **in place**.
Only stale oscillator point objects from the previous frame are deleted if they are no longer needed.

This makes the panel much more stable in live mode.

### 2) Timer-driven refresh only

`OnTick()` no longer forces redraws.
The UI is refreshed only from `OnTimer()`.

This reduces jitter and prevents unnecessary re-rendering on every market tick.

### 3) Row-based oscillator

The previous oscillator was a single shared dot cloud.
It is now a **row-based sparkline board**:

- one row per metric
- left-side label
- current numeric value
- current mini-bar
- right-side history sparkline for the last N bars

This is much easier to read, especially for M1 path-quality work.

### 4) Cleaner text panel

The text panel now:

- uses fewer lines
- shortens long source-file paths
- trims long thesis strings
- keeps the important status, time, and metric values visible

## Recommended settings

For stable live usage:

```text
InpAstroCsvFile          = astro_live_mql.csv
InpReloadCsvEverySeconds = 10
InpRefreshSeconds        = 1
InpPreset                = ASTRO_DASH_M1_PATH
InpShowTextPanel         = true
InpShowOscillator        = true
```

For compact path-quality reading on M1:

```text
InpPreset = ASTRO_DASH_M1_PATH
```

For more micro timing detail:

```text
InpPreset = ASTRO_DASH_MICRO_M1
```

## Reading model

The dashboard still follows the same research rule:

```text
Market gives direction.
Astro gives path-quality context.
```

So the improved display should be read as:

- cleaner path vs dirtier path
- breakout follow-through vs chop risk
- micro-cleanliness vs micro-noise
- pullback risk vs clean impulse

not as direct buy/sell prediction.
