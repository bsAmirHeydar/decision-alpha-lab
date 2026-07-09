# EXP0017 Chapter 03 — Hunt Doctrine and Reference Validity

> English knowledge-base version of the Strategy Architect doctrine. This document preserves the base doctrine while making the project readable for English implementation, review, collaboration, and future modeling.

## Chapter Thesis

A hunt is a high/low touch or break of a reference level; close beyond the level is not required.

## English Documents In This Chapter

- [[CH03_INDEX_EN.md]]
- [[CH03_glossary_and_language_EN.md]]
- [[CH03_hunt_false_breakout_and_reference_validity_EN.md]]
- [[CH03_hypothesis_register_EN.md]]
- [[CH03_reference_lifecycle_and_invalidation_EN.md]]
- [[CH03_research_translation_and_statistical_mission_EN.md]]

## Locked Doctrine

- High hunt: current high >= reference high.
- Low hunt: current low <= reference low.
- Equality counts as a hunt.
- Close beyond the level is not required.
- If both symbols hunt their corresponding references, divergence is invalid.

## Implementation Relevance

- Use OHLC high/low data, not close-only logic.
- Separate intrabar hunt occurrence from final close confirmation.
