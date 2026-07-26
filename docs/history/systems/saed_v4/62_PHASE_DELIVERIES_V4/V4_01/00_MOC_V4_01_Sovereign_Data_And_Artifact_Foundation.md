---
title: V4-01 Sovereign Data And Artifact Foundation
status: implemented
version: 1.0.0
phase: V4-01
created: '2026-07-13'
updated: '2026-07-13'
capability_tier: core-production-data-plane
tags:
  - saed-v4
  - v4-01
  - implementation
---

# V4-01 Sovereign Data And Artifact Foundation

> **Phase:** SAED V4-01  
> **Parent:** [[00_MOC_V4_01_Sovereign_Data_And_Artifact_Foundation]]

## Purpose

Navigation, acceptance map, implementation inventory and handoff.

## Institutional invariant

This capability is subordinate to the executable research constitution from V4-00 and to canonical UCEE I01–I18 truth. It may store, validate, version, replay and package evidence, but it cannot infer a Context, select a Treatment, sign promotion, allocate capital, activate runtime, reach a broker or place an order.

## Design

This component is implemented as an exact-version, closed-contract capability. Semantic identity is deterministic; operational timestamps, process IDs and storage locations do not silently alter the identity of the represented evidence. Every failure is explicit and fail-closed.

## Canonical flow

```text
Source or upstream artifact
→ closed schema validation
→ bitemporal and identity validation
→ role and authority gate
→ immutable content storage
→ append-only lineage/revision state
→ deterministic snapshot or bundle
→ integrity receipt
→ downstream handoff
```

## Required controls

- Unknown fields are rejected rather than ignored.
- Exact versions cannot be rebound to different content.
- Protected evidence cannot flow backward into adaptive roles.
- Corrections append revisions and never overwrite history.
- Hash, schema, lineage and role claims are independently verifiable.
- Failure produces rejection, quarantine or review; no permissive default exists.
- UCEE core remains read-only and unchanged.

## Failure modes

| Failure | Result | Recovery |
|---|---|---|
| Unknown or malformed field | Reject | Correct the producer contract |
| Known time before event time | Quarantine | Repair temporal lineage |
| Same version with different hash | Integrity incident | Freeze subject and investigate |
| Protected-to-development flow | Reject | Rebuild from admissible role |
| Lineage cycle | Reject | Correct transform graph |
| Snapshot replay mismatch | Quarantine release | Reproduce environment and inputs |
| Static evidence claimed as actual | Reject claim | Reclassify and requalify |

## Verification

The reference implementation is exercised by golden, negative, mutation and parameter-matrix tests. The MQL5 mirror verifies denial and identity semantics only. MetaEditor compile is external actual evidence and is not inferred from Linux static inspection.

## Review questions

1. What exact artifact, schema version and content hash are being referenced?
2. What was known at the declared known-time boundary?
3. Which evidence role owns the artifact and what operation is requested?
4. Can every output be traced to immutable parents and exact transform hashes?
5. What deterministic reason code is emitted when an invariant is absent?
6. Does this change UCEE truth or grant any authority beyond data custody?

## Acceptance checklist

- [ ] Closed contract validated.
- [ ] Semantic identity reproduced.
- [ ] Temporal boundary verified.
- [ ] Evidence-role operation allowed.
- [ ] Lineage is acyclic and complete.
- [ ] Integrity receipt passes.
- [ ] Failure path tested.
- [ ] Limitations recorded.

## Phase map

