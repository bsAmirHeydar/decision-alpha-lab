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

## Readable stacked labels patch

The Phoenix renderer now uses viewport-aware label spacing and deterministic time-price clusters for all main labels, origin labels, internal 1/2/3/4 labels, and Hook/ND labels. Nearby labels are assigned to the same vertical column and stacked with fixed price-space lanes so chart text remains readable instead of overlapping. Peaks stack above price; valleys stack below price. Older labels keep the closest lane and newer labels are pushed farther away from the same local structure.


## Renderer Patch: Candle-Index Arc Sampling

Phoenix flag curves and Hook/ND arcs are now sampled on candle indexes rather than interpolated timestamps.  The previous renderer shaped quadratic arcs directly in datetime space.  On instruments with session gaps or irregular chart time spacing, interpolated datetimes may land between real candles, which can visually distort the curve or create dirty broken-looking trendline chains.

The renderer now passes the copied `MqlRates` array into `FP_DrawAll`, then into the curve drawing helpers.  Each sampled curve point chooses a real candle index between the start node and the finish node, converts that index back to `rates[index].time`, and draws the segment between actual bar timestamps only.  The price curve remains quadratic through the waist/control node, but the x-domain is candle-index space.

This is a rendering-only change.  It does not modify node extraction, Hook/ND detection, F1/F2/F3 sequencing, internal counting, or ownership logic.

## Phoenix Hook/ND Display Repair — Cycle Boundary Without Downstream Origin Mutation

This repair fixes the chart state where Hook/ND context could visually dominate the chart and make the output look mostly gray.

The key distinction is now explicit:

- `start_node` remains the first counted same-side branch node. This is the semantic branch start used by downstream F1 phase-boundary logic.
- `cycle_start_node` is the true visual Hook cycle boundary. The gray Hook/ND arc starts from this node and closes at the branch resolve node through the favorable cycle extreme.

For a bullish low-side Hook, `cycle_start_node` is the nearest older LOW that is strictly below the final counted LOW. For a bearish high-side Hook, it is the nearest older HIGH that is strictly above the final counted HIGH. Equality is not a break.

The Hook cycle start must hold until the Hook closes. A bullish Hook is rejected if a later LOW strictly breaks below the cycle start before resolve. A bearish Hook is rejected if a later HIGH strictly breaks above the cycle start before resolve.

The renderer uses `cycle_start_node` only for the gray Hook/ND arc. It does not use the cycle boundary as the F1 semantic origin. This prevents the previous failure mode where fixing the arc start changed downstream sequence ownership and damaged the colored F structures.

Hook rendering is also compacted across scales at the same resolve node. If L2, L3, L5, and L8 all resolve at the same structural node, the main chart keeps the strongest branch instead of drawing every gray duplicate. The engine still scans all scales; this is a main-chart readability rule.

Gray Hook/ND arcs are drawn in the background so they cannot visually overwrite colored F1/F2/F3 structures.
