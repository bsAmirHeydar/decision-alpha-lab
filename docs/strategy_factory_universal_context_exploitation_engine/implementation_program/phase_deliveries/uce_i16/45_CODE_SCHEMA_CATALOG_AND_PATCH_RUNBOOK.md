---
title: "UCE-I16 — Code Schema Catalog And Patch Runbook"
tags: [strategy-factory, uce-i16, context-onboarding, legacy-migration]
status: implemented_static_and_python_validated
doc_version: 1.0.0
last_updated: 2026-07-13
---
# Code Schema Catalog And Patch Runbook

## Purpose

This chapter defines the executable and governance contract for **Code Schema Catalog And Patch Runbook** within UCE-I16. The controlling objective is to make context integration additive: a context contributes a package, typed adapter, fixtures, tests, capabilities and tournament identities without inserting context-specific branches into central engine modules.

## Decision

The decision is fail-closed. Generated artifacts are accepted only when the context specification is canonical, required capabilities are present, forbidden authority is denied, differential parity is measured before behavior changes, and the central-engine snapshot is unchanged.

## Contract

The machine-readable contract is versioned with exact SemVer and canonical SHA-256 identities. Consumers may not infer fields from prose. Unknown fields are rejected by closed JSON schemas, and any behavior-changing parameter must participate in serialization and identity.

## Inputs

- Frozen context specification and doctrine hash.
- Source inventory with repository-relative paths and content hashes.
- Feature, view, lifecycle, cluster, task and manual-policy declarations.
- Explicit capability decisions and exception reasons.
- I15 tournament and prospective-paper limitations.

## Outputs

- Deterministic package artifacts and scaffold manifest.
- Typed legacy-adapter specification and differential observations.
- Migration unit/wave plan and stop-safe report.
- Compiled per-context tournament template.
- Core invariance report and evidence bundle.

## Identity and serialization

All maps are key-sorted, enums serialize by exact value, floating-point values must be finite, and paths are normalized to safe repository-relative POSIX form. Generated file content hashes and artifact paths are both identity relevant. Repeated runs with the same specification, generator version, seed and core snapshot must be byte-identical.

## Causality and known-time

Every generated feature declares a known-time rule. A view cannot be marked non-causal. Future-data authority is explicitly denied. Legacy differential fixtures are replayed with the same known-time cut on both sides; future suffixes may not modify a previously generated occurrence or tournament identity.

## Determinism

The generator performs no network access, clock-derived identity, unordered traversal or ambient-random sampling. Tournament stage identities are derived from the context specification hash, frozen seed and exact stage identifier. Registry registration is idempotent for the same exact manifest and rejects conflicting manifests under one context ID.

## Failure behavior

Unsafe paths, unknown features, missing shared-path capabilities, allowed forbidden authority, duplicate artifact paths, incomplete parity, core mutations without ADR evidence, or fixture-as-alpha claims terminate the operation. Migration stops at the first unit without parity and leaves previously accepted contexts unchanged.

## Telemetry and evidence

Evidence retains generated-file counts, parity observations, migration units, changed-core counts, failure codes, manifest hashes, parity-report hashes, migration-report hashes, test evidence and limitations. Failed, stopped, pending and rejected work remains in the evidence trail.

## Required tests

1. Repeated scaffold identity and byte parity.
2. Future/forbidden capability rejection.
3. Legacy exact and mismatched differential replay.
4. Wave stop/resume and unaffected-context proof.
5. Tournament stage identity stability.
6. Core snapshot equality and ADR-required negative case.
7. Closed-schema validation and MQL5 static boundary checks.

## Operator procedure

1. Freeze the context specification and source inventory.
2. Run the generator twice and compare manifests.
3. Execute legacy differential replay before enabling any behavior change.
4. Confirm all shared-path bindings and capability denials.
5. Execute the bounded migration wave.
6. Re-snapshot the central engine and validate invariance.
7. Archive evidence, limitations and downstream handoff.

## Limitations

Static source inventory and fixture parity do not prove live MQL5 behavioral equivalence. MetaEditor compilation and representative real-market differential replay remain local-Windows gates. Consequently, migrated behavior is not activated by this phase package; adapters remain differential/shadow until those gates close.

## Downstream handoff

UCE-I17 may consume only contexts whose package manifest, parity evidence, shared-path declarations, capability scope, tournament identities and invariance report are present and hash-valid. Pending contexts may be inventoried but may not enter portfolio allocation as promoted contexts.

## Traceability

- Python package: `strategy_factory_onboarding_v3`
- Schemas: `lab/11_strategy_factory/schemas/v3/onboarding_*.schema.json`
- MQL5 mirror: `mql5/Include/AlphaLab/StrategyFactory/ContextOnboarding/`
- Tests: `lab/11_strategy_factory/tests/phase_uce_i16_context_onboarding/`
- Chapter ordinal: `45`
