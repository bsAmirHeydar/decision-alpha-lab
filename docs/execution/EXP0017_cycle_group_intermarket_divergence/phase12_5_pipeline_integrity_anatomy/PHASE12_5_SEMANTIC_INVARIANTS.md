# Phase 12.5 Semantic Invariants

Schema correctness does not guarantee meaning. Phase 12.5 therefore checks domain invariants.

## Direction and side

- BUY divergence is low-side anatomy.
- SELL divergence is high-side anatomy.

## Market roles

- `hunter_symbol != clean_symbol`.
- The clean symbol remains the studied execution symbol.
- Role labels must survive from outcome to dataset and predictions.

## Risk geometry

- A COMPLETE outcome requires `stop_points > 0`.
- A model-ready sample requires `stop_points > 0`.
- Zero-risk rows remain auditable but cannot enter model-ready populations.

## Labels

- `WIN` implies `label_binary_win = 1`.
- `LOSS` and `FLAT` imply `label_binary_win = 0`.
- positive `actual_r` implies `actual_win = 1`.
- negative `actual_r` implies `actual_loss = 1`.
- win and loss flags cannot both be true.

## Why these are hard checks

A model trained on semantically contradictory rows can look statistically valid while learning a corrupted target. Phase 12.5 blocks that failure mode before model comparison.
