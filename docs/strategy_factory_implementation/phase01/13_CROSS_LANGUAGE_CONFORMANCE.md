# Cross-Language Conformance

Golden vectors are the contract between MQL5 and Python.

## Current vectors

The repository includes a canonical EXP0017-style AnatomyEvent, one divergence-strength feature, and one FeatureSnapshot. Expected event and snapshot IDs are stored in `cross_language_vectors.json` and hard-coded into the MQL5 self-test EA.

## Conformance process

1. Python computes canonical payload and stable ID.
2. MQL5 computes the same payload and ID.
3. Both validate causality and identifiers.
4. MQL5 prints deterministic JSON for inspection.
5. Any mismatch blocks the phase.

## Future vectors

Every contract addition and every schema minor/major change must add vectors for normal, boundary, missing, stale, invalid, and migration cases.
