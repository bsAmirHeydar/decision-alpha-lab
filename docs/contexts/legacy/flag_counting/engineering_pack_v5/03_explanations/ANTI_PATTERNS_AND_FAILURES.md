# Anti-Patterns and Failure Modes

This file lists mistakes that previously produced wrong charts.

## Failure 1: Sliding-Window F1

Wrong:

```text
Every L-H-L-H window becomes a bullish F1.
```

Why wrong:

- no phase boundary;
- no ownership;
- can start in middle of move;
- creates orphan lines;
- restarts F1 even while chain should search for F2/F3.

Correct:

```text
F1 starts only from phase boundary.
```

## Failure 2: First Correction Used as Waist

Wrong:

```text
Waist = first correction node after Leg1
```

Correct:

```text
Bullish Waist = lowest correction low before Leg2
Bearish Waist = highest correction high before Leg2
```

## Failure 3: Killing Parent When Child Dies

Wrong:

```text
F2 origin passed -> kill F1 chain
```

Correct:

```text
F2 candidate dies.
F1 context remains.
F2 search continues from post-F1 context.
```

## Failure 4: Abandoning F2 Search

Wrong:

```text
One F2 failed -> no more F2 for this F1
```

Correct:

```text
While F1 context remains alive, search for F2 continues.
```

## Failure 5: Rejecting F2/F3 Too Early

Wrong:

```text
F2 smaller than F1 at first body -> reject
F3 OR condition not passed at first body -> reject
```

Correct:

```text
Keep candidate alive and allow Leg2 extension until qualification passes or own invalidation occurs.
```

## Failure 6: Using Close Logic

Wrong:

```text
close beyond a level confirms/invalidate structure
```

Correct:

```text
Only high/low node pass matters.
Close is irrelevant.
```

## Failure 7: Equality as Break

Wrong:

```text
price equals boundary -> break
```

Correct:

```text
must pass boundary with strict inequality
```

## Failure 8: Renderer Invents Lines

Wrong:

```text
Renderer scans chart and draws helpful lines.
```

Correct:

```text
Renderer only draws engine-emitted objects.
```

## Failure 9: Broken Curve Approximation

Wrong:

```text
Many angular trendline segments pretending to be a curve.
```

Correct:

```text
Use smooth arc/polyline through true Waist.
Origin -> Leg1 straight.
Leg1 -> Waist -> Leg2 smooth arc.
```

## Failure 10: Untraceable Labels

Wrong:

```text
Labels only say F1/F2/F3 with no identity.
```

Correct research label:

```text
F1 L8 Q23
F2 L8 Q23
F3 L8 Q23
ND L8 H17
```

## Failure 11: Hiding All Live Roots

Wrong:

```text
Only confirmed F1/F2 shown.
```

Result: chart becomes empty and cannot debug stage logic.

Correct:

```text
Candidate/live structures shown with different color/shade.
Rejected hidden.
```

## Failure 12: Drawing Every ND Window

Wrong:

```text
Every 3/4-node local window gets ND label.
```

Correct:

```text
ND/Hook must be emitted by hook branch/context logic.
All emitted ND shown by default, but not every arbitrary sliding window.
```
