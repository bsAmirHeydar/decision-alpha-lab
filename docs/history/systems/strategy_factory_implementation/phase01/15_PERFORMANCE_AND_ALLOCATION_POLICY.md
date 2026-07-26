# Performance and Allocation Policy

Phase 01 is designed for the future decision fast path.

## Rules

- validate at module boundaries, not repeatedly inside every getter;
- keep canonical contracts compact;
- use fixed enums and primitive fields;
- avoid JSON parsing in the live decision path;
- avoid DataFrames and dynamic imports in MQL5-facing runtime;
- preallocate feature storage in later compiled plans;
- derive IDs once and cache them on accepted immutable objects;
- serialize asynchronously or after decision emission where possible.

## Current trade-off

The FeatureSnapshot uses a dynamic array and linear duplicate lookup because Phase 01 prioritizes correctness and simple cross-version behavior. Phase 08 may replace runtime lookup with a compiled fixed vector while preserving the snapshot schema at the boundary.

## Benchmarks deferred

Microbenchmarks belong to Phase 15 after the compiled decision runtime exists. This phase provides only deterministic low-overhead primitives.
