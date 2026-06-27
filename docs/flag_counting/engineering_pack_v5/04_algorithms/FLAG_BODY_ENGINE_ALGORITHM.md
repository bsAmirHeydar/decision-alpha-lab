# Flag Body Engine Algorithm

## Purpose

Build two-leg body candidates from owned context.

Do not assign F-level confirmation here. This module only builds body geometry.

## Inputs

```text
direction
origin node
node stream for selected L/context
start index/time
mode: F1 body | F2 body | F3 body
parent context id
```

## Bullish Body Builder

Initialize:

```text
origin = low node
leg1 = none
waist = none
leg2 = none
phase = SEEK_LEG1
```

Process nodes chronologically.

### SEEK_LEG1

Track highest high after origin.

When a low correction appears after at least one high:

```text
leg1 = highest high seen before correction
waist = correction low
phase = SEEK_LEG2
```

If low correction passes origin:

```text
candidate invalid
```

### SEEK_LEG2

Update waist while deeper lows appear:

```text
if low < waist.low and low >= origin.low:
  waist = low
```

If low passes origin:

```text
candidate invalid
```

If high passes leg1:

```text
leg2 = high
body complete
```

## Bearish Body Builder

Symmetric.

### SEEK_LEG1

Track lowest low after origin.

When a high correction appears after at least one low:

```text
leg1 = lowest low seen before correction
waist = correction high
phase = SEEK_LEG2
```

If high correction passes origin:

```text
candidate invalid
```

### SEEK_LEG2

Update waist while higher highs appear:

```text
if high > waist.high and high <= origin.high:
  waist = high
```

If high passes origin:

```text
candidate invalid
```

If low passes leg1:

```text
leg2 = low
body complete
```

## Leg2 Extension

For F1 before valid post-body 1/2 exists:

Bullish:

```text
if later high > current_leg2.high:
  leg2 = later high
  post-flag context restarts after new Leg2
```

Bearish:

```text
if later low < current_leg2.low:
  leg2 = later low
  post-flag context restarts after new Leg2
```

For F2/F3 candidates that need size/qualification:

```text
same-direction extension may update Leg2 until qualification passes or origin invalidates
```

## Output

A completed body candidate emits:

```text
body_id
direction
origin
leg1
waist
leg2
flag_size
parent context id
```

## Main Failure Guard

Never create body from arbitrary 4-node window unless the origin came from an owned phase context.
