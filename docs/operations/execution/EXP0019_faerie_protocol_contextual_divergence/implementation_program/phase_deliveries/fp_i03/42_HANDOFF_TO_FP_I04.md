---
title: "FP-I03 — Handoff to FP-I04 M1 Synchronization"
tags: [exp0019, faerie-protocol, fp-i03, time-calendar, obsidian]
status: normative
phase: FP-I03
phase_version: 1.0.0
doc_version: 1.0.0
last_updated: 2026-07-13
language: en
---
# Handoff to FP-I04 M1 Synchronization

## Purpose

FP-I04 may consume canonical UTC timestamps, NyTimestamp, trading-day/session/week windows, gap states, IDs, and evidence hashes. It may not change calendar semantics while aligning two-symbol M1 data.

## Canonical decisions

- Timezone: `America/New_York`.
- Trading day: `[18:00 previous civil date, 17:00 labeled date)`.
- A: `[18:00, 04:00)`; L: `[04:00, 09:30)`; N: `[09:30, 17:00)`.
- Daily gap: `[17:00, 18:00)`.
- Week: `[Sunday 18:00, Friday 17:00)`.
- Exact boundaries belong to the interval beginning at that instant.

## Data and identity impact

This rule is semantic. Any change requires a new version and changes downstream window identities, source revision lineage, reference IDs, candidate IDs, and replay evidence. Projection styling cannot alter these identities.

## Acceptance examples

| Input | Expected evidence |
|---|---|
| Sunday 17:59:59.999 NY | weekend closed |
| Sunday 18:00:00 NY | A session and new NY week |
| 04:00:00 NY | L session |
| 09:30:00 NY | N session |
| 17:00:00 NY | daily gap, or weekend closed on Friday |

## Normative invariants

1. **UTC is the canonical instant axis.** New York and broker values are projections.
2. **Intervals are half-open.** Start is included and end is excluded.
3. **Configuration and registry versions are identity-bearing.** Silent defaults are forbidden.
4. **The kernel is deterministic.** Same config and UTC input produce byte-equivalent semantic output.
5. **The phase has no market-data, drawing, or execution authority.**

## Contract flow

```text
UTC instant or explicit-offset broker instant
                │
                ▼
versioned New York rule resolver
                │
                ├─ New York civil timestamp / offset / fold
                ├─ trading-date label and 18:00→17:00 window
                ├─ A / L / N / daily-gap classification
                └─ Sunday 18:00→Friday 17:00 week window
                │
                ▼
canonical IDs + boundary evidence + CalendarSnapshot
                │
                ▼
FP-I04 M1 synchronization and later context phases
```

## Failure matrix

| Failure | Detection | Disposition |
|---|---|---|
| Unsupported year | deterministic rule-range guard | `BLOCKED`; no extrapolation |
| Invalid broker offset | explicit range validation | reject adapter input |
| Ambiguous local boundary | candidate count = 2 | apply declared policy or reject |
| Nonexistent local boundary | candidate count = 0 | reject boundary construction |
| Session containment mismatch | classified state vs resolved window | critical failure |
| Registry/config drift | exact hash/version comparison | rebaseline required |
| Weekend or daily gap | valid calendar classification | no session ownership; not a kernel error |

## Required evidence

- `time_rule_version`, `calendar_version`, and `session_registry_version`.
- `config_hash`, registry hash, and exact contract version.
- UTC instant, New York civil value, offset, DST regime, and fold.
- Trading-day, session, week, and boundary IDs.
- Closed reason code and health state.
- Golden fixture ID or diagnostic evidence hash.

## Executable test obligations

- Repeat identical input and compare every semantic ID.
- Change one behavior-bearing policy and prove identity changes.
- Test one millisecond before and exactly at each boundary.
- Test both DST transitions and local ambiguity/nonexistence.
- Prove two broker offsets representing one UTC instant produce the same identities.
- Scan for chart, order, position, broker-action, and network authority.

## Operational guidance

- Convert source time to UTC before calendar classification.
- Never derive New York offset from the current chart or server timezone.
- Never identify a session from formatted text alone; use the resolved enum and window.
- Persist the config and registry hashes with downstream data revisions.
- Treat daily gap/weekend closure as explicit states, not missing data.

## Residual risks

- The deterministic rule supports US rules from 2007 onward; earlier history is intentionally blocked.
- Future legislation can invalidate the rule and requires a new version.
- Holiday and early-close calendars are not part of FP-I03.
- MetaEditor compilation remains a local Windows gate until actual logs are retained.

## Code surfaces

- `lab/10_infrastructure/EXP0019_faerie_protocol/phase_i03/python/fp_i03_time`
- `lab/10_infrastructure/EXP0019_faerie_protocol/phase_i03/tests`
- `lab/10_infrastructure/EXP0019_faerie_protocol/phase_i03/schemas`
- `mql5/Include/FaerieProtocol/EXP0019/Time`
- `mql5/Experts/FaerieProtocolTests/EXP0019_FP_I03_TimeCalendarSelfTest.mq5`
- `mql5/Experts/FaerieProtocol/EXP0019_FP_I03_TimeCalendarDiagnostic.mq5`

## Navigation

- [[00_FP_I03_DELIVERY_MOC|FP-I03 Delivery MOC]]
- [[../fp_i02/00_FP_I02_DELIVERY_MOC|FP-I02 Contract Kernel]]
- [[../../phases/FP_I04_MULTI-SYMBOL_M1_SYNCHRONIZATION_COVERAGE_AND_DATA_REVISION|Next phase: FP-I04]]
