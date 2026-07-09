# Parent Companion Hook

A Parent Companion Hook is the first Hook in a valid Hook-after-Hook pair.

## Rule

If Hook-2 is valid because it starts from the terminal/death-near endpoint of Hook-1, then Hook-1 must also be displayed.

```text
Hook-2 valid by Hook-after-Hook
=> show Hook-2
=> show Hook-1 as parent companion
```

## Important distinction

Hook-1 is not automatically promoted into an independently valid Hook. It is visible because Hook-2 structurally depends on it.

## Rendering

The parent companion is rendered with full detail:

- cycle arc;
- node labels;
- sequence labels;
- origin/crown/terminal structure.
