# Phoenix Flag Counting Implementation Ladder V1

This document is part of the implementation ladder for the Phoenix Flag Counting engine. The ladder is intentionally layered so that lower layers become frozen foundations before higher layers are allowed to depend on them.

Global non-negotiables:

- All structural decisions use candle `high` and `low` only.
- `open`, `close`, candle body, candle color, volume, and indicators are not structural inputs.
- Equality is not a break. A level is broken only by a strict pass beyond it.
- The renderer is non-authoritative. It may only draw logical objects emitted by engines.
- Main-chart rendering and audit rendering are separate products.
- Every layer must expose enough audit fields to prove why an object exists.
- A higher layer may never silently repair a lower-layer defect.

# Level 12 — Renderer and Label Layout

## Purpose

Renderer turns emitted objects into chart objects. It must never create, validate, reject, confirm, or merge structures. It is a display layer only.

## Owned source module

```text
mql5/Include/FlagCountingPhoenix/FP_Renderer.mqh
```

## Inputs

```text
visible_events[]
visible_hooks[]
audit_display_flags
rates[]
rates_total
chart_config
```

## Non-authority rule

Renderer cannot infer missing F structures. Renderer cannot hide semantically visible objects except by explicit display budget rules provided by canonicalization layer.

## Object naming

All objects must use a prefix:

```text
DAL_FCP_
```

Object names must include:

```text
engine version
object type
event/hook id
segment id when polyline segment
```

## Layering

Recommended layers:

```text
background gray Hook/ND arcs
thin low-priority high-L structures
colored F body curves
labels
selected/debug overlay
```

## Curve contract

### Flag body

Draw:

```text
Origin -> Leg1 straight line
Leg1 -> Waist -> Leg2 smooth curve
```

Curve x-axis sampling must use candle index and map back to `rates[index].time`.

### Hook/ND

Draw gray arc:

```text
cycle_start -> cycle_extreme -> resolve/close
```

Only in main chart if the Hook explains a visible F1 or diagnostic mode requests all hooks.

## Label contract

Main chart labels must be concise and readable.

Default main label:

```text
F1 L13 confirmed
F2 L8 qualified
F3 L21 locked
ND L5 #3
```

Detailed audit label may include:

```text
O/A/W/B node ids
parent id
phase id
source mode
hidden reason
```

## Label stacking

Labels must stack by:

```text
local time cluster
local price cluster
peak/valley side
semantic priority
```

Rules:

- peak labels above price;
- valley labels below price;
- older label closer to price;
- newer/less important label farther away;
- audit labels can be pushed farther than main labels;
- label layout must be deterministic.

## Default display modes

### Clean main chart

```text
DetailedLabels = false
ShowParentIds = false
ShowOriginLabels = false
ShowInternalLabels = false
ShowHookCountLabels = false
DrawOnlyFlagSeedHooks = true
```

### Audit chart

```text
DetailedLabels = true
ShowParentIds = true
ShowOriginLabels = true
ShowInternalLabels = true
ShowHookCountLabels = true
DrawOnlyFlagSeedHooks = false
```

## Acceptance tests

### Test 01 — Renderer cannot change counts

Toggling detailed labels must not change number of emitted logical events.

### Test 02 — Object cleanup

On redraw, stale old segments must be deleted.

### Test 03 — Gap-safe curve

Curves must not distort across gaps because they sample candle indices.

### Test 04 — Main chart readable

With clean main chart defaults, no dense column of raw internal numbers should appear.

## Failure symptoms

- Old curve fragments remain after redraw.
- Main chart shows audit numbers despite clean settings.
- Curves bend strangely across weekends.
- Renderer patch changes which F structures exist.

## Freeze condition

Renderer is frozen when it can draw a fixed emitted object list in clean and audit modes without changing the object list itself.
