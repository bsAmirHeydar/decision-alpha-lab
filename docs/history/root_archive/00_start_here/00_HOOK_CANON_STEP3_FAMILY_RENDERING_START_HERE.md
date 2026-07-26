# HOOK CANON STEP 3 — Family Rendering Start Here

This patch implements **Step 3** of the canonical valid-Hook doctrine: **valid Hook family rendering**.

Step 1 selected the canonical visible set.
Step 2 annotated the valid Hook families.
Step 3 makes those families visually readable on the chart.

## Scope

This patch changes only Hook Phase 02 visualization:

- family-aware arc colors
- family-aware node/sequence label prefixes
- parent companion labels
- documentation and Obsidian notes

It does not change Hook sequence construction, Hook validity determination, F-counting logic, Rally logic, Zone logic, execution, risk sizing, broker behavior, or live trading behavior.

## Visible family tags

| Tag | Meaning |
|---|---|
| `F3H` | Hook After Opposing F3 |
| `HH` | Hook-2 After Hook-1 |
| `F3H+HH` | Hook that qualifies by both families |
| `PARENT` | Hook-1 shown only as parent companion of a valid Hook-after-Hook |

## Production intent

When valid-only mode is enabled, the chart should show only the valid cycle set and the node/sequence labels belonging to those cycles.

```text
InpHookPhase02ShowOnlyValidHooks = true
InpHookPhase02ValidOnlyFallbackToStructural = false
```

