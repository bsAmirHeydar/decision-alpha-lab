# NDS Trade Plan Contract

## Required geometry

Bullish:

```text
stop < entry < target
```

Bearish:

```text
target < entry < stop
```

## Fields

```text
plan_id
source_setup_id
trade_direction
entry_price
stop_price
target_price
risk_distance
reward_distance
RR
minimum_RR
sizing_status
```

## Capital boundary

Phase 51 always emits:

```text
requested_risk_fraction = 0
requested_volume = 0
sizing_status = SIZING_DISABLED_NO_CAPITAL_AUTHORITY
```

A valid price geometry is not capital permission.

## Future extensions

- multiple destinations;
- open-tail management;
- thesis stop versus emergency broker stop;
- time and movement-quality exits;
- partial reductions;
- revisioned plans.

## Related

- [[NDS Risk and Capital Boundary]]
- [[NDS Command Preview Contract]]
