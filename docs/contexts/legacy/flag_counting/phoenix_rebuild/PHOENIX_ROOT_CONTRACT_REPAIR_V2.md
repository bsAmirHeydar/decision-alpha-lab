# Phoenix Root Contract Repair V2

## Purpose

This repair brings the Phoenix implementation back to the documented Flag Counting contract after the Hook/ND visual-cycle changes made the main chart gray and starved the colored F1/F2/F3 flag bodies.

The guiding rule is simple:

> Hook / ND is a phase-boundary and context layer. It must never erase the two-leg flag-body detector.

The main chart must show valid F structures first. Hook / ND is drawn as gray context behind those structures, not as a replacement for them.

## Root failure found

The uploaded project had four coupled problems.

### 1. Hook-origin filtering was too strong

`FP_DetectScale()` first collected Hook-derived roots and then built F1 only from those roots unless no Hook-derived root could build a visible F1.

That is not safe. A Hook engine under active research can be incomplete or too narrow. If it emits one usable root, the old logic would suppress all raw-origin roots in that direction and scale. The result is exactly what appeared on the chart: gray Hook/ND context remained, while many colored F bodies disappeared.

### 2. Same-direction restart pruning was too aggressive for the research chart

The project has a long-term semantic idea that a same-direction sequence should not restart until an opposite F3 phase exists. That is a sequence ownership rule, not a reason to remove every visible flag body from the research chart by default.

`InpEnforceSingleChainPerDirectionScale` was enabled by default. On larger windows and H1/H4 charts that can hide later F1 roots and descendants, leaving the chart visually dominated by Hook/ND arcs.

### 3. Hook rendering was not compact enough across scales

The Hook engine already compacted same-resolve branches inside a single scale. But the renderer still accepted many L-scale variants that resolved to the same visible F1 origin. Those arcs were all gray and could dominate the chart.

### 4. Hook counted-node labels were mixed with main-chart labels

Hook branch numbers `1/2/3/4` are useful for audit, but they are too dense for the default main chart. They should be opt-in diagnostic labels, not always-on labels.

## Repair decisions

### 1. Always keep fail-open F1 visibility when allowed

The engine now builds:

1. Hook-derived F1 roots.
2. Raw-origin fail-open F1 roots when fail-open is enabled.

Exact visual duplicates are rejected before insertion, and later pruning can still hide fallback roots that are truly inside an owned phase. This means Hook can enrich the semantic root layer, but it cannot starve the flag-body detector.

### 2. Disable same-direction chain pruning by default

`InpEnforceSingleChainPerDirectionScale` now defaults to `false`.

The input remains available. Turning it on is now an explicit ownership experiment, not the default visualization mode.

### 3. Compact Hook arcs at renderer level

When `InpDrawOnlyFlagSeedHooks=true`, the renderer draws only the best Hook/ND branch for each visible F1 seed.

The best branch is selected by:

1. More counted nodes: 4-node branch over 3-node branch.
2. Cleaner mid-scale preference around L8.
3. Stronger retracement.
4. Older cycle coverage.

This is visual compaction only. The Hook engine still emits all semantic Hook branches it detects.

### 4. Hide Hook counted numbers by default

A new input was added:

```text
InpShowHookCountLabels = false
```

When false, the chart still shows Hook/ND labels and gray arcs, but it does not print every Hook branch number on every same-side counted node. This keeps colored F labels readable.

### 5. Merge visual duplicates across L-scales

The project now distinguishes two identities:

- Structural identity: includes node id and L.
- Visual identity: same kind, same candle anchor, same price.

Main-chart duplicate filtering uses visual identity. This prevents identical geometry from being drawn multiple times just because it was rediscovered at another L.

## Contract alignment

### Flag body contract preserved

A flag body is still:

```text
Origin -> Leg1 -> Waist -> Leg2
```

For bullish:

```text
LOW origin -> HIGH leg1 -> LOW waist above origin -> HIGH leg2 breaking leg1
```

For bearish, mirrored.

No open, close, candle color, or candle body is used.

### Hook / ND contract preserved

Hook / ND remains same-side and branch-based:

- low-side Hook counts LOW nodes only;
- high-side Hook counts HIGH nodes only;
- the cycle boundary is not counted as `1`;
- valid ND branch length is exactly 3 or 4;
- equality is not a break;
- gray Hook/ND arcs are renderer output only and do not create F structures.

### Renderer authority boundary preserved

The renderer does not invent flags or Hooks. It only filters visual noise among engine-emitted structures.

## Files changed

```text
mql5/Include/FlagCountingPhoenix/FP_Types.mqh
mql5/Include/FlagCountingPhoenix/FP_SequenceEngine.mqh
mql5/Include/FlagCountingPhoenix/FP_Renderer.mqh
mql5/Experts/FlagCounting/FlagCountingPhoenixExperiment.mq5
docs/contexts/legacy/flag_counting/phoenix_rebuild/IMPLEMENTATION_NOTES.md
docs/contexts/legacy/flag_counting/phoenix_rebuild/PHOENIX_ROOT_CONTRACT_REPAIR_V2.md
```

## Expected visual result

After cleaning old objects and recompiling:

- colored F1/F2/F3 bodies should return;
- gray Hook/ND arcs should be reduced and stay in the background;
- Hook counted numbers should not flood the chart unless explicitly enabled;
- identical F geometry across L-scales should be merged on the main chart;
- the chart should no longer look like a gray Hook audit dump.

## Required MT5 cleanup after applying

MetaTrader can keep old objects and compiled artifacts. After applying this patch:

1. Remove the expert from the chart.
2. Delete old `FlagCountingPhoenixExperiment.ex5` if present.
3. Compile `mql5/Experts/FlagCounting/FlagCountingPhoenixExperiment.mq5`.
4. Open `Ctrl+B` and delete all objects with the Phoenix prefix, usually `DAL_FCP_`.
5. Attach the expert again.
6. Press Reset in Inputs once so the new defaults are loaded.

