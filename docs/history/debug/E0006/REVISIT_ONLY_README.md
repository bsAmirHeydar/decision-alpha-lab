# E0006 — Revisit-Only Entry Logic

The revisit-only mode is designed for experiments where the first touch of a zone is not traded. The zone must first survive a non-hunted touch cycle, then become tradeable only on a later revisit, and only if both the first cycle and the revisit cycle satisfy the internal hunt standard.

## Inputs

```text
InpOnlyTradeRevisitZones = false
InpRevisitFirstCycleMustQualify = true
InpRevisitMinInternalHunts = 0
```

When `InpOnlyTradeRevisitZones=false`, E0006 behaves like the standard entry-qualification mode.

When `InpOnlyTradeRevisitZones=true`, first-touch entries are skipped and the origin must prove a prior non-hunted touch event.

`InpRevisitMinInternalHunts=0` means reuse the standard threshold:

```text
InpMinInternalHuntsForZone
```

## Required sequence

A revisit-only trade requires this lifecycle:

```text
1. origin node is confirmed
2. internal same-side hunts accumulate before first touch
3. M0001 records a first touch/revisit event
4. that first touch must be confirmed
5. that first touch must not hunt the origin node
6. the first cycle must satisfy the internal hunt threshold
7. after that touch closes, a new cycle begins
8. the new/revisit cycle must also satisfy the internal hunt threshold
9. only then is the zone eligible for a pending limit order
```

## LOW origin / BUY revisit

For a LOW origin:

```text
origin = LOW
first-cycle evidence = hunted internal LOW nodes before first touch
revisit-cycle evidence = hunted internal LOW nodes after first touch closes
order = BUY LIMIT on the origin zone
```

The logic is:

```text
if prior non-hunted M0001 touch exists
and first-cycle hunted internal LOW count >= N
and current-cycle hunted internal LOW count >= N
then allow BUY LIMIT
else skip
```

## HIGH origin / SELL revisit

For a HIGH origin:

```text
origin = HIGH
first-cycle evidence = hunted internal HIGH nodes before first touch
revisit-cycle evidence = hunted internal HIGH nodes after first touch closes
order = SELL LIMIT on the origin zone
```

The logic is:

```text
if prior non-hunted M0001 touch exists
and first-cycle hunted internal HIGH count >= N
and current-cycle hunted internal HIGH count >= N
then allow SELL LIMIT
else skip
```

## Why the first cycle must qualify

The first cycle is the proof that the zone was approached with the same structural pressure standard before the first touch.

If the first cycle did not hunt enough same-side internal nodes, then the later revisit is not considered a valid continuation of the same structural story.

This is controlled by:

```text
InpRevisitFirstCycleMustQualify = true
```

When true, both cycles must pass.

When false, only the current/revisit cycle must pass, but the origin must still have a prior non-hunted touch.

## What counts as a prior touch

The prior touch comes from M0001 events. E0006 searches for a first event for the origin node where:

```text
touch_confirmed = true
hunted = false
```

That keeps the revisit mode grounded in the same official event ledger used by the visual and research modules.

## Important implication

When revisit-only mode is enabled, a zone can pass the standard internal hunt filter and still not receive an order if it does not have a prior non-hunted M0001 touch.

That is intended.

The mode is not asking:

```text
Is this a good first touch?
```

It is asking:

```text
Has this zone already survived a qualified first cycle, and is the current revisit cycle also qualified?
```

## Recommended test setup

For strict retest-only execution:

```text
InpOnlyTradeRevisitZones = true
InpRevisitFirstCycleMustQualify = true
InpRevisitMinInternalHunts = 0
InpMinInternalHuntsForZone = 3
InpInternalHuntSameSideOnly = true
```

For quick debugging:

```text
InpOnlyTradeRevisitZones = true
InpRevisitMinInternalHunts = 1
InpMinInternalHuntsForZone = 1
InpPrintOrderLogs = true
```
