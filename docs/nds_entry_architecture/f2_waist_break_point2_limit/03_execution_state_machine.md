# 03 — Execution State Machine

## 1. Candidate lifecycle

```text
IDLE / PORTFOLIO_ACTIVE
  │
  ├─ rebuild cached HTF state only on a new HTF bar
  ├─ evaluate every canonical HTF F count
  ├─ no sole qualifying HTF direction → no new order
  ├─ lower-timeframe direction conflicts with HTF → reject candidate
  ├─ no complete unconfirmed F2 body → reject candidate
  ├─ no confirmed direct parent F1 → reject candidate
  ├─ F2 or parent invalidated → reject candidate
  ├─ F2 target already retested since observability → reject candidate
  ├─ final executable entry already touched since observability → missed, reject
  ├─ setup already filled under one-attempt policy → reject
  ├─ RR below minimum + repricing disabled → reject
  ├─ RR below minimum + repricing enabled → move Entry toward fixed Stop
  ├─ final broker geometry invalid → reject
  ├─ overlap above threshold → suppress narrower context
  ├─ exposure policy blocks context → reject
  └─ valid survivor → ORDER_PENDING(context_hash)
```

There is no arbitrary age rejection by default. `InpF2BTMaxSetupAgeBars = -1` means structural lifecycle owns validity.

## 2. Pending lifecycle

```text
ORDER_PENDING(context_hash)
  │
  ├─ duplicate of same hash requested → blocked by active-attempt registry
  ├─ price reaches final limit → fill → consume one-attempt identity
  ├─ own F2 Leg2 target reached first → cancel; setup becomes structurally consumed
  ├─ HTF direction/window closes and cancellation policy is on → cancel
  │     └─ active attempt released; may re-arm later only if still causally valid
  ├─ external cancellation/rejection/expiry → release active attempt
  ├─ wider overlapping pending appears → remove narrower, submit wider
  └─ otherwise → hold independently
```

## 3. Position lifecycle

```text
POSITION_OPEN(context_hash)
  │
  ├─ own direct-parent F1-waist stop reached → stop exit
  ├─ FIXED_F2 mode + own F2 Leg2 reached → target exit
  ├─ LOCAL_F3 mode → exact source-F2 / direct-child-F3 manager
  └─ HTF_F3 mode → per-position higher-timeframe F3 manager
```

The HTF entry gate never force-closes an open position.

## 4. Local exact-F3 exit

```text
POSITION_OPEN(source_f2_identity, position_ticket)
  → detect only exact direct-child F3 of that source F2
  → wait for Waist of the same F3
  → TP = Leg1 endpoint of that same F3
  → modify or close only the bound position ticket
```

No F3 from another scale, sequence, F2, or position can own the exit.

## 5. HTF-F3 exit

```text
POSITION_OPEN(position_ticket, open_time)
  → first eligible same-direction canonical F3 on configured higher timeframe
  → lock exact F3 identity per ticket
  → wait for Waist of the same locked F3
  → TP = exact Leg1 endpoint
```

## 6. Parallel-context invariant

```text
same setup_hash + active pending → never duplicate
same setup_hash + prior fill → permanently consumed when one-attempt is on
same direction + different context → input-controlled, default allowed
opposite direction + different context → hedge input-controlled, default allowed
```

Independent same-symbol contexts require an MT5 hedging account. With the default fail-fast input, a netting account causes `INIT_PARAMETERS_INCORRECT` instead of silently producing a different portfolio model.

## 7. Near-duplicate arbitration

```text
Stop corridor = [min(final Entry, Stop), max(final Entry, Stop)]
Overlap % = intersection / narrower corridor × 100
```

At or above the configured threshold, only the wider same-direction corridor survives. An already-filled position is never replaced.

## 8. RR invariant

All three exit modes calculate minimum RR from:

```text
RR reference = original F2 Leg2 endpoint
Risk = abs(final Entry - F1-waist Stop)
Reward = abs(F2 Leg2 - final Entry)
```

Future F3 exits never enter setup-time RR.
