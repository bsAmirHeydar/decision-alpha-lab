---
id: UCPS-UC01-RECOVERY-6E7BE20D
title: "Recovery Drill and Determinism"
type: recovery_standard
status: approved
domain: unified-consolidation-platform-seal
version: 1.0.0
created: 2026-07-23
updated: 2026-07-23
tags:
  - recovery
  - determinism
  - restore
---
# Recovery Drill and Determinism

The recovery drill extracts the external materialized-source archive into a temporary isolated workspace. Every expected path is rehashed and compared with the artifact inventory. Missing, extra or changed paths fail the drill.

The drill compares both file-level values and the canonical repository root digest. It then destroys the temporary workspace. The Git bundle is independently verified.

The archive uses deterministic path ordering and fixed ZIP timestamps. Gzip JSONL outputs use fixed metadata and canonical JSON ordering, enabling byte-stable repeated capture when repository content and environment-bound inputs are unchanged.
