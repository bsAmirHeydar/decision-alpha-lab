---
title: "M0001 — Relative Territory Volatility (RTV)"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/evidence/m0001_relative_territory_volatility_rtv/9fec506c7ac3_M0001_relative_territory_volatility.md"
source_ext: ".md"
category: "core_component"
source_size_bytes: "9075"
entities:
  - "M0001"
concepts:
  - "Execution"
  - "NDS Anatomy"
  - "Structural Nodes"
---


# M0001 — Relative Territory Volatility (RTV)

**Source:** [[docs/evidence/m0001_relative_territory_volatility_rtv/9fec506c7ac3_M0001_relative_territory_volatility|docs/evidence/m0001_relative_territory_volatility_rtv/9fec506c7ac3_M0001_relative_territory_volatility.md]]

**Category:** `core_component`  
**Status:** ok  
**Size:** `9075` bytes

## خلاصه

Final Specification Frozen Design Document M0001 (Relative Territory Volatility) is a structural metric designed to quantify how price behaves when revisiting the territory of a structural node. The core question is: > Does price exhibit a different volatility regime when it returns to the vicinity of an important structural node? Instead of relying on classical volatility measures such as ATR or standard deviation, M0001 evaluates volatility through logarithmic candle movements within the context of structural node territories. OHLC data: time open high low close Nodes are supplied by: LRuleNodeDetector Only nodes satisfying: are considered. The entire metric is designed to behave exactly l

## Headings

- M0001 — Relative Territory Volatility (RTV)
-   Version
-   Status
- 1. Purpose
- 2. Inputs
-   2.1 Market Data
-   2.2 Structural Nodes
- 3. Design Philosophy
- 4. Live Market Simulation
- 5. Node States
-   TRACKING
-   ACTIVE EVENT

## Entities

`M0001`

## Concepts

- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/evidence/nds_anatomy/6a11c75733b2_NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Structural_Nodes|Structural Nodes]]

## Related documents

- [[docs/architecture|System Architecture]] — `core_docs`
- [[docs/atomic_live_research_contract|Atomic Live Research Contract]] — `core_docs`
- [[docs/debug/D0005_H5_NO_FUTURE_WALK_FORWARD_AUDIT|D0005 — H5 No-Future Walk-Forward Audit]] — `debug_docs`
- [[docs/debug/D0006_H5_LIVE_TOUCH_REPLAY_AUDIT|D0006 — H5 Live Touch Replay Audit]] — `debug_docs`
- [[docs/debug/D0009_H5_ATOMIC_NO_SAMPLE_REPLAY_AUDIT|D0009 H5 Atomic No-Sample Replay Audit]] — `debug_docs`
- [[docs/debug/E0006/ENTRY_QUALIFICATION_README|E0006 — Entry Qualification Logic]] — `debug_docs`
- [[docs/debug/E0006/EXIT_AND_RISK_README|E0006 — Exit, Stop, Spread, and Risk Logic]] — `debug_docs`
- [[docs/debug/E0006/INPUT_REFERENCE_README|E0006 — Input Reference]] — `debug_docs`
- [[docs/debug/E0006/MODULE_KERNEL_README|E0006 Modular Execution Kernel]] — `debug_docs`
- [[docs/debug/E0006/README|E0006 — Structural Execution Layer Overview]] — `debug_docs`
- [[docs/debug/E0006/REVISIT_ONLY_README|E0006 — Revisit-Only Entry Logic]] — `debug_docs`
- [[docs/debug/E0006_ALL_ZONE_TOUCH_LIMIT_README|E0006 — All-Zone Touch Limit Fixed-R Executor]] — `debug_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
