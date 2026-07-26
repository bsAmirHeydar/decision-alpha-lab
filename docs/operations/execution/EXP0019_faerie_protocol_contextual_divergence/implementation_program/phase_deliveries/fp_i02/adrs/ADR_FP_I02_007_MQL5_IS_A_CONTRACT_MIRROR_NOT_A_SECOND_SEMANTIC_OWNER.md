---
title: "ADR — MQL5 Is a Contract Mirror, Not a Second Semantic Owner"
status: accepted
date: 2026-07-13
phase: FP-I02
---
# MQL5 Is a Contract Mirror, Not a Second Semantic Owner

## Decision

Python artifacts and normative documentation own wire semantics; MQL5 mirrors them for compile/runtime use.

## Context

Independent MQL5 definitions could drift and create two incompatible Faerie Protocols.

## Consequences

- Static counts and enum parity are tested.
- MQL5 cannot add hidden defaults.
- MetaEditor compile is retained as separate evidence.


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
