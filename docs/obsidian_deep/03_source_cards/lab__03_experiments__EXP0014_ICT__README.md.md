
---
type: source_card
source_path: "lab/03_experiments/EXP0014_ICT/README.md"
source_ext: ".md"
source_size: 3341
empty: false
generated_at: 2026-07-06
concepts: ["Convexity / Optionality", "Decision Node", "Execution / Risk", "MQL Native", "Python Brain", "Validation / Audit", "Zone / RTV"]
entities: ["EXP0014"]
---

# Source Card — README.md

## Source

[[lab/03_experiments/EXP0014_ICT/README|lab/03_experiments/EXP0014_ICT/README.md]]

## Summary

This experiment is a deterministic, bar-based ICT module scaffold for Decision Alpha Lab. It does **not** run on every tick. The default expert runs once on init, scans historical bars, writes CSV journals, and removes itself. Source: `mql5/Include/ICT/DAL_ICTSweepDetector.mqh` Uses the existing DAL structural node engine: `DAL_DetectConfirmedStructuralNodes` L-rule confirmed highs/lows active-from index/time is respected to avoid future leakage A high node sweep creates a bearish setup context. A low node sweep creates a bullish setup context. Modes: `ICT_SWEEP_TOUCH`: price reaches the configured node zone touch depth. `ICT_SWEEP_HUNT`: price pierces the node zone and closes back through the node level. Zone model: node zone = `[node_price - zone_half_width, node_price + zone_half_width]` touch percent decides how deep into the zone price must travel. Source: `mql5/Include/ICT/DAL_ICTF

## Concepts

[[docs/obsidian_deep/02_concepts/Convexity____Optionality|Convexity / Optionality]], [[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]], [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

EXP0014

## Headings

- EXP0014 — ICT Sweep / FVG / IFVG / CISD Execution Lab
  - Core modules
    - 1. L-node sweep
    - 2. FVG / IFVG
    - 3. CISD
    - 4. Execution model
  - Default expert
  - Output
  - Research warning

## Related Source Documents

- [[docs/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI_NATIVE_EXECUTION_ROADMAP_FA.md]] — score `14`
- [[docs/flag_counting/FLAG_COUNTING_CURRENT_CANON|FLAG_COUNTING_CURRENT_CANON.md]] — score `14`
- [[docs/flag_counting/implementation_ladder_v1/15_MODULE_INTERFACE_CONTRACTS|15_MODULE_INTERFACE_CONTRACTS.md]] — score `14`
- [[docs/flag_counting/implementation_ladder_v1/16_IMPLEMENTATION_ORDER_AND_ACCEPTANCE_MATRIX|16_IMPLEMENTATION_ORDER_AND_ACCEPTANCE_MATRIX.md]] — score `14`
- [[docs/flag_counting/README|README.md]] — score `14`
- [[docs/M0001_EVENT_BRIDGE_ARCHITECTURE|M0001_EVENT_BRIDGE_ARCHITECTURE.md]] — score `14`
- [[docs/mql_native/M0001_CANDLE_GATED_RUNTIME|M0001_CANDLE_GATED_RUNTIME.md]] — score `14`
- [[docs/mql_native/M0001_PROFESSIONAL_VALIDATION_METRICS|M0001_PROFESSIONAL_VALIDATION_METRICS.md]] — score `14`
- [[docs/mql_native/MODULE_MAP|MODULE_MAP.md]] — score `14`
- [[mql5/Include/FlagCountingPhoenix/README_FlagCountingPhoenix|README_FlagCountingPhoenix.md]] — score `14`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
