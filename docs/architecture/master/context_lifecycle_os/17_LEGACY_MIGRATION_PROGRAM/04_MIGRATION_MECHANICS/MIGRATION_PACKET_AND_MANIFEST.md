---
title: "Migration Packet and Manifest"
status: proposed-reference
version: 1.0.0
updated: 2026-07-18
tags: [acl-os, lcm, legacy-migration]
---
# Migration Packet and Manifest

Every migrated identity owns a packet containing scope, owners, source paths, canonical target, disposition, source hashes, dependency graph, observed behavior, intended doctrine, open decisions, fixtures, trace schema, parity dimensions, tolerance policy, cutover, rollback, quarantine and deletion status.

The packet is append-only for historical transitions. Correcting a false statement creates a superseding record rather than erasing the original decision.
