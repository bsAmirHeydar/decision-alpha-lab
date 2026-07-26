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
2. `docs/contexts/legacy/flag_counting/FLAG_COUNTING_SEQUENCE_CONTRACT_V4.md` — semantic sequence contract.
3. `docs/contexts/legacy/flag_counting/FLAG_COUNTING_ENGINEERING_PACK_V5.md` and `docs/contexts/legacy/flag_counting/engineering_pack_v5/` — definitions, algorithms, and explanations.
4. `docs/contexts/legacy/flag_counting/implementation_ladder_v1/` — implementation order, interfaces, acceptance gates, and freeze protocol.
5. `docs/contexts/legacy/flag_counting/phoenix_rebuild/` — Phoenix-specific repair notes. These are valid only where they do not conflict with this canon.
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

Default phase handling is hybrid:

- hard/theoretical reset still requires opposite completed/locked F3 evidence;
- visual/working reset may start a new visible phase after an opposite confirmed F1 or confirmed F2 appears;
- the reset reason must state whether it is `reset_by_opposite_terminal_f3` or `visual_soft_reset_by_opposite_confirmed_F1/F2`;
- same-direction F1 ownership is not reset by a failed same-direction F2/F3 child.

This keeps the strict terminal theory intact while allowing the current chart state to show an active opposite structure before the full opposite F3 has completed.

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

Default main chart is **full-state diagnostic**:

- Show all F1/F2/F3 lifecycle states emitted by the engine, including live body, post-flag, size-rejected, and OR-rejected states.
- Show all Hook/ND contexts by default, seeded or unseeded.
- Clean/canonical-only output is a named release/render profile, not the default research view.
- Display does not change semantic authorization: undersized F2 cannot spawn F3, OR-rejected F3 cannot lock, and hidden ownership/canonical objects still obey engine rules.

Optional clean profiles may hide detail, but they must not change emitted logical events:

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

- F2 origin is backfilled from the deepest adverse correction after final F1 Leg2 and before F1 confirmation; F2 Leg1 is forced to the F1 confirmation hit.
- F3 origin is backfilled from the deepest adverse correction after final F2 Leg2 and before F2 confirmation; F3 Leg1 is forced to the F2 confirmation hit.
- Waist and Leg2 for the child flag may only be built after the parent confirmation hit.

Extended post-confirmation backfill may exist only behind a named diagnostic input and must be visible in audit.

### 4.8 F2 size and F3 authorization

Default:

- F2 candidate may exist in audit before size qualification.
- F2 size qualification controls F3 authorization, not default visibility. Size-rejected F2 may be displayed in the default full-state research view, but it must not set `f2_can_spawn_f3=true`.
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
- Default research chart shows all Hook/ND contexts, seeded or unseeded. Clean profiles may restrict Hook/ND to seeded visible F1 contexts.
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

---

## Level 08 implementation freeze — F2 lifecycle

Level 08 turns F2 from an implicit `SequenceEngine` child helper into a dedicated lifecycle layer. The active authority is:

```text
FP_F2LifecycleRules.mqh
FP_F2LifecycleAudit.mqh
FP_F2LifecycleEngine.mqh
```

`FP_SequenceEngine.mqh` may orchestrate calls, but it must not own F2 semantic decisions.

F2 parent authorization is now locked to Level 07 F1 lifecycle output:

```text
parent.level == F1
parent.status == confirmed
parent.has_confirm == true
parent.lifecycle_can_spawn_f2 == true
```

F2 origin is the deepest adverse node in the strict backfill window after final F1 Leg2 and before F1 confirmation. Nodes after F1 confirmation are not eligible F2 origins. F1 is not finished for child spawning until its own flag end is re-hit/confirmed. Therefore F2 may backfill only its Origin into the parent correction window; F2 Leg1 is forced to the F1 confirmation node, then Waist/Leg2 construction starts after that confirmation.

F2 size qualification is explicit:

```text
f2_size_gate_passed = F2.flag_size >= cfg.f2_min_parent_size_ratio * F1.flag_size
```

