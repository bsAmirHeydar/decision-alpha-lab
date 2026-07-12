# 03 — Execution State Machine

```text
IDLE / PORTFOLIO_ACTIVE
  │
  ├─ no complete F2 body → no new order
  ├─ no confirmed direct parent F1 → no new order
  ├─ stale or previously used F2 context → no new order
  ├─ target already consumed / F2 confirmed → no new order
  ├─ structural RR below minimum + repricing disabled → no new order
  ├─ structural RR below minimum + repricing enabled → move Entry toward Stop
  ├─ adjusted Entry invalid for broker geometry → no new order
  ├─ same-direction stop corridor overlaps above threshold → wider context wins
  ├─ concurrency policy blocks direction/context → no new order
  └─ valid surviving context → ORDER_PENDING(context_hash)

ORDER_PENDING(context_hash)
  │
  ├─ price penetrates F2 waist → LIMIT FILLED → POSITION_OPEN(context_hash)
  ├─ own F2 Leg2 target touched before fill → cancel only this order
  └─ otherwise → hold independently

POSITION_OPEN(context_hash)
  │
  ├─ own parent F1 waist stop reached → stop exit
  ├─ fixed-exit mode + own F2 Leg2 reached → target exit
  └─ dynamic F3-exit mode → WAIT_F2_CONFIRM

WAIT_F2_CONFIRM(context_hash)
  │
  ├─ source F2 confirms → capture F2.confirm = F3 Leg1
  └─ otherwise → hold

WAIT_F3_CORRECTION(context_hash)
  │
  ├─ price moves adversely by configured ticks → arm TP at F2.confirm
  └─ otherwise → hold

WAIT_F3_RETEST(context_hash)
  │
  ├─ TP can be attached → broker TP at F2.confirm
  ├─ target already re-hit → market close
  └─ otherwise → retry on next tick
```

## Parallel-context invariant

The old global invariant `pending + positions <= 1` is removed.

The new contract is:

```text
same setup_hash → never duplicated
same direction + different context → controlled by input, default allowed
opposite direction + different context → controlled by hedge input, default allowed
```

Independent same-symbol positions are authorized only on MT5 hedging accounts. On netting/exchange accounts, a second managed exposure is blocked.

## Optional exposure cap

`InpF2BTMaxConcurrentManagedExposures = 0` means unlimited by strategy policy. A positive number creates a hard cap.

## Body-version policy

A body version is identified by:

- symbol and timeframe;
- direction and scale;
- parent F1 waist time;
- F2 origin time;
- F2 waist time;
- F2 Leg2 time and price.

If Leg2 extends before entry, the old target is consumed and the old pending is cancelled. The extended Leg2 creates a new context and can arm a new order.

## Near-duplicate arbitration

```text
Stop corridor = [min(Entry, Stop), max(Entry, Stop)]
Overlap % = intersection length / narrower corridor length × 100
```

At or above the configured threshold, only the wider same-direction corridor is retained. If both appear on the same bar, arbitration occurs before any order is sent. If a wider context appears while a narrower pending order still exists, the narrower pending is removed and replaced. An already-filled overlapping position is not closed or replaced.


## Dual-exit invariant

The RR gate and RR-based Entry repricing always use the original F2 Leg2 endpoint. Dynamic F3 exit does not use future target information at setup time.
