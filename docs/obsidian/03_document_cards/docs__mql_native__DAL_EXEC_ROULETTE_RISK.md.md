---
title: "DAL_ExecRouletteRisk — Roulette Execution Risk Model"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/mql_native/DAL_EXEC_ROULETTE_RISK.md"
source_ext: ".md"
category: "mql_native_docs"
source_size_bytes: "4243"
concepts:
  - "Execution"
  - "MQL Native"
  - "NDS Anatomy"
---


# DAL_ExecRouletteRisk — Roulette Execution Risk Model

**Source:** [[docs/mql_native/DAL_EXEC_ROULETTE_RISK|docs/mql_native/DAL_EXEC_ROULETTE_RISK.md]]

**Category:** `mql_native_docs`  
**Status:** ok  
**Size:** `4243` bytes

## خلاصه

`DAL_ExecRouletteRisk` is a reusable MQL5 execution-risk module. It returns **money risk** only. It does not send orders, decide entries, or decide exits. Each cycle stores: Default inputs: At cycle start: Example: If the account moves down but stays inside the protected band: risk remains fixed: Example: The risk does not shrink on every small loss. If balance breaks below the protected floor, the base account used for lot calculation must update downward. Rule: Example: The cycle re-locks: This is the corrected rule: the base does not follow every loss, but it does follow the account down after the protected floor is broken. The cycle becomes profit-active only after balance rises above th

## Headings

- DAL_ExecRouletteRisk — Roulette Execution Risk Model
-   Core state
-   Losing-side floor band
-   Downside floor break
-   Profit-active rule
-   Profit cluster then loss re-lock
-   Final behavior summary
-   Safety contract

## Concepts

- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/MQL_Native|MQL Native]]
- [[docs/evidence/nds_anatomy/6a11c75733b2_NDS_Anatomy|NDS Anatomy]]

## Related documents

- [[docs/mql_native/H0007_F1_MQL5_IMPLEMENTATION|H0007 / M0007 — F1 Adaptive Flag Counting MQL5 Implementation]] — `mql_native_docs`
- [[docs/mql_native/H0007_FLAG_COUNTING_F1_START_STRUCTURE|H0007 — Flag Counting / F1 Start Structure]] — `mql_native_docs`
- [[docs/evidence/m0001_excel_audit/ff999bc7279e_M0001_EXCEL_AUDIT_REPORT|M0001 Excel Audit Report]] — `mql_native_docs`
- [[docs/mql_native/M0001_FINAL_ONLY_WARMUP_AND_PRUNE|M0001 Final-Only Research Report, Warmup, and MQL Prune]] — `mql_native_docs`
- [[docs/mql_native/M0001_FULL_REVISIT_LOGIC|M0001 Full Revisit Logic]] — `mql_native_docs`
- [[docs/evidence/m0001_json_audit/2e8468dd6e0a_M0001_JSON_AUDIT_REPORT|M0001 JSON Audit Report]] — `mql_native_docs`
- [[docs/mql_native/M0001_LATEST_VISUAL_CAPS|M0001 Latest Visual Caps]] — `mql_native_docs`
- [[docs/mql_native/M0001_LOGRTV_RANDOM_NULL_COMPARISON|M0001 LogRTV Random Null Comparison]] — `mql_native_docs`
- [[docs/mql_native/M0001_PROJECT_REPORT_SYNC|M0001 Project Report Sync]] — `mql_native_docs`
- [[docs/mql_native/M0001_RTV_LOG_HILO|M0001 RTV — Log High/Low Volatility]] — `mql_native_docs`
- [[docs/mql_native/M0001_RTV_SUMMARY_TEXT|M0001 RTV Summary Comment and Text File]] — `mql_native_docs`
- [[docs/mql_native/M0001_UNBOUNDED_BACKTEST_DATA|M0001 Unbounded Backtest Data]] — `mql_native_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
