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

## Duplicate-looking F2 across scales

Each scale/body version receives its own deterministic context hash, but hash difference alone is not sufficient for parallel execution. Same-direction setups are compared by their final executable stop corridors.

If the overlap percentage is at or above the configured threshold, they are one practical opportunity and only the wider corridor is kept. Below the threshold, they remain independent contexts and may coexist when the parallel-context policy allows it. Opposite-direction hedge contexts are not merged by this rule.

## Existing foreign position on the symbol

Block the setup to prevent ownership ambiguity.

## Netting account with parallel-context inputs enabled

The first context may trade. A second same-symbol context is blocked because MT5 would merge or net its position and destroy independent SL/TP ownership.

## Reward/Risk below threshold

With the default repricing switch enabled, keep the structural Stop and Target fixed and move the limit farther behind the F2 Waist toward the Stop until normalized RR reaches the configured minimum. If the required limit is not broker-valid, reject.

With repricing disabled, retain the previous behavior and reject the setup.

## Pending duration

The pending is GTC but is structurally cancelled when its target is consumed before fill. No arbitrary bar expiration is added in this contract.

## Wider context appears after narrower pending

If both are same-direction and their stop-corridor overlap meets the threshold, remove the narrower pending and submit the wider context. Equal widths keep the existing pending to prevent churn.

## Wider context appears after overlapping position has filled

Do not close or replace the live position. The already-filled position owns the opportunity and the new overlapping context is blocked.
