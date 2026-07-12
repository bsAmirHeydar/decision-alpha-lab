# 03 — Execution State Machine

```text
IDLE / PORTFOLIO_ACTIVE
  │
  ├─ no complete F2 body → no new order
  ├─ no confirmed direct parent F1 → no new order
  ├─ stale or previously used F2 context → no new order
  ├─ target already consumed / F2 confirmed → no new order
  ├─ RR below configured minimum → no new order
  ├─ concurrency policy blocks direction/context → no new order
  └─ valid independent context → ORDER_PENDING(context_hash)

ORDER_PENDING(context_hash)
  │
  ├─ price penetrates F2 waist → LIMIT FILLED → POSITION_OPEN(context_hash)
  ├─ own F2 Leg2 target touched before fill → cancel only this order
  └─ otherwise → hold independently

POSITION_OPEN(context_hash)
  │
  ├─ own parent F1 waist stop reached → stop exit
  ├─ own F2 Leg2 endpoint reached → target exit
  └─ otherwise → hold independently
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
