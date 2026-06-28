# Flag Counting Current Canon

Status: **active source of truth for Phoenix implementation**.
Scope: docs, code patches, audit, renderer, validation, and future execution modules related to Flag Counting.

This document exists to remove decision drift. If any older Flag Counting document conflicts with this file, this file wins.

---

## 1. Active implementation target

The only active implementation path is Phoenix:

```text
mql5/Experts/FlagCounting/FlagCountingPhoenixExperiment.mq5
mql5/Include/FlagCountingPhoenix/
```

Legacy paths are retained only as research history or reference material:

```text
mql5/Experts/M0007/M0007_FlagCountingF1.mq5
mql5/Include/M0007/
FlagCountingVNext*
FlagCountingV6*
```

Do not start new code from M0007, VNext, V6, old checklists, or old sequence contracts.

---

## 2. Canon hierarchy

Use the following hierarchy when implementing or auditing Phoenix:

1. **This file** — final decision source and conflict resolver.
2. `docs/flag_counting/FLAG_COUNTING_SEQUENCE_CONTRACT_V4.md` — semantic sequence contract.
3. `docs/flag_counting/FLAG_COUNTING_ENGINEERING_PACK_V5.md` and `docs/flag_counting/engineering_pack_v5/` — definitions, algorithms, and explanations.
4. `docs/flag_counting/implementation_ladder_v1/` — implementation order, interfaces, acceptance gates, and freeze protocol.
5. `docs/flag_counting/phoenix_rebuild/` — Phoenix-specific repair notes. These are valid only where they do not conflict with this canon.
6. Current Phoenix code under `mql5/Include/FlagCountingPhoenix/` — implementation reality. If code and docs differ, patch docs and code together under the correct ladder level.

Older documents are archived context unless explicitly referenced by this canon.

---

## 3. Non-negotiable invariants

These rules cannot be relaxed by renderer settings or tactical patches:

1. Structural decisions use candle `high` and `low` only.
2. `open`, `close`, candle body, candle color, volume, indicators, and external signals are not structural inputs.
3. Equality is not a break. A level is broken only by strict passage beyond it.
4. Nodes are L-based structural highs/lows with plateau handling.
5. Raw observations must remain auditable even when compressed views are used.
6. A flag body is always `Origin -> Leg1 -> Waist -> Leg2`.
7. F1, F2, and F3 share the same body shape; they differ by lifecycle, authorization, confirmation, invalidation, and terminal behavior.
8. The engine is a stateful sequence system, not a sliding-window pattern scanner.
9. Renderer is non-authoritative. It draws only engine-emitted objects.
10. Main chart and audit output are separate products.
11. Every visible or hidden decision must carry a reason.
12. Given the same bars, inputs, and range, Phoenix must emit deterministic output.
13. Phoenix structural engines must consume the Level 01 canonical closed-bar stream by default. Direct private `CopyRates` calls are not allowed in higher structural modules.
14. Canonical bar indexing is fixed: `rates[0]` is the oldest closed bar, and newer bars have higher indices.

---

## 4. Final resolved decisions

### 4.1 Phase reset

Default phase reset is strict:

```text
PHASE_RESET_OPPOSITE_F3_LOCK_ONLY
```

Meaning:

- Same-direction F1 ownership is not reset by a failed F2/F3 child.
- Same-direction F1 ownership is not reset merely because a new same-direction body appears.
- A completed F3 becomes locked only when a first confirmed opposite F1 appears.
- Broader reset modes may exist only as named diagnostic inputs, never as silent defaults.

Allowed future variants:

```text
PHASE_RESET_OPPOSITE_CONFIRMED_F1
PHASE_RESET_OPPOSITE_HOOK_OR_F1
```

If added, they must be logged in audit and cannot change the meaning of the strict default.

### 4.2 F1 root preference

Root ownership is semantic, not visual.

Default winner order inside the same phase/direction conflict:

