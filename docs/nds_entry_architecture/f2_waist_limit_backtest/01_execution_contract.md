# F2 Waist Limit — Execution Contract

## Source event

The setup source is a canonical F2 event satisfying all of the following:

```text
level = F2
status = CONFIRMED
f2_lifecycle_status = CONFIRMED
f2_can_spawn_f3 = true
has waist = true
has Leg2 = true
has confirmation = true
canonical parent F1 exists
parent F1 has waist = true
```

By default, the F2 must also be visible in the final canonical stream.

## Bullish contract

```text
Buy Limit = F2 waist − entry offset
Stop Loss = F1 waist
Take Profit = F2 Leg2 endpoint
```

Required geometry:

```text
F1 waist < entry < F2 Leg2
```

## Bearish contract

```text
Sell Limit = F2 waist + entry offset
Stop Loss = F1 waist
Take Profit = F2 Leg2 endpoint
```

Required geometry:

```text
F2 Leg2 < entry < F1 waist
```

## Exactness policy

The Stop and Take Profit references are not moved to satisfy broker constraints. They are normalized to symbol tick size only. If exact structural levels violate `SYMBOL_TRADE_STOPS_LEVEL`, the setup is blocked.

The entry offset is explicit and configurable. Default: one point beyond the F2 waist.

## Freshness

Default setup age is one bar. An old historical F2 is not armed when the tester starts. `iBarShift` must resolve the confirmation bar and the shift must not exceed `InpF2BTMaxSetupAgeBars`.

## Exposure

For the dedicated strategy magic:

```text
managed pending orders + managed positions ≤ 1
```

A pending order blocks all later F2 setups. A filled position remains owned by the broker-side SL/TP and blocks all later F2 setups until it closes.

## Attempt identity

Each F2 is identified by symbol, timeframe, event, sequence, direction, confirmation time, waist time and Leg2 time. By default, each F2 gets one successful paper/send attempt.