An undersized F2 may be counted and displayed in the default full-state research view, but it must not set `f2_can_spawn_f3=true`. Clean profiles may hide size-rejected F2 candidates.

F2 confirmation requires Level 06 evidence:

```text
valid internal 1/2 after F2 Leg2
+ later strict favorable Leg2 re-break
+ no strict F2 Origin break before confirmation
```

F2 invalidates at its own Origin, not Waist. Equality remains non-breaking.

F3 authorization is now locked to Level 08:

```text
level == F2
status == confirmed
has_confirm == true
f2_size_gate_passed == true
f2_can_spawn_f3 == true
```

`FP_LEVEL08` is the current audit form for F2. It must report parent attempts, parent-ready/rejected state, origin scan/found/missing state, body missing/complete state, size pass/reject, candidate/post-flag/confirmed/invalidated states, visibility, hidden counts, F3-ready children, emitted children, duplicate rejection, and max extension count.

---

## Level 09 implementation freeze — F3 lifecycle / terminal lock

Level 09 turns F3 from an implicit `SequenceEngine` helper into a dedicated terminal lifecycle layer. The active authority is:

```text
FP_F3LifecycleRules.mqh
FP_F3LifecycleAudit.mqh
FP_F3LifecycleEngine.mqh
```

`FP_SequenceEngine.mqh` may orchestrate calls, but it must not own F3 semantic decisions.

F3 parent authorization is now locked to Level 08 F2 lifecycle output:

```text
parent.level == F2
parent.status == confirmed
parent.has_confirm == true
parent.f2_size_gate_passed == true
parent.f2_can_spawn_f3 == true
```

F3 origin is the deepest adverse node in the strict backfill window after final F2 Leg2 and before F2 confirmation. Nodes after F2 confirmation are not eligible F3 origins in Level 09. F2 is not finished until its own flag end is re-hit/confirmed; therefore F3 may not choose a Leg1 before the F2 confirmation node. The F3 body is backfilled to the correction origin, but its Leg1 is forced to the F2 confirmation node, then normal Waist/Leg2 body construction resumes.

F3 is terminal only after a complete `Origin -> Leg1 -> Waist -> Leg2` body. It does not require a post-body internal 1/2, but the OR completion gate is not allowed to complete or lock a live/probable F3 that has no Waist/Leg2 yet. Completion is controlled by the OR contract after the body is complete:

```text
F3.flag_size >= cfg.f3_min_parent_size_ratio * F2.flag_size
OR
F3.leg1_L >= ceil(cfg.f3_leg1_L_min_ratio * F2.leg1_L)
```

A live/probable F3 body candidate and an OR-rejected complete F3 candidate may be displayed in the default full-state research view, but neither may set `f3_terminal_complete=true` and neither may lock. Clean profiles may hide OR-rejected/live F3 candidates.

Completed F3 locks only on the first opposite confirmed F1 after F3 completion. Lock evidence is carried by:

```text
f3_locked
f3_lock_ready
f3_lock_event_id
f3_lock_reason
extension_end
status = locked
f3_lifecycle_status = locked
```

`FP_LEVEL09` is the construction/OR audit form. `FP_LEVEL09_LOCK` is the cross-sequence lock audit form. Both must be available before Level 10 ownership and phase reset work is considered frozen.

---

## Level 10 implementation freeze — sequence ownership / phase reset

Level 10 turns Phoenix from a lifecycle candidate enumerator into a semantic phase owner engine. The active authority is:

```text
FP_OwnershipTypes.mqh
FP_OwnershipRules.mqh
FP_OwnershipAudit.mqh
FP_OwnershipEngine.mqh
```

`FP_SequenceEngine.mqh` may orchestrate calls, but Level 10 owns main-chart phase truth. Renderer and visual duplicate pruning are not allowed to decide phase ownership.

Every emitted F event now carries Level 10 ownership evidence:

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

Main-chart contract:

```text
one direction / one active phase / one canonical F1 owner
```

A later same-direction F1 root in the same phase is hidden unless a completed/locked opposite F3 exists between the current owner and the later root. That opposite terminal F3 is the strict phase reset evidence.

Competing root ranking is semantic, not visual:

