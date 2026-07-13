---
title: "ADR — Public Enums Are Closed and Versioned"
status: accepted
date: 2026-07-13
phase: FP-I02
---
# Public Enums Are Closed and Versioned

## Decision

Every public state, policy, relation, direction, role, and reason uses an exact enum/registry.

## Context

Free text and silent ordinal changes make Python/MQL5 parity and persisted evidence ambiguous.

## Consequences

- Unknown values fail.
- MQL5 enum ordering is versioned.
- A new value requires a versioned migration.


## Rejected alternatives

- Implicit defaults not present in the manifest.
- Free-text state or reason values.
- Runtime mutation of registries.
- Last-write-wins identity conflicts.
- Treating static MQL5 scans as successful compilation.

## Verification

- Python contract and negative tests.
- Closed JSON Schema validation.
- Golden identity vector replay.
- MQL5 static parity and local self-test compile.
- Patch boundary and previous-context regression checks.

## Rollback

Revert files in the FP-I02 file index. Persisted FP-I02 evidence remains archived; downstream checkpoints carrying FP-I02 versions are ignored by the restored code.
