# Hook Validity No-Draw Checklist

Recommended practical settings:

```text
InpHookPhase02ShowOnlyValidHooks = true
InpHookPhase02ValidOnlyFallbackToStructural = true
InpHookPhase02ValidF3RequireOppositeDirection = false
InpHookPhase02ValidOnlyRequireNearDeath = false
InpHookPhase02ValidF3RequireSameScale = false
```

If nothing draws, enable:

```text
InpHookPhase02ExportCsv = true
InpHookPhase02PrintSummary = true
```

Check:

- `valid_after_hook`
- `valid_after_opposing_f3`
- `valid_hook_family`
- `invalid_family_filtered`
