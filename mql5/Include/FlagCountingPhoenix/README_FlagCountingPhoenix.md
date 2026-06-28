# FlagCounting Phoenix

## Current canon

Phoenix must be implemented and audited from:

```text
docs/flag_counting/FLAG_COUNTING_CURRENT_CANON.md
```

That file is the source of truth. This README is an implementation index only.

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

Level 01 foundation:

- `FP_BarSnapshot.mqh`: per-bar diagnostic snapshot and OHLC sanity helper.
- `FP_TimebaseTypes.mqh`: canonical candle-stream config/report structs.
- `FP_SeriesContract.mqh`: validates ascending non-series closed-bar arrays.
- `FP_Timebase.mqh`: the only Phoenix `CopyRates` gateway. It returns canonical bars.

Structural / sequence engines:

- `FP_Types.mqh`: model types and contract helpers.
- `FP_NodeEngine.mqh`: L-based high/low node extraction with plateau handling.
- `FP_HookEngine.mqh`: branch-based ND/hook detection.
- `FP_FlagBodyEngine.mqh`: two-leg flag body construction.
- `FP_InternalCountEngine.mqh`: internal 1/2/3/4 and post-flag correction scanning.
- `FP_SequenceEngine.mqh`: F1 -> F2 -> F3 orchestration.
- `FP_Renderer.mqh`: chart drawing.
- `FP_Audit.mqh`: logs and diagnostics.


## Level 01 candle stream

Phoenix now routes terminal history through `FP_LoadCanonicalRates` before any structural engine runs. The default contract is:

```text
InpUseClosedBarsOnly = true
InpStrictTimebase = true
InpMinClosedBars = 200
InpPrintTimebaseSanity = true
```

`InpBarsToScan` means requested closed bars in this mode. The loader copies one extra raw bar, removes the current forming live candle, validates ascending non-series order, and prints an `FP_LEVEL01` sanity line.

Canonical convention:

```text
rates[0] = oldest closed bar
rates[ArraySize(rates)-1] = newest closed bar
newer bars have higher indices
```

Higher Phoenix modules must not call `CopyRates` directly. They consume the canonical array passed by the EA.

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


### Candle-index curve rendering

The Phoenix renderer samples flag-body and Hook/ND arcs by candle index, then converts each sampled index to an actual `rates[index].time`.  This avoids distorted curves caused by market time gaps or interpolated timestamps that do not correspond to real bars.

### Hook/ND cycle-boundary display repair

Hook branches now carry two different starts:

- `start_node`: first counted same-side branch node, preserved for branch identity and F1 phase-boundary logic.
- `cycle_start_node`: true visual cycle boundary used only for gray Hook/ND arc rendering and retracement measurement.

This prevents Hook arc cleanup from mutating F-sequence ownership. Hook/ND arcs start at the real cycle boundary, close at the resolve node, and are drawn behind colored F structures. Same-resolve Hook duplicates across L-scales are compacted for the main chart when compact Hook rendering is enabled.

## Root repair note - bounded Hook contexts and F visibility

The Phoenix Hook engine now follows the documented bounded-context model instead of global same-side run emission. Low-side Hooks search backward from an active LOW to the nearest older strictly lower LOW; high-side Hooks mirror this from an active HIGH to the nearest older strictly higher HIGH. Branches are extracted only inside that bounded context, discovered right-to-left, and labeled old-to-new.

The gray Hook/ND arc starts from the full-cycle `cycle_start_node`, but F1 ownership is seeded from the Hook `resolve_node`. This prevents visual cycle boundaries from moving semantic F roots.

The main chart now defaults to drawing only Hooks that seed a visible F1 through `InpDrawOnlyFlagSeedHooks=true`. This avoids gray audit-dump charts while preserving Hook context. Full Hook rendering can be restored by setting that input to false.

`InpEnforceSingleChainPerDirectionGlobal` defaults to false. Per-scale restart hygiene remains available, but global pruning is no longer allowed to hide all later flags on long chart windows.

## Main-chart contract repair V3

Phoenix now treats Hook/ND as a context layer, not as a hard gate that can erase flags. Hook roots are still preferred, but fail-open raw roots are inspected as a recovery layer and duplicate visual bodies are hidden later.

Default chart inputs now prioritize readable flag structures:

- same-direction pruning defaults off;
- Hook count labels default off;
- internal count labels default off;
- origin labels default off;
- detailed O/A/W/B labels default off;
- Hook arcs draw only when they seed a visible F1.

Turn the audit inputs back on when branch extraction or parent identity needs inspection.

### V4 strict main-chart ownership

The main chart is now treated as a sequence-state view.  Hook/ND can create phase-boundary candidates, but it cannot make every local same-direction Hook become a new visible F1 chain.  With `InpStrictMainChartOwnership=true`, only one same-direction F1 root owns a phase until an opposite completed/locked F3 resets that phase.  Competing roots are scored by chain maturity and local readability; the losing sequence is hidden together with its descendants.

Audit labels are also separated from the main chart by `InpForceCleanMainChartLabels=true`.  Turn on `InpDetailedLabels` to inspect origin, parent, internal, and Hook branch count labels.
