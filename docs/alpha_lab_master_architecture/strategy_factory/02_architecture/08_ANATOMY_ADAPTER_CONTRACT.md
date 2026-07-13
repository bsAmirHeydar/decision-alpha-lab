---
type: strategy-factory-document
status: canonical
title: "Anatomy Adapter Contract"
tags:
  - strategy-factory
---

# Anatomy Adapter Contract

The anatomy adapter is the only strategy-specific gateway into the factory. It converts approved market objects into canonical events and features without creating trading authority.

## Responsibilities

The adapter reads an existing deterministic engine or historical export, assigns stable event identity, records event time and known time, preserves parent/child lineage, assigns a market-event cluster, and provides features available at a specified decision time. It validates but does not reinterpret the canon.

## Prohibitions

Adapters may not calculate outcomes, inspect bars after decision time, choose the best entry, rank events, suppress losing examples, call broker APIs, or change event definitions based on model feedback. A feature-provider extension must declare availability time for every feature.

## Minimal implementation

Implement `emit_events` and `build_snapshot`. The CSV reference adapter allows immediate onboarding from Excel/CSV. Production adapters should read canonical engine output directly and export the same schema. Adapter tests must cover duplicate identities, missing references, partial history, and closed-bar timing.

## Acceptance criteria

Two independent replays over identical source data must emit byte-equivalent canonical payloads. Event counts and hashes must remain stable across renderer changes. If a source correction legitimately changes events, the source hash and anatomy version must change.

