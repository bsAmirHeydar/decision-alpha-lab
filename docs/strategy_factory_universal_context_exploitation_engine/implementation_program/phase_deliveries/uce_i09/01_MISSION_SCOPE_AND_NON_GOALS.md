# Mission, Scope, and Non-Goals

The phase expands the learner from a binary trade/skip filter into task formulations that match how a trading context is exploited. A single opportunity can contain several treatments, several future horizons, several exit causes, and several admissible actions. The engine must expose those alternatives without allowing labels, masks, or future observations to leak backward.

## In scope

- Group-aware ranking of opportunities and treatments.
- Action-mask-safe treatment selection.
- Right-censored survival and competing-risk outputs.
- Quantile, conformal, tail-loss, and target-first/stop-first probabilities.
- Multi-task heads and sparse-regime fallback.
- Conservative offline policy comparison restricted to logged support.
- Exact trainer descriptors, schemas, lineage, deterministic fixtures, and MQL5 mirrors.

## Non-goals

This phase does not perform broad hyperparameter search, final anti-overfit promotion, deep sequence learning, or live order authority. Those belong to UCE-I10 through UCE-I14. Every output remains research evidence until UCE-I12 promotion and UCE-I14 runtime parity gates pass.
