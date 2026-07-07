# Hook Validity No-Draw Failsafe Patch

This patch fixes the practical-valid Hook view when `ShowOnlyValidHooks=true` produces an empty chart.

It separates three layers:

1. **Hook counting** remains complete.
2. **Hook validity annotation** remains practical and configurable.
3. **Production view** is allowed to fall back to structural Hook candidates when no valid family is selected, so the chart is never blind while tuning validity rules.

Primary inputs:

```text
InpHookPhase02ShowOnlyValidHooks = true
InpHookPhase02ValidOnlyFallbackToStructural = true
InpHookPhase02ValidF3RequireOppositeDirection = false
InpHookPhase02ValidOnlyRequireNearDeath = false
InpHookPhase02ValidF3RequireSameScale = false
```

For strict research, set:

```text
InpHookPhase02ValidOnlyFallbackToStructural = false
InpHookPhase02ValidF3RequireOppositeDirection = true
```
