# EXP0013 Astro Fractal M1 Oscillator Guide

This guide documents the detailed fractal oscillator layer for EXP0013.

The goal is to observe the **quality of one-minute movement** without turning the chart into a text wall.

The indicator is research-only. It does not trade, does not predict direction, and does not modify orders.

---

## Indicator files

```text
mql5/Indicators/Research/EXP0013_AstroFractalOscillator.mq5
mql5/Indicators/Research/EXP0013_AstroRawAxesOscillator.mq5
```

`EXP0013_AstroFractalOscillator` is the new detailed one.

---

## Runtime file rule

The CSV can be placed in either location:

```text
<MQL5 Data Folder>/MQL5/Files/astro_GMT3_M1_2026_to_now_mql.csv
<MQL5 Data Folder>/MQL5/Files/astro/astro_GMT3_M1_2026_to_now_mql.csv
```

The reader also tries MetaQuotes Common Files as a fallback:

```text
C:\Users\ABN\AppData\Roaming\MetaQuotes\Terminal\Common\Files\astro_GMT3_M1_2026_to_now_mql.csv
```

Recommended input:

```text
InpAstroCsvFile         = astro_GMT3_M1_2026_to_now_mql.csv
InpBrokerGmtOffsetHours = 0
InpRequireExactBarTime  = true
InpMaxBarsToProcess     = 10000
```

The CSV already contains `broker_time`, so the indicator matches chart candle open time directly against CSV `broker_time`. There is no second GMT shift.

---

## Presets

The indicator has several display presets. Each preset uses the same data but plots a different logical layer.

### 1. RAW AXES

Shows the original Level 1 axes:

```text
Impulse
Friction
Flow
Pressure
Transition
MoonTempo
SaturnDrag
```

Use this when you want the simplest raw read.

---

### 2. MACRO BACKGROUND

Shows slow/background state:

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

Meaning:

- `MacroFlow`: broad smoothness from slower geometry.
- `MacroDrag`: slow structural resistance and compression.
- `MacroPressure`: slow hard-pressure background.
- `MacroTransition`: station/ingress/background regime-change risk.
- `Expansion`: fire/air/cardinal expansion tendency.
- `Compression`: earth/water/fixed compression tendency.
- `OuterStation`: slow-planet station risk.
- `StructuralBias`: net broad expansion minus compression.

This layer is not for exact M1 entry. It is the background weather.

---

### 3. REGIME ENGINE

Shows the active movement regime:

```text
MarsImpulse
MarsCleanImpulse
MarsSatFriction
MercuryNoise
JupiterSupport
SaturnResistance
VenusMarsCohesion
```

Meaning:

- `MarsImpulse`: raw active movement force.
- `MarsCleanImpulse`: movement force after friction/noise control.
- `MarsSatFriction`: Mars-Saturn drag and blocked movement.
- `MercuryNoise`: decision/noise/fake-move disturbance.
- `JupiterSupport`: expansion support.
- `SaturnResistance`: structural resistance and delay.
- `VenusMarsCohesion`: smoother Mars expression through Venus-Mars support.

This layer is very important for breakout and impulse strategies.

---

### 4. MOON / MICRO M1

Shows the short-term timing layer:

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

Meaning:

- `MoonTempo`: short-term M1 timing speed.
- `MoonPressure`: lunar hard-pressure noise.
- `MoonFlow`: lunar soft-flow support.
- `MoonDrag`: lunar Saturn drag.
- `MoonBoundary`: lunar sign/phase boundary risk.
- `MoonOOB`: Moon out-of-bounds intensity.
- `MicroNoise`: combined short-term noise.
- `MicroClean`: short-term clean movement context.

This layer is the closest to M1 candle quality.

---

### 5. M1 PATH QUALITY

Shows the final market-path translation:

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

Meaning:

- `CleanPath`: overall low-pullback path candidate.
- `CleanImpulse`: impulse with controlled friction.
- `SmoothCont`: smooth continuation candidate.
- `BreakoutFT`: breakout follow-through candidate.
- `PullbackRisk`: higher means worse.
- `ChopRisk`: higher means worse.
- `M1CleanWindow`: final one-minute clean-window score.
- `M1DirtyWindow`: final one-minute dirty-window warning.

This is the most useful preset for visual testing.

---

### 6. COMPACT JACKPOT

A reduced version for Roulette/Jackpot observation:

```text
M1CleanWindow
M1DirtyWindow
BreakoutFT
PullbackRisk
CleanImpulse
ChopRisk
```

Use this when the chart is too busy.

---

## Fast reading models

### Clean breakout window

```text
M1CleanWindow high
BreakoutFT high
PullbackRisk low
M1DirtyWindow low
```

Interpretation:

The astro state is more compatible with a clean breakout-style move, if the market itself gives a valid breakout signal.

---

### Clean impulse window

```text
MarsCleanImpulse high
CleanImpulse high
MarsSatFriction low
MercuryNoise low
```

Interpretation:

There is active movement force with less drag/noise.

---

### Smooth continuation window

```text
MacroFlow high
MoonFlow high
SmoothCont high
SaturnResistance low
```

Interpretation:

Better for smooth continuation than violent breakout.

---

### Dirty M1 warning

```text
M1DirtyWindow high
PullbackRisk high
ChopRisk high
MicroNoise high
```

Interpretation:

Even if the market moves, it may be noisy, choppy, or pullback-heavy.

---

## Important rule

The market still gives direction.

The astro oscillator gives path-quality context.

Correct question:

```text
If the market gives a valid direction here, does the sky-state look like clean impulse, smooth continuation, or dirty chop?
```

Wrong question:

```text
Does this oscillator tell me buy or sell?
```

---

## Validation targets

These oscillator values must later be validated against market path metrics:

```text
MAE_R
pullback_depth_R
path_efficiency
bars_to_target
opposite_close_count
TP before MAE > 0.5R
```

The oscillator is only useful if high clean-window states actually reduce MAE/pullback or improve path efficiency out of sample.
