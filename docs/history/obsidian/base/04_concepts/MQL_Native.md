---
title: "MQL Native"
type: concept
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source: "auto-derived from project docs"
document_count: "276"
---


# MQL Native

## نقش در Alpha Lab

MQL Native لایه اجرای مستقیم MQL5 و migration از Python/report به expert/indicator قابل مشاهده روی چارت است.

## Keywords

- `mql native`
- `mql5`
- `expert advisor`
- `indicator`
- `mqh`
- `mq5`

## Related source documents

- [[README|Decision Alpha Lab]] — `readme`
- [[README_M0001_PYTHON_BRAIN_MQL_VISUAL|M0001 Python Brain / MQL Visual Architecture]] — `readme`
- [[docs/00_project_index|Decision Alpha Lab — Project Index]] — `core_docs`
- [[docs/EXP0015_cme_live_backtest_plan|EXP0015 CME/live/backtest implementation plan]] — `core_docs`
- [[docs/M0001_COMMON_FILES_SYNC_FIX|M0001 Common Files Sync Fix]] — `core_docs`
- [[docs/M0001_EVENT_BRIDGE_ARCHITECTURE|M0001 Event Bridge Architecture]] — `core_docs`
- [[docs/M0001_MQL_INPUT_PARAMETER_BRIDGE|M0001 Python Brain / MQL Input Bridge]] — `core_docs`
- [[docs/M0001_PARQUET_EVENT_BRIDGE|M0001 Parquet Event Bridge]] — `core_docs`
- [[docs/M0001_SINGLE_SOURCE_LIVE_ARCHITECTURE|M0001 Single-Source Live Architecture]] — `core_docs`
- [[docs/MQL_LIVE_ALL_IN_ONE_APPLY|MQL Live Visual Lab — All-in-One Apply]] — `core_docs`
- [[docs/MQL_NATIVE_MIGRATION_DECISION|MQL-Native Migration Decision]] — `core_docs`
- [[docs/PROJECT_LAYOUT|Decision Alpha Lab project layout]] — `core_docs`
- [[docs/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI Native Execution Roadmap — نقشه راه هوش مصنوعی، بک‌تست و پل اگزکیوت]] — `ai_execution_docs`
- [[docs/architecture|System Architecture]] — `core_docs`
- [[docs/debug/D0005_H5_NO_FUTURE_WALK_FORWARD_AUDIT|D0005 — H5 No-Future Walk-Forward Audit]] — `debug_docs`
- [[docs/debug/D0006_H5_LIVE_TOUCH_REPLAY_AUDIT|D0006 — H5 Live Touch Replay Audit]] — `debug_docs`
- [[docs/debug/E0006/MODULE_KERNEL_README|E0006 Modular Execution Kernel]] — `debug_docs`
- [[docs/debug/E0006/README|E0006 — Structural Execution Layer Overview]] — `debug_docs`
- [[docs/debug/E0006_ALL_ZONE_TOUCH_LIMIT_README|E0006 — All-Zone Touch Limit Fixed-R Executor]] — `debug_docs`
- [[docs/debug/H4_FAST_ATOMIC_MAIN_REPORT|H4 Fast Atomic Main Report]] — `debug_docs`
- [[docs/debug/H6_STANDALONE_OPTIONALITY_EDGE_MAP|H0006 standalone optionality and edge-map report]] — `debug_docs`
- [[docs/debug/MAIN_ATOMIC_NO_SAMPLE_UNIFICATION|Main Atomic No-Sample Unification for H4/H5]] — `debug_docs`
- [[docs/execution/E0002_CLOSE_CONFIRMED_MARKET|E0002 — H0005 Close-Confirmed Market Executor]] — `execution_docs`
- [[docs/execution/E0003_CONTINUATION_CLOSE_HUNT|E0003 — H0005 Continuation Close-Hunt Market Executor]] — `execution_docs`
- [[docs/execution/E0004_CONTINUATION_HEIKIN_ASHI_FLIP|E0004 — Continuation Heikin Ashi Flip Executor]] — `execution_docs`
- [[docs/execution/E0005_CONTINUATION_CLOSE_BREAK_FIXED_R|E0005 — Continuation Close-Break Fixed-R Executor]] — `execution_docs`
- [[docs/execution/EXP0015_intermarket_time_divergence/LEGACY_COMPILE_FIX|EXP0015 Legacy Compile Fix]] — `execution_docs`
- [[docs/execution/EXP0016_intermarket_divergence_execution/IMPLEMENTATION_PLAN_INDEX|EXP0016 Intermarket Divergence Execution — Implementation Plan Index]] — `execution_docs`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_01_STC_SMT_SKELETON|Level 01 — STC SMT Skeleton Patch]] — `execution_docs`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_05_STC_SMT_REFERENCE_HUNT_DETECTOR|Level 05 — STC SMT Reference Matrix and Raw Hunt Detector]] — `execution_docs`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_10_STC_SMT_PARTIAL_CLOSE_SIMULATOR|LEVEL 10 — STC SMT Partial Close Simulator]] — `execution_docs`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_11_STC_SMT_HARD_CLOSE_SIMULATOR|Level 11 STC SMT Hard Close Simulator]] — `execution_docs`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_13_STC_SMT_VISUALIZATION_AUDIT_DRAWING|LEVEL 13 — EXEC001 STC SMT Visualization / Audit Drawing]] — `execution_docs`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_18_STC_SMT_REAL_HARD_CLOSE_FINALIZER|LEVEL 18 — STC SMT Real Hard Close Finalizer]] — `execution_docs`
- [[docs/execution/H0005_R1_SIX_SLOT_TOUCH_LEDGER|H0005 Reversal Structural-Target-Capped Execution — Build 1.25]] — `execution_docs`
- [[docs/execution/README|Decision Alpha Lab — Execution]] — `execution_docs`
- [[docs/experience_capture/answers/BASE-03/answer_normalized_en|BASE-03 — Normalized Interpretation]] — `experience_capture_docs`
- [[docs/experience_capture/answers/BASE-03/answer_raw_en|BASE-03 — Raw Answer]] — `experience_capture_docs`
- [[docs/experience_capture/answers/BASE-04/answer_normalized_en|BASE-04 — Normalized Interpretation]] — `experience_capture_docs`
- [[docs/experience_capture/answers/BASE-04/answer_raw_en|BASE-04 — Raw Answer]] — `experience_capture_docs`
- [[docs/experience_capture/answers/BASE-04/notes_en|BASE-04 — Notes and Open Questions]] — `experience_capture_docs`
- [[docs/experience_capture/answers/BASE-04/question_en|BASE-04 — Which Concepts Must Never Enter the System?]] — `experience_capture_docs`
- [[docs/experience_capture/answers/BASE-05/answer_normalized_en|BASE-05 — Normalized Interpretation]] — `experience_capture_docs`
- [[docs/experience_capture/answers/BASE-06/answer_normalized_en|BASE-06 — Normalized Interpretation]] — `experience_capture_docs`
- [[docs/experience_capture/answers/DST-R03/answer_normalized_en|DST-R03 — Normalized Interpretation]] — `experience_capture_docs`
- [[docs/experience_capture/answers/EXT-10/answer_normalized_en|EXT-10 — Normalized Interpretation]] — `experience_capture_docs`
- [[docs/experience_capture/answers/NDS-R01/answer_normalized_en|NDS-R01 — Normalized Interpretation]] — `experience_capture_docs`
- [[docs/flag_counting/FLAG_COUNTING_CONSOLIDATION_PATCH_01_NO_SEND_CONTEXT|Flag Counting — Consolidation Patch 01 / No-Send Context]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_CONSOLIDATION_PATCH_02_FINAL_DECISION_STATE|Flag Counting — Consolidation Patch 02 / Final No-Send Decision State]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_CONSOLIDATION_PATCH_04_FINAL_CSV_NORMALIZATION|Flag Counting — Consolidation Patch 04 / Final CSV Field Normalization]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_CONSOLIDATION_PATCH_05_RUNTIME_HEALTH_SUMMARY|Flag Counting — Consolidation Patch 05 / Runtime Health Summary]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_CURRENT_CANON|Flag Counting Current Canon]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_IMPLEMENTATION_CHECKLIST_V2|Flag Counting Implementation Checklist V2]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19A_SILENT_DEFAULTS_AND_LIFECYCLE_CLEANUP|Flag Counting Level 19A — Silent Defaults and Lifecycle Cleanup]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19B_CLOSED_BAR_STATE_LEDGER|Flag Counting Level 19B — Closed-Bar State Ledger]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19C_STATE_DELTA_LEDGER|Flag Counting Level 19C — Closed-Bar State Delta Ledger]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19D_TRANSITION_EVENT_LEDGER|Flag Counting Level 19D — Closed-Bar Transition Event Ledger]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19Z_COMPLETE_OBSERVATION_SUITE|Flag Counting Level 19Z — Complete Observation Suite]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_CLEAN_ISOLATED_STATE_GATE|Flag Counting Level 19 — Clean Isolated State Gate]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE10_PANEL_LINE_CONTRACT|Flag Counting Level 19 — Phase 10 Panel Line Debug Contract]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE11_ENTRY_BRIDGE_READINESS|Flag Counting Level 19 — Phase 11 Entry Bridge Readiness]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE12_EXTREME_CANDIDATE_MAP|Flag Counting Level 19 — Phase 12 Extreme Candidate Map]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE13_MTF_ALIGNMENT_MAP|Flag Counting Level 19 — Phase 13 Multi-Timeframe Alignment Map]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE14_ENTRY_GEOMETRY_READINESS|Flag Counting Level 19 — Phase 14 Entry Geometry Readiness]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE15_ENTRY_IDEA_LAYER|Flag Counting Level 19 — Phase 15 Entry Idea Layer]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE16_ENTRY_DECISION_DRY_RUN|Flag Counting Level 19 — Phase 16 Entry Decision Layer / Dry Run]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE17_PAPER_EXECUTION_LEDGER|Flag Counting Level 19 — Phase 17 Paper Execution / Dry Run Ledger]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE18_PAPER_LEDGER_LIFECYCLE_TRACKING|Flag Counting Level 19 — Phase 18 Paper Ledger Lifecycle Tracking]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE19_PAPER_RESULT_METRICS|Flag Counting Level 19 — Phase 19 Paper Result Metrics / R-Equivalent Summary]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE20_PAPER_PORTFOLIO_AGGREGATE_METRICS|Flag Counting Level 19 — Phase 20 Paper Portfolio / Aggregate Metrics]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE21_PAPER_REGIME_ATTRIBUTION|Flag Counting Level 19 — Phase 21 Paper Regime Attribution]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE22_PAPER_FILTER_DIAGNOSTICS|Flag Counting Level 19 — Phase 22 Paper Filter Diagnostics]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE23_DRY_RUN_DECISION_POLICY|Flag Counting Level 19 — Phase 23 Dry-Run Decision Policy]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE24_PERSISTENT_PAPER_TRADE_LEDGER|Flag Counting Level 19 — Phase 24 Persistent Paper Trade Ledger]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE25_PERSISTENT_PAPER_TRADE_LIFECYCLE|Flag Counting Level 19 — Phase 25 Persistent Paper Trade Lifecycle Engine]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE26_PAPER_PERFORMANCE_REPORT|Flag Counting Level 19 — Phase 26 Paper Performance Report]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE27_PAPER_MFE_MAE_PATH_QUALITY|Flag Counting Level 19 — Phase 27 Paper MFE / MAE Path Quality]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE28_CONTEXT_PERFORMANCE_MATRIX|Flag Counting Level 19 — Phase 28 Context Performance Matrix]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE2_CLOSED_BAR_TRACKER|Flag Counting Level 19 — Phase 2 Closed-Bar Tracker]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE4_HOOK_VIEW_PROJECTION|Flag Counting Phoenix — Level 19 Phase 4 Hook View Projection]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE7_LEFT_PANEL_SECTION_TOGGLES|Flag Counting Level 19 — Phase 7 Left-Upper Panel and Section Toggles]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE9_VISUAL_DEBUG_CONTRACT|Flag Counting Level 19 — Phase 9 Visual Debug Contract]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_STATE_GATE_DASHBOARD_SPEC|Flag Counting Level 19 — Multi-Timeframe State Gate and Dashboard Specification]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_STATE_GATE_IMPLEMENTATION_PLAN|Flag Counting Level 19 — State Gate and Dashboard Implementation Plan]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_20_ENTRY_BRIDGE_XY_ANCHOR_JOIN|Flag Counting Level 20 — Entry Bridge / X-Y Anchor Join]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_21_PAPER_INTENT_NO_ORDER|Flag Counting Level 21 — Paper Intent / No Order]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_22_PAPER_LIFECYCLE_CLOSE_ONLY|Flag Counting Level 22 — Paper Lifecycle Close-Only]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_23_PAPER_PERFORMANCE_CLOSE_ONLY|Flag Counting Level 23 — Paper Performance Close-Only]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_24_SAFETY_GATE_PRE_BROKER|Flag Counting Level 24 — Safety Gate / Pre-Broker Guard]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_25_BROKER_DRY_RUN_ONLY|Flag Counting Level 25 — Broker Dry Run Only]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_26_BROKER_VALIDATOR_NO_SEND|Flag Counting Level 26 — Broker Request Validator / No Send]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_27_BROKER_REQUEST_LEDGER_NO_SEND|Flag Counting Level 27 — Broker Request Ledger / No Send]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_28_BROKER_REQUEST_AUDIT_NO_SEND|Flag Counting Level 28 — Broker Request Audit / No Send]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_29_PAPER_BROKER_ADAPTER_NO_SEND|Flag Counting Level 29 — Paper Broker Adapter / Still No Send]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_30_PAPER_BROKER_LIFECYCLE_NO_SEND|Flag Counting Level 30 — Paper Broker Lifecycle / Still No Send]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_STABILIZATION_PATCH_01_LEVEL_24_30|Flag Counting Stabilization Patch 01 — Level 24-30 No-Send Chain]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_STATE_MACHINE_V3|Flag Counting State Machine V3]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_V6_IMPLEMENTATION_NOTES|Flag Counting V6 Implementation Notes]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_VNEXT_IMPLEMENTATION|Flag Counting vNext Implementation Notes]] — `flag_counting_docs`
- [[docs/flag_counting/IMPLEMENTATION_LADDER_V1_INDEX|Flag Counting Implementation Ladder V1 Index]] — `flag_counting_docs`
- [[docs/flag_counting/README|Flag Counting Documentation]] — `flag_counting_docs`
- [[docs/flag_counting/VALIDATION_CASE_REGISTRY|Flag Counting Validation Case Registry]] — `flag_counting_docs`
- [[docs/flag_counting/implementation_ladder_v1/00_GOVERNANCE_AND_FREEZE_PROTOCOL|Phoenix Flag Counting Implementation Ladder V1]] — `flag_counting_docs`
- [[docs/flag_counting/implementation_ladder_v1/01_LEVEL_01_CANDLE_STREAM_AND_TIMEBASE|Phoenix Flag Counting Implementation Ladder V1]] — `flag_counting_docs`
- [[docs/flag_counting/implementation_ladder_v1/02_LEVEL_02_NODE_ENGINE|Phoenix Flag Counting Implementation Ladder V1]] — `flag_counting_docs`
- [[docs/flag_counting/implementation_ladder_v1/03_LEVEL_03_NODE_IDENTITY_AND_SCALE|Phoenix Flag Counting Implementation Ladder V1]] — `flag_counting_docs`
- [[docs/flag_counting/implementation_ladder_v1/04_LEVEL_04_HOOK_ND_CONTEXT_ENGINE|Phoenix Flag Counting Implementation Ladder V1]] — `flag_counting_docs`
- [[docs/flag_counting/implementation_ladder_v1/05_LEVEL_05_FLAG_BODY_ENGINE|Phoenix Flag Counting Implementation Ladder V1]] — `flag_counting_docs`
- [[docs/flag_counting/implementation_ladder_v1/06_LEVEL_06_INTERNAL_COUNT_ENGINE|Phoenix Flag Counting Implementation Ladder V1]] — `flag_counting_docs`
- [[docs/flag_counting/implementation_ladder_v1/07_LEVEL_07_F1_LIFECYCLE_ENGINE|Phoenix Flag Counting Implementation Ladder V1]] — `flag_counting_docs`
- [[docs/flag_counting/implementation_ladder_v1/08_LEVEL_08_F2_LIFECYCLE_ENGINE|Phoenix Flag Counting Implementation Ladder V1]] — `flag_counting_docs`
- [[docs/flag_counting/implementation_ladder_v1/09_LEVEL_09_F3_EXTENSION_AND_LOCK_ENGINE|Level 09 — F3 Lifecycle / Terminal Extension / Lock Engine]] — `flag_counting_docs`
- [[docs/flag_counting/implementation_ladder_v1/10_LEVEL_10_SEQUENCE_OWNERSHIP_AND_PHASES|Phoenix Flag Counting Implementation Ladder V1]] — `flag_counting_docs`
- [[docs/flag_counting/implementation_ladder_v1/11_5_LEVEL_11_5_RAW_AUDIT_EXPORT|Level 11.5 — Raw Audit Export / Report Engine]] — `flag_counting_docs`
- [[docs/flag_counting/implementation_ladder_v1/11_LEVEL_11_CANONICALIZATION_AND_AUDIT|Phoenix Flag Counting Implementation Ladder V1]] — `flag_counting_docs`
- [[docs/flag_counting/implementation_ladder_v1/12_LEVEL_12_RENDERER_AND_LABEL_LAYOUT|Level 12 — Renderer / Labels / Visual Layer]] — `flag_counting_docs`
- [[docs/flag_counting/implementation_ladder_v1/13_LEVEL_13_VALIDATION_MATRIX|Phoenix Flag Counting Implementation Ladder V1]] — `flag_counting_docs`
- [[docs/flag_counting/implementation_ladder_v1/14_LEVEL_14_RELEASE_ROLLBACK_AND_DEBUG_PROTOCOL|Phoenix Flag Counting Implementation Ladder V1]] — `flag_counting_docs`
- [[docs/flag_counting/implementation_ladder_v1/15_MODULE_INTERFACE_CONTRACTS|Phoenix Flag Counting Implementation Ladder V1]] — `flag_counting_docs`
- [[docs/flag_counting/implementation_ladder_v1/16_IMPLEMENTATION_ORDER_AND_ACCEPTANCE_MATRIX|Phoenix Flag Counting Implementation Ladder V1]] — `flag_counting_docs`

## Agent use

- هنگام طراحی Agent، این concept باید به عنوان context قابل بازیابی استفاده شود.
- هر patch یا experiment مرتبط باید به این concept link شود.
