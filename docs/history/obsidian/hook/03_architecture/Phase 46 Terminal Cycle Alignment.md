# Phase 46 Terminal Cycle Alignment

Phase 46 implements the canonical split between structural terminal and visual terminal.

The raw terminal scanner now receives the origin boundary and stops at the first boundary touch/cross. This prevents cycle arcs from extending past the Hook death line.

## Implementation anchor

```text
mql5/Include/FlagCountingPhoenix/FP_HookPhase02Rules.mqh
```

Key functions:

```text
FP_HookP02RawTerminalCandidateInsideOriginBoundary
FP_HookP02FindRawTerminalPriceExtreme
FP_HookP02PromoteRawPriceTerminalIfMoreExtreme
```
