# Identity, Hashing, and Idempotency

## Purpose

Stable IDs prevent duplicate events, duplicate snapshots, duplicate candidate generation, duplicate orders, and silent reprocessing differences between MQL5 and Python.

## Algorithm

The kernel uses FNV-1a 64-bit over UTF-16 little-endian bytes. MQL5 strings naturally expose UTF-16 code units; Python explicitly encodes `utf-16le`. IDs use a type prefix and sixteen lowercase hexadecimal digits.

Examples:

```text
evt_<16 hex>
snap_<16 hex>
bar_<16 hex>
art_<16 hex>
```

## Canonical payload rules

- field order is fixed in code;
- identity identifiers must be ASCII-safe;
- timestamps are epoch-millisecond integers;
- enums use canonical names;
- numeric identity fields use integer representation;
- floating prices are excluded from event identity unless the owning contract explicitly freezes a decimal format;
- metadata does not silently alter identity.

## Collision policy

FNV-1a is not a cryptographic integrity hash. It is an efficient deterministic identity hash. Source artifacts retain cryptographic hashes such as SHA-256 in `source_hash` and `manifest_hash`. If two distinct canonical payloads ever produce the same stable ID, the registry must treat it as a critical incident and move to a wider ID contract in a major schema version.
