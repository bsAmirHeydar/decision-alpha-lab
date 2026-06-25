# EXP0013 Astro Dashboard V3 - Interactive Cockpit

This patch upgrades the dashboard into a more professional interactive cockpit.

## Main goals

- cleaner screen layout
- all major astro states visible
- open/close behavior through clickable chart buttons
- cockpit mode and focus mode
- more useful diagnostics when the row is not found
- stable redraws without tick-by-tick flicker

## File

```text
mql5/Experts/Research/EXP0013_AstroUnifiedDashboardEA.mq5
```

## What changed

### 1) Interactive header controls

The dashboard now has clickable chart buttons:

- `COCKPIT`
- `PATH`
- `MICRO`
- `REGIME`
- `MACRO`
- `RAW`
- `TEXT ON/OFF`
- `OSC ON/OFF`
- section toggles:
  - `PTH`
  - `MIC`
  - `REG`
  - `MAC`
  - `RAW`
- `RELOAD`

### 2) Two view modes

#### Cockpit mode

Shows multiple cards at once:

- Path Quality
- Micro M1
- Regime Engine
- Macro Background
- Raw Axes
- Diagnostics

#### Focus mode

Shows one selected section in larger form, plus diagnostics and oscillator.

### 3) Open/close behavior

In cockpit mode you can hide or show each section using the short toggle buttons:

- `PTH`
- `MIC`
- `REG`
- `MAC`
- `RAW`

This gives the requested open/close workflow without relying on a separate custom indicator.

### 4) Better diagnostics

When the chart says `ROW NOT FOUND`, the diagnostics card now makes the problem easier to inspect:

- CSV loaded or not
- row count
- actual source file
- current chart candle time
- whether lookup is exact or fallback
- matched broker time if available
- hint text

## Live usage recommendation

```text
InpAstroCsvFile          = astro_live_mql.csv
InpBrokerGmtOffsetHours  = 0
InpRequireExactBarTime   = true
InpReloadCsvEverySeconds = 10
InpRefreshSeconds        = 1
InpInitialViewMode       = ASTRO_VIEW_COCKPIT
InpInitialFocusSection   = ASTRO_SEC_PATH
```

## Historical usage recommendation

```text
InpAstroCsvFile          = astro_GMT3_M1_2026_to_now_mql.csv
InpBrokerGmtOffsetHours  = 0
InpRequireExactBarTime   = true
InpReloadCsvEverySeconds = 0
InpRefreshSeconds        = 1
```

## Interpretation structure

The dashboard is intended to answer:

```text
If the market already gives a direction,
how clean or dirty is the path likely to be?
```

### Path Quality

Use this card for:

- clean path
- clean impulse
- smooth continuation
- breakout follow-through
- pullback risk
- chop risk
- clean M1 window
- dirty M1 window

### Micro M1

Use this card for:

- moon tempo
- moon pressure
- moon flow
- moon drag
- moon boundary
- moon OOB
- micro noise
- micro cleanliness

### Regime Engine

Use this card for:

- impulse support
- friction drag
- mercury noise
- jupiter support
- saturn resistance

### Macro Background

Use this card for:

- macro flow
- macro drag
- macro pressure
- transition state
- expansion/compression
- outer station risk
- structural bias

### Raw Axes

Use this card as the basic astro layer:

- Flow
- Impulse
- Friction
- Pressure
- Transition
- MoonTempo
- SaturnDrag

## Operating idea

```text
Direction = market logic
Path quality = astro dashboard context
```

This remains a research interface, not a direct signal engine.
