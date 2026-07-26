
---
type: source_card
source_path: "docs/releases/legacy_migration/general/dc619e167a21_README_LICENSE_ISSUER.md"
source_ext: ".md"
source_size: 2983
empty: false
generated_at: 2026-07-06
concepts: ["Decision Node", "Execution / Risk", "Licensing", "Python Brain", "UI / React", "Validation / Audit"]
entities: []
---

# Source Card — README_LICENSE_ISSUER.md

## Source

[[docs/releases/legacy_migration/general/dc619e167a21_README_LICENSE_ISSUER|docs/releases/legacy_migration/general/dc619e167a21_README_LICENSE_ISSUER.md]]

## Summary

This folder is the private issuer-side archive for FlagCounting Phoenix offline licenses. Keep this folder private. Do not ship it to recipients and do not commit generated user folders. Only these guide files should remain in the repository: Each license issuance creates one user folder next to this guide: The `.gitignore` in this folder ignores generated records by default. Run from the repository root: The tool prints the recipient inputs and also writes them under: Use this only when the server name is unstable or the user legitimately needs multiple server names for the same account: By default the tool finds the next available user number and creates `user0001`, `user0002`, and so on. To force a specific code: Send only the six values from: These are the only values the user needs to paste into MT5 Inputs: Keep these private: Use `--overwrite` only when you intentionally want to re

## Concepts

[[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Licensing|Licensing]], [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]

## Entities

—

## Headings

- Offline License Issuer Folder
  - What stays in git
  - What is generated locally
  - Create a license bound to account and broker server
  - Create a license without server binding
  - Force a user code
  - Files to send to the recipient
  - Files to keep private
  - Overwrite an existing user folder

## Related Source Documents

- [[docs/flag_counting/README|README.md]] — score `20`
- [[docs/debug/MARKET_LANGUAGE/README|README.md]] — score `18`
- [[docs/flag_counting/implementation_ladder_v1/README|README.md]] — score `18`
- [[docs/nds_hook_architecture/README|README.md]] — score `18`
- [[docs/ui/README|README.md]] — score `18`
- [[lab/03_experiments/EXP_flag_counting/validation_cases/README|README.md]] — score `18`
- [[README|README.md]] — score `18`
- [[lab/03_experiments/EXP0013_astro_feature_store/README|README.md]] — score `18`
- [[lab/03_experiments/EXP0016_astro_meta_learner/README|README.md]] — score `18`
- [[mql5/Experts/AstroExecution/README|README.md]] — score `18`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
