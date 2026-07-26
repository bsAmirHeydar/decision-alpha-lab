---
title: "Stop Entry Semantics"
phase: 09
status: canonical
---
# Stop Entry Semantics

Stop entries trigger when price crosses the requested level. Conservative gap handling can fill at a worse observed open. Trigger-at-level and reject-on-gap remain available for controlled sensitivity tests.

## Invariants

- Candidate identity is immutable.
- Every decision uses information available at or before the observation known time.
- Missing or ambiguous information is never silently optimized in favor of the strategy.
- Runtime work and memory are bounded.
- Every policy, cost model and output carries exact versioned lineage.

## Acceptance evidence

Evidence consists of MQL5 self-tests, Python conformance tests, schema validation, static authority guards, deterministic replay hashes and local MetaEditor compile logs.
