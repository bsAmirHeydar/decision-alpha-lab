---
tags: [exp0019, faerie-protocol, fp-i06, relation-compiler, hunt-engine]
status: normative
phase: FP-I06
version: 1.0.0
last_updated: 2026-07-13
language: en
---
# Engine Snapshot

## Purpose

The engine snapshot contains compilation lineage, scan results, candidates, health, reason codes, source revision, and semantic hash.

## Boundary

READY means no data blocker; DEGRADED means compiler exclusions exist; BLOCKED means scan evidence cannot support classification.

## Normative invariants

1. **All behavior-bearing inputs are explicit and identity-bearing.**
2. **Input contracts are immutable; derived outputs are reproducible from canonical evidence.**
3. **UTC M1 is the only first-sweep ordering authority.**
4. **Missing, conflicting, or lineage-incompatible data fails closed.**
5. **No phase-local behavior may mutate FP-I02 through FP-I05 source contracts.**
6. **No drawing, confirmation, quota, risk, broker, order, position, or network authority is introduced.**


## Contract flow

```text
FP-I05 WindowStoreSnapshot + CalendarDaySelection
        │
        ▼
RelationCompiler → RelationInstance → HIGH/LOW SidePlan
        │
        ▼
Aligned M1 rows → MinuteContactObservation + HuntFact
        │
        ▼
FirstSweepClassification
        ├─ asymmetric → RawDivergenceCandidate
        ├─ same M1 → symmetric evidence; no candidate
        ├─ no contact → no candidate
        └─ data blocked → fail-closed evidence
        │
        ▼
Candidate transitions / cursor / snapshot / checkpoint
```

## Required evidence

| Evidence | Required fields |
|---|---|
| relation compilation | relation, reference/check window IDs, calendar offset, store hash, revision |
| side plan | side, two symbol-local references, reference states, check interval |
| hunt fact | symbol, own reference, M1, bar hash, observed extreme, revision |
| first sweep | exact outcome, first minute, roles or symmetric facts, reason code |
| candidate | relation, direction, roles, first-hunt fact, state, deadline, semantic hash |
| transition | sequence, prior/next state, event minute, evidence ID, event hash |

## Failure matrix

| Failure | Detection | Result |
|---|---|---|
| upstream hash mismatch | compiler preflight | block compilation |
| missing relation window | indexed lookup | record blocked/skipped relation |
| consumed reference | side-plan eligibility | no scan |
| same-M1 dual contact | contact classifier | symmetric evidence, no roles |
| missing/conflict M1 | aligned cell state | block classification or invalidate candidate |
| protected second touch | later HuntFact | cancel raw candidate |
| duplicate M1 row | scan preflight | hard failure |
| revision overlap | bounded invalidation | rebuild affected plans only |
| checkpoint mismatch | exact hash comparison | discard and rebuild |

## Test obligations

- Golden asymmetric HIGH and LOW cases for left and right Hunter.
- Same-M1 dual contact without invented ordering.
- No-contact and data-blocked outcomes.
- Second-touch cancellation and repeated-Hunter non-cancellation.
- Calendar offsets preserved without compression.
- Batch/replay identity stability.
- Revision and checkpoint negative fixtures.
- Static no-authority tests for Python and MQL5.

## Operational checklist

- [ ] FP-I05 status and handoff accepted.
- [ ] Store snapshot, registry, and calendar-selection hashes match.
- [ ] Relation compiler produces expected instance/plan counts.
- [ ] WW remains deferred.
- [ ] Source revision is recorded in every scan.
- [ ] Same-M1 and data-blocked outcomes are retained.
- [ ] Candidate transitions are monotonic.
- [ ] Golden vectors and cumulative regressions pass.

## Residual risks

This phase does not confirm a candidate, rank candidates, enforce pair-session quota, draw charts, or prove economic value. Tick-level ordering is deliberately ignored. A raw candidate is a contextual observation awaiting FP-I07 confirmation.

## Code surfaces

- `fp_i06_relations/contracts.py`
- `fp_i06_relations/registry.py`
- `fp_i06_relations/compiler.py`
- `fp_i06_relations/hunt.py`
- `fp_i06_relations/classification.py`
- `fp_i06_relations/engine.py`
- `fp_i06_relations/checkpoint.py`
- `fp_i06_relations/revision.py`

## Navigation

- [[00_FP_I06_DELIVERY_MOC|FP-I06 Delivery MOC]]
- [[../../phases/FP_I06_RELATION_COMPILER_HUNT_FACTS_FIRST-SWEEP_CLASSIFICATION_AND_CANDIDATES|Canonical Phase Specification]]
- [[../fp_i05/00_FP_I05_DELIVERY_MOC|FP-I05 Upstream Delivery]]
- [[../../phases/FP_I07_HOST-CANDLE_CONFIRMATION_STRICT_SESSION_DEADLINE_INVALIDATION_AND_LIFECYCLE|FP-I07 Next Phase]]
