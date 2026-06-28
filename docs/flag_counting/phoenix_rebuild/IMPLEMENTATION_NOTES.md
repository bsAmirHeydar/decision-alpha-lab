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

## Semantic cleanup notes

The Phoenix cleanup pass fixes the main remaining failure mode observed on chart review: the engine was still over-producing F1 structures inside directional continuation. The core rule is now explicit in code: if a completed flag end is crossed again before a valid post-flag internal 1/2 exists, that cross is absorbed as a Leg2 extension of the same flag body. It is not confirmation and it is not a new root F1.

The semantic chart view now also prefers phase-owned structures over fail-open structures. Fail-open remains enabled by default for inspection so the chart does not become empty while Hook/ND coverage is being audited, but fail-open roots are hidden when a real hook/ND phase root already owns the same region.

Hook rendering has also been compacted. The hook engine may still audit multiple theoretical branches, but the main render keeps the strongest branch per resolve node. This preserves ND visibility while reducing the raw sliding-window look.

## Hook / ND branch-sequence code repair

The Phoenix hook engine now follows the dedicated Hook / ND branch-sequence contract rather than the older alternating sliding-window approximation.

Changes:

- removed blind alternating 3/4-node window hook construction;
- added same-side counted-node branch extraction;
- low-side hooks count only LOW nodes and high-side hooks count only HIGH nodes;
- opposite nodes are used only for cycle extreme and arc geometry;
- branches require strict adverse progression from older counted node to newer counted node;
- branch length 1 or 2 is developing and not ND;
- branch length 3 or 4 can become ND when cycle retracement passes the configured threshold;
- branch length above 4 is rejected at the current L so a higher-L compressed view must represent it;
- hook labels now expose the counted branch length using `ND Lx #n`;
- renderer label placement now uses a deterministic cluster stacker instead of event-id modulo lanes.
