---
title: Control Plane and Data Plane
status: canonical
version: 2.0.0
created: '2026-07-13'
updated: '2026-07-13'
tags:
- saed-v2
- enterprise
---

# Thesis

The control plane declares what is allowed; the data plane executes only those declarations and records immutable evidence.

## Architectural design

### Control plane

Experiment manifests, budgets, data roles, treatment universe, model capability tiers, authority, and promotion state.

### Data plane

Event replay, feature materialization, outcome generation, training, inference, and telemetry.

### Evidence plane

Content hashes, lineage edges, logs, metrics, incidents, and reviewer decisions.

## Machine contracts

- `control_manifest`
- `execution_plan`
- `evidence_bundle`
- `lineage_graph`
- `policy_decision`

## Validation and evidence

- Plan-to-execution hash equality.
- All outputs map to one declared plan.
- Undeclared tasks cannot publish artifacts.

## Failure modes and mandatory response

- **Ad hoc notebook output promoted:** Reject; only compiled runs are admissible.
- **Missing lineage edge:** Artifact is non-promotable.
- **Plan changed after start:** Fork a new run identity.

## UCEE handoff

All outputs bind to exact upstream context, feature, data-role, treatment-universe, and economics hashes. Promotion and runtime authority remain in UCEE I12–I18.

## Related notes

- [[02_Master_System_Map]]
