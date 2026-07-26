---
status: accepted-reference
version: 1.0.0
updated: 2026-07-20
tags: [acl-os, lcm, lcm-09b, setup-migration]
phase_id: LCM-09B
claim_ceiling: LCM_09B_REFERENCE_ONLY
---
# Decision Log and ADR Summary

## ADR-09B-001 — Preserve UNKNOWN instead of reconstructing semantics

**Decision:** materialize blocked packages with explicit unknown rule slots.  
**Reason:** the accepted handoff authorizes zero semantic implementations.  
**Consequence:** portfolio accounting closes without creating false executable readiness.

## ADR-09B-002 — Separate Factory reference visibility from candidate compilation

**Decision:** expose migrated identities through `ACL04_LEGACY_REFERENCE_PORT_V1`.  
**Reason:** registration is required for integration evidence, but normal Factory candidate defaults could change behavior.  
**Consequence:** identities are inspectable and queryable while remaining ineligible for promotion or runtime.

## ADR-09B-003 — Adapters normalize supplied evidence only

**Decision:** adapters never import or execute legacy source.  
**Reason:** legacy execution would create hidden runtime dependencies and authority.  
**Consequence:** observed traces must come from an approved external replay producer.

## ADR-09B-004 — Parity may be BLOCKED but never fabricated PASS

**Decision:** all 60 records are `BLOCKED` when legacy/canonical executable evidence is absent.  
**Reason:** aggregate counts cannot prove behavioral equivalence.  
**Consequence:** LCM-10A receives truthful unresolved dependencies.

## ADR-09B-005 — Context is caller-owned

**Decision:** Setup evaluator owns no clock or Context computation.  
**Reason:** duplicated Context logic causes threshold, timeframe, and known-time drift.  
**Consequence:** incomplete known-time input is rejected and Context recomputation flags remain false.

## ADR-09B-006 — Treatment remains outside Setup

**Decision:** emit dependency seeds instead of implementing Treatment semantics.  
**Reason:** LCM-10 owns Treatment and execution package migration.  
**Consequence:** each Setup explicitly lists required capabilities and forbidden Setup-core capabilities.

## ADR-09B-007 — Deterministic IDs and atomic publication

**Decision:** derive identities/digests from bound content and publish through atomic file replacement.  
**Reason:** retries and clean overlays must be reproducible.  
**Consequence:** wall-clock time is descriptive only and never an identity input.

## ADR-09B-008 — Close LCM-09 under explicit blocker completeness

**Decision:** accept the phase when every active identity is canonical or explicitly blocked and all authority gates pass.  
**Reason:** the master acceptance criterion permits blocked identities and forbids weakening evidence gates.  
**Consequence:** closure means complete truthful migration accounting, not executable parity.
