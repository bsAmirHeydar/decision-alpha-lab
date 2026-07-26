# Invariants and Assumptions

This file lists rules that must remain true in all implementations.

## Structural Input Invariants

1. Only candle highs and lows feed structural logic.
2. Node extraction is delegated to the existing project node module.
3. Open, close, body, candle color, and candle direction do not participate in F or ND decisions.
4. A node does not expire.
5. Equality is not a break.
6. A boundary must be passed with strict inequality.

## Flag Geometry Invariants

1. A flag is always two legs:

```text
Origin -> Leg1 -> Waist -> Leg2
```

2. A body without Leg2 is not a complete flag body.
3. Leg1 is the true extreme before correction, not the first small node.
4. Waist is the true adverse correction extreme before Leg2.
5. Waist must update while correction deepens/higher-corrects.
6. In bullish body, correction must not pass origin.
7. In bearish body, correction must not pass origin.

## Sequence Invariants

1. In a chain, order is F1 -> F2 -> F3.
2. After F1 confirms, search for F2 in the same chain.
3. After F2 confirms, search for F3 in the same chain.
4. Do not start arbitrary same-direction F1 inside an active same-direction chain.
5. New F1 requires a phase boundary.
6. A child candidate death does not kill the parent chain.
7. F2 search continues while its parent F1 context remains alive.
8. F3 search continues while its parent F2 context remains alive.

## F1 Invariants

1. F1 display starts only after the F1 two-leg body exists.
2. F1 must produce minimum internal 1/2 after Leg2 before confirmation.
3. F1 confirms only after Leg2 is passed again after valid internal numbering.
4. Before confirmation, F1 invalidates if Waist is passed.
5. If Leg2 is passed before valid internal 1/2 exists, Leg2 extends; a new F is not created.

## F2 Invariants

1. F2 is authorized only after F1 confirmation.
2. F2 origin is backfilled from the deepest adverse correction after F1 body.
3. F2 is compared to F1 by flag size only.
4. If F2 size is not yet enough, it remains candidate and may extend.
5. F2 invalidates only if its origin/start of Leg1 is passed.
6. F2 may break its Waist without dying, provided origin is not passed.
7. F2 confirms when it has internal 1/2 or waist-break branch and later passes Leg2 again.

## F3 Invariants

1. F3 is authorized only after F2 confirmation.
2. F3 origin is backfilled from the deepest adverse correction after F2 body.
3. F3 needs two-leg body and OR qualification.
4. F3 is not rejected merely because qualification is not yet passed; it continues as candidate.
5. Completed F3 extends with same-direction movement.
6. F3 locks at the first confirmed opposite F1 by time of detection/confirmation.
7. Locked F3 is persistent and must not be deleted.

## Hook / ND Invariants

1. Hook branches are adverse-side numbered node sequences.
2. Two numbered nodes are internal numbering only, not ND.
3. Three or four numbered nodes can be ND/Hook.
4. More than four numbered nodes must trigger L increase until branch length is <= 4.
5. ND 50% condition is retracement from extreme toward start, not close-based.
6. ND/Hook may overlap with F if both are emitted.
7. ND/Hook drawing is gray arc/semicircle, not a 50% line.

## Rendering Invariants

1. Renderer must not invent structures.
2. Renderer only draws engine-emitted objects.
3. All lines are thin by default.
4. Sequence differentiation uses shade and labels, not large line width.
5. Detailed labels are default for research: `F1 L8 Q23` style.
6. Origin marker `O` is visible by default for debugging.
7. Invalidated/rejected objects are hidden from main chart by default.
