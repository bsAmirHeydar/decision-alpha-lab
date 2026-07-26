# 13 — Operator Runbook

## Paper/research activation

1. Install the patch and run the provided Python/static QA suite.
2. Compile central and lightweight tester experts in the supported MetaEditor build.
3. Use `NDSHookLimitF123Backtest`; verify the actual tester input `InpBTTradeProfile=HOOK_864_CYCLE_R1`.
4. Use `InpBTProfile=PARITY` for diagnosis and keep run-summary output enabled.
5. Keep exact values: ratio 0.864, closure ratio 0.50, min X 3, max X 4, confirmed Terminal true, Phase04 X closed true, untouched-after-closure true, reward 1.0.
6. Select fixed-volume or risk-cash sizing deliberately.
7. Reset the used-setup registry only for a clean controlled test run.
8. Review the run funnel first, then ledger rows for canonical sequence lineage and first-arrival status.

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

Watch status/reason, the full candidate funnel, Phase03/04 record counts, closure time, first-touch time, managed pending/positions, sequence ID, x_count, Entry/Stop/Target, setup key, and ledger write. Terminal retracement is audit-only for this first-arrival rule. A pending order should not move when the Hook extends from x3 to x4.

## Incident response

Disable send authority, preserve Experts/Journal and ledger files, record broker orders/deals/positions, and do not reset the used registry until reconciliation is complete. Missing protection, duplicate exposure, or ownership ambiguity requires manual review rather than automatic recovery.


## Zero-trade triage

Read `dominant_blocker` before changing any input. Follow [[NDS Hook 86.4 No Trade Diagnostic Funnel]]. A `ready_candidate_exists` funnel with zero sends means the setup exists and a downstream authority, exposure, broker-distance, volume, margin or session gate blocked it.


## Saved Journal analyzer

```powershell
python .\tools\flag_counting\analyze_nds_hook_864_tester_log.py .\path\to\tester.log
```

The analyzer reports wrong profile/defaults, the latest funnel blocker, and whether a structurally ready setup was stopped by downstream execution gates.
