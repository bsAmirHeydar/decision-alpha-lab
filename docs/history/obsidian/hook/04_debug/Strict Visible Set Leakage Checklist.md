# Strict Visible Set Leakage Checklist

Use this checklist when the chart still looks crowded in valid-only mode.

## Input sanity

```text
InpHookPhase02ShowOnlyValidHooks = true
InpHookPhase02ValidOnlyFallbackToStructural = false
InpHookPhase02RequireConfirmedResolveNode = true
InpHookPhase02ValidF3RequireOppositeDirection = true
```

## Expected labels

Only these prefixes should appear:

```text
F3H
HH
PARENT
F3H+HH
```

## Failure signs

- Labels without a family prefix appear.
- Many same-origin siblings appear after one valid Hook.
- Old structural sequences appear far away from valid cycles.
- Cycle arc extends to an unconfirmed wick instead of a confirmed node.

## Likely cause

- same-origin expansion reintroduced;
- structural fallback enabled;
- another renderer prefix not cleaned;
- raw terminal promotion reintroduced.
