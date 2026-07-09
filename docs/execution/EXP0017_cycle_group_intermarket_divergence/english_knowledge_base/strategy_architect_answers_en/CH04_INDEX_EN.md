# EXP0017 Chapter 04 — Reference Scope and Same-Day Cycle Memory

> English knowledge-base version of the Strategy Architect doctrine. This document preserves the base doctrine while making the project readable for English implementation, review, collaboration, and future modeling.

## Chapter Thesis

All previous cycles from the same New York trading day are valid reference candidates until invalidated or day-expired.

## English Documents In This Chapter

- [[CH04_INDEX_EN.md]]
- [[CH04_glossary_and_language_EN.md]]
- [[CH04_hypothesis_register_EN.md]]
- [[CH04_reference_family_taxonomy_EN.md]]
- [[CH04_reference_scope_and_same_day_cycle_memory_EN.md]]
- [[CH04_research_translation_and_statistical_mission_EN.md]]

## Locked Doctrine

- Reference candidates are the high and low of previous cycles in the same CG and same trading day.
- No previous-day reference is used for live decision.
- No reference hierarchy is assumed before statistics.
- A reference becomes invalid for divergence only when the asymmetry is removed by double hunt.

## Implementation Relevance

- The reference field must store all previous same-day cycle highs/lows.
- The engine must not use yesterday’s references for live signals.
