---
title: RTHP MT5 Automation — Canonical Landing Zone, Provenance, Hashing, and Immutability
status: roadmap-approved-for-implementation
version: 1.0.0
updated: 2026-07-22
tags: [rthp, data-lake, provenance, hashing]
---

# Canonical Landing Zone, Provenance, Hashing, and Immutability

## Artifact layers

```text
raw_receipts/
normalized_m1/
quality_reports/
metadata/
manifests/
hashes/
```

## Recommended generated-run placement

```text
lab/11_strategy_factory/runs/rthp_mt5/<run_id>/source/
```

The repository stores schemas, templates, and documentation. Large market-data artifacts may live outside Git but must be referenced by immutable URI and SHA-256 digest.

## Required source artifacts

Per symbol:

- normalized M1 artifact;
- symbol metadata snapshot;
- acquisition receipt ledger;
- quality report;
- coverage report;
- SHA-256 digest.

Per pair:

- common-range decision;
- cross-symbol alignment report;
- calendar version;
- cycle-registry version;
- source-binding manifest.

## Write protocol

1. Write to a run-scoped staging directory.
2. Validate all records and reports.
3. Compute hashes.
4. Write the immutable manifest.
5. Atomically promote the staging directory.
6. Never mutate a completed source snapshot.

Corrections produce a new source revision and supersession link.
