---
type: training_plan
id: ZONE-RANKING-MODEL
status: draft
language: english
---

# Zone Ranking Model

The first ML model should rank zones instead of predicting direct direction.

## Objective

```text
Rank zones by future convexity and expansion quality.
```

## Suggested Target

```text
future_mfe_mae_ratio
or
top_decile_tail_expansion
```

## Evaluation

- Top-decile MFE/MAE improvement.
- Dead-zone removal rate.
- Tail capture ratio.
- Average MAE reduction.
- Path smoothness improvement.

