# Run EXP0013 Astro Fractal Oscillator

## Compile

```text
mql5/Indicators/Research/EXP0013_AstroFractalOscillator.mq5
```

Also compile the raw-axis version if needed:

```text
mql5/Indicators/Research/EXP0013_AstroRawAxesOscillator.mq5
```

## Recommended first setup

```text
InpAstroCsvFile         = astro_GMT3_M1_2026_to_now_mql.csv
InpBrokerGmtOffsetHours = 0
InpRequireExactBarTime  = true
InpMaxBarsToProcess     = 10000
InpPreset               = ASTRO_OSC_M1_PATH_QUALITY
InpShowDiagnosticsLine  = true
```

## If the indicator appears but shows no lines

Check the Experts/Journal tab. The loader tries these locations:

```text
MQL5\Files\<input>
MQL5\Files\<basename>
MQL5\Files\astro\<basename>
Common\Files\<input>
Common\Files\<basename>
Common\Files\astro\<basename>
```

If the CSV is not loaded, the indicator still loads and draws a diagnostic zero line instead of disappearing silently.

## Best visual presets

For most M1 observation:

```text
ASTRO_OSC_M1_PATH_QUALITY
```

For compact roulette/jackpot read:

```text
ASTRO_OSC_COMPACT_JACKPOT
```

For root-cause breakdown:

```text
ASTRO_OSC_MACRO_BACKGROUND
ASTRO_OSC_REGIME_ENGINE
ASTRO_OSC_MOON_MICRO
```
