---
title: "Refined Implementation Roadmap — Balanced Phase Partition"
status: implemented-reference
version: 1.0.0
updated: 2026-07-19
tags: [acl-os, lcm, legacy-migration, roadmap-amendment]
roadmap_id: LCM_ROADMAP_R1_BALANCED_PARTITION
---
# Refined Implementation Roadmap — Balanced Phase Partition

## Authority and decision

This roadmap records the architect-approved decision to preserve the existing `LCM-00` through `LCM-16` lifecycle while dividing only the remaining heavy phases into two or three bounded implementation patches. It supersedes any earlier proposal to create dozens of micro-phases and any assumption that each remaining master phase must be delivered as one monolithic patch.

## Why this model

The previous master phases correctly described lifecycle meaning but several remaining phases combine repository-wide discovery, domain implementation, parity, cutover or deletion work. Delivering such a phase in one patch increases interruption risk, makes hostile review less precise and couples rollback of unrelated responsibilities. Conversely, splitting every workstream into a separate phase creates administrative overhead, too many handoffs and a higher chance that the overall semantic story is lost.

The balanced model uses the smallest number of partitions that separate materially different failure and rollback semantics. Each master phase has two or three subphases, and each subphase remains substantial enough to deliver a coherent vertical result.

## Governing invariants

1. Master-phase meaning and order do not change.
2. No acceptance gate is weakened by partitioning.
3. Every subphase has an exact upstream digest and downstream handoff.
4. UNKNOWN remains UNKNOWN until evidence resolves it.
5. Context, Setup, Treatment, visualization, documentation, cutover, quarantine and deletion boundaries remain explicit.
6. A subphase cannot create runtime, live-order or capital authority unless a higher ACL authority explicitly permits it; this roadmap grants none.
7. No partial/interrupted build is deliverable.
8. Clean-overlay installation and exact file indexing are mandatory.
9. Move, refactor, cutover, quarantine and deletion remain independently reviewable.
10. The final repository must be understandable without the original conversation.

## Authoritative subphase sequence