1. valid lifecycle status over weaker status;
2. confirmed/qualified over merely developing;
3. Hook/phase-boundary root over fail-open root;
4. completed child chain over single isolated root;
5. lower-L local structure over higher-L umbrella structure when semantic quality is equal;
6. earlier stable origin over later duplicate when semantic quality is equal;
7. deterministic `event_id` as final tie-breaker.

Every losing candidate remains audit-visible with a hidden reason.

### 4.3 Fail-open

Fail-open is diagnostic recovery, not semantic truth.

Default:

- Fail-open may be scanned.
- Fail-open may be main-visible only when no hook-owned canonical root exists in the same phase and it passes the same body/lifecycle rules.
- Fail-open must be explicitly tagged: `from_fail_open=true` and hidden/visible reason must include `fail_open`.

### 4.4 Main-chart visibility

Default main chart is **canonical clean**:

- Show canonical visible F1/F2/F3 structures only.
- F1 may be visible once it has a valid body and has not violated its lifecycle boundary, but it must be tagged as developing until confirmation.
- F2 main visibility requires authorized parent context and size qualification, unless candidate display is explicitly enabled.
- F3 main visibility requires authorized parent context and OR qualification or terminal/completed state, unless candidate display is explicitly enabled.
- Developing, undersized, duplicate, failed, and diagnostic structures remain in audit.

Optional display profiles may expose more detail, but they must not change emitted logical events:

```text
CLEAN_LOCAL
BALANCED
STRUCTURAL_AUDIT
```

### 4.5 High-L versus lower-L ownership

When a higher-L umbrella and a lower-L local structure overlap:

- Main chart chooses the canonical owner using the winner order above.
- Lower-L wins when semantic quality is equal because it gives a more local state reading.
- Higher-L remains audit-visible unless it owns a distinct, non-overlapping phase.
- Renderer must not decide this; the canonicalization/ownership layer decides it.

### 4.6 Pending nodes

Default:

- Pending nodes may support Hook/ND live inspection.
- Confirmed F bodies require confirmed nodes.
- Pending-node F bodies are allowed only in explicit live diagnostic mode and must never be treated as canonical historical truth.

### 4.7 Backfill window

Default strict window:

- F2 origin is backfilled from the deepest adverse correction after F1 Leg2 and before F1 confirmation.
- F3 origin is backfilled from the deepest adverse correction after F2 Leg2 and before F2 confirmation.

Extended post-confirmation backfill may exist only behind a named diagnostic input and must be visible in audit.

### 4.8 F2 size and F3 authorization

Default:

- F2 candidate may exist in audit before size qualification.
- Main-chart F2 requires size qualification unless candidate display is enabled.
- F3 authorization requires confirmed and size-qualified F2.
- If F2 later extends and reaches required size, update the same candidate/Leg2 extension path; do not emit a duplicate child unless identity truly changes.

### 4.9 F3 completion and lock

Default:

- F3 is authorized after confirmed qualified F2.
- F3 completion uses the documented OR rule: parent size ratio or Leg1 L ratio.
- A developing F3 is not rejected merely because the OR condition is not reached yet.
- Once terminal/completed and later locked by opposite confirmed F1, locked F3 never disappears from historical audit/main output.

### 4.10 Hook/ND display

Default:

- Hook/ND is a first-class context layer.
- Main chart shows Hook/ND only when connected to visible canonical ownership or when Hook debug display is enabled.
- Branch numbers belong in audit by default.
- Hook/ND must not starve all F structures.

### 4.11 Audit/export is mandatory

Before renderer is treated as trustworthy, Phoenix must expose:

```text
raw_nodes
scaled_nodes
hooks
raw_events
visible_events
hidden_events
hidden_reason
sequence_transitions
canonical_winners
candidate/qualified/confirmed/invalidated/locked counts
```

CSV/JSON export is the target audit form. Until file export exists, structured log output must expose the same fields.

---

## 4.12 Level 01 candle stream

Default structural input is the Level 01 canonical closed-bar stream:

```text
FP_LoadCanonicalRates -> canonical MqlRates[] -> node/hook/flag engines
```

Default settings:

```text
InpUseClosedBarsOnly = true
InpStrictTimebase = true
InpMinClosedBars = 200
InpPrintTimebaseSanity = true
```

