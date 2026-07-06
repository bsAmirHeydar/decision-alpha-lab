---
type: training_note
id: HOOK-VAL-0006
title: Hook Validation Dataset and Learning Policy
domain: hook_validity
status: canonical_draft
related:
  - Zone Dataset
  - Hook Validity
  - Learning Objective
  - Anti-Pattern Worship
---

# HOOK-VAL-0006 — Hook Validation Dataset and Learning Policy

## 1. Purpose

The Hook Validity Layer should not remain only philosophical. It must become testable.

The dataset must separate:

- valid Hook After Hook,
- valid Hook After Opposing F3,
- invalid hook-like structures,
- valid hook zones,
- invalid or non-tradable hook zones.

This makes it possible to test whether the validity filter improves zone quality.

## 2. Primary Research Question

The main question is:

> Do valid hooks produce better risk-contract zones than generic hook-like structures?

Better does not mean higher win rate by default. Better means:

- better MFE/MAE,
- better potential/width,
- cleaner invalidation,
- fewer dead zones,
- better tail participation,
- smoother path after activation.

## 3. Dataset Rows

The preferred training event is not a candle. It is a **HookZoneEvent**.

A HookZoneEvent begins when a valid hook creates a potential zone and price later interacts with that zone.

Suggested event types:

- `hook_candidate_event`
- `valid_hook_event`
- `hook_zone_event`
- `hook_zone_touch_event`
- `hook_zone_outcome_event`

## 4. Required Fields

Suggested fields:

```text
symbol
timeframe
hook_id
hook_validity
hook_validity_type
previous_hook_id
shared_node_id
f3_id
f3_direction
hook_direction
zone_id
zone_start_price
zone_stop_price
zone_width
zone_width_atr
entry_edge
invalidation_edge
parent_zone_id
child_zone_id
touch_time
activation_time
outcome_window_bars
mfe
mae
mfe_mae_ratio
time_to_expansion
path_smoothness
stop_hit
dead_zone_flag
tail_expansion_flag
invalid_reason
```

## 5. Learning Objective

The model should not learn generic hook prediction.

It should learn:

- which valid hook zones are worth risk,
- which valid hooks still require child-zone refinement,
- which hook zones have high tail potential,
- which hook zones become dead zones,
- whether Hook After Hook or Hook After Opposing F3 performs differently.

## 6. Invalid Hook Logging

Invalid hooks should be logged as negative or observation-only samples.

This is important because the system should empirically verify that invalid hooks are weaker as zone sources.

However, invalid hooks must not be mixed with valid hooks under the same label. They need their own category.

## 7. Comparison Tests

The first research tests should compare:

1. Hook After Hook vs invalid hooks.
2. Hook After Opposing F3 vs invalid hooks.
3. Hook After Hook vs Hook After Opposing F3.
4. Valid hook zones with child refinement vs valid hook zones without child refinement.
5. Valid hook zones inside broader HTF context vs valid hook zones outside it.

## 8. Success Metrics

The validity filter is useful if valid hook zones show:

- lower average MAE,
- better MFE/MAE,
- better tail capture,
- cleaner stop logic,
- fewer dead zones,
- better path smoothness,
- better performance after lower-timeframe refinement.

## 9. Final Policy

> The system should not train on hooks as generic shapes. It should train on structurally valid hook-derived risk contracts.
