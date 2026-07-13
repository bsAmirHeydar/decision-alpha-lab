---
type: strategy-factory-document
status: canonical
title: "Event Identity and Lineage"
tags:
  - strategy-factory
---

# Event Identity and Lineage

Stable identity makes deduplication, replay, cross-language reconciliation, and audit possible.

## Identity ingredients

An event ID is a deterministic hash of semantic fields: strategy version, symbol universe, direction, canonical reference identity, known time, timeframe or cycle group, and any object IDs required by the doctrine. Database row number, chart object handle, random UUID, and array position are forbidden.

## Lineage

Events may reference parent events, source references, anatomy objects, and a source hash. Candidate IDs include event ID and policy identity. Outcome IDs derive from candidate identity and simulation version. Model decisions include model artifact hash. Broker traces include intent identity.

## Mutation policy

Canonical artifacts are append-only. A corrected event is a new version or superseding record, not an in-place silent edit. Lineage tables preserve the mapping. Reports declare which supersession policy they applied.

