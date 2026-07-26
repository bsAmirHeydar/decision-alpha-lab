# NDS Hook Trade Operator Checklist

## Before enabling

- [ ] Compile `FlagCountingPhoenixExperiment.mq5` with zero errors and warnings.
- [ ] Confirm the account is demo or otherwise controlled.
- [ ] Confirm `InpNDSHookTradeMagic` is unique to this strategy.
- [ ] Confirm fixed volume or cash-risk sizing.
- [ ] Confirm Phase 52 source filters allow only HH and F3H.
- [ ] Confirm no pre-existing order or position uses the same magic.
- [ ] Confirm terminal AutoTrading and symbol permissions.

## Decision-audit profile

```text
InpNDSHookTradeEnabled = true
InpNDSHookTradeSendLiveOrders = false
```

- [ ] Inspect the terminal entry price.
- [ ] Inspect death and stop geometry.
- [ ] Inspect `nds_hook_limit_f123_trade_ledger.csv`.

## Controlled live profile

```text
InpNDSHookTradeEnabled = true
InpNDSHookTradeSendLiveOrders = true
```

- [ ] Verify only one pending order exists.
- [ ] After fill, verify no stray pending remains.
- [ ] Verify opposite-direction F123 does not exit.
- [ ] Verify a new full same-direction F123 closes the position.
- [ ] Verify the same Hook cannot re-enter after restart.

## Emergency

- Set `InpNDSHookTradeEnabled = false` to stop new strategy actions.
- Existing broker orders and positions remain broker state and must be reviewed explicitly.
- Multiple managed positions trigger fail-closed status rather than automatic liquidation.

## Related

- [[NDS Hook Trade State Machine]]
- [[NDS Hook Trade Audit Ledger]]
- [[NDS Single Exposure Lock]]
