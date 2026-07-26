<!-- CURRENT CANON NOTICE
This file is retained as historical/context documentation. For current Phoenix implementation decisions, use:

docs/contexts/legacy/flag_counting/FLAG_COUNTING_CURRENT_CANON.md

If this file conflicts with the current canon, the current canon wins.
-->

# Flag Counting State Machine V3

This document converts the sequence contract into a deterministic state machine. It is intended for implementation in MQL5 or any other detector backend.

---

## 1. Global State Principles

The state machine must operate on high/low nodes only.

Every sequence has:

```text
sequence_id
direction
scale_context
current_stage
parent_opposite_context
f1_event
f2_event
f3_event
active_candidate
locked_history
```

A sequence never restarts at F1 after F1 has confirmed. The sequence advances in order.

```text
F1 -> F2 -> F3 -> locked/done
```

---

## 2. Event Statuses

Use explicit statuses instead of implicit boolean flags.

```text
RAW_SEED
LIVE_BODY
POST_FLAG_CORRECTION
CONFIRMED
COMPLETED
EXTENDING
LOCKED
INVALIDATED
REJECTED
```

Display policy:

```text
RAW_SEED      -> hidden
LIVE_BODY     -> visible candidate
POST_FLAG_CORRECTION -> visible candidate with internal labels
CONFIRMED     -> visible confirmed
COMPLETED     -> visible completed
EXTENDING     -> visible extension
LOCKED        -> visible historical locked
INVALIDATED   -> hidden main chart, audit only
REJECTED      -> hidden main chart, audit only
```

---

## 3. Sequence States

### 3.1 WAITING_FOR_F1

Allowed entry points:

1. after ND/Hook,
2. after an opposite sequence endpoint,
3. after an F3 lock triggered by the first smallest confirmed opposite F1.

Transition:

```text
If a coherent two-leg F1 candidate body is hit:
    state = F1_BODY_LIVE
```

Do not transition on raw four-node windows without sequence origin.

### 3.2 F1_BODY_LIVE

The engine builds:

```text
Origin -> Leg1 -> Waist -> Leg2
```

Bullish body rules:

```text
Origin = LOW
Leg1 = highest HIGH before correction
Waist = deepest LOW correction after Leg1
Leg2 = HIGH breaking Leg1
```

Bearish body rules:

```text
Origin = HIGH
Leg1 = lowest LOW before correction
Waist = highest HIGH correction after Leg1
Leg2 = LOW breaking Leg1
```

Transition:

```text
If Leg1 correction breaks Origin:
    invalidate candidate
    state = WAITING_FOR_F1 with larger-scale context if needed

If Leg2 is hit:
    state = F1_POST_FLAG_CORRECTION
```

### 3.3 F1_POST_FLAG_CORRECTION

The engine watches post-Leg2 correction.

Rules:

```text
If post-flag correction hits F1 Waist before internal 1/2 or more:
    F1 invalidates

If no valid internal 1/2 exists and price extends beyond Leg2:
    update Leg2 endpoint
    remain in F1_POST_FLAG_CORRECTION

If internal 1/2 or more appears before Waist is hit:
    wait for rebreak of F1 Leg2

If after internal 1/2 or more price rebreaks F1 Leg2:
    F1 confirms
    state = SEEKING_F2
```

F1-specific internal restriction:

- Bullish F1: the middle high between internal 1 and 2 must not exceed F1 Leg2.
- Bearish F1: the middle low between internal 1 and 2 must not go below F1 Leg2.

### 3.4 SEEKING_F2

F2 is only sought after F1 has confirmed.

F2 origin is derived from the F1 post-flag correction context:

```text
Bullish: deepest LOW of the terminal post-F1 correction context
Bearish: highest HIGH of the terminal post-F1 correction context
```

Transition:

```text
If a coherent F2 body is hit from that origin/context:
    state = F2_BODY_LIVE
```

If an attempted F2 dies, return to `SEEKING_F2` using the same parent F1 context. Do not abandon the F2 search while F1 is valid.

### 3.5 F2_BODY_LIVE

The engine builds F2 as a two-leg flag body.

Size check:

```text
F2.flag_size >= F1.flag_size
```

Transition:

```text
If body correction breaks F2 Origin before Leg2:
    reject candidate
    state = SEEKING_F2

If Leg2 is hit:
    state = F2_POST_FLAG_CORRECTION
```

### 3.6 F2_POST_FLAG_CORRECTION

F2 differs from F1 after the flag body.

Rules:

```text
If post-flag correction breaks F2 Origin:
    F2 invalidates
    state = SEEKING_F2 under same F1 parent context

If post-flag correction breaks F2 Waist but not F2 Origin:
    create waist-break branch
    1 = F2 Waist
    2 = node that breaks F2 Waist
    wait for F2 Leg2 rebreak

If internal 1/2 or more appears:
    wait for F2 Leg2 rebreak

If after internal/branch structure price rebreaks F2 Leg2:
    F2 confirms
    state = SEEKING_F3
```

F2-specific internal allowance:

- Bullish F2: the middle high between internal 1 and 2 may exceed F2 Leg2.
- Bearish F2: the middle low between internal 1 and 2 may go beyond F2 Leg2.