`InpBarsToScan` means requested closed bars in default mode. Phoenix copies one extra raw terminal bar and drops the current forming live candle before detection.

Canonical convention:

```text
rates[0] = oldest closed bar
rates[canonical_bars - 1] = newest closed bar
newer bars have higher indices
time is display metadata, not structural x-axis authority
```

Level 01 must emit an `FP_LEVEL01` sanity line before downstream detection is trusted. If the timebase contract fails under strict mode, Phoenix must stop before node/flag detection.

---


## 4.13 Level 02 node engine

Default structural node path:

```text
Level 01 canonical MqlRates[]
-> FP_BuildCanonicalNodesForScale
-> raw FP_Node[]
-> canonical alternating FP_Node[]
-> Hook/F engines
```

Level 02 is modularized into plateau detection, L-clearance scans, canonicalization, scale-list construction, and node audit. `FP_NodeEngine.mqh` is the facade; higher layers must not duplicate node extraction logic.

Node rules:

- structural inputs are high/low only;
- adjacent equal highs/lows form one plateau candidate;
- plateau anchor is the last equal touch;
- equality is not a break and does not count as L clearance;
- confirmed nodes and live-pending candidates are explicitly tagged;
- canonical nodes are sorted by anchor index and compressed into alternating high/low runs before Hook/F layers consume them.

Default Level 02 audit inputs:

```text
InpPrintNodeSanity = true
InpPrintNodeSamples = false
InpNodeSampleLimit = 6
```

`FP_LEVEL02_RAW` and `FP_LEVEL02_CANONICAL` logs are the current audit form until raw CSV/JSON export is implemented. Renderer output is not accepted as node evidence.

---


## 4.14 Level 03 identity layer

Phoenix uses a dedicated identity kernel before Hook/F lifecycle output is trusted:

```text
FP_Identity.mqh
FP_IdentityAudit.mqh
```

Level 03 assigns deterministic identity to nodes, Hook/ND contexts, and F events. Identity is not a renderer object name and must not depend on chart drawing.

Required identity fields are:

```text
structural_id
visual_id
phase_id
chain_id
audit_id
source_L / L
source_mode
is_fail_open
canonical_rank_score
visible_main
hidden_reason
```

Node structural identity is exact and L-aware:

```text
side + L + anchor_index + normalized_price + plateau_span
```

Node visual identity is chart-geometry identity:

```text
side + anchor_index + normalized_price
```

Event structural identity uses exact O/A/W/B structural node ids. Event visual identity uses O/A/W/B visual node ids and may collapse same-geometry variants only when phase ownership also matches. Same visual geometry in different `phase_id` must not be merged automatically.

Default Level 03 audit inputs:

```text
InpPrintIdentitySanity = true
InpPrintIdentitySamples = false
InpIdentitySampleLimit = 6
```

`FP_LEVEL03` is the current identity sanity log. It must show that every event/hook has assigned identity and every hidden event has a hidden reason before renderer output is trusted.



## 4.15 Level 04 Hook / ND context engine

Phoenix Hook/ND now has an explicit Level 04 audit layer before Flag Body/F lifecycle may trust Hook roots:

```text
FP_HookAudit.mqh
FP_HookContext.mqh
FP_HookEngine.mqh
```

Default Hook path:

```text
Level 02 canonical FP_Node[]
-> bounded same-side context scan
-> cycle-start strict-break validation
-> internal branch-length audit
-> adaptive-L rejection if any branch exceeds 4 counted nodes
-> 3/4-node ND candidate
-> retracement qualification
-> seeded/unseeded visible-F1 marking
```

Level 04 invariants:

- bullish Hook counts LOW nodes; bearish Hook counts HIGH nodes;
- counted branch order is old-to-new after right-to-left discovery;
- 1-node and 2-node branches are developing Hook context only and are not ND;
- 3-node and 4-node branches may become ND only after retracement qualification;
- if any branch in the bounded context has more than 4 counted nodes, the current-L context is rejected and must be re-read at higher L;
- if the cycle start is strictly broken before resolve, the Hook context is invalid; equality does not invalidate;
- Hook/ND may seed F1 roots but cannot starve valid fail-open F bodies;
- main-chart Hook visibility is marked by whether the Hook seeds a visible canonical F1, unless debug inputs explicitly keep unseeded Hooks visible.

