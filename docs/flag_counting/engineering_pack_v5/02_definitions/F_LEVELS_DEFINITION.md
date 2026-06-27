# F-Level Definitions

## Shared Body

F1, F2, and F3 all use the same body geometry:

```text
Origin -> Leg1 -> Waist -> Leg2
```

Their differences are sequence role and post-body requirements.

## F1 Definition

F1 is the first flag in a sequence.

### F1 Start

F1 must start from a valid phase boundary:

- terminal extreme of ND/Hook;
- end of opposite sequence;
- confirmed opposite F1 that locks previous F3 and starts a new opposite sequence;
- another explicitly owned phase boundary.

F1 must not start from the middle of an active movement just because a local alternating window exists.

### F1 Display

F1 appears on chart after the probable two-leg body has been hit/completed.

Before Leg2, it is only a seed and should not appear as F1 body on main chart.

### F1 Confirmation

F1 confirms when:

```text
1. F1 body exists.
2. Post-F1 internal 1/2 or more exists.
3. Before minimum 1/2, no opposite middle node passed F1 Leg2.
4. F1 Waist was not passed before confirmation.
5. Later price passes F1 Leg2 again.
```

Bullish F1 confirms with:

```text
later high > F1 Leg2 high
```

Bearish F1 confirms with:

```text
later low < F1 Leg2 low
```

### F1 Invalidation

Before confirmation:

```text
F1 invalidates if its Waist is passed.
```

Bullish:

```text
later low < F1 Waist low
```

Bearish:

```text
later high > F1 Waist high
```

## F2 Definition

F2 is the second flag in a sequence.

### F2 Authorization

F2 is authorized only after F1 confirms.

However, F2 origin is backfilled from the F1 post-flag correction context.

### F2 Origin

Bullish:

```text
F2 Origin = lowest low after F1 Leg2 in the owned post-F1 correction context.
```

Bearish:

```text
F2 Origin = highest high after F1 Leg2 in the owned post-F1 correction context.
```

This is the deepest/farthest correction, not arbitrary terminal node.

### F2 Size

```text
F2_flag_size >= F1_flag_size
```

F2 is compared to F1 by flag size only. No default L same-scale requirement is imposed on F2.

If the current candidate F2 is too small, it remains candidate and continues. It is not rejected for being too small.

### F2 Invalidation

F2 invalidates only if its Origin/start of Leg1 is passed.

Bullish:

```text
later low < F2 Origin low
```

Bearish:

```text
later high > F2 Origin high
```

If F2 dies, it means that candidate was not F2. The parent F1 context remains alive. The engine continues searching for F2 from the same owned post-F1 correction context.

### F2 Waist-Break Branch

F2 may pass its own Waist without invalidating, provided its Origin is not passed.

In that branch:

```text
1 = F2 Waist
2 = node that passes F2 Waist
```

F2 then still needs to pass Leg2 again to confirm.

### F2 Confirmation

F2 confirms when:

```text
1. F2 body exists.
2. F2 size requirement is satisfied.
3. Post-F2 internal 1/2 or waist-break branch exists.
4. F2 Origin has not been passed.
5. Later price passes F2 Leg2 again.
```

## F3 Definition

F3 is the terminal flag in a sequence.

### F3 Authorization

F3 is authorized only after F2 confirms.

Its origin is backfilled from the post-F2 correction context.

### F3 Origin

Bullish:

```text
F3 Origin = lowest low after F2 Leg2 in the owned post-F2 correction context.
```

Bearish:

```text
F3 Origin = highest high after F2 Leg2 in the owned post-F2 correction context.
```

### F3 Completion

F3 does not require post-flag internal 1/2.

It becomes completed when:

```text
1. F3 two-leg body exists.
2. At least one F3 qualification OR condition passes.
```

### F3 Qualification OR Conditions

Condition A:

```text
F3 Leg1 endpoint node L >= 0.80 * F2 Leg1 endpoint node L
```

Condition B:

```text
F3 flag_size >= 0.70 * F2 flag_size
```

This is OR, not AND.

If neither condition is currently satisfied, F3 remains candidate and continues. It is not rejected.

### F3 Extension

After completion, same-direction movement belongs to F3 extension.

### F3 Lock

F3 locks when the first confirmed opposite F1 is detected.

This is the first by confirmation/detection time. It is not the smallest body and not necessarily the smallest L.

Once locked, F3 remains visible unless explicitly hidden by input.

The opposite F1 that locked F3 becomes the start of its own independent opposite sequence.
