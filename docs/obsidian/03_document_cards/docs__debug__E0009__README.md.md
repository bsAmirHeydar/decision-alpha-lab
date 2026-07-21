---
title: "E0009 — Reversal Macro / Latest Setup / Hook Executor"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/debug/E0009/README.md"
source_ext: ".md"
category: "debug_docs"
source_size_bytes: "2214"
entities:
  - "E0009"
concepts:
  - "Execution"
  - "Hook"
  - "NDS Anatomy"
  - "Structural Nodes"
---


# E0009 — Reversal Macro / Latest Setup / Hook Executor

**Source:** [[docs/debug/E0009/README|docs/debug/E0009/README.md]]

**Category:** `debug_docs`  
**Status:** ok  
**Size:** `2214` bytes

## خلاصه

Release 112 aligns E0009 with the intended reversal logic. Default: Index convention: Macro scans backwards from live and finds the nearest valid same-type chain. This is reversal logic: rising highs define a sell-reversal context; falling lows define a buy-reversal context. Default: Setup does **not** scan older chains. It only checks the latest N highs and latest N lows. If `InpRequireSetupAgreesWithMacro=true`, macro and setup must point to the same trade direction. Default: `InpMaxHookCandidatesPerBar = 0` means scan all eligible hooks. Entry is a limit touch on the hook extreme: `InpRejectHuntedM1Hook=true` means consumed/hunted hooks are not allowed back into the game. Default: The fil

## Headings

- E0009 — Reversal Macro / Latest Setup / Hook Executor
-   Layer 1 — Macro mode
-   Layer 2 — Middle setup
-   Layer 3 — M1 hook entry
-   Layer 4 — Micro filter
-   Layer 5 — Exit

## Entities

`E0009`

## Concepts

- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/Hook|Hook]]
- [[docs/evidence/nds_anatomy/6a11c75733b2_NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Structural_Nodes|Structural Nodes]]

## Related documents

- [[lab/03_validation/VAL0026_e9_htf_123_m1_hook_reversal/README|VAL0026 — E0009 Release 112 Validation]] — `validation`
- [[docs/debug/E0007/README|E0007 — Purple Source Extreme Executor Template]] — `debug_docs`
- [[docs/debug/E0008/README|E0008 — MTF Purple Extreme Executor]] — `debug_docs`
- [[docs/debug/MARKET_LANGUAGE/README|DAL Market Language — Nodes, Cycles, Hooks, Rallies, Flags, 123 Flags, and Open 1/2s]] — `debug_docs`
- [[docs/experience_capture/questions/README|Quant Lab Experience Capture Questionnaire]] — `experience_capture_docs`
- [[docs/flag_counting/README|Flag Counting Documentation]] — `flag_counting_docs`
- [[docs/ai_execution/README|AI Execution Docs]] — `ai_execution_docs`
- [[docs/debug/E0006/README|E0006 — Structural Execution Layer Overview]] — `debug_docs`
- [[docs/execution/README|Decision Alpha Lab — Execution]] — `execution_docs`
- [[docs/experience_capture/questions/remaining_v2/sections/03_entry_families/README|Entry Families Beyond Extreme]] — `experience_capture_docs`
- [[docs/flag_counting/engineering_pack_v5/04_algorithms/README|04 Algorithms README]] — `flag_counting_docs`
- [[docs/flag_counting/engineering_pack_v5/README|Flag Counting Engineering Pack V5]] — `flag_counting_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
