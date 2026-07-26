# 06 — Build Phases

## Phase 0 — Locate Central Expert and Protect Rally

Find the central expert that currently performs F-counting / Rally display.

Add display-family inputs, but keep default behavior as Rally-only.

Acceptance:

```text
existing F-counting output remains identical in Rally-only mode
```

## Phase 1 — Node Source Adapter

Build a Hook node adapter from the existing structural nodes used by F-counting.

Acceptance:

```text
Hook receives stable peak/valley node stream
```

## Phase 2 — CycleHook Object Model

Implement CycleHook objects for positive and negative directions.

Acceptance:

```text
origin, direction, death boundary, opposite Extreme, and lifecycle state exist
```

## Phase 3 — Multi-Sequence Builder

Implement positive and negative strict sequence building.

Acceptance:

```text
positive = descending valleys
negative = ascending peaks
multiple sequences can coexist
starter reuse rule is respected
```

## Phase 4 — X/Y Extraction

Extract X nodes and Y opposite Extremes.

Acceptance:

```text
X sequence and Y sequence are both visible and auditable
```

## Phase 5 — Closure + ND + Death

Implement:

```text
X closure
Y closure
XY closure
ND active state
death by origin penetration
```

Acceptance:

```text
alive / ND / closed / dead states are visible and consistent
```

## Phase 6 — Hook Type A/B/C

Implement positive and negative A/B/C classification.

Acceptance:

```text
Type A/B/C labels appear with reason and confidence
```

## Phase 7 — Visualization Controls

Add display controls for Hook-only, Rally-only, and both.

Acceptance:

```text
Rally-only unchanged
Hook-only clean
Both layers visible without object collisions
```

## Phase 8 — Audit and CSV Export

Add optional audit outputs.

Acceptance:

```text
chart view and CSV/debug output agree
```

## Phase 9 — Smoke Test

Run visual smoke tests on:

```text
bullish context
bearish context
positive Hook
negative Hook
alive sequence
dead sequence
X-only closure
XY closure
Type A
Type B
Type C
```

## Phase 10 — Freeze Hook v1

Once the visual and audit behavior is stable, freeze Hook v1.

After freeze, Hook can become training input.

Acceptance:

```text
Hook v1 is stable enough to feed context/zone/entry training
```


## Implementation overlay note — Phase 07

The current implementation sequence has one additional refinement layer before
view finalization:

```text
Phase 06 => X/Y closure quality scoring
Phase 07 => Visual profile orchestration for Phase 01..Phase 06
```

Phase 07 implements the planned visualization-control requirement through named
profiles instead of scattered per-phase toggles only.


## Implementation overlay note — Phase 08

Phase 08 implements the planned audit/export requirement as a reconciliation
layer over Phase 01 through Phase 07. It does not create new Hook objects and
does not draw chart objects. It verifies runtime report consistency, phase-chain
alignment, object-prefix uniqueness, nonnegative counters, and export/file-error
health before Hook output is trusted as training input.

```text
Phase 08 => Audit and CSV reconciliation
```


## Implementation overlay note — Phase 09

Phase 09 implements the planned smoke-test requirement as a runtime visual
smoke harness over Phase 01 through Phase 08. It checks the selected Phase 07
view profile, chart object census by Hook prefix, draw-contract consistency,
Phase 08 audit status, and optional smoke CSV outputs.

```text
Phase 09 => Visual smoke-test harness
```


## Implementation overlay note — Phase 10

Phase 10 finalizes the current Hook modular build as a freeze/training-contract
layer. It is intentionally no-draw and no-execution. It records whether Hook v1
is ready to become a downstream AI/training input by reconciling Phase 06
quality counts, Phase 08 audit status, Phase 09 visual-smoke status, selected
view profile, selected display family, and file-error health.

The display-family selector is now placed as the first visible input in the
central expert:

```text
InpNDSHookDisplayFamily
  FP_NDS_HOOK_DISPLAY_RALLY_ONLY
  FP_NDS_HOOK_DISPLAY_HOOK_ONLY
  FP_NDS_HOOK_DISPLAY_RALLY_AND_HOOK
```

```text
Phase 10 => Hook v1 freeze and training contract
```
