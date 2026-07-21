---
status: accepted-reference
version: 1.0.0
updated: 2026-07-20
tags: [acl-os, lcm, lcm-09b, setup-migration]
phase_id: LCM-09B
claim_ceiling: LCM_09B_REFERENCE_ONLY
---
# Artifact Catalog

## Input binding

`input/lcm09a_binding.json` locks the exact upstream handoff, freeze, contract registry, implementation authorization set, and forbidden actions.

## Identity and package artifacts

- `canonical_setup_registry.json`: 60-row package index;
- `canonical_setup_packages/<setup_id>.json`: one immutable package per frozen identity;
- `required_artifact_locator.json`: exact phase-required names, canonical paths, and digests.

## Integration artifacts

- `adapters/setup_adapter_registry.json`: 60 translation-only adapter records;
- `factory/setup_factory_registration.json`: 60 authority-negative reference registrations.

## Behavioral evidence

- `golden/setup_golden_cases.jsonl`: blocked no-trade cases;
- `golden/setup_golden_traces.jsonl`: blocked traces and restart checkpoints;
- `parity/setup_parity_registry.jsonl`: identity-level detail;
- `parity/setup_parity_registry.json`: digest-bound canonical parity registry;
- `parity/setup_variance_decisions.json`: zero waivers and zero hard mismatch decisions.

## Blocker and dependency artifacts

- `blockers/setup_blocker_registry.jsonl`: append-only blocker portfolio;
- `dependencies/treatment_dependency_inventory_seed.jsonl`: 60 LCM-10A inventory seeds.

## Audit artifacts

- `events/setup_migration_event_ledger.json`: deterministic materialization ledger;
- `provenance/setup_migration_provenance_graph.json`: upstream-to-identity-to-package graph;
- `reports/portfolio_closure_report.json`: complete accounting;
- `reports/hostile_review.json`: adversarial gate evidence;
- `reports/acceptance_report.json`: non-compensatory acceptance decisions.

## Handoff and integrity artifacts

- `handoff/lcm09b_to_lcm10a_handoff.json`: canonical nested handoff;
- `LCM09B_TO_LCM10A_HANDOFF.json`: exact specification-named byte-equivalent handoff;
- `output_manifest.json`: package byte manifest;
- `setup_migration_receipt.json`: upstream/manifest/handoff closure receipt;
- `setup_migration_marker.json`: phase status marker.

## Repository delivery metadata

`LCM_09B_FILE_INDEX.txt`, `LCM_09B_FILE_HASHES.sha256`, `LCM_09B_ARTIFACT_INVENTORY.csv`, `LCM_09B_PATCH_MANIFEST.json`, `LCM_09B_QA_REPORT.json`, README, installation guide, rollback guide, commit message, and apply batch make the patch independently reviewable and stageable.
