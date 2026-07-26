---
title: "UCE-I11 — Grid, Random, and Quasi-Random Search"
tags: [strategy-factory, uce-i11, experiment-orchestration]
status: normative
phase_version: 1.0.0
doc_version: 1.0.0
last_updated: 2026-07-13
---
# Grid, Random, and Quasi-Random Search

## Purpose

The native search floor provides exact Cartesian grid enumeration, seeded pseudo-random sampling, and seeded Halton quasi-random sampling.

## Scope

- Grid uses declared numeric steps and discrete values.
- Random uses a local Random(seed), never global RNG state.
- Halton uses fixed prime bases and deterministic duplicate suppression.
- All proposals carry ordinal, resource level, kind, and candidate hash.

## Normative invariants

1. **Search stops at max_trials.**
2. **Duplicate parameter points are not silently counted twice.**
3. **Log domains require positive lower bounds.**
4. **Continuous values are quantized before identity construction.**


## Contract flow

```text
immutable upstream evidence
        │
        ▼
validated grid, random, and quasi-random search
        │
        ├─ canonical serialization
        ├─ stable identity/hash
        ├─ executable validation
        └─ append-only evidence
        │
        ▼
downstream UCE-I11 artifact or hard rejection
```

## Required artifacts

| Artifact | Required content | Failure behavior |
|---|---|---|
| Declaration/contract | exact versions, closed enums, behavior fields | reject unknown or missing semantics |
| Identity evidence | canonical JSON and SHA-256 | refuse collision or non-finite value |
| Execution evidence | event/ledger/cache/repro record as applicable | preserve failure; never delete attempt |
| Tests | golden, negative, deterministic, failure injection | phase remains incomplete |
| Documentation | operator rule, limitation, rollback, handoff | consumer may not infer missing data |

## Failure matrix

| Failure | Detection | Required disposition |
|---|---|---|
| Missing required identity | dataclass/schema validation | reject before compilation |
| Version mismatch | exact-version comparison | fail closed; no migration inference |
| Duplicate or collision | canonical hash/set validation | stop compilation |
| Resource or timeout breach | budget/scheduler parent | deny, timeout, or quarantine with ledger entry |
| Stale or corrupt cache | payload/provenance verification | refuse cache and recompute |
| Reproducibility divergence | semantic/event/artifact comparison | blocker for handoff |

## Telemetry and evidence fields

- `experiment_id`, `manifest_hash`, and exact component version.
- `trial_id` and `node_id` for node-local evidence.
- `sequence`, `attempt`, `worker_id`, and `reason_code` for scheduler evidence.
- `policy_hash`, resource claim, usage-before, and budget decision.
- Artifact hashes, cache provenance, and selected/failed disposition.
- Known limitations and downstream gate owner.

## Executable test obligations

1. Construct the canonical golden case twice and compare exact identity.
2. Change one behavior-bearing field and prove identity changes.
3. Inject one missing, stale, corrupt, timed-out, or rejected input.
4. Verify the failed attempt remains in scheduler/ledger evidence.
5. Verify the protected final-test role cannot enter the search path.
6. Verify no broker/order/network authority exists in the implementation surface.

## Operator checklist

- [ ] Confirm repository phase status and exact package version.
- [ ] Freeze candidate/search registries before compilation.
- [ ] Confirm dataset, split, target, economics, and known-time hashes.
- [ ] Confirm budget policy before starting any trial.
- [ ] Run phase tests and conformance vectors.
- [ ] Inspect blockers, warnings, failed attempts, and cache dispositions.
- [ ] Preserve the selection ledger and event stream for UCE-I12.

## Residual risk

The reference implementation proves deterministic orchestration semantics on synthetic/golden fixtures. It does not prove that any candidate has economic edge, that an external optimizer is superior, or that a parallel scheduler is parity-equivalent. Those claims require separate evidence and remain downstream responsibilities.

## Code surfaces

- `strategy_factory_experiments_v3/contracts.py`
- `strategy_factory_experiments_v3/compiler.py`
- `strategy_factory_experiments_v3/search.py`
- `strategy_factory_experiments_v3/budget.py`
- `strategy_factory_experiments_v3/scheduler.py`
- `strategy_factory_experiments_v3/ledger.py`
- `strategy_factory_experiments_v3/cache.py`
- `strategy_factory_experiments_v3/reproducibility.py`

## Handoff rule

No downstream phase may infer an omitted trial, failure, override, cache decision, or resource cutoff. Missing evidence is a blocker, not permission to reconstruct history from prose.

## Navigation

- [[00_UCE_I11_DELIVERY_MOC|UCE-I11 delivery MOC]]
- [[../../phases/UCE_I11_EXPERIMENT_DAG_SEARCH_AND_BUDGETING|Canonical phase specification]]
- [[../../phases/UCE_I12_STATISTICAL_AND_ANTI_OVERFIT_PROMOTION_GATE|Next phase]]
