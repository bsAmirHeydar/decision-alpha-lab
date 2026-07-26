# 16 — Higher-Timeframe F1-to-F2 Confirmation Window

## 1. Requested interval

The optional window permits lower-timeframe entries only inside this half-open structural interval:

```text
[ exact HTF F1 confirmation, exact direct-child HTF F2 confirmation )
```

In words:

```text
Before HTF F1 confirmation
→ no entry

After HTF F1 confirmation and before its exact child F2 confirmation
→ that count may authorize its own direction

At or after the direct child HTF F2 confirmation
→ that count no longer authorizes a new entry
```

Default:

```text
InpF2BTUseHigherTimeframeF1ToF2ConfirmationWindow = true
```

## 2. Per-count evaluation

The window is evaluated for every visible canonical higher-timeframe F1 root, not only for one global winner.

Each candidate count must preserve:

```text
same canonical higher-timeframe count
same sequence_id
same direction
same scale L
F1 chain_index = 1
F2 chain_index = 2
F2.parent_sequence_id = F1.sequence_id
F2.parent_event_id = F1.event_id
```

A different sequence, a different scale, or a merely same-direction F2 cannot close the window.

## 3. Exact stabilization predicates

### F1 opens the window

F1 is stabilized when:

```text
level = F1
chain_index = 1
status = CONFIRMED
lifecycle_status = FP_F1_LC_CONFIRMED
has_confirm = true
```

`lifecycle_can_spawn_f2` is not part of the definition. Spawn eligibility is a separate downstream authority and must not delay the requested “F1 stabilized” boundary.

### F2 closes the window

The exact direct child F2 closes the window when:

```text
level = F2
chain_index = 2
status = CONFIRMED
f2_lifecycle_status = FP_F2_LC_CONFIRMED
has_confirm = true
exact parent identity matches F1
```

`f2_can_spawn_f3` is not part of the definition. The requested close boundary is F2 confirmation itself, not later F3 eligibility.

## 4. Multi-count truth table

```text
Count A: bullish, F1 confirmed, child F2 unconfirmed
Count B: bullish, before F1 confirmation
→ Buy remains authorized by Count A
```

```text
Count A: bullish, child F2 confirmed
Count B: bullish, F1 confirmed, child F2 unconfirmed
→ Buy remains authorized by Count B
```

```text
Count A: bullish window open
Count B: bearish window open
→ ambiguous; no entry
```

```text
All counts before F1 or after F2
→ no entry
```

This prevents a newer immature count from suppressing a different valid count.

## 5. Hook relationship

The count must also be in F phase. A Hook/ND can close only the count that owns that Hook boundary. An unrelated Hook does not globally veto every count.

## 6. Closed-bar semantics

The classifier uses closed bars only. Therefore:

```text
F1 confirmation becomes visible in the cached HTF event stream
→ window opens

Exact child F2 confirmation becomes visible in the cached HTF event stream
→ window closes
```

No live HTF candle is used.

## 7. Pending-order semantics

With pending cancellation enabled, a pending order is required to remain inside the currently authorized window. When its direction is no longer authorized, the order is cancelled.

With consume-on-fill enabled:

```text
pending accepted
→ context is active but not permanently consumed

pending cancelled before fill
→ active attempt is released

same F2 still structurally valid
+ entry and target were not already touched
+ HTF window reopens
→ order may be armed again

order fills
→ one-attempt identity becomes permanently consumed
```

Open positions are not closed by the window.

## 8. Input off

```text
InpF2BTUseHigherTimeframeF1ToF2ConfirmationWindow = false
```

The broad HTF F-phase direction filter remains active. Any count in count-local F phase may qualify without the F1-confirmed/F2-unconfirmed restriction.

## 9. State model

```text
DISABLED
NOT_EVALUATED
SEQUENCE_MISSING
AMBIGUOUS
BEFORE_F1_CONFIRM
OPEN
CLOSED_AFTER_F2_CONFIRM
```

Only `OPEN` qualifies when the lifecycle-window input is enabled.
