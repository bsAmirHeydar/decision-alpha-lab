# Phoenix Flag Counting Implementation Ladder V1

This document is part of the implementation ladder for the Phoenix Flag Counting engine.

# Level 17 — Resolved Decision Record

## Purpose

This file used to list open ambiguities before further code. Those ambiguities are now resolved by:

```text
docs/flag_counting/FLAG_COUNTING_CURRENT_CANON.md
```

This file remains as a quick implementation-facing decision index. If this file and the current canon ever conflict, the current canon wins.

---

## A. Phase reset rules — resolved

Default:

```text
PHASE_RESET_OPPOSITE_F3_LOCK_ONLY
```

Implementation meaning:

- A new same-direction F1 phase is not allowed merely because a child failed.
- A broken F2/F3 child does not reset parent ownership.
- A large opposite Hook/ND does not reset same-direction phase by default.
- Completed F3 is locked by first confirmed opposite F1.

Optional future diagnostic variants may exist only as named inputs:

```text
PHASE_RESET_OPPOSITE_CONFIRMED_F1
PHASE_RESET_OPPOSITE_HOOK_OR_F1
```

---

## B. F1 root preference — resolved

Winner order:

1. lifecycle quality;
2. confirmed/qualified over developing;
3. Hook/phase-boundary root over fail-open;
4. fuller child chain over isolated root;
5. lower-L local over high-L umbrella when semantic quality is equal;
6. earlier stable origin when semantic quality is equal;
7. deterministic `event_id` tie-breaker.

Losers remain audit-visible with hidden reason.

---

## C. F2 size handling — resolved

Default:

```text
F2 candidate may exist in audit.
Main-chart F2 requires size-qualified status unless candidate display is enabled.
F3 authorization requires confirmed and size-qualified F2.
```

If F2 extends into qualification, update the same candidate path; do not emit a duplicate unless identity truly changes.

---

## D. Hook/ND display — resolved

Default:

```text
Main chart: Hook/ND only when connected to canonical visible ownership or when Hook debug is enabled.
Audit: all Hook/ND branches and branch numbers.
```

Hook/ND is context, not a hard gate that may starve all F structures.

---

## E. Main-chart density — resolved

Default profile:

```text
CLEAN_LOCAL
```

Allowed display profiles:

```text
CLEAN_LOCAL
BALANCED
STRUCTURAL_AUDIT
```

Renderer settings must not change logical event emission.

---

## F. Live pending nodes — resolved

Default:

```text
Pending nodes may support Hook live inspection.
Confirmed F bodies require confirmed nodes.
Pending-node F bodies are diagnostic-only and must be tagged.
```

---

## G. Backfill windows — resolved

Default strict window:

```text
F2 origin: deepest adverse correction after F1 Leg2 and before F1 confirmation.
F3 origin: deepest adverse correction after F2 Leg2 and before F2 confirmation.
```

Extended windows are diagnostic variants only.

---

## Required answers before next major code patch

All previous minimum questions are now answered:

1. Same-direction ownership reset = strict opposite F3 lock default.
2. Main chart = canonical-clean; developing/diagnostic objects in audit unless explicitly enabled.
3. High-L umbrella = audit-visible unless it is the canonical owner; lower-L wins on equal semantic quality.
4. Pending live nodes = Hook/ND live inspection only by default; F bodies require confirmed nodes.

## Implementation note

Future code may add inputs for variants, but the default must remain the resolved canon behavior and every variant must be auditable.
