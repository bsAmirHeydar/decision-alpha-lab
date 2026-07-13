---
title: "ADR — Semantic and Projection Identity Are Separate"
status: accepted
date: 2026-07-13
phase: FP-I02
---
# Semantic and Projection Identity Are Separate

## Decision

Behavior semantics and chart presentation use independent hash domains.

## Context

Mixing style into signal identity would duplicate economic events after visual changes; excluding behavior from identity would contaminate replay and cache.

## Consequences

- SemanticConfiguration produces semantic_config_hash.
- ProjectionConfiguration produces projection_config_hash.
- Projection objects include signal_id + projection hash + chart instance.


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
