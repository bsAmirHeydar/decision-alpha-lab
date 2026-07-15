# 13 — Operator Runbook

## Paper/research activation

1. Install the patch and run the provided Python/static QA suite.
2. Compile central and lightweight tester experts in the supported MetaEditor build.
3. Select `HOOK_864_CYCLE_R1` in the tester.
4. Keep exact values: ratio 0.864, min X 3, max X 4, confirmed Terminal true, untouched true, reward 1.0.
5. Select fixed-volume or risk-cash sizing deliberately.
6. Reset the used-setup registry only for a clean controlled test run.
7. Review ledger rows for canonical sequence lineage and first-arrival status.

## Central EA paper mode

```text
InpNDSHookTradeEnabled = true
InpNDSHookTradeSendLiveOrders = false
InpNDSHookTradeProfile = HOOK_864_CYCLE_R1
```

Paper mode records a decision and consumes the one-attempt identity. It does not submit an order.

## Broker-demo mode

Only after compile/test approval:

```text
InpNDSHookTradeEnabled = true
InpNDSHookTradeSendLiveOrders = true
```

Verify account, symbol, magic, volume/risk, stop buffer, spread multiplier, broker stops/freeze levels, and SL/TP support. Start with one chart and a dedicated demo account/magic.

## Monitoring

Watch status/reason, managed pending/positions, sequence ID, x_count, Terminal retracement, Entry/Stop/Target, setup key, and ledger write. A pending order should not move when the Hook extends from x3 to x4.

## Incident response

Disable send authority, preserve Experts/Journal and ledger files, record broker orders/deals/positions, and do not reset the used registry until reconciliation is complete. Missing protection, duplicate exposure, or ownership ambiguity requires manual review rather than automatic recovery.
