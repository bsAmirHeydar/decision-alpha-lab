# VAL0014 — H4 Atomic Full Stress + Human Context

Goal: restore the richer H0004 stress and context diagnostics without reintroducing M0002 samples or fake same-candle ordering.

Contract:

```text
sampleCalls=0
branchSamplesBuilt=0
m0002Calls=0
sequenceOrder=known_time_batch_sequence
sameKnownTimeEventsAreSimultaneous=1
mixedEnergyBatchPolicy=ambiguous_skip_from_transition
```

Recommended defaults:

```text
InpAtomicPermutationIterations = 100
InpAtomicStressTransitionPermutation = true
InpAtomicStressRunShuffle = true
InpAtomicStressBlockConcentration = true
InpAtomicStressCircularShift = true
InpAtomicStressLocalBlockShuffle = true
InpAtomicPrintHumanContextReport = true
InpAtomicStressContextShuffle = false
InpAtomicContextLookbackFast = 5
InpAtomicContextLookbackMain = 10
InpAtomicContextLookbackSlow = 20
InpAtomicContextEwmaAlpha = 0.35
InpAtomicContextStrongThreshold = 0.60
```

For publication runs, increase `InpAtomicPermutationIterations` to 500 or 1000. For speed, switch off individual stress toggles.
