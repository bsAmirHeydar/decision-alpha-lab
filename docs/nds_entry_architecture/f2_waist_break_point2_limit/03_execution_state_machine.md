# 03 — Execution State Machine

```text
IDLE
  │
  ├─ no complete F2 body → IDLE
  ├─ no confirmed direct parent F1 → IDLE
  ├─ stale F2 body version → IDLE
  ├─ target already consumed / F2 confirmed → IDLE
  └─ valid geometry → ORDER_PENDING

ORDER_PENDING
  │
  ├─ price penetrates F2 waist → LIMIT FILLED → POSITION_OPEN
  ├─ F2 Leg2 target touched before fill → CANCEL → IDLE
  └─ otherwise → HOLD

POSITION_OPEN
  │
  ├─ parent F1 waist stop reached → STOP EXIT → IDLE
  ├─ F2 Leg2 endpoint reached → TARGET EXIT → IDLE
  └─ otherwise → HOLD
```

## Single-exposure invariant

```text
managed pending orders + managed positions <= 1
```

When a managed position exists, no detector rebuild is executed. Broker/tester SL and TP own the exit.

When a managed pending exists, only one closed bar is read to determine whether the target was consumed before fill. The full detector is not rebuilt.

## Body-version policy

A body version is identified by:

- symbol and timeframe;
- direction and scale;
- parent F1 waist time;
- F2 origin time;
- F2 waist time;
- F2 Leg2 time and price.

If Leg2 extends before entry, the old target is consumed and the old pending is cancelled. The extended Leg2 creates a new body version that can arm a new order.
