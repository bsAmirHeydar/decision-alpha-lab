# Conformal Intervals and Coverage Governance

Conformal calibration provides finite-sample empirical coverage under exchangeability assumptions. Calibration residuals must come from a dedicated calibration partition and may not be fit on final test. The interval artifact records alpha, calibration size, method, group key, residual hash, and limitations.

Supported modes are symmetric split conformal, asymmetric residual conformal, and Mondrian/group-conditional conformal where sample support is sufficient. Sparse groups fall back to global calibration or abstain according to the exact policy.

Coverage is evaluated globally, by side, symbol, session, regime, anatomy family, and treatment family. Mean coverage cannot hide a severe subgroup failure. Width, conditional coverage error, and tail misses are reported together.
