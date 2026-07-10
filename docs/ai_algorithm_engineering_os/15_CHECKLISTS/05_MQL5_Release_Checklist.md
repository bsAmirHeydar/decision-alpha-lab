---
id: AIEOS-36AC90BB3F
title: "MQL5 Release Checklist"
type: checklist
status: active
domain: checklist
version: 1.0.0
created: 2026-07-10
updated: 2026-07-10
tags:
  - ai-engineering
  - checklist
  - checklist
---
# MQL5 Release Checklist

> [!abstract] Purpose
> Control an MQL5 indicator or expert patch before delivery

## Compile

- [ ] Correct target file compiles with zero errors.
- [ ] Warnings are zero or individually justified.
- [ ] Includes and public inputs remain compatible.

## Lifecycle

- [ ] Attach, init, history load, new tick, new bar, parameter change, timeframe change, symbol change, recompile, and removal are tested.

## State

- [ ] Replay/reload state matches uninterrupted processing.
- [ ] Array direction, bar time, index, and partial-bar behavior are correct.

## Rendering

- [ ] Object IDs are deterministic.
- [ ] No duplicates or stale objects remain.
- [ ] Zoom, scroll, redraw, and cleanup behave correctly.

## Performance

- [ ] No unnecessary full-history scan, object recreation, redraw, or hot-path logging occurs.

## Package

- [ ] ZIP paths, extraction command, cleanup command, manifest, commit, and rollback are verified.

## Gate Result

- **PASS:** every mandatory item is checked and evidence is linked.
- **CONDITIONAL:** only explicitly accepted, time-bounded exceptions remain.
- **FAIL:** any domain rule, safety rule, compilation rule, or state-integrity item is unresolved.

## Evidence Record

| Item | Evidence link / command output | Reviewer | Date |
|---|---|---|---|
|  |  |  |  |

## Related Notes

- [[17_GOVERNANCE/02_Quality_Gates|Quality Gates]]
- [[17_GOVERNANCE/06_Definition_of_Done|Definition of Done]]
