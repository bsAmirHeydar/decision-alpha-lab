# EXP0013 Tester open error [3] fix

## Error

```text
Tester expert file ...\MQL5\Indicators\Shared Projects\decision-alpha-lab\mql5\Indicators\Research\ open error [3]
```

## Meaning

This is not an astro-calculation problem and not a CSV problem.

It means the Strategy Tester is trying to load a **folder path** under `Indicators\Research\` as if it were an **Expert Advisor file**.

In other words, the tester was pointed at:

```text
...\Indicators\...\Research\
```

instead of a compiled `.ex5` file.

Windows/MQL error `3` means:

```text
path not found / invalid file path
```

For this case the practical cause is usually one of these:

- the tester is in Expert mode while an indicator folder was selected
- the selected item is `Indicators\Research\` instead of an actual indicator file
- the indicator was not compiled into `.ex5`
- Shared Projects added an extra nested path and the selected tester path became ambiguous

---

## Correct runtime roles

There are two correct ways to run this research visualizer.

### Option A — run the indicator directly

Compile:

```text
mql5/Indicators/Research/EXP0013_AstroFractalOscillator.mq5
```

Then attach the compiled indicator to a chart or to the Visual Tester chart.

Do **not** select the `Research` folder itself.

### Option B — run the tester host EA

Compile:

```text
mql5/Experts/Research/EXP0013_AstroFractalOscillator_TesterHost.mq5
```

Then select this file in Strategy Tester as the **Expert**:

```text
Experts\Research\EXP0013_AstroFractalOscillator_TesterHost.ex5
```

The host EA sends no orders. It only tries to load the oscillator with `iCustom()` and add it to the Visual Tester chart.

This is the safer option when the tester UI keeps trying to open an indicator folder as an Expert file.

---

## Added safety files

This patch adds:

```text
mql5/Experts/Research/EXP0013_AstroFractalOscillator_TesterHost.mq5
mql5/Indicators/EXP0013_AstroFractalOscillator.mq5
```

The top-level indicator copy makes it easier to load via:

```text
EXP0013_AstroFractalOscillator
```

instead of relying only on:

```text
Research\EXP0013_AstroFractalOscillator
```

The tester host tries multiple paths:

```text
Research\EXP0013_AstroFractalOscillator
EXP0013_AstroFractalOscillator
Shared Projects\decision-alpha-lab\mql5\Indicators\Research\EXP0013_AstroFractalOscillator
```

---

## Correct compile order

Compile in this exact order:

```text
1. mql5/Indicators/Research/EXP0013_AstroFractalOscillator.mq5
2. mql5/Indicators/EXP0013_AstroFractalOscillator.mq5
3. mql5/Experts/Research/EXP0013_AstroFractalOscillator_TesterHost.mq5
```

If you only want one indicator file, compile step 1 and step 3.

---

## Correct Strategy Tester selection

If the tester tab is set to Expert/EA mode, choose:

```text
EXP0013_AstroFractalOscillator_TesterHost
```

Do not choose:

```text
Indicators\Research\
```

Do not choose a directory. Choose the compiled `.ex5`.

---

## CSV input

Recommended input for the host and indicator:

```text
InpAstroCsvFile         = astro_GMT3_M1_2026_to_now_mql.csv
InpBrokerGmtOffsetHours = 0
InpRequireExactBarTime  = true
InpMaxBarsToProcess     = 10000
```

The CSV reader tries all valid runtime locations:

```text
MQL5\Files\<input>
MQL5\Files\<basename>
MQL5\Files\astro\<basename>
Common\Files\<input>
Common\Files\<basename>
Common\Files\astro\<basename>
```

---

## Important

The tester host does not trade.
It has no `CTrade` calls and no order logic.
It is only a visual loader for the oscillator.
