---
id: CG-EXP0018-P01-TIME-KERNEL-MOC
title: EXP0018 Phase 01 Time Kernel MOC
type: moc
status: active
project: EXP0018
---

# EXP0018 Phase 01 — Time Kernel

## Core documents
- [[00_INDEX]]
- [[02_DOMAIN_TIME_MODEL]]
- [[04_NEW_YORK_DST_ALGORITHM]]
- [[05_TRADING_DAY_AND_GAP]]
- [[06_SESSION_AND_SUBCYCLE_WINDOWS]]
- [[07_PERIOD_WINDOW_IDENTITY]]
- [[08_TRANSITION_EVENT_MODEL]]
- [[12_TEST_FIXTURE_PLAN]]
- [[16_DEFINITION_OF_DONE]]

## Concepts
- [[UTC_Instant_Is_The_Unambiguous_Time_Identity]]
- [[New_York_Wall_Time_Defines_Daye_Boundaries]]
- [[DST_Fold_And_Gap_Are_Domain_States]]
- [[Half_Open_Intervals_Remove_Boundary_Ambiguity]]
- [[The_17_18_Gap_Is_Not_Missing_Data]]
- [[Manual_Broker_Offset_Is_Replay_Canonical]]
- [[Auto_Current_Broker_Offset_Is_Live_Only]]
- [[Period_Identity_Uses_Start_UTC]]
- [[P4_Remains_A_Thirty_Minute_Tail]]
- [[Time_Kernel_Has_No_Signal_Authority]]
- [[Transition_Event_Time_Differs_From_Availability_Time]]
- [[Weekly_Remains_Disabled_Until_ADR]]

## Maps
- [[EXP0018_P01_Time_Conversion_Map]]
- [[EXP0018_P01_DST_Resolution_Map]]
- [[EXP0018_P01_Trading_Day_Map]]
- [[EXP0018_P01_Transition_Event_Map]]
- [[EXP0018_P01_Handoff_Map]]

## Checklists
- [[EXP0018_P01_Compile_Checklist]]
- [[EXP0018_P01_Runtime_Checklist]]
- [[EXP0018_P01_DST_Checklist]]
- [[EXP0018_P01_Boundary_Checklist]]
- [[EXP0018_P01_Handoff_Checklist]]
