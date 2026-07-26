# Flag Body Definition

## Canonical Body

A flag body is:

```text
Origin -> Leg1 -> Waist -> Leg2
```

This body is the same for F1, F2, and F3.

F-levels differ by lifecycle and post-body conditions, not by the two-leg geometry itself.

## Bullish Body

```text
Origin = Low node
Leg1   = highest High before correction
Waist  = lowest Low correction after Leg1 and before Leg2
Leg2   = High node that passes Leg1
```

Validity:

```text
Waist must not pass Origin.
Leg2 must pass Leg1 with strict high > Leg1.high.
```

Invalid body:

```text
If correction low < Origin low before Leg2,
that candidate body is invalid.
```

## Bearish Body

```text
Origin = High node
Leg1   = lowest Low before correction
Waist  = highest High correction after Leg1 and before Leg2
Leg2   = Low node that passes Leg1
```

Validity:

```text
Waist must not pass Origin.
Leg2 must pass Leg1 with strict low < Leg1.low.
```

Invalid body:

```text
If correction high > Origin high before Leg2,
that candidate body is invalid.
```

## Leg1 Extreme Rule

Leg1 is the extreme before correction, not the first node after Origin.

Bullish example:

```text
Origin low -> high A -> high B -> high C -> correction low
Leg1 = highest of A/B/C before correction
```

Bearish example:

```text
Origin high -> low A -> low B -> low C -> correction high
Leg1 = lowest of A/B/C before correction
```

## Waist Extreme Rule

Waist updates until Leg2 occurs.

Bullish:

```text
correction low A
correction low B lower than A
correction low C lower than B
then Leg2 break
Waist = low C
```

Bearish:

```text
correction high A
correction high B higher than A
correction high C higher than B
then Leg2 break
Waist = high C
```

## Leg2 Extension Before Post-Flag Counting

If a body has Leg2 but has not yet produced required post-flag internal numbering, a same-direction pass beyond Leg2 is body extension.

It is not a new flag.

Bullish:

```text
Leg2 high is extended to the newer higher high.
```

Bearish:

```text
Leg2 low is extended to the newer lower low.
```

This rule is especially critical for F1.

## Flag Size

```text
flag_size = abs(Leg2.price - Origin.price)
```

F2 uses this size to compare with F1.

F3 uses this size as one of two OR qualification paths versus F2.

## Body Identity

A body identity includes:

```text
direction
origin node identity
leg1 node identity
waist node identity
leg2 node identity
owning context id
F-level if assigned
```

A body with any different node/time/price/context is a distinct structure.

## Body Display Maturity

F1 is drawn only after complete body exists.

F2 and F3 may draw earlier seed/leg development for debugging, because they are children of an already confirmed parent context.

This is a display rule only. Logical body maturity still requires Leg2.
