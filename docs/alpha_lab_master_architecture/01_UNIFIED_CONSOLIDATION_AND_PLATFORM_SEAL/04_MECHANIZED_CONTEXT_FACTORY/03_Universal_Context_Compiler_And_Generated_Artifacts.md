---
id: UCPS-2C69B94D6ADA
title: "Universal Context Compiler and Generated Artifacts"
type: architecture
status: canonical
domain: unified-consolidation-platform-seal
version: 1.0.0
created: 2026-07-23
updated: 2026-07-23
tags:
  - consolidation
  - platform-seal
---
# Universal Context Compiler and Generated Artifacts

## Compiler responsibility

The compiler validates the authored contract and deterministically produces canonical identity, Context IR, state machine, known-time guards, occurrence schemas, feature bindings, representation views, label templates, task templates, training plan, Treatment compatibility, test scaffold, MQL5 contracts, registry records, documentation projections, evidence requirements and monitoring skeleton.

## Determinism

Same source digest, compiler version, policy bundle and dependency lock must produce identical output digests. Non-deterministic inputs are explicit and seeded.

## Generated-file rules

Every generated artifact declares source, digest, producer, compiler version and schema version. Generated files are never hand-edited. Local build output resides outside authored source; selected golden outputs may be committed as fixtures.

## Universal constraint

Shared compiler code cannot branch on RTHP or any Context ID. Context-specific behavior enters through validated contracts and extension ports.

## Failure output

Compilation errors are reason-coded, point to the exact contract path and list allowed next actions. Partial output is unpublished unless the compiler explicitly supports an atomic preview mode.
