---
title: "LCM-08B — 27 Rollback Runbook"
status: accepted-reference
version: 1.0.0
updated: 2026-07-19
tags: [acl-os, lcm, lcm-08b, pilot-migration]
phase_id: LCM-08B
---
# Rollback Runbook

Remove only the LCM-08B indexed additions and restore the few modified roadmap documents from the predecessor commit. Recompute the legacy source hash and re-run LCM-08A verification. Because no consumer switched and no persistent state changed, rollback does not require data migration.
