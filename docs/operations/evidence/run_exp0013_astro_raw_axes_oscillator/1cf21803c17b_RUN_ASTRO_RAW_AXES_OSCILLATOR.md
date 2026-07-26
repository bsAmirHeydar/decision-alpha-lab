# Run EXP0013 Astro Raw Axes Oscillator

## Compile

```text
mql5/Indicators/Research/EXP0013_AstroRawAxesOscillator.mq5
```

## Attach in chart or Visual Tester

Recommended compact inputs:

```text
InpAstroCsvFile         = astro_GMT3_M1_2026_to_now_mql.csv
InpBrokerGmtOffsetHours = 0
InpRequireExactBarTime  = true
InpMaxBarsToProcess     = 5000
InpShowFlow             = true
InpShowImpulse          = true
InpShowFriction         = true
InpShowPressure         = true
InpShowTransition       = false
InpShowMoonTempo        = false
InpShowSaturnDrag       = false
```

If your CSV is stored in the `astro` subfolder under `MQL5\Files`, use:

```text
InpAstroCsvFile = astro\astro_GMT3_M1_2026_to_now_mql.csv
```

## Visual reading order

1. Impulse
2. Friction
3. Pressure
4. Flow
5. optional: Transition / MoonTempo / SaturnDrag

## First interpretation pass

```text
Impulse up + Friction down + Pressure controlled
=> cleaner breakout candidate

Flow up + Friction down
=> smoother continuation candidate

Friction up + Pressure up + Transition up
=> chop / dirty-path warning
```
