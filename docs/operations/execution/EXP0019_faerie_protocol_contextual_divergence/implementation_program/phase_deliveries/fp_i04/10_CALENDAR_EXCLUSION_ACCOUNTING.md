---
title: "Calendar Exclusion Accounting"
tags: [exp0019, faerie-protocol, fp-i04, data-synchronization, obsidian]
status: normative
phase: FP-I04
phase_version: 1.0.0
doc_version: 1.0.0
last_updated: 2026-07-13
language: en
---
# Calendar Exclusion Accounting

## Purpose

Coverage reconciles the full requested duration into expected trading minutes plus calendar-excluded minutes.

## Normative invariants

1. **Expected plus excluded equals total duration.**
2. **Excluded minutes do not reduce coverage ratio.**
3. **Calendar exclusion is not a backfill request.**
4. **Changing calendar rules requires a new upstream version.**

## Contract flow

```text
raw two-symbol M1 deliveries
        │
        ├─ symbol resolution and closed-bar validation
        ├─ duplicate canonicalization
        ├─ FP-I03 expected-minute axis
        ├─ per-symbol cell and coverage classification
        ├─ aligned pair rows
        └─ revision / cursor / backfill evidence
        │
        ▼
versioned PairDatasetSnapshot for FP-I05
```

## Required evidence

| Evidence | Requirement |
|---|---|
| pair/config identity | exact pair hash, calendar config hash, synchronizer config hash |
| source identity | bar hash, source revision, transport sequence retained separately |
| temporal identity | UTC M1 open and FP-I03 calendar snapshot hash |
| coverage | present, expected, excluded, gap reason, conflict disposition |
| revision | parent, kind, affected range, previous/current payload hashes |
| processing | batch or incremental path, cursor ID, counters, fixture ID |
| health | READY, DEGRADED, or BLOCKED with closed reason codes |

## Failure behavior

- Unknown symbol alias is rejected before bar acceptance.
- Provisional, off-grid, non-finite, or invalid-OHLC bars are rejected.
- Identical duplicate deliveries deduplicate; conflicting duplicates block the minute.
- Missing history is represented as OUT_OF_COVERAGE; internal absence is MISSING.
- Calendar-excluded minutes are not missing and never trigger backfill.
- Stale cursor or checkpoint identity triggers deterministic rebuild.
- No synthetic bar, nearest-minute substitution, or silent forward fill is permitted.

## Test obligations

1. Repeat identical inputs and compare all semantic IDs.
2. Permute input order and prove output stability.
3. Change one semantic bar field and prove revision/identity changes.
4. Change transport-only metadata and prove bar semantics remain stable.
5. Inject before/inside/after coverage gaps and verify distinct states.
6. Inject identical and conflicting duplicates.
7. Compare batch output with non-overlapping incremental chunks.
8. Prove late inserts invalidate only affected minutes/windows.
9. Scan Python and MQL5 for drawing, order, position, broker-action, and network authority.

## Operational checklist

- [ ] Pair aliases, tick sizes, and digits are exact.
- [ ] FP-I03 calendar config hash matches the accepted handoff.
- [ ] Only closed M1 bars enter the canonical path.
- [ ] Conflicts are zero or the result remains BLOCKED.
- [ ] Coverage/exclusion counters reconcile to the requested range.
- [ ] Data revision and cursor evidence are persisted.
- [ ] Batch/incremental parity is green.
- [ ] Previous FP and Daye regressions remain green.

## Residual risk

The implementation proves deterministic data-plane semantics on controlled fixtures. It does not prove vendor completeness, exchange truth, holiday correctness beyond FP-I03, strategy profitability, or parity of an unimplemented external storage adapter. Those claims require separate evidence.

## Code surfaces

- `lab/10_infrastructure/EXP0019_faerie_protocol/phase_i04/python/fp_i04_data`
- `lab/10_infrastructure/EXP0019_faerie_protocol/phase_i04/tests`
- `lab/10_infrastructure/EXP0019_faerie_protocol/phase_i04/schemas`
- `mql5/Include/FaerieProtocol/EXP0019/Data`
- `mql5/Experts/FaerieProtocolTests/EXP0019_FP_I04_DataSyncSelfTest.mq5`
- `mql5/Experts/FaerieProtocol/EXP0019_FP_I04_DataSyncDiagnostic.mq5`

## Navigation

- [[00_FP_I04_DELIVERY_MOC|FP-I04 Delivery MOC]]
- [[../fp_i03/00_FP_I03_DELIVERY_MOC|FP-I03 Time/Calendar Kernel]]
- [[../../phases/FP_I05_SESSION_WEEK_WINDOW_STORE_CALENDAR-DAY_SELECTOR_AND_REFERENCE_ENGINE|Next phase: FP-I05]]
