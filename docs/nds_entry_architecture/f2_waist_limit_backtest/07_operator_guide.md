# F2 Waist Limit — Operator Guide

## Expert

```text
NDSF2WaistLimitBacktest
```

## Recommended first run

```text
InpF2BTProfile = FAST
InpF2BTTradeEnabled = true
InpF2BTSendTesterOrders = true
InpF2BTEntryOffsetTicks = 1
InpF2BTMaxSetupAgeBars = 0
InpF2BTOneAttemptPerF2 = true
InpF2BTResetUsedSetupsOnInit = true
InpF2BTFixedVolume = 0.01
```

There is intentionally no custom startup or per-bar print. Trade acceptance and execution remain visible through the Strategy Tester’s native Deals, Orders, Results and Journal records.

Use `PARITY` only after FAST behavior is verified.
