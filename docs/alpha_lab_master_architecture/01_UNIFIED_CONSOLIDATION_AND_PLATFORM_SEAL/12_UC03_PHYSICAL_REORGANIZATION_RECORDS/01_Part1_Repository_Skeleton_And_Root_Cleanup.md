---
id: UCPS-A4E7D2B19F30
title: "UC-03 Part 1 — Repository Skeleton and Root Cleanup"
type: execution-record
status: approved
domain: unified-consolidation-platform-seal
version: 1.0.0
created: 2026-07-25
updated: 2026-07-25
tags:
  - consolidation
  - uc03
  - root-cleanup
---
# UC-03 Part 1 — Repository Skeleton and Root Cleanup

## Objective

Create the approved repository boundaries and remove historical delivery clutter from the repository root without changing executable business semantics.

## Scope

- Create the empty canonical boundaries required by the target topology.
- Retain only the approved root allowlist.
- Move every other root file byte-for-byte into `releases/history/<program>/<artifact-type>/`.
- Preserve a complete source-to-destination relocation map and hashes.
- Rewrite active textual references outside the historical archive.
- Keep all current engines, contexts, tests, registries and MQL5 sources in their existing executable locations until Part 2.

## Explicit non-scope

- No semantic merge.
- No source-code retirement.
- No Context migration.
- No MQL5 code relocation.
- No live, broker, order or capital authority.
- No authorization for UC-04.

## Root target

The accepted root contains fourteen compatibility and repository-control files, remaining below the stage limit of twenty. Generic legacy control names are temporarily retained because they are ambiguous across historical packages and will be retired only after their consumers are resolved.

## Evidence

The executable patch produces:

- root relocation receipt;
- reference rewrite receipt;
- Part 1 exit decision;
- exact Git staging index containing additions, modifications, moves and deletions.
