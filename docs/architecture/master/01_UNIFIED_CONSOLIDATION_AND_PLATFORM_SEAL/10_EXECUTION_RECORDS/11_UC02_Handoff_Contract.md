---
id: UCPS-UC01-HANDOFF-7A058C31
title: "UC-02 Handoff Contract"
type: handoff_contract
status: approved
domain: unified-consolidation-platform-seal
version: 1.0.0
created: 2026-07-23
updated: 2026-07-23
tags:
  - handoff
  - uc-02
  - authority
---
# UC-02 Handoff Contract

UC-02 receives the accepted baseline ID, repository root digest, artifact inventory, symbol inventories, dependency and consumer graphs, behavior characterization, environment manifest, unresolved-item ledger and preservation/recovery receipts.

The handoff does not authorize movement, semantic merging, cutover or deletion. UC-02 may define names, ownership, capability authority, target topology and disposition plans only.

A handoff is issued only when `stage_exit_decision.status` is `ACCEPTED`. Any other status produces `NOT_ISSUED` and keeps UC-02 unauthorized.
