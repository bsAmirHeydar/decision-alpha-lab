# Phoenix Flag Counting Implementation Ladder V1

This document is part of the implementation ladder for the Phoenix Flag Counting engine.

Global non-negotiables:

- All structural decisions use candle `high` and `low` only.
- `open`, `close`, candle body, candle color, volume, and indicators are not structural inputs.
- Equality is not a break. A level is broken only by a strict pass beyond it.
- The renderer is non-authoritative. It may only draw logical objects emitted by engines.
- Main-chart rendering and audit rendering are separate products.
- Every layer must expose enough audit fields to prove why an object exists.
- A higher layer may never silently repair a lower-layer defect.

# Module Interface Contracts

## Purpose

This document defines Phoenix module boundaries. Each module owns one layer of truth. No module may silently redo another module's work.

The active interface source is aligned with the current Phoenix shared types in:

```text
mql5/Include/FlagCountingPhoenix/FP_Types.mqh
```

Do not require older placeholder structs unless they are introduced through a dedicated Level 01/03/11.5 patch.

---

## Active shared data structures

`FP_Types.mqh` currently owns:

```text
FP_Node
FP_InternalPack
FP_HookBranch
FP_FlagEvent
FP_Config
FP_DetectResult
```

Level 02 node audit modules additionally own:

```text
FP_NodeExtractConfig
FP_NodeExtractReport
FP_NodeCompressReport
FP_NodeSource
FP_NodeClearanceStatus
```

Level 03 identity modules additionally own:

```text
FP_IdentityReport
FP_Identity.mqh helper functions
FP_IdentityAudit.mqh sanity logs
```

Level 04 Hook/ND modules additionally own:

```text
FP_HookBuildReport
FP_HookAudit.mqh report and sample logs
FP_HookContext.mqh bounded-context validation helpers
```

These are the active interface objects.

The older names below are not active mandatory structs:

```text
FP_FlagBody
FP_PhaseState
FP_AuditRecord
```

Their responsibilities are currently represented by:

- `FP_FlagEvent` body anchors and lifecycle fields;
- `sequence_id`, `parent_event_id`, `parent_sequence_id`, `chain_index`;
- `visible_main`, `reason`, and audit/export output;
- `FP_DetectResult` summary counts.

If future code introduces separate `FP_FlagBody`, `FP_PhaseState`, or `FP_AuditRecord`, it must do so as a clear interface extension without duplicating authority.

---

## FP_Types.mqh

Owns shared enums, structs, reset helpers, and simple contract helpers.

Must contain or expose:

```text
FP_NodeKind
FP_Direction
FP_Level
FP_Status
FP_BranchKind
FP_RenderKind
FP_Node
FP_InternalPack
FP_HookBranch
FP_FlagEvent
FP_Config
FP_DetectResult
```

Must not contain complex detection algorithms.

---

## Level 02 node modules

Public facade:

```text
FP_NodeEngine.mqh
```

Private/owned submodules:

```text
FP_NodeExtractTypes.mqh
FP_NodePlateau.mqh
FP_NodeClearance.mqh
FP_NodeCanonicalizer.mqh
FP_NodeScaleList.mqh
FP_NodeAudit.mqh
```

Input:

```text
canonical Level 01 rates[]
L
config.include_pending_nodes
config.boundary_epsilon_points
```

Output:

```text
raw FP_Node nodes[]
canonical alternating FP_Node nodes[]
FP_NodeExtractReport
FP_NodeCompressReport
```

Owns:

- L-based node extraction;
- adjacent equal high/low plateau detection;
- high/low-only L-clearance scans;
- equality-skip semantics;
- confirmed versus pending node tagging;
- source tagging: `confirmed_history` versus `live_candidate`;
- chronological ordering and node IDs within each generated stream;
- same-side run compression to most extreme canonical node;
- Level 02 standalone node audit logs.

Must not call `CopyRates`. Must not emit Hook, ND, F1, F2, F3, sequence, visibility, or renderer objects.

---

## Level 03 identity modules

Public identity kernel:

```text
FP_Identity.mqh
```

Audit facade:

```text
FP_IdentityAudit.mqh
```

Input:

```text
FP_Node
FP_HookBranch
FP_FlagEvent
FP_Config context_symbol/context_timeframe/identity_config_hash
```

Output fields on emitted objects:

```text
structural_id
visual_id
phase_id
chain_id
audit_id
source_L or L
source_mode
is_fail_open
canonical_rank_score
visible_main
hidden_reason
```

Owns:

- deterministic node structural and visual ids;
- deterministic Hook/ND structural, visual, phase, and audit ids;
- deterministic F-event structural, visual, phase, chain, and audit ids;
- phase-safe visual merge predicates;
- hidden-reason normalization;
- `FP_LEVEL03` identity sanity report.

Must not:

- draw chart objects;
- create Hook/F events;
- decide final lifecycle state;
- use renderer object names as semantic ids.

## Level 04 Hook/ND modules

Public facade:

```text
FP_HookEngine.mqh
```

Owned submodules:

```text
FP_HookAudit.mqh
FP_HookContext.mqh
```

