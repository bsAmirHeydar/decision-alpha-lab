# EXP0017 EN CH16 — Statistical Model and Decision Support

## Thesis

The model is a historical statistical observer and quality scorer, not an entry/exit authority.

## Doctrine

- The model analyzes past confirmed signals.
- It can evaluate CG type, CG position, win rate, expectancy, pip outcome, and normalized pip outcome.
- It does not alter entries, exits, or strategy rules.
- One unified model should analyze all CGs while preserving separable family tags.

## Fields

- `model_feature_set`
- `quality_score`
- `winrate_rank`
- `expectancy_rank`
- `historical_only_flag`

## Implementation Note

- Prepare model-ready datasets from ledger fields.
- Keep model output descriptive until rule promotion.
