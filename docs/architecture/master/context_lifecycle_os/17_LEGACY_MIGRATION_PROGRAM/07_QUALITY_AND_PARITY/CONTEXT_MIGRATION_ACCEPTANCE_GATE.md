---
title: "Context Migration Acceptance Gate"
status: proposed-reference
version: 1.0.0
updated: 2026-07-18
tags: [acl-os, lcm, legacy-migration, project-decision]
---
# Context Migration Acceptance Gate

A Context cannot advance to `CUTOVER_APPROVED` unless every gate below is satisfied or explicitly not applicable under a reviewed policy.

| Gate | Required evidence |
|---|---|
| identity | canonical ID, version, alias and locator |
| authority | semantic owner and independent reviewer |
| source integrity | original paths, hashes and baseline binding |
| doctrine | source authority and open-decision register |
| known-time | event/availability/closed-bar contract |
| state | states, events, transitions, invalid transitions |
| occurrence | positive, negative, missing and no-trade behavior |
| reference lifecycle | freshness, consumption, invalidation and expiry |
| fixtures | golden, edge, restart, session and missing-data cases |
| trace parity | zero unresolved hard mismatches |
| platform adapter | CopyRates/series/time/symbol error behavior |
| visualization | no domain mutation; anchor/lifecycle parity if present |
| execution | absent from Context core; dry adapter only if relevant |
| performance | incremental update and resource budget |
| documentation | canonical page, source evidence and successor links |
| rollback | tested restoration and consumer reversion |
| security | no hidden order, file, network or capital escalation |

Compile success is one item of platform evidence and cannot compensate for a failed semantic gate.
