---
title: Three-Plane Architecture
status: canonical
version: 2.0.0
created: '2026-07-13'
updated: '2026-07-13'
tags:
- saed-v2
- enterprise
---

# Thesis

Research, governance, and runtime must be physically and logically separated so experimentation cannot silently mutate capital-bearing decisions.

## Architectural design

### Research plane

Owns data preparation, simulation, training, causal analysis, stress generation, and candidate reports. It may read only roles allowed by the experiment manifest.

### Governance plane

Owns role locks, review workflows, signatures, model-risk records, revocation, and audit.

### Runtime plane

Loads only signed immutable generations and has no trainer, notebook, package installer, or internet dependency.

## Machine contracts

- `research_run_id`
- `governance_case_id`
- `runtime_generation_id`
- `artifact_signature`
- `environment_attestation`

## Validation and evidence

- Network and filesystem boundary tests.
- Attempted cross-plane writes are denied.
- Runtime reconstruction uses only the signed bundle.

## Failure modes and mandatory response

- **Shared mutable artifact path:** Quarantine and rebuild under content-addressed storage.
- **Research credential available in runtime:** Security blocker.
- **Runtime can import training code:** Boundary failure; no qualification.

## UCEE handoff

All outputs bind to exact upstream context, feature, data-role, treatment-universe, and economics hashes. Promotion and runtime authority remain in UCEE I12–I18.

## Related notes

- [[02_Master_System_Map]]
