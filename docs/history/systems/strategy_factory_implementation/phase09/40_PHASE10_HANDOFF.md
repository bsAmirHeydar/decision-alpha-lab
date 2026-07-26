---
title: "Phase 10 Handoff"
phase: 09
status: canonical
---
# Phase 10 Handoff

Phase 10 builds the Strategy Tester research harness, run manifests, optimization pass summaries, OnTester metrics, selected-pass full exports, fidelity presets and differential comparison between virtual outcomes and tester execution.

## Invariants

- Candidate identity is immutable.
- Every decision uses information available at or before the observation known time.
- Missing or ambiguous information is never silently optimized in favor of the strategy.
- Runtime work and memory are bounded.
- Every policy, cost model and output carries exact versioned lineage.

## Acceptance evidence

Evidence consists of MQL5 self-tests, Python conformance tests, schema validation, static authority guards, deterministic replay hashes and local MetaEditor compile logs.
