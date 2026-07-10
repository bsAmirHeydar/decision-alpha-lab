---
id: AIEOS2-A2B96223BC48
title: "Alpha Lab Data and Schema Standard"
type: standard
status: active
domain: engineering
version: 2.0.0
created: 2026-07-10
updated: 2026-07-10
tags:
  - ai-engineering
  - alpha-lab
  - engineering
---
# Alpha Lab Data and Schema Standard

## Data Contract Minimum

Every persisted table/file defines:

```text
name and owner
producer and consumers
schema_version
primary key
row grain
field names/types/units
null/unknown representation
timezone and timestamp meaning
availability time
sort order
lineage
retention and migration
```

## Identity

Primary keys are stable research identity, not display labels. Duplicate or empty keys are critical failures. Child datasets may omit parent rows only under an explicit filter contract; they may not invent orphan identities.

## Causal Availability

For every feature distinguish:

```text
event_time
observation_time
availability_time
processing_time
```

A live/model feature is legal only if availability time is not after decision time.

## Schema Evolution

- Additive compatible fields: minor schema version.
- Changed meaning/type/key/grain: major schema version and migration.
- Consumers declare supported versions.
- Producers and downstream summaries are reconciled by row counts and keys.
- CSV headers are APIs; renames require migration, not silent edits.

## Serialization

- UTF-8.
- Stable header and column order.
- Locale-independent numbers.
- ISO-8601 timestamps with explicit zone/basis.
- Explicit booleans and nulls.
- Quotes/escaping handled by a tested parser.
