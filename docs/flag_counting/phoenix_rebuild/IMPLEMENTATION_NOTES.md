# Phoenix Implementation Notes

## Module boundaries

`FP_NodeEngine` owns node extraction. No sequence code should inspect raw candle open/close/body.

`FP_HookEngine` owns hook/ND branches and F1 phase-boundary origins.

`FP_FlagBodyEngine` owns the invariant two-leg body.

`FP_InternalCountEngine` owns post-flag 1/2/3/4 counting.

`FP_SequenceEngine` owns F1 -> F2 -> F3 state transitions and parent-child ownership.

`FP_Renderer` owns only drawing.

`FP_Audit` owns diagnostic logs.

## Deliberate fail-open setting

Phoenix defaults to:

```text
InpRequireF1PhaseBoundary = true
InpAllowF1FailOpenWhenNoHook = true
```

This is deliberate. It keeps the chart inspectable while Hook/ND coverage is being verified. Once Hook/ND boundary coverage is strong, fail-open can be disabled.

## Known engineering tradeoffs

The current HookEngine builds readable 3/4-node alternating branches at each L. It is explicitly isolated so the branch algorithm can be upgraded without touching the sequence engine.

The current InternalCountEngine keeps one strict adverse-side branch per event. It is also isolated so multi-branch 1/2 counting can be expanded in one module without rewriting F1/F2/F3 orchestration.
