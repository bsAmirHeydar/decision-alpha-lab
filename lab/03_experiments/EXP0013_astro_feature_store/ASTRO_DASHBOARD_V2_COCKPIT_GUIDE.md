# EXP0013 Astro Dashboard V2 - Cockpit Layout

This version replaces the crowded single oscillator cloud with a cockpit layout.

## Main EA

```text
mql5/Experts/Research/EXP0013_AstroUnifiedDashboardEA.mq5
```

The EA is research-only:

- no orders
- no iCustom
- no indicator path dependency
- no xlsx reading in MQL
- reads only runtime CSV
- draws text/cards directly with chart objects

## Why the display is more stable

The dashboard does not delete and recreate all objects on every refresh.
It updates the existing objects in-place. This avoids:

- flicker
- cut/return effect
- unstable live rendering
- overlapping text from stale labels

## View modes

### ASTRO_VIEW_COCKPIT

Default professional layout:

- header/status card
- Path Quality card
- Micro M1 card
- Regime Engine card
- Macro Background card

### ASTRO_VIEW_MICRO_FOCUS

Prioritizes the smallest meaningful layer:

- Micro M1
- Path Quality
- Regime
- Raw Axes

### ASTRO_VIEW_SINGLE_PRESET

Uses the older single preset text panel + row sparkline board.

## Recommended live inputs

```text
InpAstroCsvFile          = astro_live_mql.csv
InpBrokerGmtOffsetHours  = 0
InpRequireExactBarTime   = true
InpReloadCsvEverySeconds = 10
InpRefreshSeconds        = 1
InpViewMode              = ASTRO_VIEW_COCKPIT
InpPreset                = ASTRO_DASH_M1_PATH
InpShowTextPanel         = true
InpShowOscillator        = true
```

## Recommended historical/tester inputs

```text
InpAstroCsvFile          = astro_GMT3_M1_2026_to_now_mql.csv
InpBrokerGmtOffsetHours  = 0
InpRequireExactBarTime   = true
InpReloadCsvEverySeconds = 0
InpRefreshSeconds        = 1
InpViewMode              = ASTRO_VIEW_COCKPIT
```

## Reading order

### 1) Header verdict

The header gives a fast verdict:

```text
CLEAN_WINDOW
DIRTY_WARNING
BREAKOUT_SUPPORT
SMOOTH_CONT_SUPPORT
MIXED_NEUTRAL
```

This is not a trade signal. It is a path-quality diagnosis.

### 2) Path Quality

Main market translation:

- CleanPath
- CleanImpulse
- BreakoutFT
- PullbackRisk
- ChopRisk
- M1CleanWindow

### 3) Micro M1

Closest astrological layer to M1 path quality:

- MoonTempo
- MoonPressure
- MoonFlow
- MoonDrag
- MicroNoise
- MicroClean

### 4) Regime Engine

Movement/noise regime:

- MarsImpulse
- MarsCleanImpulse
- MarsSatFriction
- MercuryNoise
- JupiterSupport
- SaturnResistance

### 5) Macro Background

Slow context, not candle-by-candle entry logic:

- MacroFlow
- MacroDrag
- MacroPressure
- Expansion
- Compression
- OuterStation

## Research rule

```text
Market gives direction.
Astro gives path-quality context.
```

The cockpit should be validated against:

- MAE_R
- pullback_depth_R
- path_efficiency
- bars_to_target
- chop / opposite-close count
