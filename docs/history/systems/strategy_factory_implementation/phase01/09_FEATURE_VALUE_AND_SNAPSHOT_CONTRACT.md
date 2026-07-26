# FeatureValue and FeatureSnapshot Contract

## FeatureValue

Every feature has a stable ID, version, tagged type, quality state, known time, source event, source hash, and value. Supported foundation types are double, integer, boolean, string, timestamp, and null.

## Quality is explicit

A value may be valid, missing, stale, invalid, estimated, or unknown. Missing must not be encoded as zero. Stale must not be treated as current. Later model-vector compilation will define per-feature fallback and abstention behavior.

## Snapshot

A FeatureSnapshot freezes the exact context visible to a decision. It includes event ID, strategy ID, snapshot time, producer/version, source hash, state generation, and an ordered set of unique feature values.

## Ordering policy

Phase 01 preserves insertion order in the canonical snapshot identity. Later Phase 08 will compile a fixed feature DAG and vector schema. Once a strategy is promoted, that order becomes part of its model artifact and cannot change silently.

## Fail-closed rules

Duplicate feature IDs, a feature known after snapshot time, invalid quality/type combinations, or a mismatched snapshot ID invalidate the snapshot.