Default Level 04 audit inputs:

```text
InpPrintHookSanity = true
InpPrintHookSamples = false
InpHookSampleLimit = 6
InpHookMainRequiresVisibleF1 = true
InpHookKeepUnseededVisibleForDebug = false
```

`FP_LEVEL04` reports bounded context counts, no-boundary contexts, too-short contexts, cycle-start breaks, adaptive-L overextensions, branch-length distribution, ND candidates, retracement rejections, duplicate compaction, and emitted ND hooks. `FP_LEVEL04_SEED` reports how many emitted Hooks seed visible F1 roots and how many Hook contexts are hidden from the main chart with reasons.



## 4.16 Level 05 Flag Body engine

Phoenix Flag Body is now a first-class audit layer before any F lifecycle logic may confirm or qualify a sequence. The active modules are:

```text
FP_FlagBodyRules.mqh
FP_FlagBodyAudit.mqh
FP_FlagBodyEngine.mqh
```

Level 05 owns only this invariant body:

```text
Origin -> Leg1 -> Waist -> Leg2
```

Bullish body:

```text
LOW -> HIGH -> LOW -> HIGH
```

Bearish body:

```text
HIGH -> LOW -> HIGH -> LOW
```

Level 05 invariants:

- Origin kind is direction-specific: bullish starts from LOW, bearish starts from HIGH;
- Leg1 is the opposite-side node after Origin;
- Leg1 may extend only by strict favorable passage; equality is not an extension;
- Waist is the adverse node after Leg1 and may deepen only by strict adverse passage;
- Waist equal to Origin is allowed and audited;
- Waist strictly beyond Origin invalidates the body before Leg2;
- Leg2 must strictly break Leg1; equal to Leg1 is audited but not complete;
- pre-internal favorable breaks are absorbed as Leg2 extension and counted through `leg2_extension_count`;
- Level 05 never confirms F1, never authorizes F2/F3, and never decides main-chart ownership.

Default Level 05 audit inputs:

```text
InpPrintBodySanity = true
InpPrintBodySamples = false
InpBodySampleLimit = 6
```

`FP_LEVEL05` reports body attempts, complete bodies, invalid bodies, live child body stages, Leg1 extensions, Waist deepenings, equal-Origin touches, equal-Leg1 touches, strict Leg2 breaks, and absorbed pre-internal Leg2 extensions.

Each `FP_FlagEvent` now carries Level 05 body audit fields:

```text
body_id
body_status
origin_hit_status
leg1_break_status
leg2_extension_count
body_scan_start_pos
body_scan_end_pos
body_reason
```

These fields are body-layer evidence. Higher lifecycle layers may update lifecycle `status`, but they must not rewrite body construction history.

### Level 06 — Internal Count frozen contract

Active modules:

```text
mql5/Include/FlagCountingPhoenix/FP_InternalCountRules.mqh
mql5/Include/FlagCountingPhoenix/FP_InternalCountAudit.mqh
mql5/Include/FlagCountingPhoenix/FP_InternalCountEngine.mqh
```

Level 06 owns only post-body internal-count evidence. It does not create F1/F2/F3, does not authorize parent/child lifecycle transitions, and does not draw internal labels.

Directional rule:

```text
Bullish body => count adverse LOW nodes after Leg2
Bearish body => count adverse HIGH nodes after Leg2
```

Thresholds:

```text
0 => body exists, no post-flag count
1 => developing internal
2 => valid internal 1/2 exists
3/4 => extended internal branch evidence
```

A favorable strict break beyond Leg2 before valid internal 1/2 is extension, never confirmation. With extension absorption enabled, that break updates Leg2 and increments `leg2_extension_count`.

