---
title: "UI System Architecture"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/ui/ARCHITECTURE.md"
source_ext: ".md"
category: "ui_docs"
source_size_bytes: "5000"
concepts:
  - "NDS Anatomy"
  - "Structural Nodes"
  - "Validation"
---


# UI System Architecture

**Source:** [[docs/ui/ARCHITECTURE|docs/ui/ARCHITECTURE.md]]

**Category:** `ui_docs`  
**Status:** ok  
**Size:** `5000` bytes

## خلاصه

Build a professional, extensible visual research terminal for Decision Alpha Lab while preserving strict separation between research logic and presentation logic. Responsibilities: render the visual lab terminal replay candles through time display overlays returned by the API synchronize chart selections with table selections expose filters, toggles, and inspectors call backend endpoints through typed clients Forbidden: calculating structural nodes calculating metric values deciding event validity mutating research results without explicit backend action Responsibilities: expose market data to the UI expose structural nodes to the UI expose metric runs and event rows to the UI expose experim

## Headings

- UI System Architecture
-   Objective
-   High-Level Architecture
-   Layer Responsibilities
-     1. Frontend — `apps/web`
-     2. API — `apps/api`
-     3. Research Lab — `lab/`
-     4. Cache Layer — `lab/cache_*`
-   UI Domain Model
-   Central UI Contract
-   Runtime Modes
-     Cache Mode

## Concepts

- [[docs/evidence/nds_anatomy/6a11c75733b2_NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Structural_Nodes|Structural Nodes]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[docs/architecture|System Architecture]] — `core_docs`
- [[docs/evidence/exp0002_mql_native_m0001_runtime/319a21879dae_report|EXP0002 — MQL-native M0001 Runtime]] — `experiment`
- [[lab/03_experiments/EXP0003_mql_native_m0002/report|EXP0003 — M0002 Reversal/Continuation Exit Volatility]] — `experiment`
- [[lab/03_experiments/EXP0004_mql_native_m0004/report|EXP0004 — MQL-native M0004 Branch Regime Clustering]] — `experiment`
- [[docs/evidence/val_m0001_mql_native/454e81f9f0b3_report|VAL_M0001_MQL_NATIVE]] — `validation`
- [[docs/evidence/val001/360462a17ab1_report|Report]] — `validation`
- [[docs/ui/README|Quant Lab UI Architecture]] — `ui_docs`
- [[docs/ui/ROADMAP|UI Implementation Roadmap]] — `ui_docs`
- [[docs/ui/VISUAL_REPLAY_PROTOCOL|Visual Replay Protocol]] — `ui_docs`
- [[docs/ui/VISUALIZATION_API|Visualization API Contract]] — `ui_docs`
- [[docs/evidence/exp0000_sample/58c8a635ff91_report|Report]] — `experiment`
- [[docs/evidence/exp0001_structural_highs_lows_importance/337872464ffa_report|Report]] — `experiment`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
