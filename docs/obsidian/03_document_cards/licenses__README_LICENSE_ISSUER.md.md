---
title: "Offline License Issuer Folder"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "licenses/README_LICENSE_ISSUER.md"
source_ext: ".md"
category: "license_docs"
source_size_bytes: "2983"
concepts:
  - "Execution"
  - "F-Counting"
  - "Licensing"
  - "NDS Anatomy"
  - "Validation"
---


# Offline License Issuer Folder

**Source:** [[licenses/README_LICENSE_ISSUER|licenses/README_LICENSE_ISSUER.md]]

**Category:** `license_docs`  
**Status:** ok  
**Size:** `2983` bytes

## خلاصه

This folder is the private issuer-side archive for FlagCounting Phoenix offline licenses. Keep this folder private. Do not ship it to recipients and do not commit generated user folders. Only these guide files should remain in the repository: Each license issuance creates one user folder next to this guide: The `.gitignore` in this folder ignores generated records by default. Run from the repository root: The tool prints the recipient inputs and also writes them under: Use this only when the server name is unstable or the user legitimately needs multiple server names for the same account: By default the tool finds the next available user number and creates `user0001`, `user0002`, and so on.

## Headings

- Offline License Issuer Folder
-   What stays in git
-   What is generated locally
-   Create a license bound to account and broker server
-   Create a license without server binding
-   Force a user code
-   Files to send to the recipient
-   Files to keep private
-   Overwrite an existing user folder

## Concepts

- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/F-Counting|F-Counting]]
- [[docs/obsidian/04_concepts/Licensing|Licensing]]
- [[docs/obsidian/04_concepts/NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[docs/debug/MARKET_LANGUAGE/README|DAL Market Language — Nodes, Cycles, Hooks, Rallies, Flags, 123 Flags, and Open 1/2s]] — `debug_docs`
- [[docs/flag_counting/README|Flag Counting Documentation]] — `flag_counting_docs`
- [[docs/execution/EXP0016_intermarket_divergence_execution/README|EXP0016 Intermarket Divergence Execution Documentation]] — `execution_docs`
- [[docs/experience_capture/questions/README|Quant Lab Experience Capture Questionnaire]] — `experience_capture_docs`
- [[docs/flag_counting/engineering_pack_v5/04_algorithms/README|04 Algorithms README]] — `flag_counting_docs`
- [[docs/flag_counting/engineering_pack_v5/README|Flag Counting Engineering Pack V5]] — `flag_counting_docs`
- [[docs/flag_counting/implementation_ladder_v1/README|Phoenix Flag Counting Implementation Ladder V1]] — `flag_counting_docs`
- [[docs/nds_hook_architecture/README|NDS Hook Architecture — Design Pack]] — `nds_hook_architecture_docs`
- [[lab/03_experiments/EXP0013_astro_feature_store/README|EXP0013 - Astro Feature Store]] — `experiment`
- [[lab/03_experiments/EXP0016_astro_meta_learner/README|EXP0016 Astro Meta Learner]] — `experiment`
- [[lab/03_experiments/EXP_flag_counting/README|EXP Flag Counting]] — `experiment`
- [[lab/03_experiments/EXP_flag_counting/validation_cases/README|Phoenix Flag Counting Validation Cases]] — `experiment`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
