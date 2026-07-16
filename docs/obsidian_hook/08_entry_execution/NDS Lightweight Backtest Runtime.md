---
type: architecture
system: NDS
phase: 55
status: implemented
---

# NDS Lightweight Backtest Runtime

## Purpose

Run the current executable NDS contract without the production visual/audit stack.

## Pipeline

```text
Broker exposure preflight
→ canonical closed bars and full configured scales
→ Hook ownership core
→ demand-driven F context when eligibility requires it
→ candidate-scoped Phase03/04 for Hook 86.4
→ existing trade execution core
```

## Executable

`mql5/Experts/FlagCounting/NDSHookLimitF123Backtest.mq5`

## Related

- [[NDS Backtest Performance Profiles]]
- [[NDS Backtest Parity Contract]]
- [[NDS Hook Limit Entry Contract]]
- [[NDS Same Direction F123 Exit]]
- [[NDS Single Exposure Lock]]
- [[NDS Hook 86.4 Exact Acceleration]]
