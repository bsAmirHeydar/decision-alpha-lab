---
title: "Intermarket Divergence"
type: concept
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source: "auto-derived from project docs"
document_count: "90"
---


# Intermarket Divergence

## نقش در Alpha Lab

Intermarket Divergence خانواده فرضیه/اجرا برای واگرایی چند نماد، time divergence، SMT و deployment است.

## Keywords

- `intermarket`
- `divergence`
- `smt`
- `cme`

## Related source documents

- [[README_M0001_PYTHON_BRAIN_MQL_VISUAL|M0001 Python Brain / MQL Visual Architecture]] — `readme`
- [[docs/EXP0015_cme_live_backtest_plan|EXP0015 CME/live/backtest implementation plan]] — `core_docs`
- [[docs/EXP0015_cme_live_provider_patch|EXP0015 CME Live Provider Patch]] — `core_docs`
- [[docs/M0001_SINGLE_SOURCE_LIVE_ARCHITECTURE|M0001 Single-Source Live Architecture]] — `core_docs`
- [[docs/execution/EXP0015_intermarket_time_divergence/LEGACY_COMPILE_FIX|EXP0015 Legacy Compile Fix]] — `execution_docs`
- [[docs/execution/EXP0016_intermarket_divergence_execution/IMPLEMENTATION_PLAN_INDEX|EXP0016 Intermarket Divergence Execution — Implementation Plan Index]] — `execution_docs`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_01_STC_SMT_SKELETON|Level 01 — STC SMT Skeleton Patch]] — `execution_docs`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_02_STC_SMT_TIME_ENGINE|Level 02 — STC Time Engine and Cycle Classifier]] — `execution_docs`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_03_STC_SMT_CHECK_CANDLE_AGGREGATOR|LEVEL 03 — STC SMT Check Candle Aggregator]] — `execution_docs`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_04_STC_SMT_W_LEVEL_BUILDER|Level 04 — W Level Builder]] — `execution_docs`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_05_STC_SMT_REFERENCE_HUNT_DETECTOR|Level 05 — STC SMT Reference Matrix and Raw Hunt Detector]] — `execution_docs`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_06_STC_SMT_CANDIDATE_ENGINE|Level 06 STC SMT Candidate Engine]] — `execution_docs`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_07_STC_SMT_CONFIRMATION_SIGNAL_REGISTRY|LEVEL 07 STC SMT Confirmation and Signal Registry]] — `execution_docs`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_08_STC_SMT_RISK_PLAN_PAPER_ENTRY|Level 08 STC SMT Risk Plan and Paper Entry]] — `execution_docs`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_09_STC_SMT_PAPER_OUTCOME_SIMULATOR|LEVEL 09 — STC SMT Paper Outcome Simulator]] — `execution_docs`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_10_STC_SMT_PARTIAL_CLOSE_SIMULATOR|LEVEL 10 — STC SMT Partial Close Simulator]] — `execution_docs`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_11_STC_SMT_HARD_CLOSE_SIMULATOR|Level 11 STC SMT Hard Close Simulator]] — `execution_docs`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_12_STC_SMT_PERSISTENCE_RESTART_RECOVERY|Level 12 — STC SMT Persistence and Restart Recovery]] — `execution_docs`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_13_STC_SMT_VISUALIZATION_AUDIT_DRAWING|LEVEL 13 — EXEC001 STC SMT Visualization / Audit Drawing]] — `execution_docs`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_14_STC_SMT_PAPER_LIVE_ALERTS|Level 14 — STC SMT Paper Live Alerts]] — `execution_docs`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_15_STC_SMT_BROKER_POSITION_MANAGER|Level 15 — STC SMT Broker Position Manager]] — `execution_docs`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_16_STC_SMT_REAL_AUTO_ENTRY_ROUTER|Level 16 — STC SMT Real Auto Entry Router]] — `execution_docs`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_17_STC_SMT_REAL_PARTIAL_CLOSE_MANAGER|LEVEL 17 — STC SMT Real Partial Close Manager]] — `execution_docs`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_18_STC_SMT_REAL_HARD_CLOSE_FINALIZER|LEVEL 18 — STC SMT Real Hard Close Finalizer]] — `execution_docs`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_19_STC_SMT_VALIDATION_PACK|Level 19 — STC SMT Validation Pack]] — `execution_docs`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_20_STC_SMT_OPERATOR_MANUAL|LEVEL 20 — STC SMT Operator Manual and Deployment Profiles]] — `execution_docs`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_21_STC_SMT_DRAWING_AUDIT|LEVEL 21 — STC SMT Drawing Audit Hardening]] — `execution_docs`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_22_STC_SMT_HIDDEN_LICENSE_FIX|Level 22 — STC SMT Hidden Offline License Fix]] — `execution_docs`
- [[docs/execution/EXP0016_intermarket_divergence_execution/README|EXP0016 Intermarket Divergence Execution Documentation]] — `execution_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE13_MTF_ALIGNMENT_MAP|Flag Counting Level 19 — Phase 13 Multi-Timeframe Alignment Map]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE20_PAPER_PORTFOLIO_AGGREGATE_METRICS|Flag Counting Level 19 — Phase 20 Paper Portfolio / Aggregate Metrics]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE21_PAPER_REGIME_ATTRIBUTION|Flag Counting Level 19 — Phase 21 Paper Regime Attribution]] — `flag_counting_docs`
- [[lab/03_experiments/EXP0015_intermarket_time_divergence/README|EXP0015 Intermarket Candle + Session Divergence]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/00_strategy_document_map|00 - Strategy Document Map]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/01_source_srs_extraction|01 - Source SRS Extraction]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/02_normalized_strategy_spec|02 - Normalized Strategy Specification]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/03_cycle_calendar|03 - Cycle Calendar and Time Model]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/04_smt_divergence_rules|04 - SMT Divergence Rules and Algorithms]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/05_execution_and_risk|05 - Execution, Risk, Position Management, and Outcomes]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/06_mql5_architecture_plan|06 - MQL5 Architecture Plan]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/07_test_plan|07 - Test Plan]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/08_open_questions|08 - Open Questions]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/09_owner_decisions_pass_1|09 - Owner Decisions Pass 1]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/10_owner_decisions_pass_2|10 - Owner Decisions Pass 2]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/11_algorithm_layers|11 - Algorithm Layers]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/12_state_machines|12 - State Machines]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/13_data_model_and_journals|13 - Data Model and Journals]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/14_backtest_live_runtime|14 - Backtest and Live Runtime]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/15_visualization_contract|15 - Visualization Contract]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/16_implementation_checklist|16 - Implementation Checklist]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/17_implementation_plan|EXEC001 STC SMT Cycles — Implementation Plan]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/18_module_breakdown|EXEC001 STC SMT Cycles — Module Breakdown]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/19_patch_build_sequence|EXEC001 STC SMT Cycles — Patch Build Sequence]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/20_implementation_risk_register|EXEC001 STC SMT Cycles — Implementation Risk Register]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/21_first_patch_scope|EXEC001 STC SMT Cycles — First Implementation Patch Scope]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/22_level_01_skeleton|EXEC001 STC SMT Cycles — Level 01 Skeleton Implementation]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/23_level_02_time_engine|Level 02 — STC Time Engine and Cycle Classifier]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/24_level_03_check_candle_aggregator|Level 03 — Check Candle Aggregator and Pair Data Completeness]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/25_level_04_w_level_builder|Level 04 — W Level Builder]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/26_level_05_reference_matrix_hunt_detector|Level 05 — Reference Matrix and Raw Hunt Detector]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/27_level_06_smt_candidate_engine|Level 06 — SMT Candidate Engine]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/28_level_07_confirmation_signal_registry|Level 07 — Confirmation and Signal Registry]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/29_level_08_risk_plan_paper_entry|Level 08 — Risk Plan and No-Order Paper Entry Model]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/30_level_09_paper_outcome_simulator|Level 09 — Paper Outcome Simulator and Trade Journal]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/31_level_10_partial_close_simulator|Level 10 — Paper Partial Close Simulator and W4 Management]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/32_level_11_hard_close_simulator|Level 11 — Paper Hard-Close Simulator and 15:30 End-of-Day Accounting]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/33_level_12_persistence_restart_recovery|Level 12 — Persistence and Restart Recovery]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/34_level_13_visualization_audit_drawing|Level 13 — Visualization / Audit Drawing]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/35_level_14_paper_live_alerts|Level 14 — Paper Live Alerts / No-Order Monitoring Layer]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/36_level_15_broker_position_manager|Level 15 — Broker Position Manager / Magic-Only Safety Layer]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/37_level_16_real_auto_entry_router|Level 16 — Real Auto Entry Router]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/38_level_17_real_partial_close_manager|Level 17 — Real Partial Close Manager]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/39_level_18_real_hard_close_finalizer|Level 18 — Real Hard Close Finalizer]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/40_level_19_validation_pack|Level 19 — Validation Pack / Self-Test Reports]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/41_level_20_operator_manual_deployment_profiles|Level 20 — Operator Manual and Deployment Profiles]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/42_level_20_profile_matrix|Level 20 — Deployment Profile Matrix]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/43_level_21_drawing_audit|Level 21 — Drawing Audit Hardening + HardClose Warning Fix]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/README|EXEC001 STC SMT Cycles]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/deployment_profiles/README|EXEC001 STC SMT Cycles — Deployment Profiles]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/deployment_profiles/profile_01_research_backtest_full_audit|Profile 01 — Research Backtest Full Audit]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/deployment_profiles/profile_02_paper_live_observer|Profile 02 — Paper Live Observer]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/deployment_profiles/profile_03_paper_live_broker_audit|Profile 03 — Paper Live Broker Audit]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/deployment_profiles/profile_04_auto_trade_entry_only_rehearsal|Profile 04 — Auto Trade Entry Only Rehearsal]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/deployment_profiles/profile_05_auto_trade_full_managed|Profile 05 — Auto Trade Full Managed]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/deployment_profiles/profile_06_emergency_hard_close_only|Profile 06 — Emergency Hard Close Only]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/README|EXP0016 Intermarket Divergence Execution]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/offline_license/README|Offline License Layer - EXEC001 STC SMT Cycles]] — `experiment`
- [[mql5/Experts/IntermarketDivergence/README|Intermarket Divergence Experts]] — `mql5_docs`
- [[mql5/Experts/IntermarketDivergenceExecution/README|Intermarket Divergence Execution Experts]] — `mql5_docs`
- [[tools/cme_bridge/README|DAL CME Bridge for EXP0015]] — `tool_docs`

## Agent use

- هنگام طراحی Agent، این concept باید به عنوان context قابل بازیابی استفاده شود.
- هر patch یا experiment مرتبط باید به این concept link شود.
