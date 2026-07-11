---
title: "Gap Recovery and Series Rebuild Protocol"
status: implemented
phase: PHASE_03
language: en
tags:
  - strategy-factory
  - phase03
  - mql5
  - market-services
---

# Detection is implemented; recovery is controlled

The bar cache marks a gap when a newly accepted bar opens later than the expected next open time. The flag remains set.

# Future rebuild protocol

A trusted rebuild should:

1. stop decision consumption for the affected series;
2. request a bounded history window from the source;
3. normalize oldest to newest;
4. validate every Phase 01 bar contract;
5. verify exact continuity for standard timeframes;
6. compare overlapping bars with cached content;
7. replace the series atomically;
8. increment series generation;
9. emit a recovery audit record;
10. rerun synchronization gates.

# Conflicts

If overlapping historical bars differ, the incident is a source correction rather than a simple gap. The runtime should retain old and new source hashes for investigation.

# Why no automatic forward fill

Forward filling price bars fabricates highs, lows, volume, and path ordering. It is not valid for anatomy, stop/target geometry, or outcomes. Non-price contextual sources may later define separate imputation contracts.

# Restart behavior

Persistent cache recovery is deferred. Until then, a restart warms history from the terminal before the anatomy plugin is allowed to run.
