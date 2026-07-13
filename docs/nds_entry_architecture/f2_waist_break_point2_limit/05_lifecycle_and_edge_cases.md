# 05 — Lifecycle and Edge Cases

## Complete F2 is born while HTF gate is closed

Do not discard it because one bar passed. The setup remains a candidate while its structure is valid. When the HTF gate later opens, it may arm only if neither its final executable Entry nor original F2 Leg2 target has already been touched since the body became observable.

## F2 is confirmed before arming

Reject. F2 confirmation means the original Leg2 target has already been consumed.

## Entry was already crossed before order placement

Reject. Do not send a retrospective limit and do not chase with a market order.

## F2 is size-rejected

Fixed-F2 and HTF-F3 exit modes use only the explicit general input `InpF2BTRequireF2SizeGate`.

Local exact-F3 exit has a separate explicit dependency:

```text
InpF2BTRequireCanonicalF3SpawnForLocalExit = true
```

Without canonical source-F2 spawn authority, an exact local child F3 cannot own the exit. The dedicated input makes this unavoidable dependency visible instead of silently changing the general size-gate input.

## F2 Leg2 extends before entry

The old body version is consumed. The extension creates a new body identity and target. It may arm as a new context if all gates pass.

## F2 target and entry are touched in one modeled bar

The Strategy Tester tick model determines intrabar ordering. On the next closed-bar reconciliation, any still-existing pending whose target was consumed is cancelled.

## F1 waist does not produce valid stop geometry

Reject. No substitution with F1 Origin, F2 Origin, ATR, or a fixed stop is permitted.

## Pending cancelled by HTF policy

With consume-on-fill enabled, cancellation releases the active attempt. The F2 may re-arm later only if it remains valid and causally unconsumed.

## Pending cancelled externally, rejected, or expired

The transaction handler releases its active-attempt and dynamic-exit reservation when history confirms a non-filled terminal order state.

## One-attempt point

Default:

```text
InpF2BTConsumeAttemptOnlyOnFill = true
```

The setup is permanently consumed at the first entry deal, not at pending-order acceptance.

## Duplicate-looking F2 across scales

Distinct hashes are compared using final executable stop corridors. At or above the overlap threshold, only the wider same-direction setup survives. Opposite directions remain governed by hedge policy.

## Existing foreign position on the symbol

Block new managed setup creation to avoid ownership ambiguity.

## Netting account with parallel-context inputs enabled

With the default `InpF2BTRequireHedgingAccountForParallelContexts = true`, initialization fails. This prevents a netting test from masquerading as independent hedge/parallel-position execution.

## Reward/Risk below threshold

Keep Stop and F2 Leg2 fixed. Move Entry toward Stop until the configured minimum RR is reached. Reject only if the required limit is no longer structurally or broker-valid.

## Pending duration

Pending orders are GTC, but structural lifecycle can cancel them when:

- their own target is consumed;
- HTF authorization closes and cancellation is enabled;
- a wider overlapping pending replaces them;
- the broker/operator cancels, rejects, or expires them.

There is no arbitrary bar expiration by default.

## Opposite qualifying HTF directions

Fail closed. The engine does not guess between bullish and bearish qualifying counts.
