---
title: "Astro ML"
type: concept
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source: "auto-derived from project docs"
document_count: "59"
---


# Astro ML

## نقش در Alpha Lab

Astro ML مجموعه feature store، bridge، validation و meta learner برای آزمایش ویژگی‌های آسترولوژیک/زمانی است.

## Keywords

- `astro`
- `planet`
- `ephemeris`
- `feature store`
- `meta learner`

## Related source documents

- [[docs/architecture|System Architecture]] — `core_docs`
- [[docs/astro_ml_training_quickstart|Astro ML Training Quickstart]] — `core_docs`
- [[docs/execution/E0003_CONTINUATION_CLOSE_HUNT|E0003 — H0005 Continuation Close-Hunt Market Executor]] — `execution_docs`
- [[docs/research/H0009_astro_feature_store_distribution_engineering|H0009 — Astro Feature Store for Distribution Engineering]] — `research_docs`
- [[docs/research/H0009_astro_feature_taxonomy|EXP0013 — Astro Feature Meaning and Research Semantics]] — `research_docs`
- [[docs/research/H0009_astro_path_cleanliness_metrics|H0009 — Astro Path Cleanliness Metrics]] — `research_docs`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_CSV_COMMON_FILES_TESTER_FIX|EXP0013 Astro CSV — Strategy Tester Common Files Fix]] — `experiment`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_CSV_DIAGNOSTIC_GUIDE|EXP0013 Astro CSV Runtime Diagnostic Guide]] — `experiment`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_CSV_FILES_ROOT_FALLBACK|EXP0013 Astro CSV Runtime Path Fix]] — `experiment`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_CSV_RUNTIME_PATH_AND_PANEL_FIX|EXP0013 Astro CSV Runtime Path and Panel Diagnostics]] — `experiment`
- [[docs/evidence/exp0013_astro_csv_runtime_path_fix/ad8f4c6e752a_ASTRO_CSV_RUNTIME_PATH_FIX|EXP0013 Astro CSV Runtime Path Fix]] — `experiment`
- [[docs/evidence/exp0013_astro_dashboard_header_spacing_tuning/674fd8707612_ASTRO_DASHBOARD_V10_SPACING_HEADER_TUNE|EXP0013 Astro Dashboard V10 - Header and spacing tuning]] — `experiment`
- [[docs/evidence/exp0013_astro_dashboard_best_version/5f8623d90153_ASTRO_DASHBOARD_V11_BEST_VERSION|EXP0013 Astro Dashboard V11 - Best Version]] — `experiment`
- [[docs/evidence/exp0013_astro_dashboard_clean_header_minimize_mode_cleaner_oscillator/d69d3d6a23b9_ASTRO_DASHBOARD_V12_HEADER_MINIMIZE_CLEAN_OSC|EXP0013 Astro Dashboard V12 - Clean Header, Minimize Mode, Cleaner Oscillator]] — `experiment`
- [[docs/evidence/exp0013_astro_dashboard_ui_review_redesign/3ba3ac6b98fa_ASTRO_DASHBOARD_V13_UI_REVIEW_AND_REDESIGN|EXP0013 Astro Dashboard V13 - UI Review and Redesign]] — `experiment`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_DASHBOARD_V2_COCKPIT_GUIDE|EXP0013 Astro Dashboard V2 - Cockpit Layout]] — `experiment`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_DASHBOARD_V3_INTERACTIVE_COCKPIT_GUIDE|EXP0013 Astro Dashboard V3 - Interactive Cockpit]] — `experiment`
- [[docs/evidence/exp0013_astro_dashboard_layout_cleanup/fdcb3b9b6858_ASTRO_DASHBOARD_V4_LAYOUT_CLEANUP_GUIDE|EXP0013 Astro Dashboard V4 - Layout Cleanup]] — `experiment`
- [[docs/evidence/exp0013_astro_dashboard_pro_clean_layout/45e4e980b219_ASTRO_DASHBOARD_V5_PRO_CLEAN_GUIDE|EXP0013 Astro Dashboard V5 - Pro Clean Layout]] — `experiment`
- [[docs/evidence/exp0013_astro_dashboard_cleanup_spacing_fix/e8031fe69dd3_ASTRO_DASHBOARD_V6_CLEANUP_AND_SPACING_FIX|EXP0013 Astro Dashboard V6 - Cleanup and Spacing Fix]] — `experiment`
- [[docs/evidence/exp0013_astro_dashboard_visual_polish/884be8b774a1_ASTRO_DASHBOARD_V7_VISUAL_POLISH|EXP0013 Astro Dashboard V7 - Visual Polish]] — `experiment`
- [[docs/evidence/exp0013_astro_dashboard_header_buttons_dynamic_spacing/38dfe94afabd_ASTRO_DASHBOARD_V8_HEADER_BUTTONS_DYNAMIC_SPACING|EXP0013 Astro Dashboard V8 - Header, Buttons, Dynamic Spacing]] — `experiment`
- [[docs/evidence/exp0013_astro_dashboard_stable_in_place_updates/ce83846c8724_ASTRO_DASHBOARD_V9_STABLE_IN_PLACE_UPDATE|EXP0013 Astro Dashboard V9 - Stable In-Place Updates]] — `experiment`
- [[docs/evidence/astro_doctrine/f9353abb5fd5_ASTRO_DOCTRINE_V1|ASTRO Doctrine V1]] — `experiment`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_FEATURE_MEANING|EXP0013 — Astro Feature Meaning and Research Semantics]] — `experiment`
- [[docs/evidence/exp0013_astro_fractal_m1_oscillator_guide/497686de5688_ASTRO_FRACTAL_M1_OSCILLATOR_GUIDE|EXP0013 Astro Fractal M1 Oscillator Guide]] — `experiment`
- [[docs/evidence/exp0013_astro_scale_model_m1/0800b36f63d2_ASTRO_M1_SCALE_MODEL|EXP0013 Astro Scale Model for M1]] — `experiment`
- [[docs/evidence/exp0013_astro_time_contract_no_second_gmt_shift/dff6c2da3787_ASTRO_NO_SECOND_GMT_SHIFT|EXP0013 Astro Time Contract: No Second GMT Shift]] — `experiment`
- [[docs/evidence/exp0013_astro_only_execution_contract/b50b0013f3c9_ASTRO_ONLY_EXECUTION_CONTRACT|EXP0013 Astro-Only Execution Contract]] — `experiment`
- [[docs/evidence/exp0013_astro_only_execution_roadmap/d577cd434dcb_ASTRO_ONLY_EXECUTION_ROADMAP|EXP0013 Astro-Only Execution Roadmap]] — `experiment`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_OSCILLATOR_COMPILE_FIX_AND_FRACTAL_PLAN|EXP0013 Astro Oscillator Compile Fix + Fractal Detail Plan]] — `experiment`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_PATH_CLEANLINESS_SCREEN_GUIDE|EXP0013 — Astro Path Cleanliness Screen Guide]] — `experiment`
- [[docs/evidence/astro_professionalization_gap_map/b3f4b0da7c2e_ASTRO_PROFESSIONALIZATION_GAP_MAP|Astro Professionalization Gap Map]] — `experiment`
- [[docs/evidence/exp0013_pure_astro_signal_algorithms/7e6eca7a86f8_ASTRO_PURE_SIGNAL_ALGORITHMS|EXP0013 Pure Astro Signal Algorithms]] — `experiment`
- [[docs/evidence/exp0013_astro_raw_axes_oscillator/d4d1fb06e8fa_ASTRO_RAW_AXES_OSCILLATOR_GUIDE|EXP0013 Astro Raw Axes Oscillator]] — `experiment`
- [[docs/evidence/exp0013_astro_raw_sky_radical_redesign/be7e95f4ddeb_ASTRO_RAW_SKY_RADICAL_REDESIGN|EXP0013 Astro Raw Sky Radical Redesign]] — `experiment`
- [[docs/evidence/exp0013_raw_sky_tabbed_ui_natal_doctrine/4417b5ea0f1c_ASTRO_RAW_SKY_TABBED_UI_AND_NATAL_DOCTRINE|EXP0013 Raw Sky Tabbed UI and Natal Doctrine]] — `experiment`
- [[docs/evidence/exp0013_raw_sky_compile_fix/cc710a086588_ASTRO_RAW_SKY_V14_COMPILE_FIX|EXP0013 Raw Sky V14 Compile Fix]] — `experiment`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_TESTER_OPEN_ERROR_3_FIX|EXP0013 Tester open error [3] fix]] — `experiment`
- [[docs/evidence/exp0013_astro_time_contract_panel_fix/b3c4f9d25abb_ASTRO_TIME_CONTRACT_AND_PANEL_FIX|EXP0013 Astro Time Contract and Panel Fix]] — `experiment`
- [[docs/evidence/astro_timing_doctrine/e8dec3f797a0_ASTRO_TIMING_DOCTRINE|ASTRO Timing Doctrine]] — `experiment`
- [[docs/evidence/exp0013_astro_unified_dashboard_ea_display_update_fix/da2c2a4d4bf4_ASTRO_UNIFIED_DASHBOARD_DISPLAY_FIX|EXP0013 Astro Unified Dashboard EA - Display and Update Fix]] — `experiment`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_UNIFIED_DASHBOARD_EA_GUIDE|EXP0013 Unified Dashboard EA]] — `experiment`
- [[docs/evidence/exp0013_astro_excel_csv_build_commands/6e29545f8168_BUILD_EXCEL_COMMANDS|EXP0013 — Astro Excel / CSV Build Commands]] — `experiment`
- [[lab/03_experiments/EXP0013_astro_feature_store/README|EXP0013 - Astro Feature Store]] — `experiment`
- [[docs/evidence/run_exp0013_astro_fractal_oscillator/55b1ec2fe983_RUN_ASTRO_FRACTAL_OSCILLATOR|Run EXP0013 Astro Fractal Oscillator]] — `experiment`
- [[docs/evidence/run_exp0013_astro_fractal_oscillator_through_tester_host/6ea0f9de36e9_RUN_ASTRO_FRACTAL_OSCILLATOR_TESTER_HOST|Run EXP0013 Astro Fractal Oscillator through Tester Host]] — `experiment`
- [[docs/evidence/run_astro_path_cleanliness_screen/fe12afa052cd_RUN_ASTRO_PATH_SCREEN|Run Astro Path Cleanliness Screen]] — `experiment`
- [[docs/evidence/run_exp0013_astro_raw_axes_oscillator/1cf21803c17b_RUN_ASTRO_RAW_AXES_OSCILLATOR|Run EXP0013 Astro Raw Axes Oscillator]] — `experiment`
- [[lab/03_experiments/EXP0013_astro_feature_store/finalization/README|EXP0013 Finalization Snapshot]] — `experiment`
- [[docs/evidence/exp0016_antifragile_astro_learning_doctrine/a5f84b716738_ANTIFRAGILE_LEARNING_DOCTRINE|EXP0016 Antifragile Astro Learning Doctrine]] — `experiment`
- [[lab/03_experiments/EXP0016_astro_meta_learner/README|EXP0016 Astro Meta Learner]] — `experiment`
- [[docs/releases/legacy_migration/general/79a62a424a39_README_FLAG_MARKET_ANATOMY_PHILOSOPHY|Flag Project Philosophy: Market Anatomy, Liquidity Necessity, and Objective Flow]] — `experiment`
- [[mql5/Experts/AstroExecution/README|Astro Execution]] — `mql5_docs`
- [[tools/astro_feature_builder/README|Astro Feature Builder]] — `tool_docs`
- [[tools/astro_live_bridge/README|EXP0013 Astro Live Bridge V2]] — `tool_docs`
- [[tools/astro_ml/README|Astro ML Tools]] — `tool_docs`
- [[tools/astro_validation/README|Astro Signal Validator]] — `tool_docs`
- [[docs/releases/legacy_migration/general/986fa598c76e_README_pure_entry_excel|Pure Astro Entry Excel Report]] — `tool_docs`

## Agent use

- هنگام طراحی Agent، این concept باید به عنوان context قابل بازیابی استفاده شود.
- هر patch یا experiment مرتبط باید به این concept link شود.
