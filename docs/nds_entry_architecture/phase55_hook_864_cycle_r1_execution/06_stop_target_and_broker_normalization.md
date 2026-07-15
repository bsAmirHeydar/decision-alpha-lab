# 06 — Stop, Target, and Broker Normalization

## Structural stop source

```text
Death = death_boundary_price when available
        otherwise origin_price
```

The stop is placed beyond Death using the existing combined buffer:

```text
buffer = stop_buffer_points × point
       + stop_spread_multiplier × current_spread
```

- Bullish: `StopRaw = Death − buffer`
- Bearish: `StopRaw = Death + buffer`

If broker `SYMBOL_TRADE_STOPS_LEVEL` requires more distance, the stop is expanded away from Entry. The stop never moves toward Entry to satisfy the broker.

## Fixed one-R target

After normalized Entry and Stop:

```text
Risk = |Entry − Stop|
TargetRaw = Entry + Risk   for Buy
TargetRaw = Entry − Risk   for Sell
```

The target is normalized away from Entry:

- Buy target rounds up.
- Sell target rounds down.

The final check requires normalized reward to be at least one normalized risk distance, with a small tick tolerance for floating representation.

## Ordering invariants

```text
Buy:  Stop < Entry < Target
Sell: Target < Entry < Stop
```

Any violation blocks the setup.

## Broker capabilities

The sender requires Limit and Stop-Loss capability for both profiles. It additionally requires Take-Profit capability when `target_price > 0`, which is mandatory for Phase 55. The broker request attaches SL and TP atomically with the pending limit request.

## No F123 target mutation

Once the Phase 55 position exists, the shared core validates the broker-held SL/TP geometry and does not call the F123 exit detector. It does not trail, partial-close, or reprice the target.
