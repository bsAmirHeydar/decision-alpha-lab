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
7. Visual profile orchestration
8. Audit and CSV reconciliation
9. Visual smoke-test harness
10. Hook v1 freeze and training contract
```


## Implemented overlays

```text
08_phase01_node_source_adapter_implementation.md
09_phase02_cyclehook_sequence_builder_implementation.md
10_phase03_y_axis_opposite_extremes_implementation.md
11_phase04_nd_death_x_closure_skeleton_implementation.md
12_phase05_hook_type_abc_classifier_implementation.md
13_phase06_xy_closure_quality_score_implementation.md
14_phase07_visual_profile_orchestrator_implementation.md
15_phase08_audit_csv_reconciliation_implementation.md
16_phase09_visual_smoke_test_harness_implementation.md
17_phase10_freeze_training_contract_implementation.md
```


## Implementation overlay note — Phase 10

Phase 10 implements the Hook v1 freeze and training contract. It does not draw
new Hook structure. It checks Phase 08 audit state, Phase 09 visual smoke state,
Phase 06 quality record availability, file-error health, selected display
family, and optional strict-lock rules before marking Hook output as
training-ready.

The central display-family selector is now the first visible input of the
expert:

```text
InpNDSHookDisplayFamily = RALLY_ONLY | HOOK_ONLY | RALLY_AND_HOOK
```

```text
Phase 10 => Hook v1 freeze and training contract
```
