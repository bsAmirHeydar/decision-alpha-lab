# Phase 52 NDS Hook Limit F123 Execution

## Pipeline

```text
valid HH/F3H Hook
→ limit at Hook terminal
→ one global managed exposure
→ full same-direction F1-F2-F3 after fill
→ verified market close
```

## Implementation

- `FP_NDSHookTradeTypes.mqh`
- `FP_NDSHookTradeRules.mqh`
- `FP_NDSHookTradeExport.mqh`
- `FP_NDSHookTradeEngine.mqh`
- central EA version `18.40`

## Safety

Both the strategy-enable switch and broker-send switch default to false. The Phase 51 generic NDS command preview remains zero-volume and no-send; Phase 52 is a separate narrow opt-in execution profile.

## Related

- [[../00_mocs/NDS_ENTRY_EXECUTION_MOC]]
- [[../08_entry_execution/NDS Hook Limit Entry Contract]]
- [[../08_entry_execution/NDS Single Exposure Lock]]
- [[../08_entry_execution/NDS Same Direction F123 Exit]]
- [[../08_entry_execution/NDS Hook Trade State Machine]]
