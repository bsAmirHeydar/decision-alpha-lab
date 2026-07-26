# Baselines, Manual Setups, and Null Models

Seven dependency-free trainers implement never-trade, always-trade, train-prevalence, frozen manual threshold, single-feature threshold search, rate-matched null, and random-score null behavior. Their state is canonical JSON and their output is deterministic under exact row identity and seed.

The manual policy baseline represents the trader's explicit exploitation hypothesis using the same dataset, folds, economics, outcome cube, and labels as AI. It prevents an AI result from being celebrated when it merely rediscovers or underperforms the personal setup. Manual parameters must be frozen before hidden-test access.

Rate-matched null controls trade frequency. Random-score null controls arbitrary ranking. Never-trade and always-trade expose base-rate and cost asymmetry. Single-feature search reveals whether apparent complexity is supported by more than one dominant feature.
