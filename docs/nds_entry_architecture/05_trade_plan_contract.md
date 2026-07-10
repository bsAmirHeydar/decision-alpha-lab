---
title: NDS Trade Plan Contract
status: normative
version: 1.0.0
---
# NDS Trade Plan Contract

## 1. Definition

A Trade Plan is a complete price-geometry proposal derived from a ready Setup. It is not an order and carries no capital authority.

Required fields:

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
minimum RR requirement
sizing status
```

## 2. Directional geometry

Bullish:

```text
stop < entry < target
```

Bearish:

```text
target < entry < stop
```

A plan that violates this ordering is blocked even if all prices are positive.

## 3. RR treatment

The scaffold calculates geometric RR:

```text
reward_distance / risk_distance
```

`InpNDSEntryMinRR = 0` disables an RR threshold. This is the safe default because the final optionality doctrine has not yet established a universal minimum.

RR is an audit field, not permission to bypass Hook or Zone validity.

## 4. Position sizing boundary

The current plan always sets:

```text
requested_risk_fraction = 0
requested_volume = 0
sizing_status = SIZING_DISABLED_NO_CAPITAL_AUTHORITY
```

A future sizing module must independently validate:

- account equity source;
- risk budget;
- symbol tick value;
- contract size;
- currency conversion;
- broker volume step/min/max;
- aggregate portfolio exposure;
- correlated exposure;
- daily and strategy loss limits.

## 5. Multi-target and open-profit management

The current row has one diagnostic target field for geometry validation. It does not encode the final Alpha Lab open-profit doctrine. Future versions should separate:

```text
structural destination
minimum evaluation destination
partial-management trigger
hard target, if any
open-tail management policy
time exit
thesis invalidation
```
