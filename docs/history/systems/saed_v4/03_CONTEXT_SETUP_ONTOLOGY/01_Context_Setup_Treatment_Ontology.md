---
title: Context–Setup–Treatment Ontology
status: canonical
version: 4.0.0
created: '2026-07-13'
updated: '2026-07-13'
tags:
- saed-v4
- core-production
---

# Purpose

Define the canonical entities that prevent context detection, setup hypotheses, treatment execution, and policy decisions from collapsing into one ambiguous object.

## Capability tier

**Core Production**

## System design

### ContextPackage

Versioned upstream market-state doctrine and lifecycle contract.

### ContextOccurrence

One known-time event instance with immutable evidence and cluster identity.

### SetupArchetype

A falsifiable exploitation hypothesis such as continuation, reversal, reclaim, retest, or trend capture.

### TreatmentCandidate

A complete executable composition over a finite atom registry.

### PolicyDecision

The bounded choice among treatment, skip, abstain, manual fallback, or reject.

## Input contracts

- `ContextPackage`
- `ContextOccurrence`
- `SetupArchetypeRegistry`

## Output contracts

- `TreatmentCandidate`
- `OpportunityCluster`
- `PolicyDecision`

## Measurement framework

- Entity identity collision rate must be zero.
- Schema closure and referential integrity.
- Exact lifecycle and version compatibility.

## Adversarial questions

- Can any outcome mutate the context?
- Can a treatment exist without complete invalidation and expiry?
- Can one occurrence produce unclustered sibling rows?

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
