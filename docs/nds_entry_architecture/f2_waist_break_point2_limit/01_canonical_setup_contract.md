# 01 — Canonical Setup Contract

## 1. Scope

This setup is independent of Hook, Hook-after-Hook, Hook-after-F3, Zone, Cycle Group and AI selection logic. It consumes only canonical F1/F2 anatomy from Phoenix.

## 2. Structural precondition

A valid parent-child pair exists:

```text
Confirmed F1 parent
→ complete F2 two-leg body
```

The F2 body is:

```text
F2 Origin → F2 Leg1 → F2 Waist → F2 Leg2
```

The setup is armed when the complete F2 body becomes observable without future data. It does not wait for F2 confirmation.

## 3. Point-1 / Point-2 grammar

The special F2 waist-break branch is:

```text
Point 1 = F2 Waist
Point 2 = first strict penetration beyond the F2 Waist
```

The pending order is placed before Point 2 forms:

```text
Bullish F2: Buy Limit strictly below F2 Waist
Bearish F2: Sell Limit strictly above F2 Waist
```

Therefore, the fill itself is the executable Point 2.

## 4. Risk and target

```text
Entry  = behind F2 Waist
Stop   = behind direct parent F1 Waist
Target = F2 Leg2 endpoint / end of F2 two-leg flag
```

For bullish F2:

```text
Stop < Entry < Target
```

For bearish F2:

```text
Target < Entry < Stop
```

## 5. Reward/Risk eligibility

After executable prices are normalized:

```text
RR = abs(Target - Entry) / abs(Entry - Stop)
```

The default minimum is `1.0`. A setup below the configured minimum is rejected before any order request is built.

## 6. Parallel context policy

A distinct F2 body version is a distinct context. By default:

```text
same-direction contexts = allowed
opposite-direction hedge contexts = allowed
```

The same context can still trade only once. Independent same-symbol positions require an MT5 hedging account; non-hedging accounts remain single-exposure to preserve independent SL/TP ownership.

## 7. Critical timing rule

F2 confirmation is not the entry trigger.

In the waist-break branch, F2 confirms only after Point 2 exists and price later re-breaks the F2 Leg2 endpoint. That endpoint is this setup's target. Waiting for confirmed F2 would therefore arm the trade after the target had already been reached.

## 8. Non-goals

This setup does not:

- infer Hook validity;
- wait for a Zone;
- use a CG filter;
- use an AI score;
- use F3 as an exit;
- chase a missed entry with a market order.

## 9. Relation to existing Canon

This setup reuses the already documented F2 waist-break grammar:

- `docs/flag_counting/FLAG_COUNTING_SEQUENCE_CONTRACT_V3.md` — `1 = F2 Waist`, `2 = node that breaks F2 Waist`;
- `docs/flag_counting/FLAG_COUNTING_STATE_MACHINE_V3.md` — waist-break branch remains valid while F2 Origin is preserved;
- `docs/zone_af/ZONE-AF-0008_F2_Waist_Hit_Point1_Point2_Doctrine.md` — waist contact becomes Point 1 and the following hit/extension becomes Point 2.

The new decision in this execution profile is the explicit direct risk contract:

```text
Stop authority = direct parent F1 Waist
Target authority = F2 Leg2 endpoint
```

This is a dedicated backtest authorization. It does not silently change the general Zone doctrine for other F2 contexts.
