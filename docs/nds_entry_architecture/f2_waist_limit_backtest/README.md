# NDS F2 Waist Limit Backtest — Index

## Purpose

This package defines a separate, minimal Strategy Tester executable for one mechanical entry contract:

```text
Confirmed canonical F2
→ limit beyond the F2 waist
→ stop at the canonical parent F1 waist
→ take profit at the canonical F2 Leg2 endpoint
→ one managed pending order or position at a time
```

## Important boundary

Hook is **not** an entry condition. Hook validity, Hook-after-Hook, Hook-after-F3, Zone and AI are not loaded as decision layers.

The existing Phoenix sequence detector may still scan internal Hook branches because the current canonical F1 detector uses approved phase boundaries to seed F1. This is detector infrastructure reuse, not Hook-based trade authorization.

## Documents

- [Execution Contract](01_execution_contract.md)
- [Module Reuse Map](02_module_reuse_map.md)
- [State Machine](03_state_machine.md)
- [Price Semantics](04_price_semantics.md)
- [Performance Contract](05_performance_contract.md)
- [Validation Plan](06_validation_plan.md)
- [Operator Guide](07_operator_guide.md)
