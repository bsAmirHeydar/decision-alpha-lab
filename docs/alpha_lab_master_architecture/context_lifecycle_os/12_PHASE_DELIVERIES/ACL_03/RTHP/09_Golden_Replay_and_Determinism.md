---
title: RTHP Golden Replay and Determinism
status: passed
version: 1.0.2
---
# Golden Replay and Determinism

- Golden cases compiled: `12`
- Passed: `12`
- Failed: `0`
- Replay digest: `sha256:90406ce7bab33c8d166af3370c99aa7904b2952773c5fc3033fd4ee27db7c59f`

## Covered mechanics

The replay catalog covers positive High-side and Low-side divergence, bilateral touch, no touch, price-basis mismatch, stale primary/secondary evidence, partial history, zero history, sequential and non-sequential M15 relationships, and restart deduplication.

## Claim boundary

Golden replay proves deterministic mechanics against authored fixtures. It does not prove market validity, profitability, edge, robustness, or production data quality.
