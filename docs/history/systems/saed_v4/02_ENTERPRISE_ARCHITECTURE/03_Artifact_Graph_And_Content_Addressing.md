---
title: Artifact Graph and Content Addressing
status: canonical
version: 4.0.0
created: '2026-07-13'
updated: '2026-07-13'
tags:
- saed-v4
- enterprise
---

# Thesis

Every scientific and runtime object is an immutable, content-addressed node in a lineage graph.

## Architectural design

### Node types

Raw event partitions, context packages, feature snapshots, treatment universes, outcome cubes, datasets, folds, models, calibration, policies, dossiers, runtime bundles.

### Edges

Derived-from, calibrated-on, validated-on, supersedes, challenges, promoted-as, and revoked-by.

### Storage

Object-store payloads plus transactional metadata registry; no semantic identity based on filenames alone.

## Machine contracts

- `artifact_id`
- `sha256`
- `schema_version`
- `producer_run_id`
- `lineage_edges`
- `retention_class`

## Validation and evidence

- Hash verification at read and publish.
- Garbage collection preserves all promoted or referenced ancestors.
- Reproduction resolves exact dependency graph.

## Failure modes and mandatory response

- **Mutable object under stable ID:** Critical integrity incident.
- **Orphan artifact:** Non-promotable until lineage repaired.
- **Hash mismatch:** Quarantine all descendants.

## UCEE handoff

All outputs bind to exact upstream context, feature, data-role, treatment-universe, and economics hashes. Promotion and runtime authority remain in UCEE I12–I18.

## Related notes

- [[02_Master_System_Map]]
