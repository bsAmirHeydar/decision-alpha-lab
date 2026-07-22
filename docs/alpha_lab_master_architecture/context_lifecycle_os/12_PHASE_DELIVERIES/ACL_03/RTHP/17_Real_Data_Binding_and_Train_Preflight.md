# RTHP Real Data Binding and Train Preflight

## Current readiness

The Context package, descriptors, views, clusters, task references, label templates, UCE-I16 scaffold, smoke fixture, and preflight logic are complete. Real train activation remains fail-closed because the repository snapshot does not contain a resolved immutable real-data binding for RTHP.

## Required source artifacts

### Canonical occurrence ledger

One row per confirmed RTHP occurrence, conforming to the RTHP AI source-record schema and preserving exact known-time lineage.

### Reference-state ledger

Append-only state history required to construct factual exhaustion and survival labels.

### Cycle-instance ledger

Versioned cycle boundaries, completeness, reference ancestry, and known-time information.

### Role-price-path ledger

Post-cut role-local price path used only for outcome labels. It is never feature-eligible.

## Binding metadata

The resolved binding must declare provider, symbol pair, date range, timezone, price basis, tick-size source, futures rollover policy where applicable, entitlement, producer version, availability-time policy, immutable URI, and content hash for every source.

## Preflight behavior

The context-owned preflight performs:

1. source-schema and semantic validation;
2. ContextPackage registration and resolution;
3. deterministic observation and feature construction;
4. future-perturbation conformance;
5. all non-sequence view compilation;
6. sequence-view descriptor readiness;
7. dependence-cluster assignment;
8. real binding resolution checks.

Smoke mode must pass. Real mode must remain blocked until every required source is resolved. A blocked real preflight is a correct safety result, not an error to bypass.

## Handoff to existing pipeline

After a resolved real preflight, ACL-05 must freeze source artifacts, task/label versions, outcome horizons, maturity, censoring, split policy, search authority, seed, and budget. The existing shared pipeline then performs dataset construction, training, validation, reporting, memory, and planning.
