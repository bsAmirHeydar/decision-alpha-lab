---
id: UCPS-3E8B8CF72C39
title: "Artifact Disposition and Target Assignment"
type: execution-record
status: approved
domain: unified-consolidation-platform-seal
version: 1.0.0
created: 2026-07-24
updated: 2026-07-24
tags:
  - consolidation
  - uc02
  - authority-freeze
---
# Artifact Disposition and Target Assignment

## Planning dispositions

Every path receives one of six planning dispositions: `KEEP_CANONICAL`, `MOVE`, `MERGE`, `GENERATE`, `EXTERNALIZE` or `DELETE`.

`DELETE` is a future plan, not permission. Destructive action remains prohibited until preservation, consumer cutover, parity, recovery and stage authorization are proven.

## Assignment fields

Each ledger row records:

- source path and source digest;
- source system and category;
- canonical owner and target;
- planning disposition;
- migration action;
- UC-03 wave;
- classification confidence and review requirement;
- explicit false authority flags;
- rationale.

## Review semantics

`review_required` does not mean unknown authority. It means the owner and target are fixed, while the exact file-level relocation or split is reviewed during the relevant UC-03 wave.

## Root release material

Root-level phase README, install, rollback, manifest, QA, hash and inventory files are assigned to release history and scheduled to leave the final root.

## Runtime artifacts

Datasets, models, generated reports and run outputs are scheduled for content-addressed storage outside authored source.
