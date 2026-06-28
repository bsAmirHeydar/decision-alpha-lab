# F1 / F2 / F3 Algorithms

## F1 Algorithm

### Create F1

```text
Input: phase boundary, direction, node view
Origin = boundary extreme
Build body using FlagBodyBuilder
```

### Show F1

```text
if body complete:
  emit F1 LIVE_BODY render/audit object
else:
  hide seed from main chart
```

### Track Post-F1 Context

After Leg2:

```text
track adverse nodes
track opposite nodes between adverse nodes
build hook branches
store deepest adverse correction
```

Bullish deepest adverse:

```text
lowest low after F1 Leg2
```

Bearish deepest adverse:

```text
highest high after F1 Leg2
```

### F1 Extension

If no valid internal 1/2 exists and price passes Leg2 again:

```text
extend F1 Leg2
reset/rebase post-F1 context after new Leg2
```

### F1 Invalidation

Before confirmation:

```text
if bullish and low < F1.Waist: invalidate
if bearish and high > F1.Waist: invalidate
```

### F1 Confirmation

```text
if valid internal 1/2 or more exists
and F1 Waist not passed
and price passes F1 Leg2 again:
  confirm F1
  authorize F2
```

## F2 Algorithm

### Authorize F2

Only after F1 confirmed.

```text
F2 origin = deepest adverse correction in post-F1 context
```

### Build F2

Use FlagBodyBuilder from F2 origin.

F2 seed may be shown.

### F2 Qualification

```text
if F2.flag_size < F1.flag_size:
  keep candidate
  allow Leg2 extension
else:
  size qualified
```

### F2 Invalidation

```text
if bullish and low < F2.Origin: F2 candidate dies
if bearish and high > F2.Origin: F2 candidate dies
```

Then:

```text
keep F1 context
recompute deepest post-F1 correction as needed
build new F2 candidate from same owned context
```

### F2 Waist-Break Branch

If after F2 body the correction passes F2 Waist but not F2 Origin:

```text
1 = F2 Waist
2 = node that passes F2 Waist
```

Continue branch logic into 3/4 if present.

### F2 Confirmation

```text
if F2 size qualified
and internal 1/2 or waist-break branch exists
and F2 Origin not passed
and price passes F2 Leg2 again:
  confirm F2
  authorize F3
```

## F3 Algorithm

### Authorize F3

Only after F2 confirmed.

```text
F3 origin = deepest adverse correction between final F2 Leg2 and F2 confirmation
F3 Leg1   = F2 confirmation node
```

### Build F3

Backfill Origin into the F2 correction window, force Leg1 to the F2 confirmation node, then use normal FlagBodyBuilder rules for Waist and Leg2 after F2 confirmation.

F3 seed/leg development may be shown, but incomplete bodies cannot be terminal.

### F3 Qualification

```text
condA = F3.leg1.L >= 0.80 * F2.leg1.L
condB = F3.flag_size >= 0.70 * F2.flag_size
```

If `condA OR condB`:

```text
complete F3
```

Else:

```text
keep candidate
allow extension
```

### F3 Extension

After completion:

```text
same-direction movement extends F3
```

### F3 Lock

```text
if first confirmed opposite F1 appears:
  lock F3
  close old chain
  opposite F1 starts new chain
```

## Confirmation and Completion Summary

```text
F1 confirms = internal 1/2+ then Leg2 re-pass, Waist safe.
F2 confirms = size qualified, internal/waist-break, then Leg2 re-pass, Origin safe.
F3 completes = body + OR qualification.
F3 locks = first confirmed opposite F1.
```
