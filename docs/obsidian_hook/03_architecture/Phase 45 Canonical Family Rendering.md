# Phase 45 — Canonical Family Rendering

Phase 45 decorates the canonical valid visible set with family-aware labels and colors.

Pipeline:

```text
Phase 02 sequences
→ validity fields
→ canonical visible-set indexes
→ family tag/color
→ arc + node labels + sequence labels
```

The renderer does not decide validity. It reads validity fields and companion relations already present on the selected set.

## Rendering classes

- `F3H`
- `HH`
- `F3H+HH`
- `PARENT`

## Code file

```text
mql5/Include/FlagCountingPhoenix/FP_HookPhase02Visual.mqh
```

