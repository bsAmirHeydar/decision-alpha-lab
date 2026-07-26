---
title: "Known-Time Causality"
type: concept
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source: "auto-derived from project docs"
document_count: "63"
---


# Known-Time Causality

## نقش در Alpha Lab

Known-Time Causality خط قرمز ضد lookahead است: هر label فقط بعد از زمان قابل دانستن خودش حق اثرگذاری دارد.

## Keywords

- `known time`
- `known-time`
- `live-known`
- `same-candle`
- `causal`
- `no future`

## Related source documents

- [[README|Decision Alpha Lab]] — `readme`
- [[docs/architecture|System Architecture]] — `core_docs`
- [[docs/articles/structural_regime_memory_without_samples|Article — Structural Regime Memory Without Samples]] — `article_docs`
- [[docs/atomic_live_research_contract|Atomic Live Research Contract]] — `core_docs`
- [[docs/debug/D0007_H5_CAUSAL_LIVE_REPLAY_AUDIT|D0007 — H5 Causal Live Replay Audit]] — `debug_docs`
- [[docs/debug/D0008_H4_CAUSAL_BATCH_REPORT|D0008 / H0004 Causal Known-Candle Batch Report]] — `debug_docs`
- [[docs/debug/D0010_H4_ATOMIC_NO_SAMPLE_REGIME_AUDIT|D0010 — H4 Atomic No-Sample Regime Audit]] — `debug_docs`
- [[docs/debug/E0008/README|E0008 — MTF Purple Extreme Executor]] — `debug_docs`
- [[docs/debug/H4_ATOMIC_FULL_STRESS_CONTEXT|H4 Atomic Full Stress + Human Context Diagnostics]] — `debug_docs`
- [[docs/debug/H4_DEEP_H6_OPTIONALITY_REPORT|H4 Deep Atomic Report + H6 Reversal Optionality]] — `debug_docs`
- [[docs/debug/H4_FAST_ATOMIC_EXTENDED_REPORT|H4 Fast Atomic Extended Report]] — `debug_docs`
- [[docs/debug/H4_FAST_ATOMIC_MAIN_REPORT|H4 Fast Atomic Main Report]] — `debug_docs`
- [[docs/debug/H6_CANDLE_STREAM_FAST|H6 Candle-Stream Fast Optionality]] — `debug_docs`
- [[docs/debug/H6_FAST_ACCURATE_OPTIONALITY|H6 Fast Accurate Optionality Report]] — `debug_docs`
- [[docs/debug/H6_NODE_SURVIVAL_MAP|H6 Node Survival Map]] — `debug_docs`
- [[docs/debug/H6_REACTION_BOX_ZONES|H6 Reaction Box Zones]] — `debug_docs`
- [[docs/debug/H6_STANDALONE_OPTIONALITY_EDGE_MAP|H0006 standalone optionality and edge-map report]] — `debug_docs`
- [[docs/debug/MAIN_ATOMIC_NO_SAMPLE_UNIFICATION|Main Atomic No-Sample Unification for H4/H5]] — `debug_docs`
- [[docs/glossary|Glossary]] — `core_docs`
- [[docs/mql_native/H0007_FLAG_COUNTING_F1_START_STRUCTURE|H0007 — Flag Counting / F1 Start Structure]] — `mql_native_docs`
- [[docs/principles|Research Principles]] — `core_docs`
- [[docs/reports/2026-06-20_h4_h5_gold_m10_report|Report — H4/H5 GOLD M10 Review, 2026-06-20]] — `core_docs`
- [[docs/research-roadmap|Research Roadmap]] — `core_docs`
- [[docs/research/H0008_distribution_engineering|H0008 — Distribution Engineering]] — `research_docs`
- [[docs/research/H0009_astro_feature_store_distribution_engineering|H0009 — Astro Feature Store for Distribution Engineering]] — `research_docs`
- [[docs/research/H0009_astro_feature_taxonomy|EXP0013 — Astro Feature Meaning and Research Semantics]] — `research_docs`
- [[docs/research/H0009_astro_path_cleanliness_metrics|H0009 — Astro Path Cleanliness Metrics]] — `research_docs`
- [[docs/research_lessons_and_failure_modes|Research Lessons and Failure Modes]] — `core_docs`
- [[docs/ui/ROADMAP|UI Implementation Roadmap]] — `ui_docs`
- [[docs/evidence/h0002_structural_node_territories_revisitation_dynamics/0117ab4487f7_H0002_structural_node_revisitation|H0002 — Structural Node Territories and Revisitation Dynamics]] — `hypothesis`
- [[docs/evidence/h0004_branch_regime_memory/45fad849057f_H0004_branch_regime_memory_atomic|H0004 — Branch Regime Memory]] — `hypothesis`
- [[docs/evidence/h0005_directional_memory_execution/57d9666c6533_H0005_directional_memory_atomic|H0005 — Directional Memory and Execution]] — `hypothesis`
- [[docs/evidence/h0007_flag_counting_f1_start_structure/d02c831e47bd_H0007_flag_counting_f1_start_structure|H0007 — Flag Counting / F1 Start Structure]] — `hypothesis`
- [[docs/evidence/h0008_distribution_engineering_conditional_sequence_extraction/cc5e415d24b3_H0008_distribution_engineering_sequence_clusters|H0008 — Distribution Engineering for Conditional Sequence Extraction]] — `hypothesis`
- [[docs/evidence/exp0002_mql_native_m0001_runtime/319a21879dae_report|EXP0002 — MQL-native M0001 Runtime]] — `experiment`
- [[lab/03_experiments/EXP0012_distributional_cluster_miner/README|EXP0012 — Distributional Cluster Miner]] — `experiment`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_FEATURE_MEANING|EXP0013 — Astro Feature Meaning and Research Semantics]] — `experiment`
- [[docs/evidence/astro_professionalization_gap_map/b3f4b0da7c2e_ASTRO_PROFESSIONALIZATION_GAP_MAP|Astro Professionalization Gap Map]] — `experiment`
- [[docs/evidence/exp0013_astro_raw_sky_radical_redesign/be7e95f4ddeb_ASTRO_RAW_SKY_RADICAL_REDESIGN|EXP0013 Astro Raw Sky Radical Redesign]] — `experiment`
- [[docs/evidence/exp0013_astro_excel_csv_build_commands/6e29545f8168_BUILD_EXCEL_COMMANDS|EXP0013 — Astro Excel / CSV Build Commands]] — `experiment`
- [[lab/03_experiments/EXP0016_astro_meta_learner/README|EXP0016 Astro Meta Learner]] — `experiment`
- [[docs/releases/legacy_migration/general/79a62a424a39_README_FLAG_MARKET_ANATOMY_PHILOSOPHY|Flag Project Philosophy: Market Anatomy, Liquidity Necessity, and Objective Flow]] — `experiment`
- [[lab/03_validation/VAL0007_h5_causal_live_replay/README|VAL0007 — H5 Causal Live Replay]] — `validation`
- [[lab/03_validation/VAL0008_h4_causal_batch/README|VAL0008 — H4 Causal Batch Validation]] — `validation`
- [[lab/03_validation/VAL0010_h4_atomic_no_sample_regime/README|VAL0010 — H4 Atomic No-Sample Regime Replay]] — `validation`
- [[lab/03_validation/VAL0012_h4_fast_atomic_main/README|VAL0012 — H4 Fast Atomic Main Report]] — `validation`
- [[lab/03_validation/VAL0013_h4_fast_atomic_extended/README|VAL0013 — H4 Fast Atomic Extended Diagnostics]] — `validation`
- [[lab/03_validation/VAL0014_h4_atomic_full_stress_context/README|VAL0014 — H4 Atomic Full Stress + Human Context]] — `validation`
- [[lab/03_validation/VAL0017_h6_fast_accurate/README|VAL0017 — H6 Fast Accurate Optionality]] — `validation`
- [[lab/03_validation/VAL0022_h6_reaction_box_zones/README|VAL0022 — H6 Reaction Box Zones]] — `validation`
- [[lab/04_analysis/ANL004_h4_causal_batch_vs_classic/README|ANL004 — H4 Classic vs Causal Batch Analysis]] — `analysis`
- [[lab/04_execution/EXE0011_donchian20_atr3_roulette/README|EXE0011 — Donchian 20 ATR3 Roulette Execution]] — `execution`
- [[lab/05_validation/VAL0010_h4_atomic_no_sample_regime/README|VAL0010 — H4 Atomic No-Sample Regime Validation]] — `validation`
- [[lab/05_validation/VAL0011_main_atomic_no_sample_unification/README|VAL0011 — Main Atomic No-Sample Unification]] — `validation`
- [[lab/06_production/EXECUTION_FAMILIES/README|Execution Families]] — `production_signal`
- [[docs/evidence/exec001_stc_smt_cycles_implementation_plan/0d054880f96a_17_implementation_plan|EXEC001 STC SMT Cycles — Implementation Plan]] — `experiment`
- [[docs/evidence/exec001_stc_smt_cycles_module_breakdown/0e4565d59512_18_module_breakdown|EXEC001 STC SMT Cycles — Module Breakdown]] — `experiment`
- [[docs/evidence/exec001_stc_smt_cycles_implementation_risk_register/b5f9b48975ee_20_implementation_risk_register|EXEC001 STC SMT Cycles — Implementation Risk Register]] — `experiment`
- [[docs/evidence/level_06_smt_candidate_engine/97fffdd7f422_27_level_06_smt_candidate_engine|Level 06 — SMT Candidate Engine]] — `experiment`
- [[lab/09_execution/mql5/README|MQL5 Execution and Validation Layer]] — `execution`
- [[papers/001_atomic_live_regime_framework|Atomic Live Regime Framework]] — `paper`
- [[tools/astro_feature_builder/README|Astro Feature Builder]] — `tool_docs`
- [[tools/astro_ml/README|Astro ML Tools]] — `tool_docs`

## Agent use

- هنگام طراحی Agent، این concept باید به عنوان context قابل بازیابی استفاده شود.
- هر patch یا experiment مرتبط باید به این concept link شود.
