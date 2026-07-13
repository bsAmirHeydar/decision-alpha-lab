---
title: "ADR — View known-time is part of identity"
tags: [strategy-factory, uce-i10, adr]
status: accepted
doc_version: 1.1.0
last_updated: 2026-07-13
---
# ADR — View known-time is part of identity

## Status

**Accepted** for UCE-I10 v1.1.0.

## Context

The same visual or numeric payload may be legal at one decision cut and illegal at another. Payload hashes alone cannot prove causality.

## Decision

Every sequence, raster, graph, and view tensor includes context_observation_id and known_time_ms in its contract and canonical identity.

## Decision rules

- The rule is enforced in executable contracts and tests, not only documentation.
- Any exception requires a new version and a superseding ADR.
- Rejected evidence remains visible in manifests and qualification reports.
- Downstream phases consume the decision; they may not reinterpret it.

## Alternatives considered

- Infer known-time from the last source row: rejected because padding, sparse events, and graph nodes make inference ambiguous.
- Store known-time only in logs: rejected because logs are not portable artifact identity.
- Trust the upstream dataset: rejected because every representation boundary must be independently auditable.

## Consequences

- Future-suffix invariance becomes executable.
- Caches cannot reuse an artifact across different decision cuts.
- Cross-language consumers can reject a mismatched context or known-time.

## Verification

- Unit tests cover the accepted path and at least one prohibited path.
- Schema and canonical identity include all decision-bearing fields.
- The UCE-I10 acceptance evidence records the validator result.
- The I11 handoff names this ADR as a scheduling constraint.

## Related

- [[../00_UCE_I10_DELIVERY_MOC]]
- [[../15_DEEP_QUALIFICATION_MULTI_SEED_AND_EXPORT]]
- [[../19_TEST_STRATEGY_GOLDEN_NEGATIVE_AND_CHAOS]]
