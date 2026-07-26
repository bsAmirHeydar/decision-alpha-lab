---
phase: FP-I05
experiment: EXP0019
context_id: FP-CONTEXT-001
status: normative
phase_version: 1.0.0
language: en
last_updated: 2026-07-13
---
# Security and No-Authority Boundary

## Purpose

Confirms no drawing, alerting, order, broker, position or network authority exists in FP-I05.

## Normative rules

1. All intervals are UTC millisecond half-open intervals derived from the exact FP-I03 calendar configuration hash.
2. All behavior-bearing fields participate in canonical serialization and SHA-256 identity.
3. Missing, out-of-coverage, conflict, and incomplete states remain visible; no synthetic bar or silent fallback is permitted.
4. The implementation is deterministic: repeated equal input produces equal IDs, hashes, ordering, and reason codes.
5. Downstream consumers may not reconstruct omitted semantics from filenames, chart state, broker timezone, or mutable global state.


## Contract flow

```text
validated upstream contract
        ↓
canonical FP-I05 operation
        ↓
immutable output + identity + reason code
        ↓
store/index/event evidence or hard rejection
```

## Required evidence

| Evidence | Requirement |
|---|---|
| Calendar lineage | FP-I03 config hash and source calendar window ID |
| Data lineage | FP-I04 dataset/revision IDs and source bar hashes |
| Semantic identity | canonical SHA-256 and stable ID |
| State | closed enum and legal transition |
| Failure | registered reason code, never free text alone |
| Authority | `NONE` |

## Failure behavior

- Invalid interval, identity, enum, coverage count, or lifecycle transition is rejected.
- Missing calendar dates are retained as selector items.
- Incomplete or blocked windows cannot silently generate references.
- Stale/corrupt checkpoints require deterministic rebuild.
- Revision impact invalidates overlap only; unaffected prefix evidence remains stable.

## Test obligations

- Golden complete A/L/N/W aggregation.
- Missing, out-of-coverage and duplicate-conflict paths.
- Exact calendar offsets across weekends and missing dates.
- Symbol-local high/low identity.
- Hunter non-consumption and protected consumption.
- Repeated transition rejection.
- Revision overlap and non-overlap.
- Batch/restart deterministic hash parity.

## Operator checklist

- [ ] Verify FP-I03 and FP-I04 manifests and hashes.
- [ ] Confirm calendar and data-contract hashes in configuration.
- [ ] Run the phase tests and conformance CLI.
- [ ] Inspect incomplete/blocked windows before enabling downstream Hunt.
- [ ] Retain revision invalidation and checkpoint evidence.
- [ ] Compile MQL5 diagnostic/self-test locally in MetaEditor.

## Residual risks

FP-I05 does not prove that a later hunt or divergence is economically useful. It also does not infer holidays or exchange-specific closures beyond the canonical calendar policy. Such changes require a new calendar/policy version and new identities.

## Navigation

- [[00_FP_I05_DELIVERY_MOC|FP-I05 Delivery MOC]]
- [[../../phases/FP_I05_SESSION_WEEK_WINDOW_STORE_CALENDAR-DAY_SELECTOR_AND_REFERENCE_ENGINE|Canonical Phase Specification]]
- [[29_HANDOFF_TO_FP_I06|Handoff to FP-I06]]
