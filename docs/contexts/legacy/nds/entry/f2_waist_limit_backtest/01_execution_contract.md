# F2 Waist Limit — Execution Contract

## Source event

The source must satisfy all canonical F2 lifecycle gates:

```text
level = F2
direction = bullish or bearish
f2_parent_ready = true
f2_size_gate_passed = true
f2_lifecycle_status = CONFIRMED
status = CONFIRMED
f2_can_spawn_f3 = true
waist, Leg2 and confirmation nodes exist
canonical same-direction F1 parent exists
parent F1 waist exists
```

## Bullish

```text
Buy Limit = F2 waist − configured tick offset
Stop Loss = parent F1 waist
Take Profit = F2 Leg2
```

Required ordering:

```text
F1 waist < Buy Limit < F2 Leg2
```

## Bearish

```text
Sell Limit = F2 waist + configured tick offset
Stop Loss = parent F1 waist
Take Profit = F2 Leg2
```

Required ordering:

```text
F2 Leg2 < Sell Limit < F1 waist
```

## Exposure

For the strategy Magic Number:

```text
managed pending orders ≤ 1
managed positions ≤ 1
```

Any existing managed order or position blocks detector reconstruction and new order creation.
