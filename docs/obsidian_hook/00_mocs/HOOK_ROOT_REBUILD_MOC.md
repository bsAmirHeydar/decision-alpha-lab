# Hook Root Rebuild MOC

## Core notes

- [[Seed-Owned Hook Sequence]]
- [[Consumed Node Cannot Restart As One]]
- [[Valid Hook Families]]
- [[Phase 34 Seed-Owned Hook Sequence Builder]]
- [[Hook Sequence Debug Checklist]]

## Canonical code files

```text
mql5/Include/FlagCountingPhoenix/FP_HookPhase02Rules.mqh
mql5/Include/FlagCountingPhoenix/FP_HookPhase02Types.mqh
mql5/Include/FlagCountingPhoenix/FP_HookPhase02Engine.mqh
mql5/Include/FlagCountingPhoenix/FP_HookPhase02Visual.mqh
mql5/Include/FlagCountingPhoenix/FP_HookPhase02Export.mqh
mql5/Experts/FlagCounting/FlagCountingPhoenixExperiment.mq5
```

## Canonical doctrine

Hook sequence counting is not unrestricted branch enumeration in the production view. It is seed-owned old-to-new strict extension.
