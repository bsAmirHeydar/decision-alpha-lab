# Phase 52 — NDS Hook Limit Entry and F123 Exit

Phase 52 turns two already-valid Hook families into a narrow execution profile:

```text
HH / F3H / F3H+HH
→ pending limit at raw Hook terminal
→ stop beyond death/origin
→ one magic-wide exposure
→ close on full same-direction post-entry F123
```

## Source authority

Only `valid_after_hook` and `valid_after_opposing_f3` sequences are eligible. Parent companions and generic Hook candidates remain non-tradable.

## Single exposure

Broker ownership is magic-only. A terminal compare-and-swap lock plus a second broker-state check prevents multi-chart double submission. Duplicate pending orders are reconciled; multiple positions cause fail-closed operator escalation.

## Exit authority

The position can close only when an explicit visible F1 and F2 in the same sequence authorize a completed or locked same-direction F3. Strict mode requires F1 and F2 to start after the broker position open time.

## Safety defaults

```text
InpNDSHookTradeEnabled = false
InpNDSHookTradeSendLiveOrders = false
```

The prior Phase 51 NDS pipeline remains no-send and separate.

## Detailed package

`docs/contexts/legacy/nds/entry/phase52_hook_limit_f123_execution/`
