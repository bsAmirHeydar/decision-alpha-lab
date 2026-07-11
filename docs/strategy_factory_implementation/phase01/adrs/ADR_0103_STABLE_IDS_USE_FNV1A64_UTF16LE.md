# ADR 0103 — Stable IDs Use FNV-1a 64 over UTF-16LE

**Status:** Accepted

This algorithm is fast, simple in MQL5, exactly reproducible in Python, and suitable for deterministic idempotency IDs. Cryptographic source integrity remains SHA-256 or stronger in lineage fields. A collision is treated as a critical incident and requires a major schema revision.
