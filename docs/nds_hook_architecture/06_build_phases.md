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
