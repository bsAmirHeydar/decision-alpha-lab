# NDS Hook 86.4 Cycle R1 Entry Contract

## Source contract

Only an existing canonical valid HH/F3H Hook sequence may qualify. Phase02 owns Hook identity, Origin, Crown, confirmed Terminal and `x_count` exactly 3 or 4. Phase03 owns Y references. Phase04 owns 50% X-cycle closure and origin-return death.

## Closure and first-arrival gates

```text
Phase04.x_closed == true
Phase04.origin_return_penetrated == false
no closed-bar 86.4 touch at or after closure
```

`terminal_retracement_ratio` remains audit evidence and does not own the post-closure first-arrival decision.

The closure candle is included in the price scan. Same-candle closure and 86.4 touch is blocked because the order could not have existed after observing that close.

## Entry

```text
Entry = Crown + 0.864 × (Origin − Crown)
```

- positive Hook → Buy Limit;
- negative Hook → Sell Limit.

## Protection

Stop is beyond Death Boundary, otherwise Origin, with existing point/spread/broker-distance normalization. Target is attached at exactly one risk distance and normalized away from Entry.

## Identity

One sequence has one attempt. x3→x4 does not create another key or reprice an existing order. Pending/position profile ownership survives restart through existing Magic plus broker-comment recovery.

## Related

- [[NDS Hook 86.4 Cycle R1 State Machine]]
- [[NDS Hook 86.4 Cycle R1 Audit Ledger]]
- [[NDS Hook 86.4 No Trade Diagnostic Funnel]]
- [[NDS Single Exposure Lock]]
- [[NDS Risk and Capital Boundary]]
