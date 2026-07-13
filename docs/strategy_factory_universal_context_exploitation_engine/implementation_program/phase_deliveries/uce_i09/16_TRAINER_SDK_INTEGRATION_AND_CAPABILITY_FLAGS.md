# Trainer SDK Integration and Capability Flags

Five native trainer plugins implement the UCE-I07 lifecycle: pairwise ranking, direct outcome treatment utility, discrete hazard, empirical quantiles, and shared linear heads. Each declares exact task, view, target shape, censoring support, multi-output support, calibration capability, export format, and limitations.

The advanced catalog contains native and optional algorithms. Optional libraries never silently fall back to a different estimator. Missing dependencies produce a clean unavailable status and retained trial evidence.

Prediction width, output names, feature order, action order, horizon order, quantile order, and model-state hash are immutable. Serialization parity is required before an artifact can enter later search or promotion.
