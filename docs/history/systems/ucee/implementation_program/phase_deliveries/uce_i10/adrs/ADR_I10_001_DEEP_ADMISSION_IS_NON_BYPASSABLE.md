---
title: "ADR — Deep admission is non-bypassable"
tags: [strategy-factory, uce-i10, adr]
status: accepted
doc_version: 1.1.0
last_updated: 2026-07-13
---
# ADR — Deep admission is non-bypassable

## Status

**Accepted** for UCE-I10 v1.1.0.

## Context

Deep architectures can fit noise and create false sophistication when support, causality, and classical baselines are weak.

## Decision

Every deep Trainer SDK fit requires a retained DeepAdmissionEvidence record. REJECT blocks fit. WARN may run only as challenger and can never be promoted in I10.

## Decision rules

- The rule is enforced in executable contracts and tests, not only documentation.
- Any exception requires a new version and a superseding ADR.
- Rejected evidence remains visible in manifests and qualification reports.
- Downstream phases consume the decision; they may not reinterpret it.

## Alternatives considered

- A simple configuration flag would be easier but would erase evidence lineage.
- Manual reviewer approval was rejected because it is not reproducible or machine-enforceable.
- Allowing training but blocking only final promotion was rejected because it wastes compute and encourages result-driven exceptions.

## Consequences

- Admission thresholds become explicit policy and must be versioned.
- Dataset-manifest changes invalidate prior admission evidence.
- Downstream UCE-I11 scheduling can filter candidates deterministically.

## Verification

- Unit tests cover the accepted path and at least one prohibited path.
- Schema and canonical identity include all decision-bearing fields.
- The UCE-I10 acceptance evidence records the validator result.
- The I11 handoff names this ADR as a scheduling constraint.

## Related

- [[../00_UCE_I10_DELIVERY_MOC]]
- [[../15_DEEP_QUALIFICATION_MULTI_SEED_AND_EXPORT]]
- [[../19_TEST_STRATEGY_GOLDEN_NEGATIVE_AND_CHAOS]]
