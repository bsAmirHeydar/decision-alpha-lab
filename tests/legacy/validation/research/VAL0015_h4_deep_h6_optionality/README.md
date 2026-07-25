# VAL0015 — H4 Deep Atomic + H6 Optionality Report

This validation adds richer diagnostics to the official M0004 atomic report and introduces H0006 reversal optionality metrics.

## Expected key lines

- `DAL_D0010_ATOMIC_INFORMATION`
- `DAL_D0010_ATOMIC_RUN_DISTRIBUTION`
- `DAL_D0010_ATOMIC_BATCH_INTENSITY`
- `DAL_H0006_OPTIONALITY_FAST`
- `DAL_H0006_OPTIONALITY_MAIN`
- `DAL_H0006_OPTIONALITY_SLOW`
- `DAL_H0006_OPTIONALITY_STRESS_FAST`
- `DAL_H0006_OPTIONALITY_STRESS_MAIN`
- `DAL_H0006_OPTIONALITY_STRESS_SLOW`

## Suggested input profile

Fast development:

```text
InpAtomicPermutationIterations = 100
InpAtomicPrintDeepReport = true
InpAtomicPrintH6OptionalityReport = true
InpAtomicStressH6Optionality = true
InpH6HorizonBarsFast = 5
InpH6HorizonBarsMain = 20
InpH6HorizonBarsSlow = 50
InpH6AtrPeriod = 14
InpH6TailAtr1 = 2.0
InpH6TailAtr2 = 4.0
InpH6TailAtr3 = 8.0
```

Publication/stress:

```text
InpAtomicPermutationIterations = 500
InpAtomicStressContextShuffle = true
InpAtomicStressH6Optionality = true
```
