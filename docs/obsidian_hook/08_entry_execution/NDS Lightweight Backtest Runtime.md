---
type: architecture
system: NDS
phase: 53
status: implemented
---

# NDS Lightweight Backtest Runtime

## Purpose

Run the current executable NDS contract without the production visual/audit stack.

## Pipeline

```text
Closed bars
→ F detector
→ Hook ownership core
→ F3H / HH limit entry
→ single exposure
→ same-direction F123 exit
```

## Executable

`mql5/Experts/FlagCounting/NDSHookLimitF123Backtest.mq5`

## Related

- [[NDS Backtest Performance Profiles]]
- [[NDS Backtest Parity Contract]]
- [[NDS Hook Limit Entry Contract]]
- [[NDS Same Direction F123 Exit]]
- [[NDS Single Exposure Lock]]
