# Run EXP0013 Astro Fractal Oscillator through Tester Host

## 1. Compile

Compile:

```text
mql5/Indicators/Research/EXP0013_AstroFractalOscillator.mq5
mql5/Experts/Research/EXP0013_AstroFractalOscillator_TesterHost.mq5
```

Optional simpler path:

```text
mql5/Indicators/EXP0013_AstroFractalOscillator.mq5
```

## 2. Open Strategy Tester

Select Expert Advisor:

```text
EXP0013_AstroFractalOscillator_TesterHost
```

Do not select the Indicators folder.

## 3. Inputs

```text
InpIndicatorPath        = Research\EXP0013_AstroFractalOscillator
InpAstroCsvFile         = astro_GMT3_M1_2026_to_now_mql.csv
InpBrokerGmtOffsetHours = 0
InpRequireExactBarTime  = true
InpMaxBarsToProcess     = 10000
InpPreset               = ASTRO_OSC_M1_PATH_QUALITY
InpShowDiagnosticsLine  = true
InpTryFallbackPaths     = true
InpAddIndicatorToChart  = true
```

If Shared Projects pathing blocks the default indicator path, try:

```text
InpIndicatorPath = EXP0013_AstroFractalOscillator
```

or:

```text
InpIndicatorPath = Shared Projects\decision-alpha-lab\mql5\Indicators\Research\EXP0013_AstroFractalOscillator
```

## 4. Expected behavior

The EA host should load with a chart comment:

```text
STATUS: INDICATOR HANDLE OK
```

Then the oscillator should appear in a separate subwindow.

If the subwindow is not automatically added, the host still confirms whether the indicator handle is valid. In that case, attach the compiled indicator manually to the Visual Tester chart.
