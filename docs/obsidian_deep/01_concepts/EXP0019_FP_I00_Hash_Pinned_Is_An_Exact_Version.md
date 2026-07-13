---
title: "EXP0019 FP I00 Hash Pinned Is An Exact Version"
tags: [exp0019, faerie-protocol, fp-i00, governance, obsidian]
status: implemented
experiment: EXP0019
context_id: FP-CONTEXT-001
phase_id: FP-I00
phase_version: 1.0.0
doc_version: 1.0.0
last_updated: 2026-07-13
language: en
---
# EXP0019 FP I00 Hash Pinned Is An Exact Version

## Definition

When a shared core lacks canonical SemVer, the aggregate SHA-256 of its exact ordered file set is the component version. This is stricter than a human label such as current or latest.

## Why this matters

Faerie Protocol is being integrated into a repository that already contains multiple divergence contexts, research pipelines, indicators, EAs, and Strategy Factory services. Governance must make semantic boundaries machine-verifiable before new code shares these foundations.

## Operational rule

- Put the rule in a closed policy or manifest.
- Include behavior-bearing fields in canonical identity.
- Add a positive and negative executable test.
- Preserve evidence for the next phase.
- Never substitute prose for a missing contract.

## Related artifacts

- `FP_I00_BASELINE_MANIFEST.v1.json`
- `FP_I00_VALIDATION_REPORT.json`
- [[../../execution/EXP0019_faerie_protocol_contextual_divergence/implementation_program/phase_deliveries/fp_i00/00_FP_I00_DELIVERY_MOC|FP-I00 Delivery MOC]]
