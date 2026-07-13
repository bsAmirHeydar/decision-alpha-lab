---
title: "ADR — Cross-attention requires late-fusion evidence"
tags: [strategy-factory, uce-i10, adr]
status: accepted
doc_version: 1.1.0
last_updated: 2026-07-13
---
# ADR — Cross-attention requires late-fusion evidence

## Status

**Accepted** for UCE-I10 v1.1.0.

## Context

Cross-attention adds capacity, optimization variance, export complexity, and difficult attribution before simpler fusion has established incremental value.

## Decision

I10 implements late, gated, and OOF-stacked fusion. Cross-attention remains a descriptor-only deferred capability until simpler fusion passes ablation, stability, economics, and export gates.

## Decision rules

- The rule is enforced in executable contracts and tests, not only documentation.
- Any exception requires a new version and a superseding ADR.
- Rejected evidence remains visible in manifests and qualification reports.
- Downstream phases consume the decision; they may not reinterpret it.

## Alternatives considered

- Make cross-attention the default multi-view model: rejected as unjustified complexity.
- Ban it permanently: rejected because future evidence may support it.
- Permit it whenever sample size is high: rejected because sample size alone does not prove view complementarity.

## Consequences

- Complexity is earned by comparative evidence.
- UCE-I11 may schedule cross-attention only after a future version records the prerequisite evidence.
- Late-fusion results become the mandatory baseline and debugging surface.

## Verification

- Unit tests cover the accepted path and at least one prohibited path.
- Schema and canonical identity include all decision-bearing fields.
- The UCE-I10 acceptance evidence records the validator result.
- The I11 handoff names this ADR as a scheduling constraint.

## Related

- [[../00_UCE_I10_DELIVERY_MOC]]
- [[../15_DEEP_QUALIFICATION_MULTI_SEED_AND_EXPORT]]
- [[../19_TEST_STRATEGY_GOLDEN_NEGATIVE_AND_CHAOS]]
