# H0008 — Flag Counting F2 After F1

## Hypothesis

After a valid F1, the market can produce a second continuation flag, F2. F2 is a count continuation, not a separate standalone setup.

The start of F2 is the internal `2` of the parent F1. This point is the place where price turns before touching or breaking the parent flag waist.

## Bullish model

```text
Parent F1 bullish internal 2
→ F2 Start
→ F2 Leg1 high
→ F2 Waist correction low
→ F2 Leg2 high breaking Leg1
```

Then one of two post-leg2 branches must form:

```text
A) Internal branch:
   1 = first low after F2 Leg2
   2 = later lower low, still above F2 Waist

B) Waist-break branch:
   1 = F2 Waist
   2 = new low node that breaks F2 Waist
```

Final confirmation requires price to move again in the bullish direction and rebreak the F2 Leg2 high.

## Bearish model

```text
Parent F1 bearish internal 2
→ F2 Start
→ F2 Leg1 low
→ F2 Waist correction high
→ F2 Leg2 low breaking Leg1
```

Then one of two post-leg2 branches must form:

```text
A) Internal branch:
   1 = first high after F2 Leg2
   2 = later higher high, still below F2 Waist

B) Waist-break branch:
   1 = F2 Waist
   2 = new high node that breaks F2 Waist
```

Final confirmation requires price to move again in the bearish direction and rebreak the F2 Leg2 low.

## Invalidation and pending state

A detected F2 body is pending until the branch and final rebreak are completed.

F2 is stricter than a pure visual pattern:

```text
- it must start from a parent F1 internal 2
- it must inherit the parent F1 direction
- it must form a valid F2 body
- it must produce either the internal branch or the waist-break branch
- it must rebreak F2 Leg2 to confirm
```

## Files

```text
mql5/Include/M0008/DAL_M0008F2Types.mqh
mql5/Include/M0008/DAL_M0008F2Detector.mqh
mql5/Include/M0008/DAL_M0008F2Renderer.mqh
mql5/Experts/M0008/M0008_FlagCountingF2.mq5
```
