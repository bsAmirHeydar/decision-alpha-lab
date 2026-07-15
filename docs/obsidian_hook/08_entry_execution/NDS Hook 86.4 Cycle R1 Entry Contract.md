# NDS Hook 86.4 Cycle R1 Entry Contract

## Source contract

Only an existing canonical valid HH/F3H Hook sequence may qualify. Required fields are canonical Cycle closure, confirmed Terminal, valid Crown, and `x_count` exactly 3 or 4.

## First-arrival gate

```text
terminal_retracement_ratio < 0.864
```

A Terminal that has touched or crossed 86.4 makes a newly created order late and therefore blocked.

## Entry

```text
Entry = Crown + 0.864 × (Origin − Crown)
```

- positive Hook → Buy Limit;
- negative Hook → Sell Limit.

## Protection

Stop is beyond Death Boundary, otherwise Origin, with existing point/spread/broker-distance normalization. Target is attached at exactly one risk distance and normalized away from Entry.

## Identity

One sequence has one attempt. x3→x4 does not create another key or reprice an existing order.

## Related

- [[NDS Hook 86.4 Cycle R1 State Machine]]
- [[NDS Hook 86.4 Cycle R1 Audit Ledger]]
- [[NDS Single Exposure Lock]]
- [[NDS Risk and Capital Boundary]]
