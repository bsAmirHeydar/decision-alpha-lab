# EXP0013 Astro Oscillator Compile Fix + Fractal Detail Plan

## Compile fix

The first oscillator version used non-standard plot declarations:

```mql5
#property plot1 "Flow"
```

Some MQL5 builds reject this syntax with:

```text
'plot1' - unknown property
```

The corrected indicator now uses standard MQL5 indicator properties:

```mql5
#property indicator_label1 "Flow"
#property indicator_type1  DRAW_LINE
#property indicator_color1 clrAqua
```

This is the supported MQL5 format and should compile normally.

---

## Current oscillator scope

Current file:

```text
mql5/Indicators/Research/EXP0013_AstroRawAxesOscillator.mq5
```

It plots the Level 1 raw axes:

```text
Flow
Impulse
Friction
Pressure
Transition
MoonTempo
SaturnDrag
```

Default compact mode shows only:

```text
Flow
Impulse
Friction
Pressure
```

---

## Next stage: Fractal Astro Detail Model

The current oscillator is intentionally simple. The next professional version should be fractal:

```text
Major sky state  -> slow planets / macro background
Middle sky state -> Mars/Jupiter/Saturn relation / regime pressure
Fast sky state   -> Moon/Mercury/Venus tempo / intraday timing
Micro candle use -> M1 path-quality reading
```

The goal is not to predict direction directly. The goal is to understand the **quality of M1 movement**:

```text
Will the next market-given direction have a clean path, low pullback, and follow-through?
```

---

## Layer A — Macro / Major planets

Bodies:

```text
Jupiter
Saturn
Uranus
Neptune
Pluto
```

Purpose:

```text
background regime
structural compression
macro expansion/contraction
long-horizon pressure field
```

Potential features:

```text
macro_flow
macro_drag
macro_transition
jupiter_saturn_geometry
saturn_outer_pressure
outer_station_window
```

Interpretation for M1:

Macro does not time entries. It gives the background environment.

---

## Layer B — Regime / middle planets

Bodies:

```text
Mars
Jupiter
Saturn
Venus
Mercury
```

Purpose:

```text
impulse quality
movement pressure
friction / resistance
market tempo compatibility
```

Potential features:

```text
mars_impulse
mars_saturn_friction
mars_jupiter_expansion
venus_mars_flow
mercury_noise
saturn_drag
```

Interpretation for M1:

This layer is the main path-quality layer for breakout and continuation.

---

## Layer C — Fast timing / Moon layer

Bodies:

```text
Moon
Moon aspects
Moon phase
Moon declination
Moon speed
Moon ingress / void-of-course
```

Purpose:

```text
short-term rhythm
intraday acceleration
micro pullback risk
timing sensitivity
```

Potential features:

```text
moon_tempo
moon_pressure
moon_saturn_drag
moon_mars_impulse
moon_phase_boundary
moon_ingress_near
moon_decl_oob
```

Interpretation for M1:

This is the most important timing layer for one-minute path behavior.

---

## Layer D — Market path validation layer

Astro features must be validated against real market path metrics:

```text
MAE_R
MFE_R
pullback_depth_R
path_efficiency
bars_to_target
opposite_close_count
TP_before_MAE_0_5R
```

No astro feature is accepted as useful until it improves these market metrics out-of-sample.

---

## Proposed future oscillator groups

To prevent clutter, the next indicator should not show everything at once. It should have display presets:

```text
Preset 1: RAW AXES
Flow, Impulse, Friction, Pressure

Preset 2: MACRO
macro_flow, macro_drag, macro_transition, outer_pressure

Preset 3: MIDDLE / REGIME
mars_impulse, mars_saturn_friction, mars_jupiter_expansion, mercury_noise

Preset 4: MOON / MICRO
moon_tempo, moon_pressure, moon_drag, moon_boundary

Preset 5: PATH QUALITY
clean_path, breakout_followthrough, pullback_risk, chop_risk
```

This keeps the visual tester readable while allowing very detailed analysis.

---

## Important rule

The project should not use astro as a direct buy/sell engine.

The correct contract is:

```text
market execution gives direction
astro fractal state gives path-quality context
Distribution Engineering validates the effect
```
