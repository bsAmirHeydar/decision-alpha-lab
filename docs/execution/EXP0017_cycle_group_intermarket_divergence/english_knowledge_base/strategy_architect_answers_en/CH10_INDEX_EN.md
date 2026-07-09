# EXP0017 Chapter 10 — Risk, Stop, Time Exit, and Outcome Doctrine

> English knowledge-base version of the Strategy Architect doctrine. This document preserves the base doctrine while making the project readable for English implementation, review, collaboration, and future modeling.

## Chapter Thesis

Risk is fixed in the base version, stop is absolute at the clean reference, and the initial target concept is time-based.

## English Documents In This Chapter

- [[CH10_INDEX_EN.md]]
- [[CH10_absolute_stop_and_fixed_risk_doctrine_EN.md]]
- [[CH10_glossary_and_language_EN.md]]
- [[CH10_hypothesis_register_EN.md]]
- [[CH10_research_translation_and_statistical_mission_EN.md]]
- [[CH10_risk_invalidation_and_time_exit_doctrine_EN.md]]
- [[CH10_time_target_and_dollar_outcome_doctrine_EN.md]]

## Locked Doctrine

- Base risk is fixed at 1% equity.
- Stop price is the clean symbol reference level.
- No quality-based risk adjustment exists before statistics.
- Cycle-end exit is the base time target, but later studies may add alternative targets.
- Dollar result is an important statistical outcome.

## Implementation Relevance

- Separate stop logic from model scoring.
- Record multiple outcome windows even if base exit remains cycle-end.
