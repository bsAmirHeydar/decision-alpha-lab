---
title: "JSONL Result Sink"
phase: 05
status: canonical
tags: [strategy-factory, mql5-first, runtime-generation, result-sink]
---

# JSONL Result Sink

## Purpose

Terminal sandbox paths, append semantics, flushing, error behavior and recovery.

## Canonical rules

1. MQL5 owns runtime generation, event order and result emission.
2. A run is not reproducible unless its manifest is materialized and hashed.
3. A generation is activated only after exact plugin resolution, resource preparation and sink validation.
4. Every result is append-only, monotonically sequenced and bound to one run and one generation.
5. Runtime payloads remain typed in memory; serialization belongs to the persistence path.
6. A required sink failure is explicit and may fail the runtime closed.
7. Python may validate, train and report; it cannot rewrite MQL5 runtime truth.
8. Phase 05 contains no strategy-specific anatomy and no broker order authority.

## Operational model

```text
Run Manifest
→ Exact Plugin Factory
→ Descriptor and Requirement Evidence
→ Runtime Generation Compiler
→ WARMED Generation
→ Atomic Activation
→ Typed Runtime
→ Versioned Result Envelope
→ Append-Only Sink
→ Seal and Retire
```

## Failure policy

Invalid identity, illegal lifecycle transition, sequence regression, duplicate record, path traversal, oversized payload or required write failure is never converted into a guessed success.

## Evidence

- MQL5 headers and host
- Python conformance package
- JSON schemas
- Phase-owned tests
- local MetaEditor compile log
- self-test journal
