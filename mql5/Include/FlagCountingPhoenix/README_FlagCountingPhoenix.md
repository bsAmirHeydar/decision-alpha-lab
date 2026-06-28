# FlagCounting Phoenix

Phoenix is a clean rebuild of the Flag Counting engine. It intentionally does not include, reuse, or depend on any earlier `FlagCounting`, `FlagCountingVNext`, or `FlagCountingV6` implementation.

## Core principles

1. Node logic is copied conceptually from the original project rule: a node is a candle high/low level that has at least `L` candles on both sides that do not reach that price.
2. Equality is not a break. Equal highs/lows form one plateau node.
3. Open, close, candle body, and candle color are ignored by the structural logic.
4. A flag body is always `Origin -> Leg1 -> Waist -> Leg2`.
5. F1, F2, and F3 share the same two-leg body shape; they differ in post-flag semantics.
6. F2 and F3 use backfilled origins from the deepest adverse correction after their parent flag.
7. Hook/ND is rendered and exposed as a first-class structure.
8. Renderer is non-authoritative. It draws only engine-emitted structures.

## Files

- `FP_Types.mqh`: model types and contract helpers.
- `FP_NodeEngine.mqh`: L-based high/low node extraction with plateau handling.
- `FP_HookEngine.mqh`: branch-based ND/hook detection.
- `FP_FlagBodyEngine.mqh`: two-leg flag body construction.
- `FP_InternalCountEngine.mqh`: internal 1/2/3/4 and post-flag correction scanning.
- `FP_SequenceEngine.mqh`: F1 -> F2 -> F3 orchestration.
- `FP_Renderer.mqh`: chart drawing.
- `FP_Audit.mqh`: logs and diagnostics.

## Expert

Compile:

```text
mql5/Experts/FlagCounting/FlagCountingPhoenixExperiment.mq5
```

## Recommended first run

Keep the initial settings inspectable rather than over-strict:

```text
InpRequireF1PhaseBoundary = true
InpAllowF1FailOpenWhenNoHook = true
InpEnforceSingleChainPerDirectionScale = false
InpEnforceSingleChainPerDirectionGlobal = false
InpDrawHooks = true
InpDetailedLabels = true
InpShowParentIds = true
```

After Hook/ND coverage is verified, you can tighten:

```text
InpAllowF1FailOpenWhenNoHook = false
InpEnforceSingleChainPerDirectionScale = true
InpEnforceSingleChainPerDirectionGlobal = true
```

## Phoenix semantic cleanup patch

This patch tightens the Phoenix engine without returning to the failed hard-gate behavior.
The main fixes are:

- pre-internal favorable breaks are absorbed into the current Leg2 instead of creating a new F1;
- same-direction restarts are guarded by default both per scale and globally, while fail-open remains available so the chart does not go empty;
- fail-open F1 roots are hidden when they are inside a readable hook-owned phase root;
- hook rendering is compacted by keeping the best 3/4-node branch per resolve node;
- superseded non-confirmed parent states are hidden when a visible child already represents the active chain state;
- parent labels are rebuilt after sorting and pruning so visual ownership remains auditable.

New inputs:

- `InpAbsorbPreInternalExtensions`
- `InpHideSupersededParentStates`
- `InpCompactHookRendering`

Recommended semantic-view defaults keep all three enabled.

## Hook / ND branch-sequence repair

The Hook engine now follows the branch-sequence contract:

- Hook / ND is not detected from arbitrary alternating 3/4-node windows.
- Bullish hook contexts count same-side LOW nodes.
- Bearish hook contexts count same-side HIGH nodes.
- Counted branches must be strict adverse staircases.
- Only branches with exactly three or four counted same-side nodes can become ND.
- Runs with more than four counted same-side nodes are skipped at the current L and are expected to appear in a higher-L compressed view.
- Opposite-side nodes remain available for cycle extreme detection and gray arc rendering, but they are not counted as internal hook numbers.
- Chart labels now use cluster-based stacking so dense text appears in deterministic lanes instead of overlapping randomly.

## Readable stacked labels patch

The Phoenix renderer now uses viewport-aware label spacing and deterministic time-price clusters for all main labels, origin labels, internal 1/2/3/4 labels, and Hook/ND labels. Nearby labels are assigned to the same vertical column and stacked with fixed price-space lanes so chart text remains readable instead of overlapping. Peaks stack above price; valleys stack below price. Older labels keep the closest lane and newer labels are pushed farther away from the same local structure.

