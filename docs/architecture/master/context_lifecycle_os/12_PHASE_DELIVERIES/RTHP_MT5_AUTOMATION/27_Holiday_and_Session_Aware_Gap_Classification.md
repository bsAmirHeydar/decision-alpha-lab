---
note_id: RTHP_MT5_AUTOMATION_27_HOLIDAY_SESSION_AWARE_GAPS
note_type: implementation_delivery
status: IMPLEMENTED_AND_TESTED
owner: RTHP_MT5_ACTIVATION
---

# Holiday and Session-Aware Joint-Gap Classification

## Purpose

The MT5 quality gate must distinguish a genuine data outage from a paired market closure. It must never solve a missing-data problem by increasing a threshold, forward-filling bars, or synthesizing ticks.

## Implemented profiles

- `WEEKLY_ONLY_V1` is the conservative fallback. Long weekday joint gaps remain blockers.
- `US_INDEX_CFD_NY_V1` recognizes declared United States market holidays in `America/New_York` time.
- `AUTO` resolves to `US_INDEX_CFD_NY_V1` only when both broker symbols independently match the US index CFD metadata predicate. Otherwise it resolves to `WEEKLY_ONLY_V1`.

## Classification contract

A long joint gap is classified as `SCHEDULED_MARKET_CLOSURE` only when all conditions hold:

1. Both symbols are missing over the same minute interval.
2. The resolved calendar profile permits holiday classification.
3. The interval overlaps a declared holiday date.
4. The interval does not exceed `max_scheduled_closure_minutes`.
5. Closed M1 bars exist immediately before and after the interval for both symbols when boundary evidence is required.

A declared closure remains absent from the source. It is not forward-filled. M15 windows lacking exact M1 coverage remain unconfirmed.

## Quality evidence

`RTHP_MT5_M1_QUALITY_V2` records:

- resolved calendar profile and resolution reason;
- holiday rule version;
- scheduled closure IDs and exact UTC boundaries;
- boundary-bar evidence status;
- declared short joint gaps;
- unexplained long joint gaps;
- calendar evidence digest;
- explicit `forward_fill_allowed=false`.

## Memorial Day regression

The observed paired gap on 2026-05-25 from 19:55 UTC to 2026-05-26 01:00 UTC is classified as `US_MEMORIAL_DAY` under `US_INDEX_CFD_NY_V1`. Its 305 missing minutes remain missing, but they no longer constitute unexplained data loss.

## Fail-closed behavior

Unknown instruments, missing boundary evidence, excessive closure duration, semantic symbol ambiguity, and non-holiday long joint gaps remain blockers under `UNEXPLAINED_JOINT_GAP_EXCEEDS_POLICY`.

## Related notes

- [[docs/architecture/master/context_lifecycle_os/12_PHASE_DELIVERIES/RTHP_MT5_AUTOMATION/11_Session_Aware_Gap_Duplicate_and_Cross_Symbol_Quality_Gates]]
- [[docs/architecture/master/context_lifecycle_os/12_PHASE_DELIVERIES/RTHP_MT5_AUTOMATION/17_Test_Strategy_Acceptance_Matrix_and_Definition_of_Done]]
- [[docs/architecture/master/context_lifecycle_os/12_PHASE_DELIVERIES/RTHP_MT5_AUTOMATION/29_Real_MT5_Smoke_Train_Evidence]]