Input:

```text
canonical Level 02 FP_Node nodes[]
FP_Config config
```

Output:

```text
FP_HookBranch hooks[]
FP_HookBuildReport report
```

Owns:

- bounded same-side Hook/ND contexts;
- cycle-start strict-break validation;
- branch node count distribution;
- adaptive-L acceptance/rejection reason;
- retracement ratio and threshold rejection;
- cycle start, cycle extreme, and resolve node fields;
- seeded visible-F1 marking;
- Hook/ND reason strings and `FP_LEVEL04` audit logs.

Must not emit F1/F2/F3 events. It may provide phase-boundary context through `FP_HookBranch` fields only. It must not call `CopyRates` or draw renderer objects.

---

## FP_FlagBodyRules.mqh

Input:

```text
FP_Node
direction
epsilon
```

Output:

```text
pure boolean predicates and body identity helpers
```

Owns strict Origin/Leg/Waist/Leg2 predicates, equality-is-not-break checks, body size, and body id construction. It must not scan sequences, build hooks, confirm flags, or draw objects.

---

## FP_FlagBodyAudit.mqh

Input:

```text
FP_FlagBodyBuildReport
FP_FlagEvent body samples
```

Output:

```text
FP_LEVEL05 structured logs
```

Owns body build counters, body sample logs, extension absorption counters, and first/last body failure reasons. It must not decide body validity.

---

## FP_FlagBodyEngine.mqh

Input:

```text
FP_Node nodes[]
root node or root candidate context
FP_Config config
```

Output:

```text
FP_FlagEvent body-stage event
FP_FlagBodyBuildReport audit evidence
```

Current Phoenix represents the flag body inside `FP_FlagEvent` using:

```text
origin
leg1
waist
leg2
has_origin
has_leg1
has_waist
has_leg2
pos_origin
pos_leg1
pos_waist
pos_leg2
flag_size
body_id
body_status
origin_hit_status
leg1_break_status
leg2_extension_count
body_scan_start_pos
body_scan_end_pos
body_reason
reason
```

Owns:

- `Origin -> Leg1 -> Waist -> Leg2` construction;
- strict Leg2 break;
- Origin/waist boundary checks during body formation;
- pre-internal Leg2 extension absorption where applicable.

Must not confirm F1 or authorize F2/F3. It may emit probable child body stages for audit, but sequence lifecycle layers decide whether those are visible/usable.

---

## FP_InternalCountRules.mqh / FP_InternalCountAudit.mqh / FP_InternalCountEngine.mqh

Input:

```text
FP_FlagEvent body_event
FP_Node canonical_nodes[]
FP_Config config
```

Output:

```text
FP_InternalPack internal_pack
FP_InternalCountBuildReport report
```

Owns:

- post-Leg2 adverse internal 1/2/3/4 scanning;
- strict adverse branch progression;
- best opposite middle-node selection between adverse nodes;
- F1-specific middle-node rejection before valid 1/2;
- pre-internal Leg2 extension evidence and absorption helper;
- `valid12`, first valid 1/2 position, confirm support position, invalid support position;
- `FP_LEVEL06` report and optional internal samples.

Required active fields:

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

Must not create F1/F2/F3, authorize F2/F3 parents, decide sequence ownership, or draw internal labels.

---


## FP_F1LifecycleRules.mqh / FP_F1LifecycleAudit.mqh / FP_F1LifecycleEngine.mqh

Input:

```text
FP_Node canonical_nodes[]
FP_FlagEvent body_event from Level 05
FP_InternalPack / Level 06 internal evidence
FP_Config config
```

Output:

```text
FP_FlagEvent level=F1 with lifecycle fields
FP_F1LifecycleBuildReport report
```

Owns:

- F1 phase-gate pass/reject;
- fail-open tagging at the lifecycle layer;
- F1 candidate/post-flag/confirmed/invalidated semantic state;
- F1-only Waist invalidation before confirmation;
- F1 confirmation after valid internal 1/2 and later Leg2 strict re-break;
- F1 pre-internal Leg2 extension absorption as lifecycle evidence;
- `lifecycle_can_spawn_f2` authorization;
- `FP_LEVEL07` report and optional lifecycle samples.

Required active fields:

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

Must not build F2/F3, decide phase ownership across competing sequences, perform duplicate canonicalization, or draw renderer objects.

---


## FP_F2LifecycleRules.mqh / FP_F2LifecycleAudit.mqh / FP_F2LifecycleEngine.mqh

Input:

```text
FP_Node canonical_nodes[]
FP_FlagEvent confirmed F1 parent from Level 07
FP_Config config
Level 05 body service
Level 06 internal-count service
```

Output:

```text
FP_FlagEvent level=F2 with f2 lifecycle fields
FP_F2LifecycleBuildReport report
```

Owns:

