---
title: "LCM-01 Stage Receipt Model"
status: implemented-reference
version: 1.0.0
updated: 2026-07-18
tags: [acl-os, lcm, lcm-01]
phase_id: LCM-01
claim_ceiling: FORENSIC_SURVEY_REFERENCE_ONLY
---
# LCM-01 Stage Receipt Model

Every scan stage emits a receipt containing baseline bindings, output paths, file sizes, SHA-256 digests, metrics and explicit denials of destructive or runtime authority.

Finalization fails when a stage receipt is absent, has an invalid digest, references a changed output, binds another baseline, or claims source mutation. Stage receipts make partial scan execution visible rather than silently treating missing stages as empty evidence.
