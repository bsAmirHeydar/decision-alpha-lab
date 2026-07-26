# Quantile, Distributional, and Tail-Risk Learning

Expected value is insufficient when treatments have asymmetric payoff shapes. The distributional task estimates selected quantiles, probability of positive net return, probability of target first, probability of stop first, Value at Risk, and Conditional Value at Risk.

Quantile levels are ordered, fixed in the task contract, and included in output identity. Predictions must be monotone. Crossing quantiles trigger rejection or an explicitly versioned monotonic repair. Pinball loss is reported per quantile, not averaged away.

Tail summaries are computed from side-aware net outcomes after spread, commission, slippage, financing, and management path. A high mean with unacceptable CVaR can be rejected by the decision or capital layer.
