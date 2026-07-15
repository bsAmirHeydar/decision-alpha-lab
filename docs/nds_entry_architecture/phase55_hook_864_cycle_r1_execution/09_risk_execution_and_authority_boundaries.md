# 09 — Risk, Execution, and Authority Boundaries

## Independent authority gates

The central EA requires:

```text
InpNDSHookTradeEnabled = true
InpNDSHookTradeSendLiveOrders = true
```

The first allows setup evaluation; the second allows broker submission. Both default false. Choosing the profile does not imply either authority.

## Sizing

Phase 55 reuses the existing sizing modes:

- fixed normalized volume;
- risk-cash sizing through `DAL_ExecCalculateRiskVolume` including optional round-turn commission.

The setup adapter does not invent portfolio capital, leverage, or risk budgets.

## Broker checks

Before send, existing code checks:

- terminal trade permission;
- MQL trade permission;
- account trade permission;
- symbol trade mode and direction restrictions;
- limit-order support;
- stop-loss support;
- take-profit support for Phase 55;
- symbol fill mode;
- synchronous retcode acceptance.

## Exposure boundary

Only one managed pending or position is allowed globally for the configured magic. A foreign position on the same symbol blocks entry to avoid netting/ownership ambiguity.

## Comment boundary

Broker comments are diagnostic. Ownership is symbol/magic/ticket based and never depends on mutable/truncated comments.

## Evidence boundary

Static Python tests and source QA cannot grant broker authority. MetaEditor compile, Strategy Tester, demo broker, spread/stop-level, restart, fill, SL/TP, and ledger evidence remain separate acceptance gates.