1. chain has locked F3;
2. chain has completed F3;
3. chain has confirmed and size-qualified F2;
4. chain has confirmed F1;
5. root is Hook/phase-boundary derived;
6. root is not fail-open;
7. lower/local L if semantic quality is equal;
8. earliest valid root;
9. deterministic id tie-break.

If a root loses ownership, all descendants in that sequence must be hidden. F2/F3 orphans are hidden after ownership. Fail-open roots inside a Hook-owned phase region are audit-visible but hidden from the main chart.

`FP_LEVEL10` is the ownership audit form. It must report visible-before/after, root candidates, owner roots, competing roots, strict resets, hidden roots, hidden descendants, fail-open hides, superseded parent hides, orphan hides, and rank range.

---

## Level 11 implementation freeze — canonicalization / audit invariants

Level 11 is the final engine-owned consistency pass before renderer and export/report layers. The active authority is:

```text
FP_CanonicalTypes.mqh
FP_CanonicalRules.mqh
FP_CanonicalAudit.mqh
FP_Canonicalizer.mqh
```

`FP_SequenceEngine.mqh` may orchestrate the pass, but Level 11 owns final pre-render stream integrity. Renderer is still non-authoritative and must not repair visibility, parent linkage, hidden reasons, or duplicate conflicts.

Level 11 does **not** create new market structure. It only normalizes structures already emitted by Node, Hook, Body, Internal Count, F1/F2/F3 lifecycle, and Level 10 ownership.

Every F event now carries final canonical evidence:

```text
canonical_id
canonical_state
canonical_rank_final
canonical_conflict_group_id
canonical_invariant_flags
canonical_reason
```

Canonical states:

```text
visible
hidden
hidden_duplicate
hidden_orphan
hidden_invalid
repaired
invariant_failed
```

Level 11 must enforce these invariants before the renderer is trusted:

```text
1. every hidden event has hidden_reason
2. visible events do not carry stale hidden_reason
3. visible F2/F3 descendants have visible parents
4. visible F1 owners have phase_owner_root_id
5. visible events have structural_id, visual_id, phase_id, chain_id, audit_id
6. phase-safe visible duplicate geometry is hidden deterministically
7. malformed visible bodies are hidden, not drawn
8. invalidated events are hidden unless audit display explicitly asks for them
9. hook hidden-state has a hidden_reason
10. final identity is rebuilt after canonicalization
```

The final pipeline after Level 10 is:

```text
ownership result
-> old compatibility duplicate pruning
-> provisional Hook seed visibility
-> Level 11 canonicalization
-> final Hook seed visibility
-> final identity assignment
-> FP_LEVEL11 audit
-> renderer/export
```

`FP_LEVEL11` is the canonicalization audit form. It must report visible-before/after, hidden-before/after, repaired IDs, repaired parent links, repaired hidden reasons, duplicate groups, duplicates hidden, orphan hides, malformed-body hides, invalid hides, invariant failures, post-canonical duplicate conflicts, and rank range.

If `canonical_strict_invariants=true`, any `FP_LEVEL11 status=failed` means the renderer output is diagnostic only and must not be treated as canonical research evidence until the invariant failure is fixed.

---

## Level 11.5 implementation freeze — raw audit export / report engine

Level 11.5 is the first file-based audit/report layer. It sits after Level 11 canonicalization and before Level 12 renderer/layout:

```text
Level 11 canonical stream
-> Level 11.5 raw audit export/report
-> Level 12 renderer
```

The active authority is:

```text
FP_ExportTypes.mqh
FP_ExportRows.mqh
FP_ExportEngine.mqh
```

`FlagCountingPhoenixExperiment.mq5` owns only input wiring and the call site. The export layer is read-only and may not mutate events, hooks, identity, visibility, parent links, hidden reasons, chart objects, or renderer state.

Default export is disabled:

```text
InpExportAuditFiles = false
```

When enabled, Phoenix writes CSV files under:

```text
MQL5/Files/FlagCountingPhoenix/
```

Default file mode writes deterministic latest files:

```text
latest_events.csv
latest_hooks.csv
latest_summary.csv
latest_manifest.csv
```

