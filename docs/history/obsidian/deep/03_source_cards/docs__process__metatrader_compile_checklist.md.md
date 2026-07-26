
---
type: source_card
source_path: "docs/process/metatrader_compile_checklist.md"
source_ext: ".md"
source_size: 1470
empty: false
generated_at: 2026-07-06
concepts: ["Decision Node", "Execution / Risk", "MQL Native"]
entities: ["M0001", "M0004", "M0005"]
---

# Source Card — metatrader_compile_checklist.md

## Source

[[docs/process/metatrader_compile_checklist|docs/process/metatrader_compile_checklist.md]]

## Summary

Use this checklist after applying any MQL5 release. Close MetaEditor before applying the release. Apply ZIP or PATCH, not both. Run the release installer if one exists. Reopen MetaEditor. Compile shared include changes through the Experts that use them. Suggested order: M0001 / node and event Experts, M0004 / regime memory Experts, M0005 / directional memory Experts, Debug validators, Execution EAs. If compile fails, capture the full MetaEditor error list. Do not summarize from memory. A useful error report contains: file path, line number, column number, exact error text, whether the file is repo-level or terminal include-level. The repo include changed, but MetaEditor is reading an older terminal-level include. Fix: run the installer or manually copy the include tree. An enum name was assumed from memory and does not exist in the current project. Fix: inspect the actual enum definition

## Concepts

[[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]]

## Entities

M0001, M0004, M0005

## Headings

- MetaTrader Compile Checklist
  - Before compile
  - Compile order
  - Error handling
  - Frequent failure modes
    - Include mismatch
    - Enum mismatch
    - Function signature mismatch
    - Debug-only logic not promoted

## Related Source Documents

- [[docs/architecture|architecture.md]] — score `21`
- [[docs/debug/MAIN_ATOMIC_NO_SAMPLE_UNIFICATION|MAIN_ATOMIC_NO_SAMPLE_UNIFICATION.md]] — score `19`
- [[lab/03_experiments/EXP0003_mql_native_m0002/report|report.md]] — score `19`
- [[lab/03_experiments/EXP0002_mql_native_m0001/report|report.md]] — score `17`
- [[lab/05_validation/VAL_M0001_MQL_NATIVE/report|report.md]] — score `17`
- [[lab/03_experiments/EXP0004_mql_native_m0004/report|report.md]] — score `17`
- [[docs/mql_native/MODULE_MAP|MODULE_MAP.md]] — score `16`
- [[docs/debug/H4_FAST_ATOMIC_MAIN_REPORT|H4_FAST_ATOMIC_MAIN_REPORT.md]] — score `14`
- [[docs/mql_native/H0001_H0002_ALGORITHM_AND_HYPOTHESIS_README|H0001_H0002_ALGORITHM_AND_HYPOTHESIS_README.md]] — score `14`
- [[docs/mql_native/H0001_H0004_RESEARCH_LOCK|H0001_H0004_RESEARCH_LOCK.md]] — score `14`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
