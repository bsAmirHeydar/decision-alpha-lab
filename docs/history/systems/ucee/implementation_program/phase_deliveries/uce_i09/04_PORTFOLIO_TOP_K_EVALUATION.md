# Portfolio-Relevant Top-K Evaluation

A ranker is useful only after portfolio constraints. Evaluation therefore has two layers. The first evaluates pure within-group ordering. The second applies a deterministic top-k allocator with risk budget, one-treatment-per-opportunity, symbol exposure, strategy exposure, correlation-group limits, and maximum concurrent positions.

Top-k utility is calculated after executable spread, commission, slippage, financing, stop reserve, and volume rounding inherited from UCE-I05. A ranker that improves NDCG but loses net utility after constraints is not promoted.

Reports must disclose k, skipped opportunities, rejected treatments, risk utilization, concentration, turnover, and the sensitivity of utility to k. The search phase may compare several k values, but UCE-I12 must correct for that search multiplicity.