- [[01_Mission_Scope_And_Non_Goals]] — Defines the sovereign data-plane mission, exact boundaries and claims that remain prohibited.
- [[02_Constitutional_Entry_Gates]] — Binds every ingestion, access, migration, snapshot and release action to V4-00 authority and evidence rules.
- [[03_Data_Threat_Model]] — Enumerates leakage, revision, contamination, corruption, provenance, poisoning and privilege threats.
- [[04_Bitemporal_Truth_Model]] — Separates event time from known time and prevents future-suffix information from changing historical truth.
- [[05_Source_Trust_And_Connector_Identity]] — Pins source, jurisdiction, trust tier and connector version for every sovereign record.
- [[06_Stable_Identity_And_Content_Hashing]] — Defines semantic IDs, content hashes and fields excluded from semantic identity.
- [[07_Content_Addressed_Artifact_Store]] — Specifies atomic writes, verification, immutable addressing and corruption detection.
- [[08_Closed_Schema_Registry]] — Registers exact schema versions, rejects unknown fields and forbids silent schema drift.
- [[09_Append_Only_Revision_Chains]] — Models corrections without destructive overwrite and preserves exact historical as-of views.
- [[10_Point_In_Time_Query_Semantics]] — Defines known-as-of and event-as-of query semantics for leakage-safe dataset construction.
- [[11_Lineage_DAG_And_Transformation_Identity]] — Records derivation edges, transform hashes and cycle-free ancestry.
- [[12_Evidence_Role_Isolation]] — Prevents protected evidence from flowing back into train, tune or adaptive selection.
- [[13_Atomic_Ingestion_Protocol]] — Validates complete batches before commit and quarantines invalid inputs without partial state.
- [[14_Quarantine_And_Resolution]] — Makes invalid or suspicious data an explicit state requiring evidence-bound resolution.
- [[15_Immutable_Dataset_Snapshots]] — Builds deterministic sorted snapshots with schema-set and lineage roots.
- [[16_Deterministic_Replay_And_Reproduction]] — Reconstructs snapshots exactly and emits mismatch evidence rather than approximate success.
- [[17_Integrity_Receipts_And_Merkle_Roots]] — Packages component hashes into verifiable receipts and detects tampering.
- [[18_Artifact_Catalog_And_Exact_Versioning]] — Registers exact-version artifacts and rejects same-version hash conflicts.
- [[19_Retention_Legal_Hold_And_Deletion]] — Defines minimum retention, permanent evidence and deletion denial semantics.
- [[20_Data_Access_Control]] — Combines principal allowlists with evidence-role operation rules.
- [[21_Explicit_Schema_Migration]] — Requires registered transforms and output hashes for all migrations.
- [[22_Contract_And_Schema_Catalog]] — Maps the twenty-five closed schemas to Python, examples and negative fixtures.
- [[23_Artifact_Bundle_Construction]] — Builds deterministic bundles from artifact, lineage and schema registry hashes.
- [[24_Twin_Seed_Handoff_Contract]] — Defines the only admissible input package for the V4-02 Context Digital Twin Kernel.
- [[25_Python_Reference_API]] — Documents package modules, pure functions, stateful registries and integration boundaries.
- [[26_Command_Line_Interface]] — Documents contract validation and canonical hashing commands.
- [[27_MQL5_Diagnostic_Mirror]] — Mirrors temporal and role denial semantics without broker, order, network or risk authority.
- [[28_Conformance_Vector_Program]] — Defines golden, negative and mutation vectors shared by implementations.
- [[29_Test_Strategy_And_Coverage]] — Covers deterministic identity, temporal integrity, role firewall, storage, replay and schema closure.
- [[30_Failure_Semantics_And_Reason_Codes]] — Defines reject, quarantine, require-review and integrity-incident behavior.
- [[31_Scale_Shards_And_Concurrency]] — Explains content-addressed parallelism, entity revision serialization and partition-safe scale-out.
- [[32_Sovereign_Storage_Layout]] — Defines Bronze, Silver, Gold, Feature, Sequence, Graph, Path, Embedding and Evidence layers.
- [[33_Observability_And_Telemetry]] — Specifies metrics, hashes, reason codes and evidence references for every data-plane action.
- [[34_Security_And_Supply_Chain]] — Addresses untrusted sources, dependency pinning, path traversal, deserialization and artifact signing.
- [[35_Model_Risk_And_Data_Risk_Interface]] — Makes data limitations and support debt visible to downstream model-risk governance.
- [[36_Operations_And_Ownership]] — Defines steward, platform, researcher, validator, security and audit responsibilities.
- [[37_Runbook_Ingest_A_New_Source]] — Step-by-step source onboarding with schema, trust, quarantine and replay gates.
- [[38_Runbook_Apply_A_Data_Revision]] — Step-by-step append-only correction and historical as-of validation.
- [[39_Runbook_Resolve_An_Integrity_Incident]] — Contains corruption, lineage, role and hash incidents without mutating evidence.
- [[40_Acceptance_Evidence_And_QA]] — Maps executable checks to phase acceptance gates and states actual external evidence limits.
- [[41_Limitations_Residual_Risk_And_V4_02_Handoff]] — Freezes unresolved risks and V4-02 entry gates without claiming a Context Twin exists.

## Atomic concepts

- [[01_Bitemporal_Truth_Is_Two_Clocks]]
- [[02_Known-Time_Snapshot_Is_Immutable]]
- [[03_Exact_Version_Means_Exact_Content]]
- [[04_Content_Address_Is_The_Artifact]]
- [[05_Revision_Never_Overwrites_History]]
- [[06_Closed_Schema_Rejects_Surprise]]
- [[07_Lineage_Root_Is_Evidence]]
- [[08_Evidence_Role_Is_A_Firewall]]
- [[09_Atomic_Ingestion_Is_All_Or_None]]
- [[10_Quarantine_Is_A_First-Class_State]]
- [[11_Replay_Must_Reconstruct_Exactly]]
- [[12_Twin_Seed_Is_Not_A_Digital_Twin]]
