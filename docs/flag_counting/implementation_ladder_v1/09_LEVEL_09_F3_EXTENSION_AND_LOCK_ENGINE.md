# Level 09 — F3 Lifecycle / Terminal Extension / Lock Engine

## Purpose

Level 09 makes F3 a first-class lifecycle layer. F3 is no longer a generic body plus a few `SequenceEngine` conditionals. It is the terminal child of an authorized F2 and it owns:

```text
F2 parent gate
F3 origin backfill
terminal body construction
OR qualification by size or L
completed terminal state
lock evidence from the first opposite confirmed F1
```

Renderer output is still non-authoritative. `FP_LEVEL09` and `FP_LEVEL09_LOCK` are the audit source of truth.

## Owned modules

```text
mql5/Include/FlagCountingPhoenix/FP_F3LifecycleRules.mqh
mql5/Include/FlagCountingPhoenix/FP_F3LifecycleAudit.mqh
mql5/Include/FlagCountingPhoenix/FP_F3LifecycleEngine.mqh
```

Wiring only:

```text
mql5/Include/FlagCountingPhoenix/FP_SequenceEngine.mqh
mql5/Include/FlagCountingPhoenix/FP_Types.mqh
mql5/Include/FlagCountingPhoenix/FP_Identity.mqh
mql5/Include/FlagCountingPhoenix/FP_Audit.mqh
mql5/Experts/FlagCounting/FlagCountingPhoenixExperiment.mq5
```

## Authorization

F3 may only be attempted from F2 when all Level 08 gates are true:

```text
F2.level = F2
F2.status = confirmed
F2.has_confirm = true
F2.f2_size_gate_passed = true
F2.f2_can_spawn_f3 = true
```

F2 candidate, post-flag F2, invalidated F2, undersized F2, and hidden fail-open F2 cannot authorize F3.

## Origin backfill

F3 origin is the deepest adverse node after F2 Leg2 and before F2 confirmation.

```text
search window = (F2.Leg2, F2.confirm)
bullish F3 origin = deepest LOW in that window
bearish F3 origin = highest HIGH in that window
```

Nodes after F2 confirmation are not valid F3 origins.

## Terminal body

F3 uses the same body engine as F1/F2:

```text
bullish: LOW -> HIGH -> LOW -> HIGH
bearish: HIGH -> LOW -> HIGH -> LOW
```

Level 09 does not require post-F3 internal 1/2. F3 is terminal after a valid body and OR qualification.

## OR qualification

F3 completes when either condition is true:

```text
F3.flag_size >= InpF3MinParentSizeRatio * F2.flag_size
```

or:

```text
F3.leg1_L >= ceil(InpF3Leg1LMinRatio * F2.leg1_L)
```

Both are not required. If neither passes, F3 remains an OR-rejected candidate for audit. It cannot lock.

## Lock

A completed F3 locks on the first opposite confirmed F1 that starts and confirms after F3 completion.

Lock evidence:

```text
f3_locked = true
f3_lock_event_id = opposite confirmed F1 event id
extension_end = opposite F1 origin
status = locked
f3_lifecycle_status = locked
```

Locked F3 is historical evidence and must not disappear from audit.

## Required fields

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
f3_lock_reason
f3_lifecycle_reason
```

## Audit

```text
FP_LEVEL09
FP_LEVEL09_LOCK
```

`FP_LEVEL09` reports construction and OR qualification. `FP_LEVEL09_LOCK` reports cross-sequence lock scans after all scales are collected and sorted.

## Acceptance

- F3 never appears from F2 unless Level 08 authorizes F3.
- F3 origin is backfilled only inside the strict post-F2/pre-confirmation window.
- F3 completes by size OR L, not both.
- OR-rejected F3 cannot lock.
- Completed F3 locks on the first opposite confirmed F1 after completion.
- Identity includes F3 lifecycle state.
- Summary and event audit include F3 lifecycle fields.
