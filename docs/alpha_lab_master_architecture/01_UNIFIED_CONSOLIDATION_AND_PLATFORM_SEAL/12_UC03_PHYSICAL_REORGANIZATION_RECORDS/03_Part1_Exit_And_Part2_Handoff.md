---
id: UCPS-C86F4D1035AE
title: "UC-03 Part 1 Exit and Part 2 Handoff"
type: handoff
status: approved
domain: unified-consolidation-platform-seal
version: 1.0.0
created: 2026-07-25
updated: 2026-07-25
tags:
  - consolidation
  - uc03
  - handoff
---
# UC-03 Part 1 Exit and Part 2 Handoff

## Acceptance gates

- Root file count is at most twenty.
- Root contents equal the approved allowlist.
- Every relocation destination exists and matches its declared source hash before rewriting.
- No historical archived artifact is content-rewritten.
- Active references are rewritten once and recorded.
- Canonical target boundaries exist.
- No executable engine, Context, test or MQL5 source is intentionally relocated in Part 1.

## Handoff

An accepted Part 1 sets `uc03_part2_authorized=true` and leaves `uc04_authorized=false`.

Part 2 may move code, Context packages, tests and MQL5 sources. It may not semantically merge duplicate implementations or retire behavior; those authorities remain reserved for UC-04 and UC-07 respectively.
