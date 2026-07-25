# EXP0013 Unified Dashboard EA

## Why this patch exists

The custom indicator route caused Strategy Tester / Shared Projects loading problems.
This patch stops depending on indicators.

The new file is an Expert Advisor:

```text
mql5/Experts/Research/EXP0013_AstroUnifiedDashboardEA.mq5
```

It is research-only and sends no orders.

## What it does

It draws everything with chart objects:

- text diagnostics
- current fractal astro state
- pseudo-oscillator 0..100 dot map
- preset views for macro, regime, micro, and M1 path quality
- a manual-analysis board for discretionary reading
- all 12 tracked bodies: Sun, Moon, Mercury, Venus, Mars, Jupiter, Saturn, Uranus, Neptune, Pluto, True Node, Mean Node

It does not call `iCustom`.
It does not load an indicator.
It does not read `.xlsx`.
It reads the Python-generated `.csv`.

## Inputs for historical CSV

```text
InpAstroCsvFile = astro_GMT3_M1_2026_to_now_mql.csv
InpBrokerGmtOffsetHours = 0
InpRequireExactBarTime = true
InpReloadCsvEverySeconds = 0
InpPreset = ASTRO_DASH_M1_PATH
```

## Inputs for live Python bridge

```text
InpAstroCsvFile = astro_live_mql.csv
InpBrokerGmtOffsetHours = 0
InpRequireExactBarTime = true
InpReloadCsvEverySeconds = 10
InpPreset = ASTRO_DASH_M1_PATH
```

## Presets

### ASTRO_DASH_COMPACT_JACKPOT

Most compact view for execution gating:

```text
M1CleanWindow
M1DirtyWindow
BreakoutFT
PullbackRisk
CleanImpulse
ChopRisk
```

### ASTRO_DASH_RAW_AXES

Level 1 axes:

```text
Flow
Impulse
Friction
Pressure
Transition
MoonTempo
SaturnDrag
```

### ASTRO_DASH_MACRO

Slow-background layer:

```text
MacroFlow
MacroDrag
MacroPressure
MacroTransition
Expansion
Compression
OuterStation
StructuralBias
```

### ASTRO_DASH_REGIME

Active movement regime:

```text
MarsImpulse
MarsCleanImpulse
MarsSatFriction
MarsJupExpansion
MercuryNoise
VenusMarsCoh
JupiterSupport
SaturnResistance
```

### ASTRO_DASH_MICRO_M1

Lunar/Mercury short-term M1 layer:

```text
MoonTempo
MoonPressure
MoonFlow
MoonDrag
MoonBoundary
MoonOOB
MicroNoise
MicroClean
```

### ASTRO_DASH_M1_PATH

Default recommended M1 path-quality layer:

```text
CleanPath
CleanImpulse
SmoothCont
BreakoutFT
PullbackRisk
ChopRisk
M1CleanWindow
M1DirtyWindow
```

## Reading rule

Market gives direction.  
Astro gives path-quality context.

The unified dashboard is now also meant for manual reading. The right-side manual board condenses:

- macro bias
- path cleanliness vs friction
- nodal / eclipse event field
- timing trigger state
- grouped planetary positions and cues

Use it as a reading cockpit, not only as a raw CSV monitor.

Correct question:

```text
If market gives a signal here, does the astro environment look clean, dirty, impulsive, smooth, or transitional?
```

Wrong question:

```text
Does astrology alone say buy or sell?
```
