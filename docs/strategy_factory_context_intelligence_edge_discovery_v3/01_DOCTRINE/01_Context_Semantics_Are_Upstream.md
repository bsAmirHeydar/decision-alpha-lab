---
title: Context Semantics Are Upstream
status: canonical
version: 3.0.0
created: '2026-07-13'
updated: '2026-07-13'
tags:
- saed-v3
- doctrine
---

# Thesis

The trainer may learn exploitation conditional on a context, but it may not redefine, relabel, repair, or backfill the context after seeing outcomes.

## Architectural design

### Immutable semantic boundary

A ContextPackage and ContextOccurrence are consumed by exact identifier and hash. Trainer features may summarize the context but cannot alter its lifecycle or known-time record.

### Allowed learning

The system may learn conditional eligibility, expected outcomes, treatment rankings, support, uncertainty, and abstention.

### Forbidden learning

No latent model may silently replace the canonical context detector or create retrospective context occurrences.

## Machine contracts

- `context_package_hash`
- `context_occurrence_id`
- `known_time`
- `lifecycle_state`
- `context_support_signature`

## Validation and evidence

- Future-suffix perturbation leaves all prior context evidence unchanged.
- Recomputing a run from the same event log yields identical context references.
- All rejected/stale/incomplete contexts remain visible in the opportunity ledger.

## Failure modes and mandatory response

- **Outcome-informed relabeling:** Quarantine the dataset generation and invalidate downstream models.
- **Context drift without version change:** Block training and require a new context version.
- **Missing lifecycle history:** Abstain and emit a data-integrity incident.

## UCEE handoff

All outputs bind to exact upstream context, feature, data-role, treatment-universe, and economics hashes. Promotion and runtime authority remain in UCEE I12–I18.

## Related notes

- [[03_UCEE_I01_I18_Compatibility]]
- [[Context_Setup_Treatment_Ontology]]
