# NDS Command Preview Contract

## Definition

The Command Preview is a broker-neutral envelope. It describes a possible future operational instruction but is not an `MqlTradeRequest` and cannot send an order.

## Hard locks

```text
volume = 0
send_allowed = false
command_action = PREVIEW_ONLY_NO_SEND
```

## Preview order families

- limit at first edge;
- limit at Zone midpoint;
- limit near death edge;
- market after confirmation;
- laddered limit preview.

These are enum contracts, not approved NDS doctrine until the Entry Canon selects them.

## Future promotion gates

A broker adapter must remain separately gated by:

- canonical Zone and trade contract;
- risk authorization;
- symbol metadata validation;
- volume normalization;
- spread, stops, freeze-level, slippage, and session checks;
- duplicate and idempotency protection;
- deployment profile authorization.

## Related

- [[NDS Trade Plan Contract]]
- [[NDS Risk and Capital Boundary]]
