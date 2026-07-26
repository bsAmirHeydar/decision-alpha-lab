# Valid Only Leakage Debug Checklist

When `InpHookPhase02ShowOnlyValidHooks = true`:

- Raw Hook candidates should not draw.
- Phase01 raw nodes should not draw.
- Phase03-06 diagnostic Hook overlays should not draw.
- Same-origin sibling branches should not draw unless they are independently valid or required parent companions.
- Structural fallback should be off for production.
- If no valid Hook exists, the chart may show no Hook objects.
