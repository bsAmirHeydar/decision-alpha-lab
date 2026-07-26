---
title: "ADR-0003 — Consolidate Artifact Persistence"
status: accepted
---

# ADR-0003 — Consolidate Artifact Persistence

## Context

Market bars, nodes, and metrics each construct and persist Parquet paths independently. None records complete lineage, schema version, atomic-write status, or run identity.

## Decision

Phase 05 will implement one shared Artifact Store contract. Domain modules can define payload serializers and logical artifact types but cannot define incompatible physical persistence lifecycles.

## Consequences

- Existing caches are migrated, not deleted immediately.
- Dual-read or dual-write may be used temporarily.
- Artifact identity will include source, producer, schema, configuration, and content hashes.
- Direct `to_parquet` calls inside anatomy/feature modules become deprecated after parity validation.
