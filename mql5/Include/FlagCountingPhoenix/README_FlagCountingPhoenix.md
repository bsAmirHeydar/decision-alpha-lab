# FlagCounting Phoenix

## Current canon

Phoenix must be implemented and audited from:

```text
docs/contexts/legacy/flag_counting/FLAG_COUNTING_CURRENT_CANON.md
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
- `FP_NodeExtractTypes.mqh`: Level 02 node config/report structs and node-source enums.
- `FP_NodePlateau.mqh`: adjacent equal high/low plateau detection.
- `FP_NodeClearance.mqh`: L-clearance scans with equality-skip and strict-break audit.
- `FP_NodeCanonicalizer.mqh`: chronological ordering, stable re-id, and alternating same-side compression.
- `FP_NodeScaleList.mqh`: deterministic multi-L list construction.
- `FP_NodeAudit.mqh`: standalone Level 02 node report and sample logs.
- `FP_NodeEngine.mqh`: Level 02 facade used by Hook/F layers.
- `FP_Identity.mqh`: Level 03 deterministic structural/visual/phase/chain/audit identity kernel.
- `FP_IdentityAudit.mqh`: Level 03 identity sanity report and optional samples.
- `FP_HookAudit.mqh`: Level 04 Hook/ND bounded-context report and samples.
- `FP_HookContext.mqh`: Level 04 cycle-start strict-break and bounded-context helpers.
- `FP_HookEngine.mqh`: Level 04 branch-based ND/hook facade.
- `FP_FlagBodyRules.mqh`: Level 05 pure O/A/W/B strict-break predicates.
- `FP_FlagBodyAudit.mqh`: Level 05 body build report and body samples.
- `FP_FlagBodyEngine.mqh`: Level 05 two-leg body facade.
- `FP_InternalCountRules.mqh`: Level 06 pure adverse/favorable, middle-node, branch-id, and boundary predicates.
- `FP_InternalCountAudit.mqh`: Level 06 internal-pack report, counters, and optional samples.
- `FP_InternalCountEngine.mqh`: Level 06 facade for internal 1/2/3/4 and pre-confirmation extension absorption.
- `FP_F1LifecycleRules.mqh`: Level 07 pure F1 phase-gate, lifecycle-id, visibility, and F2-authorization predicates.
- `FP_F1LifecycleAudit.mqh`: Level 07 F1 lifecycle report and optional samples.
- `FP_F1LifecycleEngine.mqh`: Level 07 facade that converts body/internal evidence into candidate/post-flag/confirmed/invalidated F1 roots.
- `FP_F2LifecycleRules.mqh`: Level 08 pure F2 parent-gate, size-gate, lifecycle-id, visibility, and F3-authorization predicates.
- `FP_F2LifecycleAudit.mqh`: Level 08 F2 lifecycle report and optional samples.
- `FP_F2LifecycleEngine.mqh`: Level 08 facade that converts confirmed F1 parents into candidate/post-flag/confirmed/invalidated F2 children.
- `FP_F3LifecycleRules.mqh`: Level 09 pure F3 parent-gate, terminal OR qualification, lifecycle-id, visibility, and lock predicates.
- `FP_F3LifecycleAudit.mqh`: Level 09 F3 lifecycle and lock report with optional samples.
- `FP_F3LifecycleEngine.mqh`: Level 09 facade that converts authorized F2 parents into completed/locked terminal F3 children.
- `FP_OwnershipTypes.mqh`: Level 10 ownership report and phase-state audit types.
- `FP_OwnershipRules.mqh`: Level 10 pure owner ranking, reset, root, and descendant rules.
- `FP_OwnershipAudit.mqh`: Level 10 FP_LEVEL10 report and ownership samples.
- `FP_OwnershipEngine.mqh`: Level 10 semantic phase owner facade.
- `FP_CanonicalTypes.mqh`: Level 11 final canonical state and invariant report types.
- `FP_CanonicalRules.mqh`: Level 11 pure final-stream invariant and duplicate rules.
- `FP_CanonicalAudit.mqh`: Level 11 FP_LEVEL11 report and canonical samples.
- `FP_Canonicalizer.mqh`: Level 11 final pre-render canonicalization facade.
- `FP_ExportTypes.mqh`: Level 11.5 raw audit export config/report types.
- `FP_ExportRows.mqh`: Level 11.5 CSV header and row serialization helpers.
- `FP_ExportEngine.mqh`: Level 11.5 file export facade for events, hooks, summary, and manifest CSV.
- `FP_RenderTypes.mqh`: Level 12 renderer config/report types.
- `FP_RenderRules.mqh`: Level 12 pure display filtering and canonical object-name helpers.
- `FP_RenderAudit.mqh`: Level 12 `FP_LEVEL12` report and optional render samples.
- `FP_SequenceEngine.mqh`: F1 -> F2 -> F3 orchestration, ownership, and canonicalization wiring.
- `FP_Renderer.mqh`: Level 12 chart drawing facade; read-only consumer of canonical events/hooks.
- `FP_ValidationTypes.mqh`: Level 13 validation config/report types.
- `FP_ValidationRules.mqh`: Level 13 baseline/regression and invariant check helpers.
- `FP_ValidationAudit.mqh`: Level 13 `FP_LEVEL13` report and validation samples.
- `FP_ValidationEngine.mqh`: Level 13 read-only validation facade.
- `FP_ReleaseTypes.mqh`: Level 14 release/debug/rollback config/report types.
- `FP_ReleaseRules.mqh`: Level 14 release-profile override and gate rules.
- `FP_ReleaseAudit.mqh`: Level 14 `FP_LEVEL14` report and release samples.
- `FP_ReleaseEngine.mqh`: Level 14 profile, release gate, and release manifest facade.
- `FP_InterfaceTypes.mqh`: Level 15 interface contract config/report types.
- `FP_InterfaceRules.mqh`: Level 15 facade, config, dependency, identity, parent, and result checks.
- `FP_InterfaceAudit.mqh`: Level 15 `FP_LEVEL15_PRE` / `FP_LEVEL15` reports and samples.
- `FP_InterfaceEngine.mqh`: Level 15 read-only preflight/postflight interface contract facade.
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


## Level 02 node engine

Phoenix now builds nodes through a modular Level 02 facade. The pipeline is:

```text
canonical closed bars
-> plateau candidates
-> L-clearance scans
-> raw FP_Node[]
-> chronological re-id
-> alternating same-side compression
-> canonical FP_Node[] for Hook/F engines
```

Default node audit inputs:

```text
InpPrintNodeSanity = true
InpPrintNodeSamples = false
InpNodeSampleLimit = 6
```

`FP_LEVEL02_RAW` explains candidate plateaus, emitted raw nodes, confirmed/pending counts, equality skips, and rejection reasons. `FP_LEVEL02_CANONICAL` explains same-side run compression and final canonical node counts.

Confirmed nodes and live-pending candidates are no longer implicit. Each `FP_Node` carries:

```text
confirmed
is_confirmed
is_live_pending
source = confirmed_history | live_candidate
plateau_start_index
plateau_end_index
```

Equality remains non-breaking and non-confirming: it does not reject a candidate as a break, but it also does not count toward L clearance.


## Level 03 identity layer

Phoenix now assigns identity before renderer and ownership decisions are trusted. The identity kernel separates exact replay identity from visual chart identity:

```text
structural_id = exact L-aware replay identity
visual_id     = chart-geometry identity across L variants
phase_id      = ownership window
chain_id      = F1 -> F2 -> F3 sequence
audit_id      = source/config/pass trace
```

Default identity audit inputs:

```text
InpPrintIdentitySanity = true
InpPrintIdentitySamples = false
InpIdentitySampleLimit = 6
```

`FP_LEVEL03` reports whether every emitted event and Hook/ND context has identity and whether hidden events carry a non-empty `hidden_reason`. Visual duplicate pruning is now phase-safe: same geometry may merge only when `phase_id` also matches.



## Level 04 Hook / ND context engine

Phoenix now audits Hook/ND before using it as phase context. The path is:

```text
canonical FP_Node[]
-> bounded same-side Hook contexts
-> cycle-start strict-break validation
-> branch-length audit
-> adaptive-L rejection for branch length >4
-> 3/4-node ND retracement qualification
-> visible-F1 seed marking
```

Default Hook audit inputs:

```text
InpPrintHookSanity = true
InpPrintHookSamples = false
InpHookSampleLimit = 6
InpHookMainRequiresVisibleF1 = true
InpHookKeepUnseededVisibleForDebug = false
```

`FP_LEVEL04` explains bounded context counts, branch-length distribution, cycle-start breaks, overextended current-L contexts, retracement rejections, duplicate compaction, and emitted ND hooks. `FP_LEVEL04_SEED` runs after event pruning and reports how many Hook contexts actually seed visible canonical F1 roots.

Hook/ND still does not emit F events. It only provides phase-boundary context. Fail-open raw roots remain the diagnostic safety net so Hook mistakes cannot starve all flag bodies.


## Level 05 Flag Body engine

Phoenix now builds the invariant body through a dedicated Level 05 pipeline:

```text
canonical FP_Node[]
-> origin kind check
-> Leg1 candidate / strict favorable extension
-> Waist candidate / strict adverse deepening without Origin break
-> Leg2 strict break of Leg1
-> body identity + body status + body audit
```

Default body audit inputs:

```text
InpPrintBodySanity = true
InpPrintBodySamples = false
InpBodySampleLimit = 6
```

`FP_LEVEL05` reports body attempts, completed bodies, invalid origins, origin-break invalidations, Leg1 extensions, Waist deepenings, equal-Origin touches, equal-Leg1 touches, strict Leg2 breaks, and pre-internal Leg2 extension absorption.

Level 05 emits body-stage facts only. It does not confirm F1, qualify F2/F3, reset phases, or decide ownership. Every `FP_FlagEvent` now carries `body_id`, `body_status`, `leg2_extension_count`, `body_scan_start_pos`, `body_scan_end_pos`, and `body_reason` so post-body lifecycle layers can be audited against the exact body they received.


## Level 11.5 Raw audit export

Phoenix now has a file-based export/report layer before renderer trust. Default export is disabled:

```text
InpExportAuditFiles = false
```

When enabled, Level 11.5 writes CSV files under `MQL5/Files/FlagCountingPhoenix/`:

```text
latest_events.csv
latest_hooks.csv
latest_summary.csv
latest_manifest.csv
```

The export layer is read-only. It serializes the Level 11 canonical stream and never mutates visibility, parent links, hidden reasons, identity, renderer objects, or sequence ownership.

Default export inputs:

```text
InpExportFolder = "FlagCountingPhoenix"
InpExportVisibleOnly = false
InpExportEventsCsv = true
InpExportHooksCsv = true
InpExportSummaryCsv = true
InpExportManifestCsv = true
InpExportOverwriteLatest = true
InpPrintExportSanity = true
```

The terminal sanity line is `FP_LEVEL11_5`. `FP_SUMMARY` also includes export counters.

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


## Level 06 internal count

Phoenix now treats post-body internal counting as its own audited layer before lifecycle ownership.  `FP_InternalCountRules.mqh` owns pure predicates, `FP_InternalCountAudit.mqh` owns `FP_LEVEL06`, and `FP_InternalCountEngine.mqh` owns the facade used by the sequence engine.

The internal contract is:

```text
0 adverse nodes => body exists but no post-flag count
1 adverse node  => developing internal
2 adverse nodes => valid 1/2 and confirmation-ready once Leg2 breaks again
3/4 adverse nodes => extended internal / ND-like branch state
```

Before a valid internal 1/2 exists, a favorable break beyond Leg2 is recorded as `pre_internal_leg2_extension_node` and, when absorption is enabled, folded back into the body as the new Leg2.  It is never confirmation.  F1 also keeps the stricter middle-opposite rule: the best middle node between internal 1 and 2 must not break Leg2 before the valid 1/2 is formed.

New controls:

```text
InpPrintInternalSanity = true
InpPrintInternalSamples = false
InpInternalSampleLimit = 6
```

Main-chart labels remain renderer-owned.  Level 06 only provides `internal_pack_id`, branch evidence, valid12 state, confirmation/invalid positions, and extension evidence for later lifecycle layers.


## Level 07 F1 lifecycle

Phoenix now promotes F1 roots through a dedicated lifecycle layer instead of letting `FP_SequenceEngine` infer F1 status directly from body/internal helper calls.  The active modules are:

```text
FP_F1LifecycleRules.mqh
FP_F1LifecycleAudit.mqh
FP_F1LifecycleEngine.mqh
```

Level 07 consumes Level 05 body evidence and Level 06 internal-count evidence. It owns these F1 facts:

```text
lifecycle_id
lifecycle_status
lifecycle_phase_gate_passed
lifecycle_body_complete
lifecycle_internal_ready
lifecycle_can_spawn_f2
lifecycle_reason
```

Default F1 lifecycle controls:

```text
InpPrintF1Sanity = true
InpPrintF1Samples = false
InpF1SampleLimit = 6
InpF1ShowPostFlagCandidates = true
InpF1ShowLiveBodyCandidates = true
```

`FP_LEVEL07` reports root attempts, phase-boundary versus fail-open attempts, phase-gate rejections, body-missing roots, candidate/post-flag/confirmed/invalidated F1s, extension absorption, visible/hidden lifecycle counts, duplicate rejection, emitted roots, and F2-ready parents.

F2 may now only spawn from a Level 07 F1 with:

```text
status = confirmed
has_confirm = true
lifecycle_can_spawn_f2 = true
```

This prevents body-only or post-flag F1 structures from silently authorizing F2/F3.



## Level 08 F2 lifecycle

Phoenix now promotes F2 through a dedicated lifecycle layer instead of letting `FP_SequenceEngine` infer child status from a generic body helper. The active modules are:

```text
FP_F2LifecycleRules.mqh
FP_F2LifecycleAudit.mqh
FP_F2LifecycleEngine.mqh
```

Level 08 consumes confirmed Level 07 F1 parents, Level 05 body evidence, and Level 06 internal-count evidence. It owns these F2 facts:

```text
f2_lifecycle_id
f2_lifecycle_status
f2_parent_ready
f2_origin_found
f2_body_complete
f2_size_gate_passed
f2_internal_ready
f2_can_spawn_f3
f2_parent_size_ratio
f2_lifecycle_reason
```

Default F2 lifecycle controls:

```text
InpPrintF2Sanity = true
InpPrintF2Samples = false
InpF2SampleLimit = 6
InpF2ShowSizeRejectedCandidates = false
InpF2ShowPostFlagCandidates = true
InpF2ShowLiveBodyCandidates = true
```

`FP_LEVEL08` reports parent attempts, parent-ready/rejected state, strict-window origin scans, origin found/missing state, body missing/complete state, size pass/reject, candidate/post-flag/confirmed/invalidated states, extension absorption, visibility, F3-ready children, emitted children, and duplicate rejection.

F3 may now only spawn from a Level 08 F2 with:

```text
status = confirmed
has_confirm = true
f2_size_gate_passed = true
f2_can_spawn_f3 = true
```

This prevents undersized or unconfirmed F2 bodies from silently authorizing F3.



## Level 09 F3 lifecycle

Phoenix now promotes F3 through a dedicated terminal lifecycle layer. The active modules are:

```text
FP_F3LifecycleRules.mqh
FP_F3LifecycleAudit.mqh
FP_F3LifecycleEngine.mqh
```

Level 09 consumes only F2 parents that Level 08 has authorized with `f2_can_spawn_f3=true`. It owns these F3 facts:

```text
f3_lifecycle_id
f3_lifecycle_status
f3_parent_ready
f3_origin_found
f3_body_complete
f3_size_gate_passed
f3_leg1_L_gate_passed
f3_or_gate_passed
f3_terminal_complete
f3_lock_ready
f3_locked
f3_parent_size_ratio
f3_parent_leg1_L_ratio
f3_lock_event_id
f3_lifecycle_reason
```

Default F3 lifecycle controls:

```text
InpPrintF3Sanity = true
InpPrintF3Samples = false
InpF3SampleLimit = 6
InpF3ShowORRejectedCandidates = false
InpF3ShowLiveBodyCandidates = true
```

F3 completes through OR qualification only after its own body is complete:

```text
F3.flag_size >= InpF3MinParentSizeRatio * F2.flag_size
OR
F3.leg1_L >= ceil(InpF3Leg1LMinRatio * F2.leg1_L)
```

F2 is not finished until its own flag end is re-hit/confirmed. F3 therefore backfills its Origin from the deepest correction between final F2 Leg2 and F2 confirmation, but forces F3 Leg1 to the F2 confirmation node. Favorable nodes before F2 confirmation do not become F3 Leg1. F3 does not need a post-body internal 1/2 in Level 09. Once completed, it can lock on the first opposite confirmed F1 after F3 completion. `FP_LEVEL09` reports construction and OR qualification; `FP_LEVEL09_LOCK` reports cross-sequence lock scans.


## Level 10 sequence ownership and phase reset

Phoenix now separates lifecycle emission from main-chart phase ownership. The active modules are:

```text
FP_OwnershipTypes.mqh
FP_OwnershipRules.mqh
FP_OwnershipAudit.mqh
FP_OwnershipEngine.mqh
```

Level 10 runs after Level 09 F3 lock evidence and before visual duplicate pruning. It owns these event fields:

```text
phase_direction
phase_owner_root_id
chain_state
next_expected_f_level
phase_reset_reason
owner_rank_score
losing_candidate_ids
hidden_descendant_ids
```

The main-chart rule is now explicit:

```text
one direction / one phase / one canonical F1 owner
```

Later same-direction F1 roots inside the same phase are hidden as competing roots unless an opposite terminal F3 reset exists between the previous owner and the new root. If a root loses ownership, every F2/F3 descendant in the same sequence is hidden with a deterministic reason.

Owner ranking follows semantic maturity first: locked F3, completed F3, confirmed qualified F2, confirmed F1, Hook/phase-boundary source, non-fail-open source, lower local L on equal semantic quality, then deterministic time/id tie-breaks.

Default Level 10 controls:

```text
InpPrintOwnershipSanity = true
InpPrintOwnershipSamples = false
InpOwnershipSampleLimit = 8
InpStrictMainChartOwnership = true
InpOwnershipScoreMargin = 25
InpOwnershipHideOrphans = true
```

`FP_LEVEL10` reports phase count, root candidates, owner roots, competing roots, resets, hidden roots, hidden descendants, fail-open hides, superseded parent hides, orphan hides, and visible-before/after counts. Renderer remains non-authoritative.


## Level 11 canonicalization and audit invariants

Phoenix now runs a final engine-owned canonicalization pass before renderer/export. The active modules are:

```text
FP_CanonicalTypes.mqh
FP_CanonicalRules.mqh
FP_CanonicalAudit.mqh
FP_Canonicalizer.mqh
```

Level 11 does not create nodes, Hooks, bodies, or lifecycle events. It normalizes the final stream after Level 10 ownership and compatibility duplicate pruning. It owns these event fields:

```text
canonical_id
canonical_state
canonical_rank_final
canonical_conflict_group_id
canonical_invariant_flags
canonical_reason
```

Default Level 11 controls:

```text
InpPrintCanonicalSanity = true
InpPrintCanonicalSamples = false
InpCanonicalSampleLimit = 8
InpCanonicalStrictInvariants = true
InpCanonicalHideUnresolvedOrphans = true
```

`FP_LEVEL11` reports visible-before/after, hidden-before/after, id repairs, parent-link repairs, hidden-reason repairs, phase-safe duplicate hides, orphan hides, malformed-body hides, invalid hides, invariant failures, post-canonical duplicate conflicts, and canonical rank range. If `FP_LEVEL11 status=failed`, renderer output is diagnostic only until the invariant failure is fixed.

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


## Level 12 renderer

Renderer now uses `FP_RenderTypes`, `FP_RenderRules`, `FP_RenderAudit`, and `FP_Renderer`. It draws after Level 11.5 export, uses canonical object names by default, emits `FP_LEVEL12`, and does not mutate logical events or hooks.

## Level 13 validation suite

Phoenix now has a read-only validation harness backed by:

```text
FP_ValidationTypes.mqh
FP_ValidationRules.mqh
FP_ValidationAudit.mqh
FP_ValidationEngine.mqh
```

Validation runs after Level 11.5 export and Level 12 renderer. It does not mutate events, hooks, visibility, identity, ownership, canonical state, export output, or chart objects.

Default validation is disabled:

```text
InpValidationEnabled = false
```

When enabled, baseline mode writes unset expected ranges as warnings so the user can create broker-specific baselines without inventing counts:

```text
InpValidationBaselineMode = true
MQL5/Files/FlagCountingPhoenix/latest_validation.csv
```

Regression mode is created by filling the expected min/max inputs. Exact expectations use the same min and max. The terminal sanity line is `FP_LEVEL13`, and `FP_SUMMARY` includes validation pass/fail/warn counters.


## Level 14 release/debug/rollback layer

Phoenix now includes `FP_ReleaseTypes.mqh`, `FP_ReleaseRules.mqh`, `FP_ReleaseAudit.mqh`, and `FP_ReleaseEngine.mqh`. The active EA exposes `InpReleaseProfile` with `normal`, `clean_main`, `audit_export`, `validation`, `debug_max`, `render_off`, and `safe_rollback` profiles. Level 14 writes `latest_release.csv` and prints `FP_LEVEL14`; it does not mutate market structure.

## Level 15 module interface contracts

Phoenix now includes `FP_InterfaceTypes.mqh`, `FP_InterfaceRules.mqh`, `FP_InterfaceAudit.mqh`, and `FP_InterfaceEngine.mqh`. The EA runs a read-only preflight pass after Level 14 profile overrides and a read-only postflight pass before final `FP_SUMMARY`. The layer emits `FP_LEVEL15_PRE` and `FP_LEVEL15`, optionally writes `latest_interface_pre.csv` and `latest_interface_post.csv`, and adds interface counters to `FP_SUMMARY`. It does not mutate event/hook streams, renderer objects, lifecycle state, ownership state, or canonical state.


## Level 16 acceptance matrix

Phoenix now includes `FP_AcceptanceTypes.mqh`, `FP_AcceptanceRules.mqh`, `FP_AcceptanceAudit.mqh`, and `FP_AcceptanceEngine.mqh`. Level 16 runs after Level 15 postflight and before `FP_SUMMARY`, emits `FP_LEVEL16`, and can optionally write `latest_acceptance.csv`. It is a read-only runbook gate: it aggregates timebase, node, hook, body, internal-count, F1/F2/F3 lifecycle, ownership, canonicalization, export, renderer, validation, release, and interface health into one acceptance matrix.

## Level 17 ambiguity / decision lock

Level 17 adds the final read-only decision-lock layer:

- `FP_AmbiguityTypes.mqh`
- `FP_AmbiguityRules.mqh`
- `FP_AmbiguityAudit.mqh`
- `FP_AmbiguityEngine.mqh`

The active EA now uses `identity_generation_pass=phoenix_level18`, prints
`FP_LEVEL17`, and can write `latest_ambiguity.csv`. This layer verifies that
closed-bar timebase, confirmed-node F bodies, phase-gated F1, fail-open
diagnostic behavior, F2/F3 display policy, seeded Hook display, strict renderer
visibility, canonical object names, and release-like profile gates remain aligned
with `FLAG_COUNTING_CURRENT_CANON.md`.


## Level 18 static QA / compile hardening layer

Phoenix now includes `FP_StaticQaTypes.mqh`, `FP_StaticQaRules.mqh`, `FP_StaticQaAudit.mqh`, and `FP_StaticQaEngine.mqh`. Level 18 runs after Level 17 decision lock and before `FP_SUMMARY`, emits `FP_LEVEL18`, and can optionally write `latest_static_qa.csv`.

This layer is read-only. It checks final runtime contracts, identity pass, interface contract version, partition consistency, counter sanity, report alignment, and I/O error state. Source-side checks that MQL cannot do internally are handled by `contexts/legacy/tools/flag_counting/static_qa.py`.


## Debug lock: F2/F3 child-start chronology

Default research display is full-state: all Hook/ND contexts and all emitted F lifecycle states may be shown. Clean/canonical-only display belongs to release/render profiles.

F2 and F3 follow the child-start rule: only Origin is backfilled into the parent correction window; Leg1 is forced to the parent confirmation hit; Waist and Leg2 must occur after that parent confirmation. For F3, the Origin is the bullish lowest low or bearish highest high after final F2 Leg2 and before F2 confirmation. F2 confirmation is the strict high/low hit of F2 Leg2; close is not required. F3 still needs its own Waist and Leg2, but no post-F3 internal count is required.

## Offline license layer

`FlagCountingPhoenixExperiment.mq5` now includes an offline fail-closed runtime gate before Level 01. The issuer generates a bundle with:

```powershell
python contexts/legacy/tools/flag_counting/offline_license_keygen.py --account <LOGIN> --server "<SERVER>" --expires <YYYYMMDD>
```

The recipient fills the neutral-looking runtime fields:

```text
InpPhaseModelProfile
InpRenderMemo
InpNodeModelSeed
InpBoundaryModelSeed
InpValidationModelSeed
InpReleaseModelSeed
```

The expert checks product, account, server hash, expiry, password, hidden numeric gates, and signature before running structural detection. Expiry is rechecked periodically while attached.
