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

## 4. Risk and exit authority

```text
Entry = behind F2 Waist
Stop  = behind direct parent F1 Waist
```

Exit is selected by input:

```text
Fixed mode:
TP = F2 Leg2 endpoint / end of F2 two-leg flag

F3 retest mode:
RR reference = original F2 Leg2
initial broker TP = none
dynamic TP = F2 confirmation node / canonical F3 Leg1 after correction
```

For bullish F2:

```text
Stop < Entry < Target
```

For bearish F2:

```text
Target < Entry < Stop
```

## 5. Reward/Risk entry repricing

After structural Entry, Stop and Target are normalized:

```text
RR = abs(Target - Entry) / abs(Entry - Stop)
```

The default minimum is `1.0`. If the structural limit behind the F2 Waist is below the configured minimum, the setup is not rejected immediately. The Stop and Target remain fixed, while the pending Entry is moved farther behind the F2 Waist—toward the F1-waist Stop—until the executable tick-normalized geometry provides at least the requested RR.

The exact boundary is:

```text
Required Entry = (Target + MinimumRR × Stop) / (1 + MinimumRR)
```

For bullish setups the price is rounded down; for bearish setups it is rounded up. This rounding is toward the Stop and therefore cannot reduce RR below the request. If the adjusted price is not a valid pending limit or violates broker distance rules, the setup is rejected.

## 6. Parallel context and near-duplicate policy

A distinct F2 body version is a distinct context. By default:

```text
same-direction contexts = allowed
opposite-direction hedge contexts = allowed
```

However, different hashes do not automatically authorize two nearly identical same-direction trades. The executable stop corridor of each setup is the interval between its final Entry and Stop. If the intersection covers at least the configured percentage of the narrower corridor, the contexts are treated as one opportunity and only the wider corridor survives.

Default:

```text
Stop-space overlap threshold = 80%
Winner = wider executable stop corridor
```

The percentage is an input and may be changed to `70`, `80`, or another controlled value. Opposite-direction contexts are not deduplicated by this rule because they belong to the explicit hedge policy. The same exact context remains one-attempt-only. Independent same-symbol positions require an MT5 hedging account.

## 7. Critical timing rule

F2 confirmation is not the entry trigger.

In the waist-break branch, F2 confirms only after Point 2 exists and price later re-breaks the F2 Leg2 endpoint. That endpoint is this setup's target. Waiting for confirmed F2 would therefore arm the trade after the target had already been reached.

## 8. Higher-timeframe directional authorization

By default, a new lower-timeframe setup must agree with the current canonical H1 F phase:

```text
H1 bullish F → Buy setups only
H1 bearish F → Sell setups only
H1 Hook/ND, ambiguous or unavailable → no new setup
```

This gate uses closed H1 bars and the canonical Phoenix F/Hook architecture. It does not alter the structural Entry, Stop, Target, RR or overlap formulas. It is entry authorization only. Managed pending orders that cease to match the gate are cancelled by default; open positions remain under their original exit contract.

## 9. Non-goals

This setup does not:

- infer Hook validity;
- wait for a Zone;
- use a CG filter;
- use an AI score;
- chase a missed entry with a market order.

## 10. Relation to existing Canon

This setup reuses the already documented F2 waist-break grammar:

- `docs/flag_counting/FLAG_COUNTING_SEQUENCE_CONTRACT_V3.md` — `1 = F2 Waist`, `2 = node that breaks F2 Waist`;
- `docs/flag_counting/FLAG_COUNTING_STATE_MACHINE_V3.md` — waist-break branch remains valid while F2 Origin is preserved;
- `docs/zone_af/ZONE-AF-0008_F2_Waist_Hit_Point1_Point2_Doctrine.md` — waist contact becomes Point 1 and the following hit/extension becomes Point 2.

The new decision in this execution profile is the explicit direct risk contract:

```text
Stop authority = direct parent F1 Waist
RR-reference authority = original F2 Leg2 endpoint
Fixed-exit authority = original F2 Leg2 endpoint
Dynamic-exit authority = F2 confirmation node / F3 Leg1 after correction
```

This is a dedicated backtest authorization. It does not silently change the general Zone doctrine for other F2 contexts.
