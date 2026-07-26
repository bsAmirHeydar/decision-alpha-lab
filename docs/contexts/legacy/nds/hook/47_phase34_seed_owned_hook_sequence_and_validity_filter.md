# Phase 34 — Seed-Owned Hook Sequence and Validity-Filter Rebuild

## Purpose

This phase repairs the root Hook sequence-counting contract and adds a production visibility filter for valid Hook families.

The repair is based on the corrected manual doctrine:

```text
Build a raw same-side node list old-to-new.
Start the next sequence from the first raw node that has not participated in earlier accepted sequences.
Extend that sequence forward to the end of the raw list.
Every strict same-side continuation becomes the next sequence number.
A node that participated earlier cannot become node 1 of a later sequence.
A participated node may still appear later as continuation node 2/3/4 when the strict scan requires it.
```

## Why the previous behavior was wrong

The previous implementation behaved like an overlapping branch enumerator. It could produce a short sequence such as:

```text
A:1 -> B:2
```

and then later re-seed from `B` or another internal participant, producing another sequence:

```text
B:1 -> D:2
```

This is not the desired production interpretation. If valid continuation nodes exist after `B`, the original sequence should continue rather than terminating early.

## Positive Hook sequence rule

For a positive / low-side Hook, the raw material is a list of valleys ordered from old to new.

```text
raw = V0, V1, V2, ..., Vn
```

Within a Hook origin-boundary context:

```text
first unused valley -> node 1
next strictly lower valley -> node 2
next strictly lower valley -> node 3
next strictly lower valley -> node 4
... continue until raw list ends
```

## Negative Hook sequence rule

For a negative / high-side Hook, the raw material is a list of peaks ordered from old to new.

```text
raw = P0, P1, P2, ..., Pn
```

Within a Hook origin-boundary context:

```text
first unused peak -> node 1
next strictly higher peak -> node 2
next strictly higher peak -> node 3
next strictly higher peak -> node 4
... continue until raw list ends
```

## Seed-ownership rule

A node that participated in an accepted sequence is no longer allowed to be the seed of a later sequence.

```text
participated node cannot become node 1 again
```

This is not a full node exclusion rule. A previously participated node can still be used as a continuation node in a later sequence when the strict forward scan reaches it.

```text
participated node may become node 2/3/4 later
```

## Boundary context

The Hook origin / death boundary is not counted as node 1. It scopes the raw same-side node list. The counted sequence starts after the boundary.

The boundary remains the structural death line for the Hook context.

## Sequence length

The engine scans to the true terminal node. The compact chart label model still has readable display slots `1..4`. If the true sequence extends beyond four counted nodes, the sequence is marked capped while its resolve fields preserve the true terminal node.

This prevents premature termination while avoiding misleading re-seeding from internal nodes.

## Valid Hook families

The production-valid Hook families are:

```text
1. Hook After Hook
2. Hook After Opposing F3
```

### Hook After Hook

A Hook is valid after Hook when:

```text
previous_hook.resolve_node_id == current_hook.origin_node_id
```

This means the terminal node of the previous Hook becomes the origin node of the next Hook. The shared node is an origin/boundary for the next Hook, not node 1 of the next Hook.

### Hook After Opposing F3

A Hook is valid after opposing F3 when:

```text
completed_or_locked_F3.direction == -hook.direction
F3 completion time < hook start time
```

This turns a broad opposing F3 context into a valid Hook context.

## New inputs

```text
InpHookPhase02SeedUsedNodesCannotRestart = true
InpHookPhase02ShowOnlyValidHooks = false
```

When `InpHookPhase02ShowOnlyValidHooks` is true, Phase 02 semantic rendering hides unqualified Hook-like sequences and shows only Hooks qualified by the valid-family layer.

## Files changed

```text
mql5/Include/FlagCountingPhoenix/FP_HookPhase02Types.mqh
mql5/Include/FlagCountingPhoenix/FP_HookPhase02Rules.mqh
mql5/Include/FlagCountingPhoenix/FP_HookPhase02Engine.mqh
mql5/Include/FlagCountingPhoenix/FP_HookPhase02Visual.mqh
mql5/Include/FlagCountingPhoenix/FP_HookPhase02Export.mqh
mql5/Experts/FlagCounting/FlagCountingPhoenixExperiment.mq5
```

## Scope

This patch changes Hook Phase 02 sequence counting, Hook validity annotation, and Hook Phase 02 semantic visibility filtering. It does not change F1/F2/F3 canonical logic, Rally logic, broker behavior, execution, risk sizing, or live trading behavior.