F1 keeps the stricter middle-node rule: the best opposite-side middle node between internal 1 and 2 must not break Leg2 before valid 1/2 is formed.

Each `FP_InternalPack` now carries:

```text
internal_pack_id
branch_id
branch_id_text
count
valid12
has_valid12
first_valid12_pos
first_valid12_node
middle_opposite_node
middle_opposite_breaks_leg2
pre_internal_leg2_extension_node
pre_internal_leg2_extension_pos
confirm_pos
invalid_pos
scan_start_pos
scan_end_pos
status
reason
```

`FP_LEVEL06` reports internal pack attempts, count distribution, valid12, confirmation-ready state, invalidations, pre-internal extensions, F1 middle-node rejections, non-deeper branch rejections, and F3 body-only completions.

---


### Level 07 — F1 Lifecycle frozen contract

Active modules:

```text
mql5/Include/FlagCountingPhoenix/FP_F1LifecycleRules.mqh
mql5/Include/FlagCountingPhoenix/FP_F1LifecycleAudit.mqh
mql5/Include/FlagCountingPhoenix/FP_F1LifecycleEngine.mqh
```

Level 07 is the first layer allowed to turn body/internal evidence into an F1 lifecycle state. Level 05 owns body facts. Level 06 owns internal-count evidence. Level 07 owns F1 candidate/post-flag/confirmed/invalidated state and F2 authorization.

Required F1 lifecycle fields on `FP_FlagEvent`:

```text
lifecycle_id
lifecycle_status
lifecycle_stage_level
lifecycle_phase_gate_passed
lifecycle_body_complete
lifecycle_internal_ready
lifecycle_can_spawn_f2
lifecycle_scan_start_pos
lifecycle_scan_end_pos
lifecycle_reason
```

F1 root authorization:

- Hook/ND phase-boundary roots pass the phase gate.
- Fail-open raw roots may pass only when fail-open is enabled and must remain tagged.
- Non-phase, non-fail-open roots are rejected when `require_f1_phase_boundary=true`.

F1 confirmation requires:

1. complete two-leg Level 05 body;
2. valid Level 06 internal 1/2;
3. later strict favorable Leg2 re-break;
4. no strict Waist break before confirmation.

A favorable Leg2 break before valid internal 1/2 is extension only and must not confirm F1. With absorption enabled, it updates the current Leg2 and increments `leg2_extension_count`.

F1 invalidates before confirmation only at strict Waist break. Equality is not invalidation.

F2 authorization is locked to Level 07:

```text
level == F1
status == confirmed
has_confirm == true
lifecycle_can_spawn_f2 == true
```

`FP_LEVEL07` is the current audit form. It must report root attempts, phase/fail-open attempts, gate pass/reject, body missing/complete, candidate/post-flag/confirmed/invalidated/extended states, visibility, hidden counts, F2-ready parents, duplicate rejection, emitted roots, and max extension count.

---

## 5. Interface decision

Current Phoenix uses these active shared structs:

```text
FP_Node
FP_InternalPack
FP_HookBranch
FP_FlagEvent
FP_Config
FP_DetectResult
```

The older interface names below are not required active structs:

```text
FP_FlagBody
FP_PhaseState
FP_AuditRecord
```

Their responsibilities are represented by `FP_FlagEvent`, canonical visibility fields, reason strings, and audit/export output. If separate structs are later introduced, they must be added through Level 01/03/11.5 and must not duplicate authority.

---

## 6. Validation policy

Validation has two phases:

1. **Baseline creation**: first accepted validation run records deterministic outputs for pinned chart ranges.
2. **Regression comparison**: later patches compare their output to the baseline and explain any expected change.

Do not fake expected counts without broker/range data. If a count is not yet baselined, mark the case as `baseline_required`, not `passed`.

---

## 7. Patch policy

Every future patch must state:

```text
Highest touched ladder level:
Canon version used: FLAG_COUNTING_CURRENT_CANON.md
Files touched:
Invariant preserved:
Invariant intentionally changed:
Tests/audit evidence:
Known limitations:
```

If a patch conflicts with this canon, update this canon first in a separate governance patch.
