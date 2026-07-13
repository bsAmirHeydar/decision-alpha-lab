# Survival, Censoring, and Time Calibration

Trading outcomes are often censored: the observation window can end before stop or target, an order can expire, or a data gap can terminate evidence. Treating these rows as ordinary negatives creates bias. UCE-I09 therefore carries duration, event indicator, cause, weight, and known-time explicitly.

The native discrete-hazard model estimates interval hazards and produces a monotone survival curve. Optional Cox, accelerated-failure-time, survival-forest, and survival-boosting adapters are catalogued but must report dependency and assumption status.

Evaluation uses Harrell-style concordance for comparable pairs, integrated Brier score across declared horizons, and time-dependent calibration. Reports disclose event count, censored count, comparable pairs, horizon grid, and sparse-horizon warnings.
