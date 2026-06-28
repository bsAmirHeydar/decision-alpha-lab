<!-- CURRENT CANON NOTICE
This file is retained as historical/context documentation. For current Phoenix implementation decisions, use:

docs/flag_counting/FLAG_COUNTING_CURRENT_CANON.md

If this file conflicts with the current canon, the current canon wins.
-->

# Flag Counting State Machine V4

This document converts the sequence contract into implementation states.

The state machine is sequence-based. It is not a sliding-window detector.

---

## 1. Main Chain State

A directional chain has the following high-level states:

```text
WAIT_PHASE_BOUNDARY
BUILD_F1_BODY
F1_POST_FLAG_COUNTING
F1_CONFIRMED_BUILD_F2
F2_BODY_OR_SEED
F2_POST_FLAG_COUNTING
F2_CONFIRMED_BUILD_F3
F3_BODY_OR_SEED
F3_COMPLETED_EXTENSION
F3_LOCKED_CHAIN_DONE
```

---

## 2. WAIT_PHASE_BOUNDARY

The engine waits for a legal F1 start context:

- terminal ND/Hook extreme;
- end/lock of opposite sequence;
- first confirmed opposite F1 that locks a previous F3.

No arbitrary mid-move F1 is allowed.

---

## 3. BUILD_F1_BODY

The engine builds a two-leg F1 candidate:

```text
Origin -> Leg1 -> Waist -> Leg2
```

F1 is drawn only after Leg2 exists.

Leg1 and Waist must update to their true extremes:

- bullish Leg1 = highest high before correction;
- bullish Waist = lowest low before Leg2;
- bearish Leg1 = lowest low before correction;
- bearish Waist = highest high before Leg2.

If correction passes Origin before Leg2, the body dies.

---

## 4. F1_POST_FLAG_COUNTING

After F1 Leg2 exists, the engine counts adverse-side internal nodes.

Bullish: numbered nodes are lows.

Bearish: numbered nodes are highs.

If price passes Leg2 before valid 1/2 exists, extend F1 Leg2.

If price passes F1 Waist before confirmation, invalidate F1.

If valid 1/2 or more exists and price later passes Leg2, confirm F1.

If correction creates 3/4 nodes, also emit ND/Hook.

---

## 5. F1_CONFIRMED_BUILD_F2

Once F1 confirms, F2 becomes authorized.

F2 origin is backfilled from the deepest adverse correction in the F1 post-flag context.

Bullish:

```text
F2 Origin = lowest low after F1 Leg2 in the owned post-F1 correction context.
```

Bearish:

```text
F2 Origin = highest high after F1 Leg2 in the owned post-F1 correction context.
```

The confirming break of F1 may also become part of F2 development.

---

## 6. F2_BODY_OR_SEED

F2 may be displayed from probable seed/Leg1 stage.

F2 must eventually form:

```text
Origin -> Leg1 -> Waist -> Leg2
```

F2 must satisfy:

```text
F2 flag_size >= F1 flag_size
```

If not yet satisfied, F2 remains candidate and may extend.

If F2 origin is passed, candidate F2 dies, but parent F1 context remains active and F2 search continues from the owned post-F1 correction context.

---

## 7. F2_POST_FLAG_COUNTING

After F2 body exists, F2 needs post-flag counting and a later break of Leg2 to confirm.

Unlike F1, F2 may break its own Waist without dying, provided its Origin remains unbroken.

Waist-break branch:

```text
1 = F2 Waist
2 = node that passes F2 Waist
```

F2 confirms when it has a valid 1/2 or waist-break branch and then passes F2 Leg2 again.

---

## 8. F2_CONFIRMED_BUILD_F3

Once F2 confirms, F3 becomes authorized.

F3 origin is backfilled from the deepest adverse correction after F2 Leg2.

Bullish:

```text
F3 Origin = lowest low after F2 Leg2 in the owned post-F2 correction context.
```

Bearish:

```text
F3 Origin = highest high after F2 Leg2 in the owned post-F2 correction context.
```

---

## 9. F3_BODY_OR_SEED

F3 forms a two-leg body.

It does not need post-flag 1/2.

F3 becomes completed when:

```text
F3 body exists
AND
(
  F3 Leg1 endpoint L >= 0.80 * F2 Leg1 endpoint L
  OR
  F3 flag_size >= 0.70 * F2 flag_size
)
```

If conditions do not yet pass, F3 remains candidate and continues extending.

---

## 10. F3_COMPLETED_EXTENSION

After F3 completes, all further movement in the same direction belongs to F3 extension.

The chain waits for the first confirmed opposite F1.

The first confirmed opposite F1 locks F3 and starts its own opposite-direction sequence.

---

## 11. F3_LOCKED_CHAIN_DONE

The chain is closed.

F3 remains visible and must not be deleted by later reversal.

---

## 12. Hook/ND State Machine

Hook/ND detection is branch-based.

For an owned context:

1. collect adverse-side nodes;
2. build possible hook branches, often easiest from newest node backward;
3. number each branch chronologically;
4. if any branch has more than four numbered nodes, increase L;
5. if a branch has three or four nodes and passes the 50% retracement rule, emit ND/Hook;
6. render ND/Hook as gray arc.

Two nodes are not ND.

---

## 13. Renderer Boundary

The state machine emits drawable events.

The renderer may draw only those events.

If the state machine does not emit a valid event, no visual object should be drawn.
