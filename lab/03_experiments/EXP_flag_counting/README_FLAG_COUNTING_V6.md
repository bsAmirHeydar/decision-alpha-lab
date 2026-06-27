# Flag Counting V6 Experiment

Compile and attach:

```text
mql5/Experts/FlagCounting/FlagCountingV6Experiment.mq5
```

Recommended first inputs:

```text
InpBarsToScan = 5000
InpUseMultiScale = true
InpSwingL1 = 2
InpSwingL2 = 3
InpSwingL3 = 5
InpSwingL4 = 8
InpSwingL5 = 13
InpSwingL6 = 21
InpSwingL7 = 34
InpSwingL8 = 55
InpIncludePendingNodes = false
InpShowInvalidatedInAudit = false
InpMaxEventsToDraw = 1200
InpMaxHooksToDraw = 1200
InpDrawCandidates = true
InpDetailedLabels = true
InpShowOriginLabels = true
InpShowInternalLabels = true
InpFixedLineWidth = 1
InpCurveSegments = 32
```

For audit:

```text
InpVerboseAuditLogs = true
```

For less visual noise:

```text
InpDrawHooks = false
```

or

```text
InpMaxEventsToDraw = 300
InpMaxHooksToDraw = 300
```

## V6.1 recommended clean semantic view

After the first visual audit, the default view was changed so the chart does not
show raw audit transitions as if they were final structures.

Recommended default inputs:

```text
InpRequireF1PhaseBoundary = true
InpDrawRawSeeds = false
InpDrawLifecycleHistory = false
InpShowParentIds = true
InpLabelTimeClusterBars = 4
InpLabelPriceClusterPoints = 160
```

For full audit/debug mode, enable:

```text
InpDrawRawSeeds = true
InpDrawLifecycleHistory = true
InpVerboseAuditLogs = true
```

Use debug mode only when validating internal transitions.  For normal visual
inspection, keep raw seeds and lifecycle history off so each chain displays its
current meaningful state.

## Recommended troubleshooting view

For the normal semantic chart:

```text
InpRequireF1PhaseBoundary = true
InpEnforceSingleChainPerDirectionScale = true
InpMergeVisualDuplicateBodies = true
InpDrawRawSeeds = false
InpDrawLifecycleHistory = false
InpShowParentIds = true
```

For full audit inspection, temporarily enable:

```text
InpDrawRawSeeds = true
InpDrawLifecycleHistory = true
InpVerboseAuditLogs = true
```


## V6.2 semantic-origin repair

The default semantic view is now stricter about root F1 creation. A root F1 is not allowed to be created from arbitrary two-leg windows when no readable ND/Hook phase boundary is available. The old fail-open scan remains available through `InpAllowF1FailOpenWhenNoHook=true`, but it is intended for audit/debug only because it can create mid-move roots.

The sequence post-processor also has an optional global same-direction ownership gate (`InpEnforceSingleChainPerDirectionGlobal=true` by default). If a direction already has an active root chain, a later same-direction root is pruned unless an opposite F3 appears between the two roots. This implements the documented phase rule more strongly than the earlier per-scale-only pruning.


### Visibility recovery note

The previous strict phase gate (`InpAllowF1FailOpenWhenNoHook=false` together with global same-direction pruning) could legitimately produce an empty chart whenever the Hook/ND boundary extractor did not emit readable phase boundaries for the active symbol/timeframe. That was not acceptable for research inspection.

The V6 default is now a **soft semantic gate**:

- `InpRequireF1PhaseBoundary = true` still prefers ND/Hook phase-boundary roots.
- `InpAllowF1FailOpenWhenNoHook = true` allows fallback roots only when no readable Hook/ND boundary exists for that scale/direction.
- `InpEnforceSingleChainPerDirectionGlobal = false` keeps cross-scale visibility while the phase-boundary engine is still being audited.
- per-scale ownership pruning remains enabled through `InpEnforceSingleChainPerDirectionScale = true`.

For strict experiments, turn on the hard gate manually:

```text
InpAllowF1FailOpenWhenNoHook = false
InpEnforceSingleChainPerDirectionGlobal = true
```

If that strict mode returns an empty chart, the issue is not the renderer; it means the Hook/ND phase-boundary extractor is not emitting enough semantic boundaries for that market segment.
