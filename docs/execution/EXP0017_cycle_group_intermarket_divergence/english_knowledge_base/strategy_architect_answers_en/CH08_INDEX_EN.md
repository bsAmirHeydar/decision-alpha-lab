# EXP0017 Chapter 08 — Candle Close Confirmation and Trade Permission

> English knowledge-base version of the Strategy Architect doctrine. This document preserves the base doctrine while making the project readable for English implementation, review, collaboration, and future modeling.

## Chapter Thesis

A divergence becomes confirmed and tradeable only after the active chart timeframe candle closes with asymmetry still valid.

## English Documents In This Chapter

- [[CH08_INDEX_EN.md]]
- [[CH08_candle_close_confirmation_and_trade_permission_EN.md]]
- [[CH08_glossary_and_language_EN.md]]
- [[CH08_hypothesis_register_EN.md]]
- [[CH08_invalidation_and_simultaneous_hunt_doctrine_EN.md]]
- [[CH08_research_translation_and_statistical_mission_EN.md]]
- [[CH08_signal_visibility_and_equality_EN.md]]

## Locked Doctrine

- Hunt can happen intrabar; confirmation waits for candle close.
- If both symbols have hunted by confirmation time, no trade exists.
- Temporal close is not a price filter.
- All confirmed signals should remain visible.

## Implementation Relevance

- The EA must use closed candle events as the final signal boundary.
- Do not execute on intrabar potential states.
