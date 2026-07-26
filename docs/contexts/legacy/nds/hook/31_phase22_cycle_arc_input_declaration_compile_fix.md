# Phase 22 Compile Fix — Missing Cycle Arc Color Input

## Issue

MetaEditor reported:

```text
undeclared identifier 'InpHookPhase02CycleArcUseSequenceColor'
FlagCountingPhoenixExperiment.mq5
```

The Phase 22 loader assigned:

```mql5
cfg.cycle_arc_use_sequence_color = InpHookPhase02CycleArcUseSequenceColor;
```

but the corresponding expert input was missing from the input declaration block.

## Fix

Added:

```mql5
input bool InpHookPhase02CycleArcUseSequenceColor = false;
```

near the Phase 02 cycle-arc drawing inputs.

## Behavior

No Hook logic changed. This is a compile-only fix.