### 3.7 SEEKING_F3

F3 is only sought after F2 has confirmed.

F3 origin comes from the correction after the F2 flag context.

Transition:

```text
If coherent F3 body is hit and same-scale compatibility passes:
    state = F3_COMPLETED_EXTENDING
```

### 3.8 F3_BODY_LIVE

F3 is built as a two-leg body.

Unlike F1/F2, F3 does not need post-flag internal 1/2 to complete.

Same-scale compatibility is OR-based:

```text
Pass if:
    F3_leg1_L >= ceil(0.80 * F2_leg1_L)
OR:
    F3_flag_size >= 0.70 * F2_flag_size
```

If neither condition passes, the candidate is not accepted as the sequence F3.

### 3.9 F3_COMPLETED_EXTENDING

Once F3 completes:

```text
No F4 is created.
Same-direction movement is treated as F3 extension.
```

Transition:

```text
If first smallest confirmed opposite F1 appears:
    lock F3 at reached extension endpoint
    state = F3_LOCKED
```

Do not lock F3 on raw seeds or live unconfirmed opposite candidates.

### 3.10 F3_LOCKED

A locked F3 is historical completed structure.

Rules:

```text
Never delete locked F3 from chart because of later reversal.
Mark sequence as done.
Allow new sequence logic from opposite confirmed context.
```

---

## 4. ND/Hook State Integration

ND/Hook is not a flag state but can trigger F1 context.

ND can be detected anywhere, including inside larger F structures.

ND detection algorithm:

```text
For each base start node at L=2:
    collect following high/low nodes
    compress downstream view by increasing L until count <= 4

    if count == 3 or count == 4:
        compute retracement_ratio
        if retracement_ratio >= threshold or below-half mode enabled:
            emit ND label/event
    else:
        no ND
```

ND retracement formula:

```text
cycle_range = abs(extreme_price - start_price)
retraced_distance = abs(extreme_price - last_price)
retracement_ratio = retraced_distance / cycle_range
```

Default threshold:

```text
retracement_ratio >= 0.50
```

---

## 5. High-Level Pseudocode

```text
for each symbol/timeframe update:
    raw_nodes = RawNodeStore.update_from_high_low_only()

    for each scale_context:
        scaled_view = ScaledNodeView.build(raw_nodes, scale_context)
        nd_events = NDDetector.scan_all(scale_context)

        for each active_sequence:
            switch active_sequence.state:

                WAITING_FOR_F1:
                    if phase_boundary_allows_f1_start():
                        candidate = FlagBodyBuilder.try_build_f1_body()
                        if candidate.body_hit:
                            show candidate
                            state = F1_BODY_LIVE

                F1_BODY_LIVE:
                    update_leg1_waist_leg2(candidate)
                    if origin_broken_before_leg2:
                        invalidate candidate
                    if leg2_hit:
                        state = F1_POST_FLAG_CORRECTION

                F1_POST_FLAG_CORRECTION:
                    analyze_post_flag_correction()
                    if waist_hit_before_valid_internal:
                        invalidate F1
                    elif no_internal_and_leg2_extended:
                        update_leg2_extension()
                    elif internal_exists_and_leg2_rebroken:
                        confirm F1
                        state = SEEKING_F2

                SEEKING_F2:
                    f2_origin = terminal_deepest_post_f1_correction_node()
                    candidate = FlagBodyBuilder.try_build_f2_body(f2_origin)
                    if candidate.body_hit:
                        state = F2_BODY_LIVE

                F2_BODY_LIVE:
                    update_f2_body()
                    if origin_broken:
                        reject F2
                        state = SEEKING_F2
                    if leg2_hit:
                        state = F2_POST_FLAG_CORRECTION

                F2_POST_FLAG_CORRECTION:
                    analyze_post_flag_correction()
                    if origin_broken:
                        invalidate F2
                        state = SEEKING_F2
                    elif waist_broken_not_origin:
                        create_waist_break_branch()
                    elif internal_or_branch_exists_and_leg2_rebroken:
                        confirm F2
                        state = SEEKING_F3

                SEEKING_F3:
                    f3_origin = correction_after_f2_flag()
                    candidate = FlagBodyBuilder.try_build_f3_body(f3_origin)
                    if candidate.body_hit and f3_same_scale_passes():
                        complete F3
                        state = F3_COMPLETED_EXTENDING

                F3_COMPLETED_EXTENDING:
                    update_f3_extension()
                    if smallest_confirmed_opposite_f1_appears:
                        lock F3
                        state = F3_LOCKED
```

---

## 6. Key Guardrails

### 6.1 Do not draw every four-node window

Alternating four-node geometry is not enough.

The detector must require:

```text
sequence context
valid origin
true Leg1
true Waist
true Leg2
level-specific post-flag rules
```

### 6.2 Do not kill parent because child dies

If F2 dies by hitting its own Origin, F1 remains alive unless F1 invalidates by its own rule.

If a future F3 candidate dies, F2 remains alive unless F2 invalidates by its own rule.

### 6.3 Do not lose F2 search

When an F2 attempt dies, the engine still seeks F2 from the F1 post-flag correction context.

### 6.4 Do not delete locked F3

Locked F3 is historical. Later reversal does not erase it.
