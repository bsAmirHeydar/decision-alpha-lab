# CH08 — Invalidation and Simultaneous Hunt Doctrine

## 1. Core Invalidation Rule

A divergence requires asymmetry.

If both symbols hunt their corresponding reference, the asymmetry disappears. When asymmetry disappears, the divergence is invalid.

This is not a weak signal. It is not a lower-quality signal. It is not a signal that needs a different label in the base layer.

It is invalid.

## 2. Simultaneous Hunt

If both symbols hunt the reference level in the same decision window, the event is not a divergence.

For example:

```text
SPXUSD hunts its previous-cycle high
NDXUSD hunts its previous-cycle high
```

Result:

```text
No bearish divergence
```

Because both markets participated in the same reference hunt.

For bullish divergence:

```text
SPXUSD hunts its previous-cycle low
NDXUSD hunts its previous-cycle low
```

Result:

```text
No bullish divergence
```

Again, no asymmetry remains.

## 3. Invalidation After Initial Hunt

The same logic applies if one symbol hunts first and the other hunts later before confirmation is accepted.

Sequence:

```text
Symbol A hunts reference
Symbol B has not hunted yet
Potential divergence exists
Symbol B then hunts its corresponding reference
Active candle closes
```

Result:

```text
Divergence invalid
```

The reason is simple:

> By the time the strategy is allowed to judge the event, both markets have already consumed the reference.

## 4. Invalidation After Confirmation

The earlier Chapter 03 doctrine says that if the clean symbol later hunts its corresponding reference, the divergence is invalidated.

Chapter 08 adds precision:

- before confirmation, the event does not yet have full trade permission;
- at confirmation, the event must still be asymmetric;
- after confirmation, if the clean symbol hunts, the original divergence thesis is no longer intact.

This produces a clean lifecycle:

```text
Potential divergence
↓
Confirmed divergence
↓
Trade permission
↓
Either movement validates the thesis
or clean-symbol hunt invalidates the thesis
```

## 5. No Partial Validity for Double Hunt

If both symbols hunt, there is no partial divergence in the base layer.

The model does not say:

- first hunter is more important,
- second hunter is late confirmation,
- double hunt is still a signal,
- double hunt is a weaker divergence,
- double hunt is a different trade family.

At the base layer:

```text
Double hunt = no divergence
```

Later statistics may choose to study double hunts as their own market condition, but not as a valid divergence in the base definition.

## 6. Same-Direction Clarification

The strategy architect clarified that if “same direction” means both symbols hunt the reference level at the same time, the divergence is invalid.

This means the invalidation rule is directional:

| Case | Result |
|---|---|
| Both hunt high references | Bearish divergence invalid. |
| Both hunt low references | Bullish divergence invalid. |
| One hunts high while the other does not | Bearish divergence candidate. |
| One hunts low while the other does not | Bullish divergence candidate. |

## 7. Strategic Meaning

Divergence is not about movement alone. It is about non-confirmation.

If both symbols confirm the hunt, the market relationship is no longer split. The liquidity event may still matter, but it no longer belongs to this strategy's divergence family.

## 8. Invalidation Law

> A divergence lives only while one market has hunted and the other has not. Once both markets hunt the corresponding reference, the divergence is cancelled.
