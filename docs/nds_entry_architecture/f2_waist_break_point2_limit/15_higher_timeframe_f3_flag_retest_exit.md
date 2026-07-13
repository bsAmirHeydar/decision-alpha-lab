# 15 — Higher-Timeframe F3 Flag-Retest Exit

## 1. Purpose

This exit mode keeps the original lower-timeframe F2 Point-2 trade open beyond its normal local exit and transfers exit authority to a canonical F3 on a configured higher timeframe.

```text
Lower-timeframe F2 Point-2 entry
→ position remains open
→ first eligible same-direction higher-timeframe F3 forms Leg1
→ that exact higher-timeframe F3 forms its own Waist
→ Waist is the correction gate
→ TP is armed at the end of that exact F3 Leg1
→ retest of the Leg1 endpoint closes the bound position
```

The default higher timeframe is `H1`. The selected exit timeframe must be strictly higher than the entry chart timeframe; otherwise initialization fails with an input-parameter error.

## 2. Input contract

```text
InpF2BTExitMode = FP_NDS_F2_EXIT_HIGHER_TIMEFRAME_F3_FLAG_RETEST
InpF2BTF3ExitHigherTimeframe = PERIOD_H1
```

The exit timeframe is independent from the entry timeframe. It is also independent from whether the higher-timeframe entry filter is enabled. The existing `InpF2BTHigherTimeframe` input still controls entry authorization; `InpF2BTF3ExitHigherTimeframe` controls this exit mode.

## 3. Reward/Risk authority remains unchanged

The future higher-timeframe F3 target is unknown at entry. It must not be used to admit, reject, or reprice the setup.

```text
RR Reference Target = original lower-timeframe F2 Leg2 endpoint
Risk                = abs(Entry - Stop)
Reference Reward    = abs(F2 Leg2 - Entry)
Reference RR        = Reference Reward / Risk
```

Therefore all existing minimum-RR and RR-repricing rules continue to use the original F2 endpoint.

## 4. Order creation

The pending order is submitted with:

```text
Entry = final Point-2 limit behind F2 Waist
SL    = behind direct parent F1 Waist
TP    = 0
```

A dynamic exit context is registered before the setup is consumed. An accepted order is removed if its context cannot be registered, preventing an unmanaged no-TP position.

## 5. Per-position binding

Every position keeps an independent exit context:

```text
Position Ticket
→ Position Open Time
→ Configured HTF
→ First eligible canonical same-direction HTF F3 after entry
→ Exact F3 sequence identity
→ Exact F3 Leg1 node
→ Exact F3 Waist node
→ Dynamic target and TP state
```

Two positions may legitimately observe the same higher-timeframe F3, but they do not share mutable state. Each ticket separately stores the F3 identity, target, correction state, and TP-armed state.

## 6. Candidate-selection rule

The system scans closed bars only and selects the first eligible canonical F3 whose Leg1 belongs to the entry HTF bar or a later HTF bar.

Eligibility requires:

- `level == F3`;
- same direction as the position;
- `visible_main == true`;
- valid body and lifecycle;
- an existing positive-price Leg1 node;
- Leg1 later than the position-specific search boundary.

When several candidates have the same Leg1 time, canonical priority resolves the tie. The selected candidate is then locked by stable anatomy:

- direction;
- scale `L`;
- sequence ID;
- parent-sequence ID;
- Leg1 node ID;
- Leg1 anchor time.

Event IDs remain audit metadata and are not the sole runtime identity.

## 7. Correction gate

Leg1 alone does not arm TP. The same locked F3 must create its own Waist after Leg1:

```text
F3 Leg1 exists
→ WAIT_HTF_F3_WAIST
→ same F3 has Waist with pos_waist > pos_leg1
→ correction confirmed
→ target becomes exact Leg1 price
```

No generic one-tick pullback, unrelated F3 Waist, or latest same-direction F3 may satisfy the correction gate.

## 8. Retest exit

After the exact F3 Waist exists:

```text
Bullish position:
TP = exact HTF F3 Leg1 endpoint above market

Bearish position:
TP = exact HTF F3 Leg1 endpoint below market
```

If the target has already been reached before broker geometry permits attaching TP, the existing policy applies:

```text
InpF2BTCloseAtMarketIfF3TargetAlreadyReached = true
→ close only the bound position ticket
```

## 9. Candidate invalidation

The HTF exit scanner retains invalidated candidates in its audit stream. If the locked F3 invalidates before producing a valid Waist:

```text
locked candidate invalidates
→ release only that candidate
→ advance the position-specific search boundary
→ wait for the next eligible HTF F3
```

This prevents a position from being permanently attached to a dead F3 while also preventing it from falling backward to an older structure.

## 10. Interaction with the HTF entry filter

The entry filter and HTF exit serve different authorities.

```text
HTF entry filter:
controls whether a new Buy or Sell may be submitted

HTF F3 exit:
controls an already-open position's future target
```

A later Hook/ND state or direction change may block new entries and cancel pending orders, but it does not terminate an open position waiting for its HTF F3 exit.

## 11. Runtime and performance

The higher-timeframe F3 stream is rebuilt only when all conditions are true:

- the selected exit mode is HTF F3 retest;
- at least one managed position is open;
- the configured HTF has opened a new bar.

The scan uses closed bars and is cached for all lower-timeframe ticks and bars until the next HTF bar. No renderer, CSV, timer, chart object, or runtime print is introduced.

## 12. State machine

```text
DYNAMIC ORDER PENDING
  ├─ original F2 reference target touched before fill → cancel
  └─ filled → WAIT_HTF_F3_LEG1

WAIT_HTF_F3_LEG1
  ├─ Stop hit → closed
  └─ first eligible same-direction canonical HTF F3 Leg1 → lock candidate

WAIT_HTF_F3_WAIST
  ├─ candidate invalidates → release and wait for next HTF F3
  ├─ Stop hit → closed
  └─ same locked F3 creates Waist → WAIT_HTF_F3_RETEST

WAIT_HTF_F3_RETEST
  ├─ target already reached → close bound ticket at market by policy
  ├─ broker TP geometry valid → arm TP at exact F3 Leg1 endpoint
  └─ otherwise → retry without changing candidate

TP_ARMED
  ├─ Stop hit → closed
  └─ exact HTF F3 Leg1 retest → TP exit
```

## 13. Non-negotiable invariants

1. Higher-timeframe exit mode never changes the original RR reference.
2. Every position owns an independent context and position ticket.
3. Direction must match the open position.
4. The Waist must belong to the same locked F3 as the target Leg1.
5. A local-timeframe F3 cannot service HTF exit mode.
6. An unrelated or newer F3 cannot replace a valid locked candidate.
7. The scanner uses closed higher-timeframe bars only.
8. Open positions continue to be managed even when the HTF entry gate is closed.
