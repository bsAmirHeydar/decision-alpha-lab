# Phase 02 Handoff — Package Skeleton and Boundaries

Phase 02 must build the stable package and module boundaries around the contracts frozen here.

## Required inputs

- MQL5 contract headers and registry;
- Python mirror package;
- schema files;
- golden vectors;
- Phase 01 QA report;
- unresolved MetaEditor compile evidence, if not yet attached.

## Phase 02 objectives

1. Create MQL5 and Python package roots with explicit ownership.
2. Define ports for market data, artifact persistence, anatomy adapters, and clocks.
3. Remove import-path fragility from clean-checkout tests.
4. Add build/test entry points.
5. Establish dependency direction: contracts <- plugins <- services <- applications.
6. Prevent strategy-specific code from entering the kernel.
7. Preserve MQL5-first runtime authority.

## Exit requirement

A clean checkout must run contract tests with one command, compile the MQL5 self-test through the provided Windows harness, and allow a new adapter package without modifying the contract kernel.
