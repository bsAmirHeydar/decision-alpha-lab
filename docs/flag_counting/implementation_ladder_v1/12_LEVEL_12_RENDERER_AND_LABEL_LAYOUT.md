# Level 12 — Renderer / Labels / Visual Layer

## Purpose

Level 12 turns the final Level 11 canonical stream into MetaTrader chart objects.

It is a **visual product only**. It cannot create structure, delete structure, confirm structure, lock structure, change ownership, repair hidden reasons, or decide parent/child truth. Those decisions already belong to Levels 01 through 11.

The renderer is allowed to do only these things:

```text
read FP_FlagEvent[]
read FP_HookBranch[]
read final visible_main / hidden_reason / canonical_id fields
apply user display filters
create/delete chart objects under one prefix
emit FP_LEVEL12 render audit
```

## Owned source modules

```text
mql5/Include/FlagCountingPhoenix/FP_RenderTypes.mqh
mql5/Include/FlagCountingPhoenix/FP_RenderRules.mqh
mql5/Include/FlagCountingPhoenix/FP_RenderAudit.mqh
mql5/Include/FlagCountingPhoenix/FP_Renderer.mqh
mql5/Experts/FlagCounting/FlagCountingPhoenixExperiment.mq5 # wiring only
```

## Execution order

```text
Level 11 canonicalization
-> Level 11.5 export/report
-> Level 12 renderer
-> FP_SUMMARY
```

Export must be able to run even when renderer is visually disabled. Renderer output is never the source of truth.

## Input contract

Renderer consumes:

```text
FP_FlagEvent events[] after Level 11 canonicalization
FP_HookBranch hooks[] after final Hook seed visibility
MqlRates rates[] from Level 01 canonical timebase
FP_RenderConfig
```

Renderer assumes:

```text
visible_main already means engine-approved main-chart visibility
hidden_reason already explains hidden objects
canonical_id / visual_id / structural_id already exist when available
rates[0] is oldest closed bar
```

## Output contract

Renderer returns:

```text
FP_RenderReport
FP_LEVEL12 sanity line
optional FP_LEVEL12 samples
chart objects under InpObjectPrefix only
```

`FP_RenderReport` counts:

```text
input_events / input_hooks
visible_events_seen / visible_hooks_seen
drawn_events / drawn_hooks
objects_requested / objects_created / object_create_failures
objects_deleted_by_prefix
duplicate_object_names
fallback_curves
event filter reasons
hook filter reasons
first/last drawn event and hook ids
```

The report is folded into `FP_DetectResult` so `FP_SUMMARY` exposes render counts.

## Object naming contract

Object names are derived from canonical identity by default:

```text
InpRenderUseCanonicalObjectNames = true
```

Preferred stems:

```text
<prefix>EV_<canonical_id>_<segment>
<prefix>HK_<visual_or_structural_id>_<segment>
```

Fallback stems:

```text
<prefix>EV_Q<event_id>_<segment>
<prefix>HK_H<branch_id>_<segment>
```

All names are sanitized into chart-safe ids. Renderer may truncate long ids, but it must keep deterministic naming for the same stream.

## Visibility contract

Default:

```text
InpRenderStrictVisibility = true
```

Meaning:

- hidden engine objects are not drawn;
- hidden engine objects are not reinterpreted as audit overlay by default;
- detailed labels can add more text to already-drawn objects, but cannot make hidden structures visible;
- `DrawInvalidated` is a display filter only and cannot change event status.

## Curve contract

### Flag body

```text
Origin -> Leg1 straight line
Leg1 -> Waist -> Leg2 index-sampled curve
```

The curve x-domain is candle index, then each sampled point maps back to `rates[index].time`. This keeps curves stable across session gaps and weekends.

### Hook / ND

```text
cycle_start/start -> extreme -> resolve
```

Hook arcs are drawn in the background by default:

```text
InpRenderDrawHookBack = true
```

Hooks are main-visible only if engine visibility and seed policy allow it.

## Label contract

Clean default labels are concise:

```text
F1 L13 confirmed
F2 L8 confirmed
F3 L21 locked
ND L5 #3 seed
```

Detailed mode may add:

```text
canonical id fragment
chain id fragment
O/A/W/B node ids
parent id
F2 size gate
F3 OR gate
F3 lock id
hidden reason for audit-visible hidden objects
```

Label stacking remains deterministic by:

```text
time-index cluster
price cluster
peak/valley side
lane counter
```

## New EA inputs

```text
InpPrintRenderSanity = true
InpPrintRenderSamples = false
InpRenderSampleLimit = 8
InpRenderStrictVisibility = true
InpRenderUseCanonicalObjectNames = true
InpRenderDeleteExistingByPrefix = true
InpRenderDrawHookBack = true
```

Existing visual filters remain:

```text
InpDrawF1/F2/F3
InpDrawBullish/Bearish
InpDrawCandidates/Confirmed/Locked/Invalidated
InpDrawHooks
InpDrawOnlyFlagSeedHooks
InpDetailedLabels
InpShowParentIds
InpShowOriginLabels
InpShowInternalLabels
InpShowHookCountLabels
```

## Acceptance tests

### Test 01 — Renderer does not change logical output

Toggle each renderer input and confirm exported `latest_events.csv` and `latest_hooks.csv` logical fields do not change.

### Test 02 — Prefix cleanup

With `InpRenderDeleteExistingByPrefix=true`, stale objects under the selected prefix disappear on redraw.

### Test 03 — Canonical naming

With `InpRenderUseCanonicalObjectNames=true`, object names contain deterministic canonical/visual ids rather than only unstable sequential ids.

### Test 04 — Strict visibility

With `InpRenderStrictVisibility=true`, no event or hook with `visible_main=false` appears on the chart.

### Test 05 — Gap-safe curves

On a range with session gaps, curves remain anchored to actual candle times and do not use interpolated timestamps.

### Test 06 — Clean chart defaults

With clean defaults, internal numbers and hook branch counts do not flood the chart.

## Failure symptoms

- `FP_LEVEL12 object_errors > 0`.
- `FP_LEVEL12 duplicate_names > 0` after deterministic naming.
- Hidden objects appear with strict visibility on.
- Curves have orphan segments after a redraw.
- Changing label settings changes export or event counts.
- Renderer becomes necessary to understand why an object exists.

## Freeze condition

Level 12 is frozen when:

```text
FP_LEVEL12 status=ok
render_errors=0 in FP_SUMMARY
export output remains stable across renderer toggles
strict visibility hides all hidden objects
canonical object names are deterministic
clean chart and audit chart are both readable
```
