---
title: "UCE-I19 Atomic Concept — Authority Is Recomputed Every Cycle"
tags: [strategy-factory, uce-i19, atomic-concept, production-operations]
status: canonical
doc_version: 1.0.0
last_updated: 2026-07-15
---
# Authority Is Recomputed Every Cycle

## Atomic decision

A prior passing evaluation cannot authorize a later action. Each cycle recomputes plan, lease, health, reconciliation, incident, and risk conditions from current known-time evidence.

## Consequences

- The concept is enforced by a closed Python contract, machine-readable reason codes, negative tests, and a corresponding MQL5 diagnostic or mirror where applicable.
- Missing or incompatible evidence fails closed and cannot be repaired by aggregate scoring, manual narrative, or a later observation.
- Every consumer receives an immutable artifact and must not infer omitted semantics.
- The reference repository retains `activation_allowed=false` until external evidence is accepted.

## Verification

The verification suite includes a positive deterministic vector, at least one boundary vector, a hostile negative vector, canonical hash stability, unknown-field rejection, and an authority scan. External production acceptance additionally requires Windows MetaEditor compilation, MT5 terminal execution, exact broker/account/symbol binding, restart and reconciliation evidence, and human approval.

## Links

- [[00_UCE_I19_DELIVERY_MOC|UCE-I19 Delivery MOC]]
- [[03_PRODUCTION_OPERATIONS_STATE_MACHINE|Operations State Machine]]
- [[46_ACCEPTANCE_EVIDENCE_MATRIX|Acceptance Evidence Matrix]]
- [[53_CURRENT_PHASE_STATUS|Current Status]]
