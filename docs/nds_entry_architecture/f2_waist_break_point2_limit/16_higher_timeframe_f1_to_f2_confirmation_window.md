# 16 — Higher-Timeframe F1-to-F2 Confirmation Window

## 1. Purpose

This optional filter narrows the existing higher-timeframe F-phase direction gate to one exact lifecycle interval on the same canonical higher-timeframe count that supplies direction.

```text
Before HTF F1 confirmation
→ no new lower-timeframe trade

After HTF F1 confirmation
and before the direct child HTF F2 confirmation
→ lower-timeframe trades may be authorized

At or after the direct child HTF F2 confirmation
→ no new lower-timeframe trade
```

Default:

```text
InpF2BTUseHigherTimeframeF1ToF2ConfirmationWindow = true
```

The filter is subordinate to the existing requirement that the higher timeframe is in F rather than Hook/ND. Both conditions must pass.

## 2. Exact-count authority

The window is not evaluated from any F1 and any F2 found on the higher timeframe. It is evaluated from the exact canonical sequence selected by the existing higher-timeframe phase classifier.

```text
Selected HTF canonical F event
→ selected sequence_id
→ exact F1 root of that sequence
→ exact direct-child F2 of that F1
```

The following identity fields must agree:

- `sequence_id`;
- direction;
- scale `L`;
- F1 `chain_index = 1`;
- F2 `chain_index = 2`;
- F2 `parent_sequence_id = F1.sequence_id`;
- F2 `parent_event_id = F1.event_id`.

A similarly directed F1 or F2 from another scale, another sequence, or another parent is not allowed to open or close this window.

## 3. Confirmation definitions

### F1 confirmation

F1 is considered stabilized only when all canonical lifecycle evidence is present:

```text
level = F1
status = CONFIRMED
lifecycle_status = FP_F1_LC_CONFIRMED
has_confirm = true
lifecycle_can_spawn_f2 = true
```

A complete F1 body, live F1, post-flag F1, or probable F1 does not open the window.

### F2 confirmation

The window closes only when the exact direct child F2 is stabilized:

```text
level = F2
status = CONFIRMED
f2_lifecycle_status = FP_F2_LC_CONFIRMED
has_confirm = true
f2_can_spawn_f3 = true
```

A live-body, size-rejected, post-flag, or otherwise unconfirmed F2 does not close the window.

## 4. Direction contract

The direction continues to come from the selected canonical higher-timeframe F phase.

```text
Selected HTF count is bullish F
+ exact F1 confirmed
+ exact F2 not yet confirmed
→ Buy setups only

Selected HTF count is bearish F
+ exact F1 confirmed
+ exact F2 not yet confirmed
→ Sell setups only
```

The lifecycle window does not create a direction. It only narrows the time interval during which the already-selected direction has entry authority.

## 5. Combined gate

The full authorization is:

```text
HTF data ready
AND canonical F exists
AND latest phase is F, not Hook/ND
AND no equal-priority direction conflict
AND selected count F1 is confirmed
AND selected count direct-child F2 is not confirmed
AND lower-timeframe setup direction matches selected HTF direction
```

Any failure closes the gate.

## 6. Closed-bar semantics

The higher-timeframe classifier uses closed bars only. Therefore the lifecycle boundary becomes effective only after the higher-timeframe bar containing the canonical confirmation has closed and the cached snapshot refreshes.

```text
F1 confirmation becomes visible on a closed H1 bar
→ window opens on the next cached H1 snapshot

F2 confirmation becomes visible on a closed H1 bar
→ window closes on the next cached H1 snapshot
```

No live higher-timeframe candle is used. This preserves causal replay and prevents future leakage.

## 7. Pending-order lifecycle

The existing pending-order policy also applies to this window:

```text
InpF2BTCancelPendingWhenHigherTimeframeDisallows = true
```

With the default enabled:

- pending orders created before F1 confirmation are not allowed;
- pending orders are allowed only inside the open F1→F2 interval;
- when the exact F2 confirms, still-unfilled managed pending orders are cancelled;
- open positions are not force-closed by this entry filter.

Position exit authority remains with the selected fixed, local-F3, or higher-timeframe-F3 exit mode.

## 8. Optionality

```text
InpF2BTUseHigherTimeframeF1ToF2ConfirmationWindow = true
→ strict F1-confirmed / F2-unconfirmed window

InpF2BTUseHigherTimeframeF1ToF2ConfirmationWindow = false
→ original HTF F-phase direction filter only
```

Turning this input off does not turn off the higher-timeframe direction filter. The two controls are separate.

## 9. Fail-closed cases

No entry is authorized when:

- the selected canonical event has no valid sequence id;
- the exact F1 root is missing;
- more than one F1 root exists for the selected sequence;
- more than one exact direct-child F2 exists for that F1;
- F1 is not confirmed;
- F2 is already confirmed;
- the phase is Hook/ND;
- direction is ambiguous;
- higher-timeframe history is incomplete.

The filter never substitutes another sequence merely to keep trading.

## 10. State model

```text
DISABLED
NOT_EVALUATED
SEQUENCE_MISSING
AMBIGUOUS
BEFORE_F1_CONFIRM
OPEN
CLOSED_AFTER_F2_CONFIRM
```

Only `OPEN` authorizes a new setup when the input is enabled.

## 11. Performance contract

No second higher-timeframe scan is added. The lifecycle window consumes the same event array already produced by the cached higher-timeframe F/Hook classifier.

```text
One HTF canonical scan per new HTF bar
→ phase selection
→ same-array F1/F2 lineage-window evaluation
→ cached gate
```

There is no per-tick detector, renderer, CSV, timer, or print.

## 12. Acceptance cases

### Before F1 confirmation

```text
HTF bullish F1 body exists but is not confirmed
→ Buy blocked
→ Sell blocked
```

### Open interval

```text
HTF bullish F1 confirmed
HTF direct-child F2 absent or unconfirmed
→ Buy allowed
→ Sell blocked
```

### Close boundary

```text
Same HTF direct-child F2 confirms
→ new Buy blocked
→ pending Buy cancelled when cancellation policy is enabled
→ existing Buy position remains under its own exit mode
```

### Different sequence cannot close the window

```text
Selected sequence A: F1 confirmed, F2 unconfirmed
Different sequence B: F2 confirmed
→ sequence B cannot close sequence A's window
```

### Input disabled

```text
Lifecycle-window input = false
HTF is bullish canonical F and not Hook/ND
→ Buy may be authorized under the original phase-direction contract
```

## 13. Non-goals

This filter does not:

- change lower-timeframe entry geometry;
- change RR calculation or entry repricing;
- change overlap arbitration;
- close live positions when F2 confirms;
- select another HTF count by AI;
- use an F2 from another sequence as the close boundary;
- use the live higher-timeframe candle.
