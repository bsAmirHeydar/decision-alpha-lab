---
type: moc
domain: hook_lifecycle
status: active
---

# Hook Lifecycle MOC

## Core doctrine

- [[Hook Candidate vs Valid Hook]]
- [[Origin Breach Before Terminal Confirmation]]
- [[No Origin Survival, No Hook Zone]]
- [[Hook After Hook]]
- [[Hook After Opposing F3]]

## Implementation references

- [[Phase 32 — Raw Origin-Breach Lifecycle Guard]]
- `mql5/Include/FlagCountingPhoenix/FP_HookPhase02Rules.mqh`
- `mql5/Include/FlagCountingPhoenix/FP_HookPhase02Types.mqh`
- `mql5/Experts/FlagCounting/FlagCountingPhoenixExperiment.mq5`

## Trading interpretation

The Hook engine must not treat every fractal hook-like shape as a valid Hook.
A candidate first has to survive its origin boundary until the terminal node is
confirmed. If it does not, it is removed from production visualization and zone
logic.

## Related Alpha Lab concepts

- [[Zone as Risk Contract]]
- [[No Stop, No Direct Trade]]
- [[Fractal Noise Control]]
- [[Limit Entry Optionality]]
- [[Antifragile Loss Policy]]

## Runtime Redraw / Timeframe Change

- [[Runtime_Redraw_State]]
- [[Chart_Change_Must_Rebuild_Hook_View]]
- [[Phase_33_Timeframe_Change_Redraw_State_Guard]]
- [[Hook_Timeframe_Change_Debug_Checklist]]

## Phase 34 — Hook Sequence Partition

- [[Greedy_Hook_Sequence_Partition]]
- [[Consumed_Node_Cannot_Start_New_Hook_Sequence]]
- [[Phase_34_Hook_Sequence_Partition_Guard]]
- [[Hook_Sequence_Numbering_Debug_Checklist]]