If `InpExportOverwriteLatest=false`, file names include the run id. `InpExportRunTag` may force a stable run id for validation packs.

Required Level 11.5 output groups:

```text
events.csv      # full canonical event stream, visible and hidden unless visible-only is enabled
hooks.csv       # full Hook/ND stream, visible and hidden unless visible-only is enabled
summary.csv     # one-row aggregate counter snapshot
manifest.csv    # run metadata, input hash, generated file paths, row counts
FP_LEVEL11_5    # terminal sanity log for export status
```

Export must preserve hidden structures by default. `InpExportVisibleOnly=true` is a convenience filter only; it must never change engine output.

Every exported event row must include identity, lifecycle, ownership, canonicalization, hidden reason, node geometry, and body/internal evidence. This makes the CSV a research object, not just a renderer dump.

`FP_SUMMARY` now includes export counters:

```text
export_attempted
export_ok
export_files
export_errors
export_events
export_events_visible
export_events_hidden
export_hooks
export_hooks_visible
export_hooks_hidden
```

Level 11.5 is frozen when renderer can be disabled and the same canonical event/hook stream can still be inspected from the exported files.


## Level 12 renderer

Phoenix Level 12 is a read-only visual layer. It consumes the Level 11 canonical stream and draws chart objects after Level 11.5 export. It may apply display filters, but it cannot create or modify semantic truth.

Active renderer modules:

```text
mql5/Include/FlagCountingPhoenix/FP_RenderTypes.mqh
mql5/Include/FlagCountingPhoenix/FP_RenderRules.mqh
mql5/Include/FlagCountingPhoenix/FP_RenderAudit.mqh
mql5/Include/FlagCountingPhoenix/FP_Renderer.mqh
```

Default renderer contract:

```text
InpRenderStrictVisibility = true
InpRenderUseCanonicalObjectNames = true
InpRenderDeleteExistingByPrefix = true
InpRenderDrawHookBack = true
InpPrintRenderSanity = true
```

`FP_LEVEL12` is the renderer sanity line. `FP_SUMMARY` must include render counters so chart-object problems are visible without trusting the chart visually.

## Level 13 validation is active

Phoenix Level 13 is now the official validation harness for the canonical stream.

Active modules:

```text
mql5/Include/FlagCountingPhoenix/FP_ValidationTypes.mqh
mql5/Include/FlagCountingPhoenix/FP_ValidationRules.mqh
mql5/Include/FlagCountingPhoenix/FP_ValidationAudit.mqh
mql5/Include/FlagCountingPhoenix/FP_ValidationEngine.mqh
```

Execution order:

```text
Level 11 canonicalization
-> Level 11.5 export/report
-> Level 12 renderer
-> Level 13 validation
-> FP_SUMMARY
```

Level 13 is read-only. It may only inspect the final canonical event/hook stream and aggregate counters. It must not change renderer output, export output, identity, hidden reasons, lifecycle status, ownership, or canonicalization.

Expected counts must come from MT5 baselines. Documentation must not invent them. New cases start with `InpValidationBaselineMode=true`; accepted cases then copy actual counts into the expected min/max inputs.


## Level 14 release/debug/rollback layer

Phoenix now includes `FP_ReleaseTypes.mqh`, `FP_ReleaseRules.mqh`, `FP_ReleaseAudit.mqh`, and `FP_ReleaseEngine.mqh`. The active EA exposes `InpReleaseProfile` with `normal`, `clean_main`, `audit_export`, `validation`, `debug_max`, `render_off`, and `safe_rollback` profiles. Level 14 writes `latest_release.csv` and prints `FP_LEVEL14`; it does not mutate market structure.

## Level 15 module interface contract layer

Phoenix now includes an implementation-backed interface contract layer:

```text
FP_InterfaceTypes.mqh
FP_InterfaceRules.mqh
FP_InterfaceAudit.mqh
FP_InterfaceEngine.mqh
```

Level 15 is read-only. It runs preflight checks after Level 14 profile overrides and postflight checks after Level 14 final release reporting. It validates the integration boundary rather than market structure itself.

