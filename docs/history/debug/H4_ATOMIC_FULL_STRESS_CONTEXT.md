# H4 Atomic Full Stress + Human Context Diagnostics

This release restores the full stress/test surface for the official H0004 atomic no-sample report while preserving the strict contract:

- no M0002 branch samples
- no sample order
- no same-candle fake sequencing
- raw M0001 events only
- known-time batches only
- mixed reversal/continuation batches skipped from transitions by default

## Added input toggles

Stress groups can now be enabled or disabled independently:

- `InpAtomicStressTransitionPermutation`
- `InpAtomicStressRunShuffle`
- `InpAtomicStressBlockConcentration`
- `InpAtomicStressCircularShift`
- `InpAtomicStressLocalBlockShuffle`
- `InpAtomicStressContextShuffle`

Human-context diagnostics are controlled by:

- `InpAtomicPrintHumanContextReport`
- `InpAtomicContextLookbackFast`
- `InpAtomicContextLookbackMain`
- `InpAtomicContextLookbackSlow`
- `InpAtomicContextEwmaAlpha`
- `InpAtomicContextStrongThreshold`

## Added report lines

The official atomic report can now print:

- `DAL_D0010_ATOMIC_RUN_SHUFFLE_STRESS`
- `DAL_D0010_ATOMIC_BLOCK_CONCENTRATION_STRESS`
- `DAL_D0010_ATOMIC_CIRCULAR_SHIFT_STRESS`
- `DAL_D0010_ATOMIC_LOCAL_BLOCK_SHUFFLE_STRESS`
- `DAL_D0010_ATOMIC_LAST_ONLY_QUALITY`
- `DAL_D0010_ATOMIC_HUMAN_CONTEXT_STATE`
- `DAL_D0010_ATOMIC_CONTEXT_SHUFFLE_STRESS`

## Interpretation

`LAST_ONLY` remains the direct one-step regime memory signal. The human-context reports test whether rolling or EWMA context over recent pure known-time batches adds information beyond last-only.

This is not a return to the old sample-based H4. All context and stress diagnostics are computed over pure atomic known-time batches.
