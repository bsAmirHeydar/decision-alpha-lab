# Flag Counting MQL5 Implementation

## Why this exists

The old split between `M0007` and `M0008` made F-counting harder to maintain. The new design treats F-counting as one experiment and one module family:

```text
mql5/Include/FlagCounting/*
mql5/Experts/FlagCounting/FlagCountingExperiment.mq5
```

## Include strategy

The expert uses relative quoted includes, not terminal-level angle includes. This avoids this error:

```text
file MQL5/Include/M0008/... not found
```

## Module layers

```text
DAL_FlagCountingTypes.mqh        shared event/node types
DAL_FlagCountingNodeDetector.mqh swing node detector and alternating compression
DAL_FlagCountingDetector.mqh     F1/F2 structural logic
DAL_FlagCountingRenderer.mqh     chart drawing only
```

## Reusability

Future execution or statistics modules should depend on `DAL_FlagCountingDetector.mqh` and ignore the renderer.

The event object is intentionally generic:

```text
level
parent_event_index
direction
status
branch_type
origin
leg1
waist
leg2
n1
n2
confirm
```

This allows the same detector output to be used for:

- chart visualization
- CSV export
- volatility around F nodes
- directional-memory tests
- continuation/reversal tests
- trade simulation
- multi-timeframe counting

## F2 symmetry / size filter

F2 now has an explicit parent-size symmetry filter. The body size of a flag is measured as the vertical price distance from its origin/start-of-leg to its Leg2 final point:

```text
flag_size = abs(Leg2.price - Origin.price)
```

For every F2 candidate:

```text
F2_size >= Parent_F1_size * InpF2MinParentSizeRatio
```

The default ratio is `1.0`, so F2 must be at least as large as its parent F1. This keeps F2 as a real continuation count, not a small noisy nested flag. The filter is controlled by:

```text
InpRequireF2AtLeastParentSize = true
InpF2MinParentSizeRatio = 1.0
```

