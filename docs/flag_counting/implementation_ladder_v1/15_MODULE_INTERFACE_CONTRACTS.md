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

## FP_NodeEngine.mqh

Input:

```text
rates[]
L
config.include_pending_nodes
config.boundary_epsilon_points
```

Output:

```text
FP_Node nodes[]
```

Owns:

- L-based node extraction;
- plateau handling;
- high/low-only rules;
- confirmed versus pending node tagging;
- node ordering and node IDs within the generated stream.

Must not emit Hook, ND, F1, F2, F3, sequence, visibility, or renderer objects.

---

## FP_HookEngine.mqh

Input:

```text
FP_Node nodes[]
rates[] only for documented strict boundary hit checks
FP_Config config
```

Output:

```text
FP_HookBranch hooks[]
```

Owns:

- branch-based Hook/ND context;
- branch node count;
- adaptive-L acceptance/rejection reason;
- retracement ratio;
- cycle start and resolve identity;
- Hook/ND reason strings.

Must not emit F1/F2/F3 events. It may provide phase-boundary context through `FP_HookBranch` fields only.

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
FP_FlagEvent body-stage event or service result
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
reason
```

Owns:

- `Origin -> Leg1 -> Waist -> Leg2` construction;
- strict Leg2 break;
- Origin/waist boundary checks during body formation;
- pre-internal Leg2 extension absorption where applicable.

Must not confirm F1 or authorize F2/F3.

---

## FP_InternalCountEngine.mqh

Input:

```text
FP_FlagEvent body_event
FP_Node nodes[]
FP_Config config
```

Output:

```text
FP_InternalPack internal_pack
```

Owns:

- post-Leg2 internal 1/2/3/4 scanning;
- normal internal branch;
- waist-break branch representation where applicable;
- `valid12` and ND-related internal-pack fields;
- confirmation support data.

Must not create F2/F3 or decide sequence ownership.

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

- F1 lifecycle;
- F2 lifecycle;
- F3 lifecycle;
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

- Every output object has identity.
- Every hidden object has reason.
- Every parent-child link is explicit.
- Raw events and visible events are distinguishable.
- Every module can be tested without renderer.
- No module has ambiguous authority.
