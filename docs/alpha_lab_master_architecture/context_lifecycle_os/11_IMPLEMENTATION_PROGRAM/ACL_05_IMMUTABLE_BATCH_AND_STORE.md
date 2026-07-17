---
title: ACL-05 — Immutable Batch and Artifact Store
status: accepted-reference
version: 1.0.0
updated: 2026-07-18
tags: [acl-os, context-lifecycle, acl-05]
---

# ACL-05 — Immutable Batch and Artifact Store

## Status

`accepted-reference-implementation`

Claim ceiling: `RESEARCH_BATCH_FREEZE_REFERENCE_ONLY`

ACL-05 accepts the exact `ACL04_TO_ACL05` handoff produced by the accepted ACL-04 Dual Setup Factory and converts it into an immutable, content-addressed Research Batch. The phase is complete at reference level only. It does not execute research, infer alpha, submit orders, allocate capital or establish production readiness.

## Accepted upstream dependency

The intake gateway verifies the generated-root marker, closed handoff schema, embedded semantic digests, ACL-04 output manifest, exact file sizes and SHA-256 byte digests, factory receipt, canonical candidate folder, candidate behavior/candidate digests, deduplication report, complete search-exposure ledger and provenance reachability to `ACL03_TO_ACL04`. Partial or hand-edited bundles are denied.

ACL-05 inherits these non-bypassable boundaries:

- Context semantics and known-time rules remain owned by ACL-03.
- Candidate generation, Treatment semantics, behavior normalization and deduplication remain owned by ACL-04.
- Diagnostic candidates are not eligible for ordinary research selection.
- Live order submission and capital activation remain false.

## Owned capabilities

ACL-05 owns:

1. exact ACL-04 binding;
2. authority-permit verification for `ACL05_FREEZE_RESEARCH_BATCH`;
3. deterministic candidate and search-space freeze;
4. dataset snapshot and known-time cut compilation;
5. label maturity and diagnostic segregation contracts;
6. purged walk-forward split contract;
7. reproducible environment lock;
8. compute/storage budget;
9. SHA-256 byte-addressed artifact storage;
10. stable Batch identity and terminal `FROZEN` state;
11. append-only event ledger and provenance graph;
12. atomic publication, manifests and receipts;
13. bounded `ACL05_TO_ACL06` handoff.

It explicitly does not own candidate regeneration, behavior repair, alpha inference, model promotion, portfolio allocation, order construction, broker adapters or runtime execution.

## Batch identity equation

The Batch ID is a deterministic function of the batch key, exact context identity, ACL-04 binding, candidate freeze, search-space freeze, dataset snapshot set, label contract set, split, environment, budget, CAS object index and declared `frozen_at`. No random UUID and no implicit current time participates. Any material change creates a different Batch ID.

## Publication transaction

Outputs are assembled under an isolated staging directory. The destination must be empty. Only after all contracts, CAS objects, event chain, lineage, reports, projections, manifests, receipts and ACL-06 handoff pass validation is staging atomically renamed into place. Exceptions remove staging. Existing non-empty output roots are never overwritten.

## Machine outputs

- `binding/acl04_binding.json`
- `authority/authority_report.json`
- `batch/batch_request.json`
- `batch/candidate_freeze_set.json`
- `batch/search_space_freeze.json`
- `batch/dataset_snapshot_set.json`
- `batch/label_contract_set.json`
- `batch/split_contract.json`
- `batch/environment_lock.json`
- `batch/compute_budget.json`
- `batch/batch_definition.json`
- `batch/batch_manifest.json`
- `batch/freeze_receipt.json`
- `store/object_index.json` and immutable blob objects
- `events/batch_event_ledger.json`
- `lineage/batch_provenance_graph.json`
- integrity and security reports
- generated Obsidian projections
- `handoff/acl06_handoff.json`
- byte-level output manifest and Batch receipt

## Acceptance evidence

Acceptance requires ACL-05 unit/contract/property/mutation/security/replay tests, ACL-04 regression tests, Python compilation, closed JSON schema checks, policy-registry checks, static MQL5 capability scan, reference Batch generation, byte-level manifest verification and clean-checkout delivery validation.

MQL5 files are static contract mirrors only. MetaEditor compilation and MT5 runtime parity are environment-specific evidence and are not claimed.

## Residual risks

The reference dataset is synthetic. No external feed quality, corporate action handling, exchange calendar, broker history, distributed object-store durability, production IAM, signature infrastructure or operational disaster recovery is proven. ACL-06 must consume only the immutable handoff and may not infer that a frozen Batch has research merit.

## Rollback

Before publication, delete staging. After repository installation, revert this commit or remove exactly the patch paths. Never rewrite a generated frozen Batch in place.

## Related

- [[ACL_04_DUAL_SETUP_FACTORY]]
- [[ACL_06_RESEARCH_DAG_ORCHESTRATION]]
- [[IMMUTABLE_RESEARCH_BATCH]]
- [[CONTENT_ADDRESSED_ARTIFACT_STORE]]
- [[BATCH_FREEZE_PROTOCOL]]