- F2 parent gate from `lifecycle_can_spawn_f2`;
- deepest adverse F2 origin backfill between F1 Leg2 and F1 confirmation;
- F2 parent-size gate and size ratio evidence;
- F2 candidate/post-flag/confirmed/invalidated semantic state;
- F2-only Origin invalidation before confirmation;
- F2 confirmation after valid internal 1/2 and later Leg2 strict re-break;
- F2 pre-internal Leg2 extension absorption as lifecycle evidence;
- `f2_can_spawn_f3` authorization;
- `FP_LEVEL08` report and optional lifecycle samples.

Required active fields:

```text
f2_lifecycle_id
f2_lifecycle_status
f2_parent_ready
f2_origin_found
f2_body_complete
f2_size_gate_passed
f2_internal_ready
f2_can_spawn_f3
f2_origin_scan_start_pos
f2_lifecycle_scan_end_pos
f2_parent_size_ratio
f2_lifecycle_reason
```

Must not build F3, decide cross-sequence phase ownership, perform duplicate canonicalization, or draw renderer objects.

---

## FP_F3LifecycleRules.mqh / FP_F3LifecycleAudit.mqh / FP_F3LifecycleEngine.mqh

Input:

```text
FP_Node canonical_nodes[]
FP_FlagEvent confirmed and F3-authorized F2 parent from Level 08
FP_Config config
Level 05 body service
```

Output:

```text
FP_FlagEvent level=F3 with f3 lifecycle fields
FP_F3LifecycleBuildReport report
```

Owns:

- F3 parent gate from `f2_can_spawn_f3`;
- deepest adverse F3 origin backfill between F2 Leg2 and F2 confirmation;
- terminal F3 body construction;
- OR qualification by parent-size ratio or parent-L ratio;
- F3 completed versus OR-rejected state;
- F3 lock readiness and lock evidence;
- first opposite confirmed F1 lock scan;
- `FP_LEVEL09` construction report;
- `FP_LEVEL09_LOCK` cross-sequence lock report.

Required active fields:

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
f3_origin_scan_start_pos
f3_lifecycle_scan_end_pos
f3_parent_size_ratio
f3_parent_leg1_L_ratio
f3_lock_event_id
f3_lock_reason
f3_lifecycle_reason
```

Must not decide same-direction restart ownership, duplicate canonicalization across L-scales, renderer labels, or execution signals.

---
## FP_SequenceEngine.mqh

Input:

```text
FP_Node nodes[]
FP_HookBranch hooks[]
body/internal services or lower-level builder functions
FP_Config config
```

Output:

```text
FP_FlagEvent raw_events[]
FP_FlagEvent visible_events[] or visible_main flags on raw_events[]
FP_DetectResult summary
```

Owns:

- wiring Level 07 F1 lifecycle output into parent/child sequence construction;
- wiring Level 08 F2 lifecycle output into F3 authorization;
- wiring Level 09 F3 lifecycle output into terminal chain state;
- parent-child links;
- phase ownership;
- same-direction root control;
- semantic canonicalization;
- main visibility decisions;
- hidden reasons.

Must not draw chart objects.

---

## FP_Audit.mqh

Input:

```text
FP_Node nodes[]
FP_HookBranch hooks[]
FP_FlagEvent raw_events[]
FP_FlagEvent visible_events[] or visible_main flags
FP_DetectResult summary
FP_Config config
```

Output:

```text
structured logs
CSV/JSON export when implemented
debug summaries
```

Owns:

- raw versus visible count reporting;
- hidden reason reporting;
- fail-open tag reporting;
- canonical winner reporting;
- deterministic output ordering for audit/export.

Must not change engine decisions.

---

## FP_Renderer.mqh

Input:

```text
visible_events[]
visible_hooks[] or hooks filtered by canonical/display profile
rates[]
visual config flags
```

Output:

```text
chart objects only
```

Must not:

- change event status;
- change `visible_main`;
- invent missing structures;
- hide semantically visible objects except by explicit display-budget directives already provided by canonicalization/audit layer.

---

## FlagCountingPhoenixExperiment.mq5

Owns:

- user inputs;
- rate copying;
- config construction;
- module call orchestration;
- cleanup and renderer invocation;
- debug/audit toggles.

Must not contain hidden business logic that belongs in include modules.

---

## Forbidden cross-module dependencies

- Renderer querying raw bars to create new structures.
- HookEngine creating F events.
- FlagBodyEngine deciding sequence phase ownership.
- InternalCountEngine authorizing F2/F3.
- NodeEngine knowing about F1/F2/F3.
- Audit code mutating visible objects.
- Expert `.mq5` bypassing module contracts with ad hoc fixes.

---

## Module call order

```text
Copy rates
-> build FP_Config
-> NodeEngine for each L
-> HookEngine context scan
-> FlagBodyEngine body services
-> InternalCountEngine post-body services
-> SequenceEngine lifecycle + ownership + canonical visibility
-> FP_Audit structured report/export
-> FP_Renderer draw
```

---

## Interface freeze checklist

Before a layer is frozen:

- Every output object has `structural_id`, `visual_id`, `phase_id`, `chain_id` where applicable, and `audit_id`.
- Every hidden object has `hidden_reason`.
- Every parent-child link is explicit.
- Raw events and visible events are distinguishable.
- Every module can be tested without renderer.
- No module has ambiguous authority.
