---
title: "ADR — Public Registries Are Frozen"
status: accepted
date: 2026-07-13
phase: FP-I02
---
# Public Registries Are Frozen

## Decision

Contract, relation, reason, and transition registries are immutable exact-version objects.

## Context

Runtime mutation would make identical manifests behave differently across processes or restarts.

## Consequences

- Registry hashes enter evidence.
- Unknown exact key fails.
- Change requires new version and vectors.


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
