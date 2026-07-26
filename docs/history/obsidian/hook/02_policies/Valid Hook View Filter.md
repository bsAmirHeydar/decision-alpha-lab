# Valid Hook View Filter

## Rule

In production mode, show only valid Hook families:

- [[Hook After Opposing F3]]
- [[Hook After Hook]]

## Companion Exception

When the visible valid Hook is a second Hook in a Hook-after-Hook chain, show the first Hook as well.

```text
Hook-1 terminal = Hook-2 origin
```

Hook-2 is the valid Hook. Hook-1 is only displayed as the required parent companion.

## Hidden

- unqualified Hook candidates
- standalone Hook candidates
- hook-like fractal noise
- first Hooks without a valid second Hook

## Input

```text
InpHookPhase02ShowOnlyValidHooks = true
```
