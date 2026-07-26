---
title: Treatment Lattice Compiler
status: canonical
version: 4.0.0
created: '2026-07-13'
updated: '2026-07-13'
tags:
- saed-v4
- core-production
---

# Purpose

Compile a finite, typed, dominance-pruned universe of complete treatment bundles for each context occurrence.

## Capability tier

**Core Production**

## System design

### Atom registries

Entry, stop, target, trail, management, time exit, cancellation, re-entry, and risk eligibility atoms.

### Compatibility graph

Context, archetype, profile, mechanism, and atom compatibility is evaluated before candidate materialization.

### Static feasibility

Broker, tick, volume, stop-level, session, MQL5, and replay feasibility are validated.

### Dominance pruning

Candidates that are structurally identical or universally dominated under declared assumptions are removed with reasons.

## Input contracts

- `ContextOccurrence`
- `ArchetypeSet`
- `RegistryVersions`
- `BrokerProfile`

## Output contracts

- `TreatmentUniverseManifest`
- `TreatmentCandidates`
- `PruningLedger`

## Measurement framework

- Candidate count and growth.
- Compiler determinism.
- Invalid-combination rejection.
- Dominance audit accuracy.

## Adversarial questions

- Can search silently expand after final-test viewing?
- Does pruning remove rare convex candidates using average metrics?
- Are runtime-infeasible candidates trained anyway?

## Mandatory controls

1. Exact upstream hashes and data roles are recorded.
2. Candidate and failure ledgers are complete.
3. Costs, capacity, missingness, censoring, and support are explicit.
4. Validation uses chronological, cluster-aware, purged folds.
5. Advanced outputs cannot bypass manual policy, hard risk, portfolio, or UCEE promotion.
6. Any runtime handoff requires deterministic export, parity, latency, fallback, and revocation evidence.

## Acceptance boundary

Passing research metrics is necessary but never sufficient. The component remains non-authoritative until its evidence is admitted through UCEE I12, compiled by I14, challenged prospectively under I15, bounded by I17, and qualified under I18.

## Related notes

- [[Finite_Action_Lattice]]
- [[Search_Space_Governance]]
