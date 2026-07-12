# 05 — Lifecycle and Edge Cases

## F2 is confirmed before arming

Reject. Confirmation means the F2 Leg2 endpoint has already been re-broken after an internal or waist-break branch. That endpoint is the setup target.

## F2 is size-rejected

The setup contract itself does not require the F2/F1 size gate. The input `InpF2BTRequireF2SizeGate` can enable it for controlled research. Default is `false` to avoid adding an unstated filter.

## F2 Leg2 extends before entry

The previous target is consumed, so the old pending is cancelled. The canonical extension becomes a new F2 body version with a new Leg2 target and may arm again.

## F2 target and entry are touched in one modeled bar

The Strategy Tester order engine determines the intrabar order according to the selected tick model. At the next closed bar, target-consumption cancellation is applied only if the pending order still exists. If the order filled and closed, no pending remains.

## F1 waist does not produce valid stop geometry

Reject the setup. No fallback to F1 origin, F2 origin, ATR or fixed stop is allowed.

## Duplicate F2 across scales

The freshest observable body wins. Ties prefer the later Leg2, then the later origin, then the smaller scale L. Only one order can exist.

## Existing foreign position on the symbol

Block the setup to prevent netting-account contamination.

## Pending duration

The pending is GTC but is structurally cancelled when its target is consumed before fill. No arbitrary bar expiration is added in this contract.
