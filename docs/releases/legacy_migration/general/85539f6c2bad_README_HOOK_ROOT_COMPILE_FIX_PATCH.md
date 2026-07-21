# Hook Root Compile Fix Patch

## Problem

`FP_HookPhase03Engine.mqh` through `FP_HookPhase06Engine.mqh` can still call:

```mql5
FP_HookP02BuildSequencesWithRates(...)
```

After the Hook root rebuild, `FP_HookPhase02Rules.mqh` exposed only:

```mql5
FP_HookP02BuildSequences(...)
```

This created the compile error:

```text
undeclared identifier 'FP_HookP02BuildSequencesWithRates'
```

## Fix

Add a compatibility wrapper:

```mql5
int FP_HookP02BuildSequencesWithRates(const MqlRates &rates[],
                                      const int copied,
                                      const FP_HookPhase01Node &nodes[],
                                      const FP_HookPhase02Config &cfg,
                                      FP_HookPhase02Sequence &sequences[],
                                      FP_HookPhase02Report &report)
```

The wrapper forwards to the canonical seed-owned Phase 02 builder.

## Scope

Compile compatibility only.
