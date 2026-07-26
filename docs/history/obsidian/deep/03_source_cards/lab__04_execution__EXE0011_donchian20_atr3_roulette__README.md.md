
---
type: source_card
source_path: "lab/04_execution/EXE0011_donchian20_atr3_roulette/README.md"
source_ext: ".md"
source_size: 6078
empty: false
generated_at: 2026-07-06
concepts: ["Convexity / Optionality", "Execution / Risk", "Known-Time Causality", "MQL Native", "Python Brain", "Rally"]
entities: ["E0011", "EXE0011"]
---

# Source Card — README.md

## Source

[[lab/04_execution/EXE0011_donchian20_atr3_roulette/README|lab/04_execution/EXE0011_donchian20_atr3_roulette/README.md]]

## Summary

`E0011_Donchian20Atr3Roulette` is a pure MQL5 execution expert for a simple breakout continuation model: entry from a fresh Donchian 20 breakout stop-loss at 3 ATR take-profit at 2R money risk from the reusable Roulette risk module No Python, no external execution scripts, and no structural-regime dependency are used. The expert does not evaluate on every tick. It evaluates once when a new `InpSignalTimeframe` candle opens. Therefore the signal candle is always the last closed candle, `shift 1`. The Donchian channel is calculated causally. For a period of 20: signal candle = `shift 1` Donchian range for the signal = highs/lows of `shift 2` through `shift 21` previous candle = `shift 2` previous Donchian range = highs/lows of `shift 3` through `shift 22` This means the last closed candle freshly broke above the previous 20-candle Donchian upper band. This means the last closed candle fres

## Concepts

[[docs/obsidian_deep/02_concepts/Convexity____Optionality|Convexity / Optionality]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Known-Time_Causality|Known-Time Causality]], [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]], [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]], [[docs/obsidian_deep/02_concepts/Rally|Rally]]

## Entities

E0011, EXE0011

## Headings

- EXE0011 — Donchian 20 ATR3 Roulette Execution
  - Purpose
  - Default Inputs
  - Execution Clock
  - Donchian Breakout Rule
    - Buy
    - Sell
  - Stop-Loss
    - Buy Stop
    - Sell Stop
  - Take-Profit
    - Buy

## Related Source Documents

- [[lab/03_experiments/EXP0012_distributional_cluster_miner/README|README.md]] — score `13`
- [[docs/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI_NATIVE_EXECUTION_ROADMAP_FA.md]] — score `10`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE11_ENTRY_BRIDGE_READINESS|FLAG_COUNTING_LEVEL_19_PHASE11_ENTRY_BRIDGE_READINESS.md]] — score `10`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE12_EXTREME_CANDIDATE_MAP|FLAG_COUNTING_LEVEL_19_PHASE12_EXTREME_CANDIDATE_MAP.md]] — score `10`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE4_HOOK_VIEW_PROJECTION|FLAG_COUNTING_LEVEL_19_PHASE4_HOOK_VIEW_PROJECTION.md]] — score `10`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE7_LEFT_PANEL_SECTION_TOGGLES|FLAG_COUNTING_LEVEL_19_PHASE7_LEFT_PANEL_SECTION_TOGGLES.md]] — score `10`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_STATE_GATE_IMPLEMENTATION_PLAN|FLAG_COUNTING_LEVEL_19_STATE_GATE_IMPLEMENTATION_PLAN.md]] — score `10`
- [[docs/nds_hook_architecture/07_mql5_integration_contract|07_mql5_integration_contract.md]] — score `10`
- [[docs/nds_hook_architecture/15_phase08_audit_csv_reconciliation_implementation|15_phase08_audit_csv_reconciliation_implementation.md]] — score `10`
- [[docs/nds_hook_architecture/16_phase09_visual_smoke_test_harness_implementation|16_phase09_visual_smoke_test_harness_implementation.md]] — score `10`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
