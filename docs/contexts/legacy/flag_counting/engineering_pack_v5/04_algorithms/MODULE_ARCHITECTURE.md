# Module Architecture

## Target Modules

```text
FCN_NodeProviderAdapter
FCN_NodeViewCache
FCN_FlagBodyBuilder
FCN_PostFlagContextTracker
FCN_HookBranchEngine
FCN_SequenceEngine
FCN_F1StateMachine
FCN_F2StateMachine
FCN_F3StateMachine
FCN_IdentityDeduplicator
FCN_AuditEmitter
FCN_RenderModelBuilder
FCN_Renderer
```

## 1. NodeProviderAdapter

Responsibility:

- call existing project node module;
- provide high/low nodes by L;
- preserve node identity;
- expose plateau metadata if available.

Must not:

- reinvent node rules;
- use open/close;
- expire nodes.

## 2. NodeViewCache

Responsibility:

- cache NodeView(L);
- allow L increase for hook readability;
- supply nodes in chronological order.

## 3. FlagBodyBuilder

Responsibility:

- build candidate flag bodies from an owned origin/context;
- maintain Leg1 extreme;
- maintain Waist extreme;
- detect Leg2 pass;
- handle Leg2 extension where applicable.

Must not:

- decide F1/F2/F3 confirmation;
- start arbitrary origins.

## 4. PostFlagContextTracker

Responsibility:

- after a body exists, track post-flag adverse-side nodes;
- store deepest adverse correction;
- store opposite nodes between numbered nodes;
- supply context for next-F backfill;
- feed HookBranchEngine.

## 5. HookBranchEngine

Responsibility:

- build branchable internal numbering;
- count 1/2/3/4;
- increase L if any branch > 4;
- evaluate ND 50% retracement rule;
- emit ND/Hook events.

## 6. SequenceEngine

Responsibility:

- own chains;
- create F1 only at phase boundary;
- authorize F2 after F1 confirmation;
- authorize F3 after F2 confirmation;
- keep parent context alive when child candidate dies;
- lock F3 with first confirmed opposite F1.

## 7. F-Level State Machines

Separate F1/F2/F3 logic prevents rule mixing.

F1:

- Waist invalidation before confirmation;
- internal 1/2 requirement;
- Leg2 re-pass confirmation.

F2:

- origin invalidation;
- size >= F1;
- waist-break branch;
- Leg2 re-pass confirmation.

F3:

- two-leg body;
- OR qualification;
- extension;
- lock by first opposite confirmed F1.

## 8. IdentityDeduplicator

Responsibility:

- assign stable ids;
- prevent exact duplicate emission;
- preserve all genuinely different structures;
- never merge near-duplicates by visual similarity.

## 9. AuditEmitter

Responsibility:

- log every state transition;
- write enough data to reconstruct why an object exists;
- support debugging without chart clutter.

## 10. RenderModelBuilder

Responsibility:

- convert emitted logical objects into render instructions;
- stack labels;
- assign shades;
- assign object names.

Must not:

- create structure;
- reject structure;
- change logic status.

## 11. Renderer

Responsibility:

- draw render instructions;
- delete stale visual objects only when corresponding logical object no longer appears in render model;
- keep locked objects if enabled.
