# NDS Hook Architecture — Design Pack

This documentation freezes the Hook architecture before implementation.

The implementation target is the central expert that already performs Rally / F-counting. The existing Rally mode must remain unchanged. Hook rendering and Hook diagnostics should be added as a parallel display family.

## Primary Integration Goal

Add a display selector to the central expert:

```text
RALLY_ONLY
HOOK_ONLY
RALLY_AND_HOOK
```

Expected behavior:

```text
RALLY_ONLY      => existing F-counting / Rally behavior without changes
HOOK_ONLY       => draw Hook / CycleHook architecture only
RALLY_AND_HOOK  => draw both Rally/F-counting and Hook/CycleHook architecture
```

## Non-Negotiable Boundary

This is visualization and structural diagnostics only.

Do not add execution logic, broker requests, order sending, volume sizing, risk sizing, or live trading behavior.

## Core NDS Rule

Hook and CycleHook are the same algorithmic object.

The Hook layer must be built from the same NDS anatomy:

```text
Node
CycleHook
Sequence
X-axis
Y-axis
ND / return toward origin
death by origin penetration
opposite Extreme
Hook type A/B/C
fractal parent-child relation
```

## Build Philosophy

Hook must become infrastructure like F-counting.

The system should be built in layers:

```text
1. Object model
2. Sequence builder
3. X/Y extraction
4. Closure logic
5. Hook type classification
6. X/Y closure quality scoring
7. Visualization
7. Diagnostics and audit
8. Integration with Rally display mode
```
