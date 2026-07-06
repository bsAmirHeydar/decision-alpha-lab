---
title: "Hook"
type: concept
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source: "auto-derived from project docs"
document_count: "278"
---


# Hook

## نقش در Alpha Lab

Hook لایه تشخیص چرخه، برگشت به مبدا، Sequence و نقطه‌های تصمیم در ساختار NDS است. این مفهوم باید با Rally/F-counting هم‌زیست باشد و execution مستقیم نداشته باشد مگر بعد از validation.

## Keywords

- `hook`
- `cyclehook`
- `cycle hook`
- `nds hook`

## Related source documents

- [[docs/ai_execution/AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA|AI Algorithm Layer Map for Extreme Engine — نقشه الگوریتم‌های هوش مصنوعی برای اکستریم L2]] — `ai_execution_docs`
- [[docs/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI Native Execution Roadmap — نقشه راه هوش مصنوعی، بک‌تست و پل اگزکیوت]] — `ai_execution_docs`
- [[docs/ai_execution/AMIR_STRUCTURAL_EXPERIENCE_MAP_FA|Amir Structural Experience Map — نقشه تجربه‌های ساختاری امیر]] — `ai_execution_docs`
- [[docs/ai_execution/EXPERIENCE_CAPTURE_LOG_TEMPLATE_FA|Experience Capture Log Template — قالب ثبت تجربه‌های امیر]] — `ai_execution_docs`
- [[docs/ai_execution/EXTREME_L2_NODE_CYCLE_LIMIT_ENTRY_FA|Extreme L2 Node Cycle Limit Entry — تعریف رسمی اکستریم، نود L2 و ورود لیمیت]] — `ai_execution_docs`
- [[docs/ai_execution/README|AI Execution Docs]] — `ai_execution_docs`
- [[docs/debug/E0007/README|E0007 — Purple Source Extreme Executor Template]] — `debug_docs`
- [[docs/debug/E0008/README|E0008 — MTF Purple Extreme Executor]] — `debug_docs`
- [[docs/debug/E0009/README|E0009 — Reversal Macro / Latest Setup / Hook Executor]] — `debug_docs`
- [[docs/debug/MARKET_LANGUAGE/README|DAL Market Language — Nodes, Cycles, Hooks, Rallies, Flags, 123 Flags, and Open 1/2s]] — `debug_docs`
- [[docs/experience_capture/EXPERIENCE_CAPTURE_INDEX_EN|Experience Capture Index]] — `experience_capture_docs`
- [[docs/experience_capture/answers/BASE-01/answer_normalized_en|BASE-01 — Normalized Interpretation]] — `experience_capture_docs`
- [[docs/experience_capture/answers/BASE-01/answer_raw_en|BASE-01 — Raw Answer]] — `experience_capture_docs`
- [[docs/experience_capture/answers/BASE-01/notes_en|BASE-01 — Notes and Open Questions]] — `experience_capture_docs`
- [[docs/experience_capture/answers/BASE-02/answer_normalized_en|BASE-02 — Normalized Interpretation]] — `experience_capture_docs`
- [[docs/experience_capture/answers/BASE-02/answer_raw_en|BASE-02 — Raw Answer]] — `experience_capture_docs`
- [[docs/experience_capture/answers/BASE-02/notes_en|BASE-02 — Notes and Open Questions]] — `experience_capture_docs`
- [[docs/experience_capture/answers/BASE-03/answer_normalized_en|BASE-03 — Normalized Interpretation]] — `experience_capture_docs`
- [[docs/experience_capture/answers/BASE-03/answer_raw_en|BASE-03 — Raw Answer]] — `experience_capture_docs`
- [[docs/experience_capture/answers/BASE-03/notes_en|BASE-03 — Notes and Open Questions]] — `experience_capture_docs`
- [[docs/experience_capture/answers/BASE-04/answer_normalized_en|BASE-04 — Normalized Interpretation]] — `experience_capture_docs`
- [[docs/experience_capture/answers/BASE-04/answer_raw_en|BASE-04 — Raw Answer]] — `experience_capture_docs`
- [[docs/experience_capture/answers/BASE-04/notes_en|BASE-04 — Notes and Open Questions]] — `experience_capture_docs`
- [[docs/experience_capture/answers/BASE-05/answer_normalized_en|BASE-05 — Normalized Interpretation]] — `experience_capture_docs`
- [[docs/experience_capture/answers/BASE-05/answer_raw_en|BASE-05 — Raw Answer]] — `experience_capture_docs`
- [[docs/experience_capture/answers/BASE-05/notes_en|BASE-05 — Notes and Open Questions]] — `experience_capture_docs`
- [[docs/experience_capture/answers/BASE-06/answer_normalized_en|BASE-06 — Normalized Interpretation]] — `experience_capture_docs`
- [[docs/experience_capture/answers/BASE-06/answer_raw_en|BASE-06 — Raw Answer]] — `experience_capture_docs`
- [[docs/experience_capture/answers/BASE-06/notes_en|BASE-06 — Notes and Open Questions]] — `experience_capture_docs`
- [[docs/experience_capture/answers/DST-R01/answer_normalized_en|DST-R01 — Normalized Interpretation]] — `experience_capture_docs`
- [[docs/experience_capture/answers/DST-R01/answer_raw_en|DST-R01 — Raw Answer]] — `experience_capture_docs`
- [[docs/experience_capture/answers/DST-R01/notes_en|DST-R01 — Notes and Open Questions]] — `experience_capture_docs`
- [[docs/experience_capture/answers/DST-R01/question_en|DST-R01 — Destination Taxonomy and Open One-Two]] — `experience_capture_docs`
- [[docs/experience_capture/answers/DST-R02/answer_normalized_en|DST-R02 — Normalized Interpretation]] — `experience_capture_docs`
- [[docs/experience_capture/answers/DST-R03/answer_normalized_en|DST-R03 — Normalized Interpretation]] — `experience_capture_docs`
- [[docs/experience_capture/answers/DST-R03/notes_en|DST-R03 — Notes and Open Questions]] — `experience_capture_docs`
- [[docs/experience_capture/answers/DST-R03/question_en|DST-R03 — Destination Repricing and Completion]] — `experience_capture_docs`
- [[docs/experience_capture/answers/ENT-R01/answer_normalized_en|ENT-R01 — Normalized Interpretation]] — `experience_capture_docs`
- [[docs/experience_capture/answers/ENT-R01/answer_raw_en|ENT-R01 — Raw Answer]] — `experience_capture_docs`
- [[docs/experience_capture/answers/ENT-R01/notes_en|ENT-R01 — Notes and Open Questions]] — `experience_capture_docs`
- [[docs/experience_capture/answers/ENT-R01/question_en|ENT-R01 — Entry-Level Extreme Definition]] — `experience_capture_docs`
- [[docs/experience_capture/answers/ENT-R02/question_en|ENT-R02 — Limit Entry, Stop Geometry, and Practical Fill Policy]] — `experience_capture_docs`
- [[docs/experience_capture/answers/EXE-R01/answer_normalized_en|EXE-R01 — Normalized Interpretation]] — `experience_capture_docs`
- [[docs/experience_capture/answers/EXT-01/answer_normalized_en|EXT-01 — Normalized Interpretation]] — `experience_capture_docs`
- [[docs/experience_capture/answers/EXT-02/answer_normalized_en|EXT-02 — Normalized Interpretation]] — `experience_capture_docs`
- [[docs/experience_capture/answers/EXT-02/notes_en|EXT-02 — Notes and Open Questions]] — `experience_capture_docs`
- [[docs/experience_capture/answers/EXT-02/question_en|EXT-02 — Which Project Logic Produces the Anchor Node for Extreme?]] — `experience_capture_docs`
- [[docs/experience_capture/answers/EXT-03/notes_en|EXT-03 — Notes and Open Questions]] — `experience_capture_docs`
- [[docs/experience_capture/answers/EXT-04/answer_normalized_en|EXT-04 — Normalized Interpretation]] — `experience_capture_docs`
- [[docs/experience_capture/answers/EXT-04/notes_en|EXT-04 — Notes and Open Questions]] — `experience_capture_docs`
- [[docs/experience_capture/answers/EXT-04/question_en|EXT-04 — Is L2 Always the Default, or Only in Specific Contexts?]] — `experience_capture_docs`
- [[docs/experience_capture/answers/EXT-08/notes_en|EXT-08 — Notes and Open Questions]] — `experience_capture_docs`
- [[docs/experience_capture/answers/NDS-R01/answer_normalized_en|NDS-R01 — Normalized Interpretation]] — `experience_capture_docs`
- [[docs/experience_capture/answers/NDS-R01/answer_raw_en|NDS-R01 — Raw Answer]] — `experience_capture_docs`
- [[docs/experience_capture/answers/NDS-R01/notes_en|NDS-R01 — Notes and Open Questions]] — `experience_capture_docs`
- [[docs/experience_capture/answers/NDS-R01/question_en|NDS-R01 — Canonical NDS Object Model]] — `experience_capture_docs`
- [[docs/experience_capture/answers/NDS-R02/answer_normalized_en|NDS-R02 — Normalized Interpretation]] — `experience_capture_docs`
- [[docs/experience_capture/answers/NDS-R02/answer_raw_en|NDS-R02 — Raw Answer]] — `experience_capture_docs`
- [[docs/experience_capture/answers/NDS-R02/notes_en|NDS-R02 — Notes and Open Questions]] — `experience_capture_docs`
- [[docs/experience_capture/answers/NDS-R02/question_en|NDS-R02 — Cycle Lifecycle: Birth, Life, Near-Death, Death, and New Cycle]] — `experience_capture_docs`
- [[docs/experience_capture/answers/NDS-R03/answer_normalized_en|NDS-R03 — Normalized Interpretation]] — `experience_capture_docs`
- [[docs/experience_capture/answers/NDS-R03/answer_raw_en|NDS-R03 — Raw Answer]] — `experience_capture_docs`
- [[docs/experience_capture/answers/NDS-R03/notes_en|NDS-R03 — Notes and Open Questions]] — `experience_capture_docs`
- [[docs/experience_capture/answers/NDS-R03/question_en|NDS-R03 — Node Identity, Node Cluster, and Node Replacement]] — `experience_capture_docs`
- [[docs/experience_capture/answers/RSK-R02/answer_normalized_en|RSK-R02 — Normalized Interpretation]] — `experience_capture_docs`
- [[docs/experience_capture/answers/SCN-R01/answer_normalized_en|SCN-R01 — Normalized Interpretation]] — `experience_capture_docs`
- [[docs/experience_capture/answers/SCN-R01/answer_raw_en|SCN-R01 — Raw Answer]] — `experience_capture_docs`
- [[docs/experience_capture/answers/SCN-R01/notes_en|SCN-R01 — Notes and Open Questions]] — `experience_capture_docs`
- [[docs/experience_capture/answers/SCN-R01/question_en|SCN-R01 — Context Power Scoring]] — `experience_capture_docs`
- [[docs/experience_capture/answers/SCN-R02/answer_normalized_en|SCN-R02 — Normalized Interpretation]] — `experience_capture_docs`
- [[docs/experience_capture/answers/SCN-R02/answer_raw_en|SCN-R02 — Raw Answer]] — `experience_capture_docs`
- [[docs/experience_capture/answers/SCN-R02/notes_en|SCN-R02 — Notes and Open Questions]] — `experience_capture_docs`
- [[docs/experience_capture/answers/SCN-R04/answer_normalized_en|SCN-R04 — Normalized Interpretation]] — `experience_capture_docs`
- [[docs/experience_capture/index_fragments/DST-R01_en|Index Fragment — DST-R01]] — `experience_capture_docs`
- [[docs/experience_capture/index_fragments/ENT-R01_en|Index Fragment — ENT-R01]] — `experience_capture_docs`
- [[docs/experience_capture/index_fragments/SCN-R02_en|Index Fragment — SCN-R02]] — `experience_capture_docs`
- [[docs/experience_capture/questions/README|Quant Lab Experience Capture Questionnaire]] — `experience_capture_docs`
- [[docs/experience_capture/questions/remaining_v2/ACTIVE_REMAINING_QUESTIONS_V2_EN|Active Remaining Questions v2]] — `experience_capture_docs`
- [[docs/experience_capture/questions/remaining_v2/by_code/ENT-R02|ENT-R02 — Hook-Hook-Rally Formal Definition]] — `experience_capture_docs`
- [[docs/experience_capture/questions/remaining_v2/by_code/EXT-R03|EXT-R03 — L-Level Adaptive Policy]] — `experience_capture_docs`
- [[docs/experience_capture/questions/remaining_v2/by_code/NDS-R01|NDS-R01 — Canonical NDS Object Model]] — `experience_capture_docs`
- [[docs/experience_capture/questions/remaining_v2/by_code/SCN-R02|SCN-R02 — Potential Zone Definition]] — `experience_capture_docs`
- [[docs/experience_capture/questions/remaining_v2/by_code/SCN-R03|SCN-R03 — Destination and Open Reward Path]] — `experience_capture_docs`
- [[docs/experience_capture/questions/remaining_v2/sections/03_entry_families/README|Entry Families Beyond Extreme]] — `experience_capture_docs`
- [[docs/experience_capture/questions/remaining_v3_split/DATA-R01/question_en|DATA-R01 — Canonical State Packet v1]] — `experience_capture_docs`
- [[docs/experience_capture/questions/remaining_v3_split/DATA-R01/question_fa|DATA-R01 — Canonical State Packet v1]] — `experience_capture_docs`
- [[docs/experience_capture/questions/remaining_v3_split/DATA-R02/question_en|DATA-R02 — Label and Event Ledger]] — `experience_capture_docs`
- [[docs/experience_capture/questions/remaining_v3_split/DATA-R02/question_fa|DATA-R02 — Label and Event Ledger]] — `experience_capture_docs`
- [[docs/experience_capture/questions/remaining_v3_split/DST-R01/question_en|DST-R01 — Destination Taxonomy and Open One-Two]] — `experience_capture_docs`
- [[docs/experience_capture/questions/remaining_v3_split/DST-R01/question_fa|DST-R01 — Destination Taxonomy and Open One-Two]] — `experience_capture_docs`
- [[docs/experience_capture/questions/remaining_v3_split/TEST-R01/question_en|TEST-R01 — Baseline, Ablation, and Family Testing]] — `experience_capture_docs`
- [[docs/experience_capture/questions/remaining_v3_split/TEST-R01/question_fa|TEST-R01 — Baseline, Ablation, and Family Testing]] — `experience_capture_docs`
- [[docs/flag_counting/FLAG_COUNTING_ALGORITHM_BLUEPRINT|Flag Counting Algorithm Blueprint]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_CONCEPT_SPEC_V2|Flag Counting Concept Specification v2]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_CONCEPT_SPEC_V3|Flag Counting Concept Specification v3]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_CURRENT_CANON|Flag Counting Current Canon]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_GLOSSARY|Flag Counting Glossary]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_IMPLEMENTATION_CHECKLIST_V3|Flag Counting Implementation Checklist V3]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_IMPLEMENTATION_CHECKLIST_V4|Flag Counting Implementation Checklist V4]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19A_SILENT_DEFAULTS_AND_LIFECYCLE_CLEANUP|Flag Counting Level 19A — Silent Defaults and Lifecycle Cleanup]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19B_CLOSED_BAR_STATE_LEDGER|Flag Counting Level 19B — Closed-Bar State Ledger]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19C_STATE_DELTA_LEDGER|Flag Counting Level 19C — Closed-Bar State Delta Ledger]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19D_TRANSITION_EVENT_LEDGER|Flag Counting Level 19D — Closed-Bar Transition Event Ledger]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19Z_COMPLETE_OBSERVATION_SUITE|Flag Counting Level 19Z — Complete Observation Suite]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_CLEAN_ISOLATED_STATE_GATE|Flag Counting Level 19 — Clean Isolated State Gate]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE10_PANEL_LINE_CONTRACT|Flag Counting Level 19 — Phase 10 Panel Line Debug Contract]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE11_ENTRY_BRIDGE_READINESS|Flag Counting Level 19 — Phase 11 Entry Bridge Readiness]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE12_EXTREME_CANDIDATE_MAP|Flag Counting Level 19 — Phase 12 Extreme Candidate Map]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE13A_COMPILE_FIX|Flag Counting Level 19 — Phase 13A Compile Fix]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE13_MTF_ALIGNMENT_MAP|Flag Counting Level 19 — Phase 13 Multi-Timeframe Alignment Map]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE14_ENTRY_GEOMETRY_READINESS|Flag Counting Level 19 — Phase 14 Entry Geometry Readiness]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE15_ENTRY_IDEA_LAYER|Flag Counting Level 19 — Phase 15 Entry Idea Layer]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE16_ENTRY_DECISION_DRY_RUN|Flag Counting Level 19 — Phase 16 Entry Decision Layer / Dry Run]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE17_PAPER_EXECUTION_LEDGER|Flag Counting Level 19 — Phase 17 Paper Execution / Dry Run Ledger]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE18_PAPER_LEDGER_LIFECYCLE_TRACKING|Flag Counting Level 19 — Phase 18 Paper Ledger Lifecycle Tracking]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE19_PAPER_RESULT_METRICS|Flag Counting Level 19 — Phase 19 Paper Result Metrics / R-Equivalent Summary]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE20A_COMPILE_FIX|Flag Counting Level 19 — Phase 20A Compile Fix]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE20_PAPER_PORTFOLIO_AGGREGATE_METRICS|Flag Counting Level 19 — Phase 20 Paper Portfolio / Aggregate Metrics]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE21_PAPER_REGIME_ATTRIBUTION|Flag Counting Level 19 — Phase 21 Paper Regime Attribution]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE22_PAPER_FILTER_DIAGNOSTICS|Flag Counting Level 19 — Phase 22 Paper Filter Diagnostics]] — `flag_counting_docs`

## Agent use

- هنگام طراحی Agent، این concept باید به عنوان context قابل بازیابی استفاده شود.
- هر patch یا experiment مرتبط باید به این concept link شود.
