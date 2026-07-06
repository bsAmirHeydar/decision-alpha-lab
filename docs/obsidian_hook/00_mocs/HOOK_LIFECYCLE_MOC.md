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
