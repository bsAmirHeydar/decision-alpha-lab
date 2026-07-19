---
title: "Migration Wave Portfolio"
status: proposed-reference
version: 2.0.0
updated: 2026-07-19
tags: [acl-os, lcm, legacy-migration]
---
# Migration Wave Portfolio

Wave order is based on dependency and risk, not business importance or age. Every wave begins with a fresh ownership, identity, reachability, evidence and shared-dependency review.

## Relationship to the refined phases

- LCM-08A freezes candidate wave assignment and selects the pilot.
- LCM-08B proves the migration pattern on Wave 01 pilot scope.
- LCM-08C authors and parity-verifies Context packages wave by wave but does not switch active consumers.
- LCM-09 through LCM-12 complete Setup, Treatment, visual and documentation packages needed by each wave.
- LCM-13 performs actual dual run and consumer cutover in bounded wave releases.
- LCM-14 and LCM-15 operate only after wave cutover closure.

| Wave | Scope | Admission condition | Package-ready exit | Cutover exit |
|---|---|---|---|---|
| 00 | protect platform; characterize shared primitives | LCM-07 accepted | approved shared dependencies and exclusions | not a consumer wave |
| 01 | low-risk read-only pilot | LCM-08A pilot selected | LCM-08B accepted | LCM-13 wave closure |
| 02 | M-series and research contexts | pilot pattern accepted | packages and parity accepted | LCM-13 wave closure |
| 03 | EXP0018 Daye Trader | time/session dependencies accepted | MTF/session/reference packages accepted | LCM-13 wave closure |
| 04 | EXP0015/16/17 intermarket | intermarket primitives accepted | Context/Setup/Treatment boundaries accepted | LCM-13 wave closure |
| 05 | EXP0019 Faerie Protocol | shared cores and owner decisions accepted | all explicit variants and open decisions preserved | LCM-13 wave closure |
| 06 | FlagCounting/NDS/Hook/Zone | high-risk sub-wave plan accepted | state/file/drawing/order paths separated | LCM-13 wave closure |
| 07 | E-series, CG/STC, Astro and broker adapters | canonical domain packages accepted | disabled adapter and dry parity accepted | separate execution authority still required |
| 08 | docs/root/archive cleanup | all relevant cutovers closed | documentation reconciliation accepted | LCM-14/15 closure |

## Non-compensatory wave rule

A wave cannot be declared ready because most identities pass. Every active identity must be migrated, explicitly blocked, archived by approved disposition or excluded with authority. Aggregate parity percentages cannot compensate for one failed known-time, state, execution-authority or deletion gate.

## LCM-08C closure snapshot

Closure `CTXWAVECLOSE_D14965CFA16DD2B417DEE789D21AF5C3` published deterministic wave receipts for 6 frozen waves. The EXP0015 pilot is the only migrated Context; all other members remain visible as blocked. No consumer cutover occurred.
