# Phoenix Flag Counting Implementation Ladder V1

This document is part of the implementation ladder for the Phoenix Flag Counting engine. The ladder is intentionally layered so that lower layers become frozen foundations before higher layers are allowed to depend on them.

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

This document defines module boundaries. Each module owns one layer of truth. No module may silently redo another module's work.

## FP_Types.mqh

Owns shared data structures and config.

Must contain:

```text
FP_Node
FP_HookBranch
FP_FlagBody
FP_InternalPack
FP_FlagEvent
FP_PhaseState
FP_AuditRecord
FP_Config
```

Must not contain complex detection algorithms.

## FP_NodeEngine.mqh

Input:

```text
rates[]
L
config
```

Output:

```text
FP_Node nodes[]
```

May use candle highs/lows. Must not emit F structures.

## FP_HookEngine.mqh

Input:

```text
nodes[]
rates[] for strict boundary hit checks if documented
config
```

Output:

```text
FP_HookBranch hooks[]
```

Must not emit F1/F2/F3. May propose root candidates through explicit fields.

## FP_FlagBodyEngine.mqh

Input:

```text
nodes[]
root candidates
config
```

Output:

```text
FP_FlagBody bodies[]
```

Must not confirm F1 or authorize F2/F3.

## FP_InternalCountEngine.mqh

Input:

```text
FP_FlagBody body
nodes[]
config
```

Output:

```text
FP_InternalPack internal_pack
```

Must not create F2/F3.

## FP_SequenceEngine.mqh

Input:

```text
nodes[]
hooks[]
bodies/internal packs or services to build them
config
```

Output:

```text
FP_FlagEvent events[]
visible_events[] after canonicalization
```

Owns:

- F1 lifecycle;
- F2 lifecycle;
- F3 lifecycle;
- phase ownership;
- sequence parent-child links;
- canonical visibility.

Must not draw chart objects.

## FP_Renderer.mqh

Input:

```text
visible_events[]
visible_hooks[]
rates[]
config visual flags
```

Output:

```text
chart objects only
```

Must not change event status or visibility.

## FP_Audit.mqh

Input:

```text
nodes[]
hooks[]
events[]
visibility decisions
```

Output:

```text
logs / labels / debug records
```

Must not change engine decisions.

## FlagCountingPhoenixExperiment.mq5

Owns:

- inputs;
- copying rates;
- calling modules in correct order;
- cleaning and drawing through renderer;
- exposing debug mode.

Must not contain hidden business logic that belongs in include modules.

## Forbidden cross-module dependencies

- Renderer querying raw bars to create new structures.
- HookEngine creating F events.
- FlagBodyEngine deciding sequence phase ownership.
- NodeEngine knowing about F1/F2/F3.
- Audit code mutating visible objects.
- Expert `.mq5` bypassing module contracts with ad hoc fixes.

## Module call order

```text
Copy rates
-> NodeEngine for each L
-> HookEngine context scan
-> FlagBodyEngine root/body scan
-> InternalCountEngine body post-processing
-> SequenceEngine lifecycle + ownership
-> Canonicalization + visibility
-> Audit record generation
-> Renderer draw
```

## Interface freeze checklist

Before coding:

- Every output object has identity.
- Every hidden object has reason.
- Every parent-child link is explicit.
- Every module can be tested without renderer.
- No module has ambiguous authority.
