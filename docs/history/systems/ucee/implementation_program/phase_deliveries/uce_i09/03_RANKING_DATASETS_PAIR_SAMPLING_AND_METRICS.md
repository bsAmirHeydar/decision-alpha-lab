# Ranking Datasets, Pair Sampling, and Metrics

Ranking rows are never treated as independent global examples. Each row belongs to a declared ranking group, normally an opportunity timestamp, decision batch, portfolio rebalance point, or anatomy cluster. Comparisons are generated only inside that group.

The native pair builder is deterministic: rows are sorted by stable row identity, ties below the configured utility gap are omitted, pair weights incorporate sample weight and utility separation, and a bounded pair count prevents quadratic explosions. The pair identity includes group, preferred row, other row, and weight.

Required metrics include pairwise accuracy, NDCG@k, MAP@k, and top-k net utility. NDCG answers whether the best alternatives rise to the top; top-k utility answers whether that ordering survives economic selection. Group counts, pair counts, weights, and missing-group failures are preserved in the report.

Negative gates reject blank ranking groups, cross-group pairs, zero utility gaps, duplicate row IDs, and evaluations that flatten all groups into one global order.