- [[LCM_08A_CONTEXT_PORTFOLIO_FREEZE_RISK_CLASSIFICATION_AND_PILOT_SELECTION|LCM-08A — Context Portfolio Freeze, Risk Classification and Pilot Selection]]
- [[LCM_08B_PILOT_CONTEXT_MIGRATION_COMPATIBILITY_ADAPTER_AND_BEHAVIORAL_PARITY|LCM-08B — Pilot Context Migration, Compatibility Adapter and Behavioral Parity]]
- [[LCM_08C_CONTEXT_WAVE_MIGRATION_AND_CONTEXT_PORTFOLIO_CLOSURE|LCM-08C — Context Wave Migration and Context Portfolio Closure]]
- [[LCM_09A_SETUP_INVENTORY_FAMILY_REGISTRY_AND_CANONICAL_CONTRACT_FREEZE|LCM-09A — Setup Inventory, Family Registry and Canonical Contract Freeze]]
- [[LCM_09B_SETUP_MIGRATION_SETUP_FACTORY_BINDING_AND_BEHAVIORAL_PARITY|LCM-09B — Setup Migration, Setup Factory Binding and Behavioral Parity]]
- [[LCM_10A_TREATMENT_AND_EXECUTION_CAPABILITY_INVENTORY|LCM-10A — Treatment and Execution Capability Inventory]]
- [[LCM_10B_TREATMENT_PACKAGE_EXTRACTION_AND_EXECUTION_BOUNDARY_CONSTRUCTION|LCM-10B — Treatment Package Extraction and Execution Boundary Construction]]
- [[LCM_10C_DRY_RUN_PARITY_SAFETY_CONTROLS_AND_AUTHORITY_NEGATIVE_CLOSURE|LCM-10C — Dry-Run Parity, Safety Controls and Authority-Negative Closure]]
- [[LCM_11A_VISUAL_OBJECT_INVENTORY_NAMESPACE_AND_LIFECYCLE_CONTRACTS|LCM-11A — Visual Object Inventory, Namespace and Lifecycle Contracts]]
- [[LCM_11B_MULTI_CHART_ISOLATION_VISUAL_PARITY_AND_VISUALIZER_CUTOVER|LCM-11B — Multi-Chart Isolation, Visual Parity and Visualizer Cutover]]
- [[LCM_12A_DOCUMENTATION_AUTHORITY_DUPLICATE_ANALYSIS_AND_CANONICAL_MAPPING|LCM-12A — Documentation Authority, Duplicate Analysis and Canonical Mapping]]
- [[LCM_12B_OBSIDIAN_RECONCILIATION_RELOCATION_AND_DOCUMENTATION_CLOSURE|LCM-12B — Obsidian Reconciliation, Relocation and Documentation Closure]]
- [[LCM_13A_DUAL_RUN_HARNESS_AND_MISMATCH_REGISTRY|LCM-13A — Dual-Run Harness and Mismatch Registry]]
- [[LCM_13B_CONTROLLED_CONSUMER_WAVE_CUTOVER|LCM-13B — Controlled Consumer Wave Cutover]]
- [[LCM_13C_ROLLBACK_DRILL_AND_CUTOVER_CLOSURE|LCM-13C — Rollback Drill and Cutover Closure]]
- [[LCM_14A_DEPRECATION_REGISTRY_AND_COMPATIBILITY_REDIRECTS|LCM-14A — Deprecation Registry and Compatibility Redirects]]
- [[LCM_14B_QUARANTINE_OBSERVATION_AND_RETIREMENT_ELIGIBILITY|LCM-14B — Quarantine, Observation and Retirement Eligibility]]
- [[LCM_15A_DELETION_CANDIDATE_INVENTORY_AND_REFERENCE_PROOF|LCM-15A — Deletion Candidate Inventory and Reference Proof]]
- [[LCM_15B_ROOT_RELEASE_AND_DOCUMENTATION_REORGANIZATION|LCM-15B — Root, Release and Documentation Reorganization]]
- [[LCM_15C_CONTROLLED_DELETION_AND_CLEAN_CLONE_VERIFICATION|LCM-15C — Controlled Deletion and Clean-Clone Verification]]
- [[LCM_16A_FULL_REGRESSION_MQL5_MATRIX_PARITY_AND_SECURITY_AUDIT|LCM-16A — Full Regression, MQL5 Matrix, Parity and Security Audit]]
- [[LCM_16B_RECOVERY_DRILL_FINAL_LEDGER_AND_PROGRAM_CLOSURE|LCM-16B — Recovery Drill, Final Ledger and Program Closure]]

## State semantics

- `PLANNED`: documented but not started.
- `IN_PROGRESS`: bounded working state; no downstream handoff.
- `BLOCKED`: required evidence/decision/tool unavailable.
- `FAILED`: deterministic gate failed.
- `ACCEPTED`: subphase artifacts and handoff accepted.
- `SUPERSEDED`: replaced by a versioned amendment; historical record retained.

A master phase is `ACCEPTED` only when its final subphase is accepted and the consolidated master gate passes.

## Checkpoint strategy

Internal processing may use checkpoints to survive tool/session interruption, but checkpoints are not repository releases. A checkpoint must record input digest, completed workstreams, generated artifacts, failed/unknown checks and resumption instructions. Only the final atomic patch may be committed.

## Change control

Changing subphase order, merging partitions, adding a fourth planned partition, weakening a gate or moving deletion earlier requires a new ADR. Small wording or operational clarifications may update this roadmap without changing the phase graph, provided version and digest are incremented.

## Immediate next action

Implement LCM-08A only. It freezes the Context portfolio and pilot decision; it does not migrate a Context.

## LCM-08B accepted reference

The selected EXP0015 Python pilot is canonicalized and parity-verified under `PILOTMIG_344455420C8CA68E865FD54135E891D7`. LCM-08 remains open until LCM-08C closes the Context wave portfolio.

## LCM-08B accepted reference

The selected EXP0015 Python pilot is canonicalized and parity-verified under `PILOTMIG_344455420C8CA68E865FD54135E891D7`. LCM-08 remains open until LCM-08C closes the Context wave portfolio.
