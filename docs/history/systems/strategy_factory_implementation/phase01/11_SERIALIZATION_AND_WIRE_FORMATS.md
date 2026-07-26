# Serialization and Wire Formats

## Runtime preference

Inside MQL5, contracts remain typed structures. Serialization is for persistence, replay, cross-language transport, and audit—not for every in-memory function call.

## JSONL

Phase 01 provides deterministic field emission for core MQL5 records and a canonical JSON encoder in Python. JSONL is preferred for append-only event streams, debug traces, golden fixtures, and human-auditable interchange.

## CSV

CSV remains acceptable for large terminal exports where MQL5 throughput and spreadsheet inspection matter. Every CSV must have a versioned header and explicit UTC fields. Nested snapshots should use a long feature table or JSONL rather than ad-hoc column explosion.

## Parquet

Python may materialize Parquet for research, but Parquet is not a primary MQL5 runtime format. Parquet artifacts must still carry ArtifactIdentity and schema version.

## Determinism

Key ordering, decimal formatting, enum names, and time units are fixed. Readers reject unknown major versions rather than guessing.
