# 02 — Structural Anatomy

## 1. The complete F2 lifecycle is larger than its two-leg flag body

```text
F2 flag body
Origin → Leg1 → Waist → Leg2 / flag end

then

post-flag correction
→ internal 1
→ internal 2 at minimum

then

return in F2 direction
→ re-hit / strict pass of original flag end
→ F2 confirmation
```

The entry setup operates in the post-flag correction. It does not redefine the body or confirmation stages.

## 2. Bullish F2

```text
                                      original F2 flag end / Leg2
                                      fixed TP and RR reference
                                      ●──────────────────────────
                                     /                            ↑
                                    /                             │ later return
                         Leg1      ●                              │ confirms F2
                                   \                             /
                                    \                           /
F2 flag Origin                      ● F2 flag Waist             /
●───────────────────────────────────┘ = projected Point 1      /
                                      \                        /
                                       \ post-flag correction /
                                        ● executable Point 2
                                          Buy Limit fill
                                          strictly below Waist

Parent F1 Waist  ───────────────────────────────────────────────
Stop is placed strictly below this level
```

Operational mapping:

```text
Point 1 projection = f2.waist
Point 2 execution  = strict Buy-Limit fill below f2.waist
Stop authority     = direct parent f1.waist
Fixed target/RR    = original f2.leg2
```

## 3. Bearish F2

```text
Stop is placed strictly above this level
Parent F1 Waist  ───────────────────────────────────────────────

                                          Sell Limit fill
                                        ● executable Point 2
                                       /  strictly above Waist
                                      / post-flag correction
F2 flag Origin                      ● F2 flag Waist             \
●───────────────────────────────────┘ = projected Point 1      \
                                    /                           \
                         Leg1      ●                             │ later return
                                     \                           │ confirms F2
                                      ●──────────────────────────
                                      original F2 flag end / Leg2
                                      fixed TP and RR reference
```

Operational mapping:

```text
Point 1 projection = f2.waist
Point 2 execution  = strict Sell-Limit fill above f2.waist
Stop authority     = direct parent f1.waist
Fixed target/RR    = original f2.leg2
```

## 4. Canonical field mapping

| Meaning | Existing Phoenix field / execution field |
|---|---|
| Two-leg F2 body | `f2.origin`, `f2.leg1`, `f2.waist`, `f2.leg2` |
| Post-flag count | `f2.internal_pack` |
| F2 lifecycle stage | `f2.status`, `f2.f2_lifecycle_status` |
| F2 confirmation | `f2.confirm`, only after valid post-flag structure and favorable re-break |
| Preferred branch Point 1 | execution projection of `f2.waist` |
| Executable Point 2 | pending limit strictly beyond `f2.waist` |
| Parent risk edge | direct parent `f1.waist` |
| Fixed target / RR reference | original `f2.leg2` |

## 5. Why Point 2 is projected, not awaited

A confirmed adverse node is only known after right-side clearance. Waiting for the canonical node to become confirmed would place the order after the intended entry event.

Therefore:

```text
Phoenix detects the body and lifecycle
Execution adapter stages the level in advance
The fill captures the future Waist-break Point 2
Phoenix later continues its normal F2 lifecycle
```

No core structural definition is changed.
