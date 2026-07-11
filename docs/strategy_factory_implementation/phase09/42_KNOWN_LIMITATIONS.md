---
title: "Known Limitations"
phase: 09
status: canonical
---
# Known Limitations

V1 supports one target with optional partial fraction. Queue position, partial broker fills, exchange fees, dynamic trailing and structural multi-stage exits are deferred to later execution and policy extensions.

## Invariants

- Candidate identity is immutable.
- Every decision uses information available at or before the observation known time.
- Missing or ambiguous information is never silently optimized in favor of the strategy.
- Runtime work and memory are bounded.
- Every policy, cost model and output carries exact versioned lineage.

## Acceptance evidence

Evidence consists of MQL5 self-tests, Python conformance tests, schema validation, static authority guards, deterministic replay hashes and local MetaEditor compile logs.
