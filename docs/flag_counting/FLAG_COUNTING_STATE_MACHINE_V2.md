<!-- CURRENT CANON NOTICE
This file is retained as historical/context documentation. For current Phoenix implementation decisions, use:

docs/flag_counting/FLAG_COUNTING_CURRENT_CANON.md

If this file conflicts with the current canon, the current canon wins.
-->

# Flag Counting State Machine V2

This document defines a state-machine interpretation of the Flag Counting Sequence Contract V2.

The purpose is to prevent the detector from behaving like a sliding-window pattern scanner.

---

## 1. Top-level sequence states

```text
NO_SEQUENCE
WAIT_F1
F1_CANDIDATE
F1_CONFIRMED_WAIT_F2
F2_CANDIDATE
F2_CONFIRMED_WAIT_F3
F3_CANDIDATE
F3_LOCKED
```

---

## 2. Shared event types

```text
NODE_HIGH
NODE_LOW
ND_FOUND
OPPOSITE_SEQUENCE_END
BODY_STARTED
LEG1_UPDATED
WAIST_UPDATED
LEG2_CREATED
LEG2_EXTENDED
INTERNAL_1_FOUND
INTERNAL_2_FOUND
ENDPOINT_REBROKEN
WAIST_HIT
ORIGIN_HIT
F_CONFIRMED
F_REJECTED
F3_BODY_COMPLETE
OPPOSITE_F1_FOUND
```

---

## 3. WAIT_F1

### Entry conditions

```text
NO_SEQUENCE
or after ND
or after opposite sequence end
```

### Valid transitions

```text
ND_FOUND or OPPOSITE_SEQUENCE_END -> attempt F1 origin selection
valid F1 origin + Leg1 + Waist + Leg2 -> F1_CANDIDATE
```

### Invalid transitions

Do not create F1 from arbitrary four-node middle windows.

---

## 4. F1_CANDIDATE

### Internal substates

```text
BUILDING_BODY
EXTENDING_LEG2
WAIT_INTERNAL_12
WAIT_ENDPOINT_REBREAK
```

### Rules

```text
F1 invalidation = waist
F1 requires internal 1/2 before confirmation
F1 endpoint rebreak after internal 1/2 confirms F1
```

### Transitions

```text
WAIST_HIT -> F1_REJECTED -> WAIT_F1 with larger-scale context
LEG2_EXTENDED before internal 1/2 -> remain F1_CANDIDATE, update Leg2
INTERNAL_1_FOUND -> wait for INTERNAL_2_FOUND
INTERNAL_2_FOUND -> WAIT_ENDPOINT_REBREAK
ENDPOINT_REBROKEN -> F1_CONFIRMED_WAIT_F2
```

### Important F1-specific rule

The intervening node between internal 1 and internal 2 must not exceed the F1 flag endpoint.

For bullish F1:

```text
intervening high <= F1 Leg2 endpoint
```

For bearish F1:

```text
intervening low >= F1 Leg2 endpoint
```

---

## 5. F1_CONFIRMED_WAIT_F2

### Entry conditions

```text
F1 confirmed
```

### Rules

```text
F2 must be searched from the F1 post-flag correction endpoint.
F2 must not be created before F1 confirmation.
F1 remains the parent while searching for F2.
```

### Transitions

```text
valid F2 body starts -> F2_CANDIDATE
F1 parent invalidated by its own rule -> sequence rejected/closed
```

---

## 6. F2_CANDIDATE

### Internal substates

```text
BUILDING_BODY
EXTENDING_LEG2
WAIT_INTERNAL_12
WAIST_BREAK_BRANCH
WAIT_ENDPOINT_REBREAK
```

### Rules

```text
F2 invalidation = origin / beginning of Leg1
F2 may break its waist without invalidating
F2 must satisfy size >= F1 size by default
```

### Transitions

```text
ORIGIN_HIT -> F2_REJECTED -> F1_CONFIRMED_WAIT_F2
WAIST_HIT but ORIGIN not hit -> WAIST_BREAK_BRANCH
INTERNAL_1_FOUND -> wait for INTERNAL_2_FOUND
INTERNAL_2_FOUND -> WAIT_ENDPOINT_REBREAK
ENDPOINT_REBROKEN -> F2_CONFIRMED_WAIT_F3
```

### Parent continuity

If F2 rejects:

```text
remove F2 from main chart
keep F1 parent alive
continue F2 search from F1 context
```

---

## 7. F2_CONFIRMED_WAIT_F3

### Entry conditions

```text
F2 confirmed or accepted as valid F2 context
```

### Rules

```text
Search for F3.
F3 only needs the two-leg flag body.
```

### Transitions

```text
valid F3 body starts -> F3_CANDIDATE
F2 origin invalidated before F3 -> return to F1_CONFIRMED_WAIT_F2 if F1 alive
```

---

## 8. F3_CANDIDATE

### Rules

```text
F3 requires only the flag body.
F3 does not require post-body internal 1/2.
F3 must be in the same scale context as F1/F2, pending exact same-scale definition.
```

### Transitions

```text
F3_BODY_COMPLETE -> F3_LOCKED
```

---

## 9. F3_LOCKED

### Rules

```text
sequence is complete
sequence remains on chart
later reversal does not delete it
same-direction continuation is F3 extension
no F4 is created
```

### Exit condition

```text
smallest opposite F1 appears
```

The exact definition of smallest opposite F1 remains open.

---

## 10. Rejection visibility policy

Rejected states must be logged but not drawn on the main chart.

```text
candidate rejected -> remove chart objects
confirmed historical object remains only if it was already locked/terminal
F3 locked remains even after reversal
```

---

## 11. Detector pseudocode

```text
for each scale_context:
    preserve raw high/low nodes
    build compressed views as needed
    update ND detector

    for each active sequence:
        if state == WAIT_F1:
            try_start_f1_after_nd_or_opposite_end()

        if state == F1_CANDIDATE:
            update_f1_body()
            if f1_waist_hit(): reject_f1()
            else if no_internal_12_and_endpoint_extends(): extend_f1_leg2()
            else if internal_12_complete() and endpoint_rebroken(): confirm_f1()

        if state == F1_CONFIRMED_WAIT_F2:
            try_start_f2_from_f1_post_correction_endpoint()

        if state == F2_CANDIDATE:
            update_f2_body()
            if f2_origin_hit(): reject_f2_keep_f1()
            else if f2_waist_hit_not_origin(): create_waist_break_branch()
            else if internal_12_complete() and endpoint_rebroken(): confirm_f2()

        if state == F2_CONFIRMED_WAIT_F3:
            try_start_f3()

        if state == F3_CANDIDATE:
            if f3_body_complete(): lock_sequence()

        if state == F3_LOCKED:
            extend_f3_until_smallest_opposite_f1()
```
