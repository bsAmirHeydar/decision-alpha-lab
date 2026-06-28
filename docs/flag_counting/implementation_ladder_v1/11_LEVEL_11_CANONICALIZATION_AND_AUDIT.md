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

# Level 11 — Canonicalization and Audit Invariants

## Purpose

Level 11 is the final engine-owned consistency pass before renderer/export. It separates:

```text
raw lifecycle candidates
owned phase sequences
final canonical visible stream
complete hidden/audit stream
```

It does **not** discover new market structure. It only normalizes the final event stream after Level 10 ownership.

## Owned source modules

```text
mql5/Include/FlagCountingPhoenix/FP_CanonicalTypes.mqh
mql5/Include/FlagCountingPhoenix/FP_CanonicalRules.mqh
mql5/Include/FlagCountingPhoenix/FP_CanonicalAudit.mqh
mql5/Include/FlagCountingPhoenix/FP_Canonicalizer.mqh
```

`FP_SequenceEngine.mqh` orchestrates the call. Renderer does not canonicalize.

## Final pipeline

```text
Level 10 ownership result
-> compatibility duplicate pruning
-> provisional Hook seed visibility
-> Level 11 canonicalization
-> final Hook seed visibility
-> final identity assignment
-> FP_LEVEL11 audit
-> renderer/export
```

## Canonical event fields

Every final F event carries:

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
FP_CANON_VISIBLE
FP_CANON_HIDDEN
FP_CANON_HIDDEN_DUPLICATE
FP_CANON_HIDDEN_ORPHAN
FP_CANON_HIDDEN_INVALID
FP_CANON_REPAIRED
FP_CANON_INVARIANT_FAILED
```

## Invariants

Level 11 must enforce these before renderer/export is trusted:

```text
1. every hidden event has hidden_reason
2. visible events do not carry stale hidden_reason
3. visible F2/F3 descendants have visible parents
4. visible F1 owners have phase_owner_root_id
5. visible events have structural_id, visual_id, phase_id, chain_id, audit_id
6. phase-safe visible duplicate geometry is hidden deterministically
7. malformed visible bodies are hidden, not drawn
8. invalidated events are hidden unless audit display explicitly asks for them
9. hook hidden-state has hidden_reason
10. final identity is rebuilt after canonicalization
```

## Duplicate rule

A visible duplicate conflict exists only when events are:

```text
same direction
same F level
same phase or merge-safe phase
same visual_id or same O/A/W/B visual body identity
```

The loser is selected by semantic canonical rank, not renderer order.

Canonical rank prefers:

```text
locked F3
completed F3
confirmed F2 authorized for F3
confirmed F1 authorized for F2
phase-boundary source
non-fail-open source
visible child maturity
lower/local L when semantic quality is equal
```

## Orphan rule

Visible F2/F3 events require a visible parent in the same sequence and previous chain index.

If `InpCanonicalHideUnresolvedOrphans=true`, unresolved visible descendants are hidden with:

```text
canonical_hide_unresolved_orphan_descendant
```

If disabled, they remain visible only as diagnostic output and `FP_LEVEL11` should report post-canonical parent invariant failures.

## Malformed body rule

A visible F event that lacks required O/A/W/B evidence after its status implies a full body is hidden with:

```text
canonical_hide_missing_required_body_nodes
```

Live-leg/seed states may lack full body evidence only when their display inputs explicitly allow them.

## Invalidated rule

If `show_invalidated_in_audit=false`, invalidated visible events are hidden with:

```text
canonical_hide_invalidated_not_requested
```

Invalidated events remain audit-visible through logs/export.

## Audit output

`FP_LEVEL11` reports:

```text
events
hooks
visible_before
visible_after
hidden_before
hidden_after
ids_reassigned
event_ids_repaired
parent_ids_repaired
missing_identity_repaired
hidden_reason_repaired
visible_reason_cleaned
hidden_no_reason_after
duplicate_groups
duplicates_hidden
visual_conflicts
structural_conflicts
phase_safe_duplicate_hides
exact_duplicate_hides
orphan_visible_before
orphan_hidden
orphan_visible_after
invalid_visible_hidden
render_none_hidden
missing_body_hidden
invariant_checks
invariant_failures
visible_missing_identity
visible_duplicate_visual_after
parent_missing_after
parent_mismatch_after
phase_owner_missing_after
broken_chain_after
hook_hidden_reason_repaired
hook_visible_after
hook_hidden_after
rank_min
rank_max
status
reason
```

Optional samples use:

```text
InpPrintCanonicalSamples=true
InpCanonicalSampleLimit=N
```

## Inputs

```text
InpPrintCanonicalSanity = true
InpPrintCanonicalSamples = false
InpCanonicalSampleLimit = 8
InpCanonicalStrictInvariants = true
InpCanonicalHideUnresolvedOrphans = true
```

## Acceptance tests

### Test 01 — Hidden reason complete

No final hidden event or hidden Hook may have empty `hidden_reason`.

### Test 02 — Visible duplicate clean

After Level 11, no two visible events may share a phase-safe visual duplicate body.

### Test 03 — Parent chain intact

Visible F2/F3 events must have visible previous-chain parents in the same sequence.

### Test 04 — Identity finality

After Level 11, every visible event must have `structural_id`, `visual_id`, `phase_id`, `chain_id`, and `audit_id`.

### Test 05 — Renderer cannot repair

Toggling renderer labels, object budget, Hook drawing, or detailed labels may change drawing only. It must not change Level 11 event emission or canonical audit counters.

## Freeze condition

This layer is frozen when `FP_LEVEL11 status=ok` for canonical validation windows and renderer output can be regenerated entirely from the final event/hook stream without repairing logic inside the renderer.
