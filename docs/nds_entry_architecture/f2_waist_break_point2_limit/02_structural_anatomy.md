# 02 — Structural Anatomy

## Bullish case

```text
                         F2 Leg2 / flag end / TP
                         ●
                        / \
                       /   \
F2 Leg1              ●      \
                     \       \
                      ● F2 Waist = Point 1
                      ───────────── Buy Limit below Waist
                                     ↓ fill = Point 2

F1 Waist             ───────────── Stop strictly below
```

Operational mapping:

```text
Point 1 price = f2.waist.price
Point 2 price = limit price below f2.waist.price
Stop reference = f1.waist.price
Target = f2.leg2.price
```

## Bearish case

```text
F1 Waist             ───────────── Stop strictly above

                                     ↑ fill = Point 2
                      ───────────── Sell Limit above Waist
                      ● F2 Waist = Point 1
                     /       /
F2 Leg1              ●      /
                       \   /
                        \ /
                         ●
                         F2 Leg2 / flag end / TP
```

Operational mapping:

```text
Point 1 price = f2.waist.price
Point 2 price = limit price above f2.waist.price
Stop reference = f1.waist.price
Target = f2.leg2.price
```

## Canonical field mapping

| Semantic role | Phoenix field |
|---|---|
| Parent risk edge | `f1.waist` |
| F2 Point 1 | `f2.waist` |
| Executable Point 2 | pending limit beyond `f2.waist` |
| F2 flag end | `f2.leg2` |
| F2 body readiness | `f2.f2_body_complete` |
| Invalid F2 | `f2.status == FP_STATUS_INVALIDATED` |
| Target already consumed | F2 confirmed / Leg2 re-break |

## Why the order is staged at the waist

Point 2 is not a separate pre-known Phoenix node. It is the event created when price penetrates beyond Point 1. A pending limit one tick beyond the waist is the exact executable representation of that event without future knowledge.
