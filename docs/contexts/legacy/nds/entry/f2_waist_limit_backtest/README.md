# NDS F2 Waist Limit Backtest — Index

## Mechanical contract

```text
Fresh confirmed F2 becomes observable
→ bullish Buy Limit one tick below F2 waist
→ bearish Sell Limit one tick above F2 waist
→ Stop at canonical parent F1 waist
→ Take Profit at F2 Leg2 endpoint
→ no second pending order or position
```

## Runtime boundary

This executable is F-only. Hook scanning, Hook validity, Zone, AI, drawing, CSV, timer, chart events and production governance are not part of the tester path.

The implementation reuses the approved Phoenix node, F1 lifecycle, F2 lifecycle, parent-resolution, tick-normalization and risk-sizing modules. It replaces only the heavy orchestration path with an execution-only detector.

## Documents

- [Execution Contract](01_execution_contract.md)
- [Module Reuse Map](02_module_reuse_map.md)
- [State Machine](03_state_machine.md)
- [Price Semantics](04_price_semantics.md)
- [Performance Contract](05_performance_contract.md)
- [Validation Plan](06_validation_plan.md)
- [Operator Guide](07_operator_guide.md)
- [Fast Exact Runtime Hotfix](08_fast_exact_runtime_hotfix.md)
