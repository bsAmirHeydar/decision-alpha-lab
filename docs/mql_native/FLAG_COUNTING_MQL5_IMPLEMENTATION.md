# Flag Counting MQL5 Implementation

The active expert is:

```text
mql5/Experts/FlagCounting/FlagCountingExperiment.mq5
```

It includes reusable modules from:

```text
mql5/Include/FlagCounting/
```

## Core architecture

```text
NodeDetector -> FlagCountingDetector -> optional Renderer
```

The detector emits `FC_FlagEvent` records. The renderer is optional and only draws body geometry and labels.

## Active levels

```text
F1 root
F2 child of F1 from F1.n2
F3 child of F2 from F2.n2
```

Continuation levels share the same builder and can be extended later.

## Confirmation and invalidation

```text
confirm = Leg2 rebreak before invalidation
F1 invalid = waist break
F2/F3 invalid = origin/start break
```

Internal `1/2` are labels/audit and child-origin points. They are not a hard validity gate for the parent body.

## Renderer

The renderer draws:

```text
origin -> leg1
leg1 -> waist -> leg2
F-level label
1/2 labels
```

No post-Leg2 lines are drawn.
