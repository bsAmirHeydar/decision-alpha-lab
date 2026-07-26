---
title: "NDS Anatomy"
type: concept
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source: "auto-derived from project docs"
document_count: "640"
---


# NDS Anatomy

## نقش در Alpha Lab

NDS Anatomy زبان مشترک Node، CycleHook، Sequence، X/Y axis، return-to-origin و parent-child fractal relation است.

## Keywords

- `nds`
- `node`
- `cyclehook`
- `sequence`
- `x-axis`
- `y-axis`
- `origin penetration`

## Related source documents

- [[README|Decision Alpha Lab]] — `readme`
- [[README_M0001_PYTHON_BRAIN_MQL_VISUAL|M0001 Python Brain / MQL Visual Architecture]] — `readme`
- [[docs/EXP0015_cme_live_provider_patch|EXP0015 CME Live Provider Patch]] — `core_docs`
- [[docs/M0001_EVENT_BRIDGE_ARCHITECTURE|M0001 Event Bridge Architecture]] — `core_docs`
- [[docs/M0001_LIVE_PAST_ONLY_BRIDGE_FIX|M0001 Live Past-Only Event Bridge Fix]] — `core_docs`
- [[docs/M0001_MQL_INPUT_PARAMETER_BRIDGE|M0001 Python Brain / MQL Input Bridge]] — `core_docs`
- [[docs/M0001_NODE_ARROW_TIP_ANCHOR_FIX|M0001 Node Arrow Tip Anchor Fix]] — `core_docs`
- [[docs/M0001_NODE_MARKER_PRECISION_AND_PERFORMANCE_FIX|M0001 Node Marker Precision and Bridge Performance Fix]] — `core_docs`
- [[docs/M0001_NODE_REVEAL_TIMING_FIX|M0001 Node Reveal Timing Fix]] — `core_docs`
- [[docs/M0001_PARQUET_TYPE_SAFETY_FIX|M0001 Parquet Type Safety Fix]] — `core_docs`
- [[docs/M0001_REVERT_NODE_TIMING_FAST_SYNC|M0001 Revert Node Timing Mode and Fast Sync]] — `core_docs`
- [[docs/M0001_SINGLE_SOURCE_LIVE_ARCHITECTURE|M0001 Single-Source Live Architecture]] — `core_docs`
- [[docs/MQL_LIVE_ALL_IN_ONE_APPLY|MQL Live Visual Lab — All-in-One Apply]] — `core_docs`
- [[docs/MQL_NATIVE_MIGRATION_DECISION|MQL-Native Migration Decision]] — `core_docs`
- [[docs/operations/ai_execution/AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA|AI Algorithm Layer Map for Extreme Engine — نقشه الگوریتم‌های هوش مصنوعی برای اکستریم L2]] — `ai_execution_docs`
- [[docs/operations/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI Native Execution Roadmap — نقشه راه هوش مصنوعی، بک‌تست و پل اگزکیوت]] — `ai_execution_docs`
- [[docs/operations/ai_execution/AMIR_STRUCTURAL_EXPERIENCE_MAP_FA|Amir Structural Experience Map — نقشه تجربه‌های ساختاری امیر]] — `ai_execution_docs`
- [[docs/operations/ai_execution/EXPERIENCE_CAPTURE_LOG_TEMPLATE_FA|Experience Capture Log Template — قالب ثبت تجربه‌های امیر]] — `ai_execution_docs`
- [[docs/operations/ai_execution/EXTREME_L2_NODE_CYCLE_LIMIT_ENTRY_FA|Extreme L2 Node Cycle Limit Entry — تعریف رسمی اکستریم، نود L2 و ورود لیمیت]] — `ai_execution_docs`
- [[docs/operations/ai_execution/README|AI Execution Docs]] — `ai_execution_docs`
- [[docs/architecture|System Architecture]] — `core_docs`
- [[docs/standards/articles/distribution_engineering_for_conditional_sequence_extraction|H0008 — Distribution Engineering Instead of Raw Edge Hunting]] — `article_docs`
- [[docs/standards/articles/structural_regime_memory_without_samples|Article — Structural Regime Memory Without Samples]] — `article_docs`
- [[docs/atomic_live_research_contract|Atomic Live Research Contract]] — `core_docs`
- [[docs/history/debug/D0005_H5_NO_FUTURE_WALK_FORWARD_AUDIT|D0005 — H5 No-Future Walk-Forward Audit]] — `debug_docs`
- [[docs/history/debug/D0006_H5_LIVE_TOUCH_REPLAY_AUDIT|D0006 — H5 Live Touch Replay Audit]] — `debug_docs`
- [[docs/history/debug/D0007_H5_CAUSAL_LIVE_REPLAY_AUDIT|D0007 — H5 Causal Live Replay Audit]] — `debug_docs`
- [[docs/history/debug/D0008_H4_CAUSAL_BATCH_REPORT|D0008 / H0004 Causal Known-Candle Batch Report]] — `debug_docs`
- [[docs/history/debug/D0009_H5_ATOMIC_NO_SAMPLE_REPLAY_AUDIT|D0009 H5 Atomic No-Sample Replay Audit]] — `debug_docs`
- [[docs/history/debug/D0010_H4_ATOMIC_NO_SAMPLE_REGIME_AUDIT|D0010 — H4 Atomic No-Sample Regime Audit]] — `debug_docs`
- [[docs/history/debug/E0006/ENTRY_QUALIFICATION_README|E0006 — Entry Qualification Logic]] — `debug_docs`
- [[docs/history/debug/E0006/EXIT_AND_RISK_README|E0006 — Exit, Stop, Spread, and Risk Logic]] — `debug_docs`
- [[docs/history/debug/E0006/INPUT_REFERENCE_README|E0006 — Input Reference]] — `debug_docs`
- [[docs/history/debug/E0006/MODULE_KERNEL_README|E0006 Modular Execution Kernel]] — `debug_docs`
- [[docs/history/debug/E0006/README|E0006 — Structural Execution Layer Overview]] — `debug_docs`
- [[docs/history/debug/E0006/REVISIT_ONLY_README|E0006 — Revisit-Only Entry Logic]] — `debug_docs`
- [[docs/history/debug/E0006/REVISIT_SECONDARY_NODE_ANCHORS_README|E0006 — Revisit Secondary-Node Entry and Stop Anchors]] — `debug_docs`
- [[docs/history/debug/E0006_ALL_ZONE_TOUCH_LIMIT_README|E0006 — All-Zone Touch Limit Fixed-R Executor]] — `debug_docs`
- [[docs/history/debug/E0007/README|E0007 — Purple Source Extreme Executor Template]] — `debug_docs`
- [[docs/history/debug/E0008/README|E0008 — MTF Purple Extreme Executor]] — `debug_docs`
- [[docs/history/debug/E0009/README|E0009 — Reversal Macro / Latest Setup / Hook Executor]] — `debug_docs`
- [[docs/history/debug/H4_DEEP_H6_OPTIONALITY_REPORT|H4 Deep Atomic Report + H6 Reversal Optionality]] — `debug_docs`
- [[docs/history/debug/H4_FAST_ATOMIC_MAIN_REPORT|H4 Fast Atomic Main Report]] — `debug_docs`
- [[docs/history/debug/H6_BOX_ALGORITHM_README|H6 Fast Box Visualizer — Official Algorithm]] — `debug_docs`
- [[docs/history/debug/H6_FAST_ACCURATE_OPTIONALITY|H6 Fast Accurate Optionality Report]] — `debug_docs`
- [[docs/history/debug/H6_NODE_SURVIVAL_MAP|H6 Node Survival Map]] — `debug_docs`
- [[docs/history/debug/H6_REACTION_BOX_ZONES|H6 Reaction Box Zones]] — `debug_docs`
- [[docs/history/debug/MAIN_ATOMIC_NO_SAMPLE_UNIFICATION|Main Atomic No-Sample Unification for H4/H5]] — `debug_docs`
- [[docs/history/debug/MARKET_LANGUAGE/README|DAL Market Language — Nodes, Cycles, Hooks, Rallies, Flags, 123 Flags, and Open 1/2s]] — `debug_docs`
- [[docs/operations/execution/E0002_CLOSE_CONFIRMED_MARKET|E0002 — H0005 Close-Confirmed Market Executor]] — `execution_docs`
- [[docs/operations/execution/E0003_CONTINUATION_CLOSE_HUNT|E0003 — H0005 Continuation Close-Hunt Market Executor]] — `execution_docs`
- [[docs/operations/execution/E0004_CONTINUATION_HEIKIN_ASHI_FLIP|E0004 — Continuation Heikin Ashi Flip Executor]] — `execution_docs`
- [[docs/operations/execution/E0005_CONTINUATION_CLOSE_BREAK_FIXED_R|E0005 — Continuation Close-Break Fixed-R Executor]] — `execution_docs`
- [[docs/operations/execution/EXP0015_intermarket_time_divergence/LEGACY_COMPILE_FIX|EXP0015 Legacy Compile Fix]] — `execution_docs`
- [[docs/operations/execution/EXP0016_intermarket_divergence_execution/IMPLEMENTATION_PLAN_INDEX|EXP0016 Intermarket Divergence Execution — Implementation Plan Index]] — `execution_docs`
- [[docs/operations/execution/EXP0016_intermarket_divergence_execution/LEVEL_02_STC_SMT_TIME_ENGINE|Level 02 — STC Time Engine and Cycle Classifier]] — `execution_docs`
- [[docs/operations/execution/EXP0016_intermarket_divergence_execution/LEVEL_10_STC_SMT_PARTIAL_CLOSE_SIMULATOR|LEVEL 10 — STC SMT Partial Close Simulator]] — `execution_docs`
- [[docs/operations/execution/EXP0016_intermarket_divergence_execution/LEVEL_11_STC_SMT_HARD_CLOSE_SIMULATOR|Level 11 STC SMT Hard Close Simulator]] — `execution_docs`
- [[docs/operations/execution/EXP0016_intermarket_divergence_execution/LEVEL_13_STC_SMT_VISUALIZATION_AUDIT_DRAWING|LEVEL 13 — EXEC001 STC SMT Visualization / Audit Drawing]] — `execution_docs`
- [[docs/operations/execution/EXP0016_intermarket_divergence_execution/LEVEL_17_STC_SMT_REAL_PARTIAL_CLOSE_MANAGER|LEVEL 17 — STC SMT Real Partial Close Manager]] — `execution_docs`
- [[docs/operations/execution/EXP0016_intermarket_divergence_execution/README|EXP0016 Intermarket Divergence Execution Documentation]] — `execution_docs`
- [[docs/operations/execution/H0005_R1_SIX_SLOT_TOUCH_LEDGER|H0005 Reversal Structural-Target-Capped Execution — Build 1.25]] — `execution_docs`
- [[docs/operations/execution/README|Decision Alpha Lab — Execution]] — `execution_docs`
- [[docs/contexts/legacy/experience_capture/EXPERIENCE_CAPTURE_INDEX_EN|Experience Capture Index]] — `experience_capture_docs`
- [[docs/contexts/legacy/experience_capture/answers/BASE-01/answer_normalized_en|BASE-01 — Normalized Interpretation]] — `experience_capture_docs`
- [[docs/contexts/legacy/experience_capture/answers/BASE-02/answer_normalized_en|BASE-02 — Normalized Interpretation]] — `experience_capture_docs`
- [[docs/contexts/legacy/experience_capture/answers/BASE-02/notes_en|BASE-02 — Notes and Open Questions]] — `experience_capture_docs`
- [[docs/contexts/legacy/experience_capture/answers/BASE-03/answer_normalized_en|BASE-03 — Normalized Interpretation]] — `experience_capture_docs`
- [[docs/contexts/legacy/experience_capture/answers/BASE-03/answer_raw_en|BASE-03 — Raw Answer]] — `experience_capture_docs`
- [[docs/contexts/legacy/experience_capture/answers/BASE-03/notes_en|BASE-03 — Notes and Open Questions]] — `experience_capture_docs`
- [[docs/contexts/legacy/experience_capture/answers/BASE-04/answer_normalized_en|BASE-04 — Normalized Interpretation]] — `experience_capture_docs`
- [[docs/contexts/legacy/experience_capture/answers/BASE-04/answer_raw_en|BASE-04 — Raw Answer]] — `experience_capture_docs`
- [[docs/contexts/legacy/experience_capture/answers/BASE-04/notes_en|BASE-04 — Notes and Open Questions]] — `experience_capture_docs`
- [[docs/contexts/legacy/experience_capture/answers/BASE-05/answer_normalized_en|BASE-05 — Normalized Interpretation]] — `experience_capture_docs`
- [[docs/contexts/legacy/experience_capture/answers/BASE-05/notes_en|BASE-05 — Notes and Open Questions]] — `experience_capture_docs`
- [[docs/contexts/legacy/experience_capture/answers/BASE-06/answer_normalized_en|BASE-06 — Normalized Interpretation]] — `experience_capture_docs`
- [[docs/contexts/legacy/experience_capture/answers/BASE-06/notes_en|BASE-06 — Notes and Open Questions]] — `experience_capture_docs`
- [[docs/contexts/legacy/experience_capture/answers/DATA-R03/answer_normalized_en|DATA-R03 — Normalized Interpretation]] — `experience_capture_docs`
- [[docs/contexts/legacy/experience_capture/answers/DATA-R03/answer_raw_en|DATA-R03 — Raw Answer]] — `experience_capture_docs`
- [[docs/contexts/legacy/experience_capture/answers/DATA-R03/notes_en|DATA-R03 — Notes and Open Questions]] — `experience_capture_docs`
- [[docs/contexts/legacy/experience_capture/answers/DATA-R03/question_en|DATA-R03 — Layered Training, Knowledge Consolidation, and Training Granularity]] — `experience_capture_docs`
- [[docs/contexts/legacy/experience_capture/answers/DST-R01/answer_normalized_en|DST-R01 — Normalized Interpretation]] — `experience_capture_docs`
- [[docs/contexts/legacy/experience_capture/answers/DST-R01/notes_en|DST-R01 — Notes and Open Questions]] — `experience_capture_docs`
- [[docs/contexts/legacy/experience_capture/answers/DST-R01/question_en|DST-R01 — Destination Taxonomy and Open One-Two]] — `experience_capture_docs`
- [[docs/contexts/legacy/experience_capture/answers/DST-R02/answer_normalized_en|DST-R02 — Normalized Interpretation]] — `experience_capture_docs`
- [[docs/contexts/legacy/experience_capture/answers/DST-R02/notes_en|DST-R02 — Notes and Open Questions]] — `experience_capture_docs`
- [[docs/contexts/legacy/experience_capture/answers/DST-R02/question_en|DST-R02 — Take Profit, Partial Exit, and Multi-Destination Policy]] — `experience_capture_docs`
- [[docs/contexts/legacy/experience_capture/answers/DST-R03/answer_normalized_en|DST-R03 — Normalized Interpretation]] — `experience_capture_docs`
- [[docs/contexts/legacy/experience_capture/answers/DST-R03/answer_raw_en|DST-R03 — Raw Answer]] — `experience_capture_docs`
- [[docs/contexts/legacy/experience_capture/answers/DST-R03/notes_en|DST-R03 — Notes and Open Questions]] — `experience_capture_docs`
- [[docs/contexts/legacy/experience_capture/answers/DST-R03/question_en|DST-R03 — Destination Repricing and Completion]] — `experience_capture_docs`
- [[docs/contexts/legacy/experience_capture/answers/ENT-R01/answer_normalized_en|ENT-R01 — Normalized Interpretation]] — `experience_capture_docs`
- [[docs/contexts/legacy/experience_capture/answers/ENT-R01/notes_en|ENT-R01 — Notes and Open Questions]] — `experience_capture_docs`
- [[docs/contexts/legacy/experience_capture/answers/ENT-R01/question_en|ENT-R01 — Entry-Level Extreme Definition]] — `experience_capture_docs`
- [[docs/contexts/legacy/experience_capture/answers/ENT-R02/answer_normalized_en|ENT-R02 — Normalized Interpretation]] — `experience_capture_docs`
- [[docs/contexts/legacy/experience_capture/answers/ENT-R02/answer_raw_en|ENT-R02 — Raw Answer]] — `experience_capture_docs`
- [[docs/contexts/legacy/experience_capture/answers/ENT-R02/notes_en|ENT-R02 — Notes and Open Questions]] — `experience_capture_docs`
- [[docs/contexts/legacy/experience_capture/answers/ENT-R02/question_en|ENT-R02 — Limit Entry, Stop Geometry, and Practical Fill Policy]] — `experience_capture_docs`
- [[docs/contexts/legacy/experience_capture/answers/ENT-R03/answer_normalized_en|ENT-R03 — Normalized Interpretation]] — `experience_capture_docs`
- [[docs/contexts/legacy/experience_capture/answers/ENT-R03/notes_en|ENT-R03 — Notes and Open Questions]] — `experience_capture_docs`
- [[docs/contexts/legacy/experience_capture/answers/ENT-R03/question_en|ENT-R03 — Pending Limit Lifecycle: Cancel, Missed, Replace]] — `experience_capture_docs`
- [[docs/contexts/legacy/experience_capture/answers/ENT-R04/answer_normalized_en|ENT-R04 — Normalized Interpretation]] — `experience_capture_docs`
- [[docs/contexts/legacy/experience_capture/answers/ENT-R04/notes_en|ENT-R04 — Notes and Open Questions]] — `experience_capture_docs`
- [[docs/contexts/legacy/experience_capture/answers/EXE-R01/answer_normalized_en|EXE-R01 — Normalized Interpretation]] — `experience_capture_docs`
- [[docs/contexts/legacy/experience_capture/answers/EXE-R01/notes_en|EXE-R01 — Notes and Open Questions]] — `experience_capture_docs`
- [[docs/contexts/legacy/experience_capture/answers/EXE-R01/question_en|EXE-R01 — ExecutionIntent Contract Finalization]] — `experience_capture_docs`
- [[docs/contexts/legacy/experience_capture/answers/EXE-R02/answer_normalized_en|EXE-R02 — Normalized Interpretation]] — `experience_capture_docs`
- [[docs/contexts/legacy/experience_capture/answers/EXE-R02/answer_raw_en|EXE-R02 — Raw Answer]] — `experience_capture_docs`
- [[docs/contexts/legacy/experience_capture/answers/EXE-R02/notes_en|EXE-R02 — Notes and Open Questions]] — `experience_capture_docs`
- [[docs/contexts/legacy/experience_capture/answers/EXE-R02/question_en|EXE-R02 — Broker Validator and Send Gate]] — `experience_capture_docs`
- [[docs/contexts/legacy/experience_capture/answers/EXT-01/answer_normalized_en|EXT-01 — Normalized Interpretation]] — `experience_capture_docs`
- [[docs/contexts/legacy/experience_capture/answers/EXT-01/answer_raw_en|EXT-01 — Raw Answer]] — `experience_capture_docs`
- [[docs/contexts/legacy/experience_capture/answers/EXT-01/notes_en|EXT-01 — Notes and Open Questions]] — `experience_capture_docs`
- [[docs/contexts/legacy/experience_capture/answers/EXT-01/question_en|EXT-01 — How Exactly Is Extreme Defined Relative to an Untouched Node?]] — `experience_capture_docs`
- [[docs/contexts/legacy/experience_capture/answers/EXT-02/answer_normalized_en|EXT-02 — Normalized Interpretation]] — `experience_capture_docs`
- [[docs/contexts/legacy/experience_capture/answers/EXT-02/answer_raw_en|EXT-02 — Raw Answer]] — `experience_capture_docs`
- [[docs/contexts/legacy/experience_capture/answers/EXT-02/notes_en|EXT-02 — Notes and Open Questions]] — `experience_capture_docs`
- [[docs/contexts/legacy/experience_capture/answers/EXT-02/question_en|EXT-02 — Which Project Logic Produces the Anchor Node for Extreme?]] — `experience_capture_docs`
- [[docs/contexts/legacy/experience_capture/answers/EXT-03/answer_normalized_en|EXT-03 — Normalized Interpretation]] — `experience_capture_docs`
- [[docs/contexts/legacy/experience_capture/answers/EXT-03/answer_raw_en|EXT-03 — Raw Answer]] — `experience_capture_docs`

## Agent use

- هنگام طراحی Agent، این concept باید به عنوان context قابل بازیابی استفاده شود.
- هر patch یا experiment مرتبط باید به این concept link شود.
