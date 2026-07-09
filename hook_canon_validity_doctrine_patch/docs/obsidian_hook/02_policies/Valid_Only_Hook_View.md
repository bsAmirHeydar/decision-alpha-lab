# Valid Only Hook View

## Policy

When valid-only Hook mode is enabled, the chart must show only valid Hook cycles and required parent companions.

## Visible families

```text
1. Hook After Opposing F3
2. Hook After Hook
3. Parent Companion Hook when needed for Hook-after-Hook
```

## Hidden objects

Everything else is hidden:

- raw structural Hooks;
- invalid Hook labels;
- invalid Hook nodes;
- invalid Hook cycles;
- structural fallback Hooks;
- stale Hook objects;
- unrelated debug overlays.

## Empty state

If no valid Hook exists, draw nothing.
