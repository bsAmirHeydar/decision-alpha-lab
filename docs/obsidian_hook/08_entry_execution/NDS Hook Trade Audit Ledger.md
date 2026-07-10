# NDS Hook Trade Audit Ledger

## File

```text
MQL5/Files/FlagCountingPhoenix/nds_hook_limit_f123_trade_ledger.csv
```

## Trace fields

- generated time, symbol, timeframe;
- action, status, reason;
- managed pending and position counts;
- broker order and position tickets;
- Hook sequence, family, direction;
- terminal entry, death, stop, volume;
- one-attempt setup key;
- F1 start, F2 start, F3 completion and F3 price;
- final state key.

## Use

The ledger is the first diagnostic source for:

- why no order was sent;
- why a pending order was held or cancelled;
- why a position did not exit;
- which F123 sequence authorized the exit;
- whether the single-exposure invariant was active.

## Related

- [[NDS Same Direction F123 Exit]]
- [[NDS Hook Trade Operator Checklist]]
- [[NDS Entry Audit Outputs]]