The preflight pass freezes active assumptions around enums, constants, identity generation pass, context metadata, config bounds, and dependency-facing settings. The postflight pass checks final stream counters, event partition, visible parent continuity, public identity coverage, and non-negative result counters.

Level 15 emits `FP_LEVEL15_PRE` and `FP_LEVEL15`. Optional CSV output writes `latest_interface_pre.csv` and `latest_interface_post.csv` under the configured interface folder.

The active identity generation pass is now:

```text
phoenix_level17
```

Level 15 may only report interface status and add interface counters to `FP_DetectResult`; it may not mutate events, hooks, identities, ownership, canonical state, renderer objects, export files, validation decisions, or release gate semantics.


## Level 16 acceptance matrix layer

Phoenix now includes an implementation-backed acceptance matrix layer:

```text
FP_AcceptanceTypes.mqh
FP_AcceptanceRules.mqh
FP_AcceptanceAudit.mqh
FP_AcceptanceEngine.mqh
```

Level 16 is read-only. It aggregates the Level 01 timebase report, Level 02-11 counters, Level 11.5 export report, Level 12 render report, Level 13 validation report, Level 14 release report, and Level 15 interface reports into one operator-facing acceptance matrix. It cannot mutate events, hooks, identities, visibility, hidden reasons, lifecycle state, ownership state, canonical state, export files, release decisions, or renderer objects.

Default execution order is now:

```text
Level 14 profile pre-apply
-> Level 15 preflight
-> Level 01 timebase
-> Levels 02-11 detection/canonicalization
-> Level 11.5 export
-> Level 12 renderer
-> Level 13 validation
-> Level 14 release gate
-> Level 15 postflight
-> Level 16 acceptance matrix
-> FP_SUMMARY
```

The active identity generation pass is now:

```text
phoenix_level17
```

Level 16 emits `FP_LEVEL16`. Optional CSV output writes:

```text
MQL5/Files/FlagCountingPhoenix/latest_acceptance.csv
```

Acceptance modes are `observe`, `baseline`, `regression`, and `release`. Baseline mode may warn with actual counts that must be copied into validation/acceptance case files; it must not invent expected values. Regression and release modes only pass when configured hard gates pass.

## Level 17 runtime decision lock

The ambiguity list is no longer an open design document. Phoenix Level 17 turns
it into a runtime decision registry backed by:

```text
mql5/Include/FlagCountingPhoenix/FP_AmbiguityTypes.mqh
mql5/Include/FlagCountingPhoenix/FP_AmbiguityRules.mqh
mql5/Include/FlagCountingPhoenix/FP_AmbiguityAudit.mqh
mql5/Include/FlagCountingPhoenix/FP_AmbiguityEngine.mqh
```

The active identity pass is:

```text
phoenix_level17
```

Level 17 is read-only and runs after Level 16 acceptance. It audits decision
alignment and does not mutate structure, renderer state, export state,
validation state, release state, acceptance state, or interface reports.


## Level 18 static QA canon addendum

The official post-ladder hardening layer is Level 18. Phoenix runtime must use `identity_generation_pass=phoenix_level18` and `FP_INTERFACE_CONTRACT_VERSION=18.00`. Level 18 is read-only and may only report static QA / compile-hardening state through `FP_LEVEL18` and optional `latest_static_qa.csv`. Source-side checks are performed with `tools/flag_counting/static_qa.py`.

## Offline runtime license decision lock

Phoenix now has a fail-closed offline license gate for distributable EX5 builds. The gate runs before Level 01 and on a timer during runtime. The visible inputs are intentionally neutral operational names rather than obvious license names:

- `InpPhaseModelProfile`: signed token
- `InpRenderMemo`: passphrase/password
- `InpNodeModelSeed`, `InpBoundaryModelSeed`, `InpValidationModelSeed`, `InpReleaseModelSeed`: hidden numeric gates
- `InpSessionCacheDepth`: periodic recheck interval in minutes

The license token binds product, account login, optional server hash, expiry date, feature flags, nonce, and signature. The numeric gates are derived from the same payload and passphrase. The license layer is operational only and is not a market-structure layer.
