# Interpretability and Explanation Lineage

Explanations are versioned artifacts, not screenshots. Each record binds feature, index, method, magnitude, variability, direction, fold, role, model state, and rank. Native coefficients and impurity values are supplemented by permutation, ablation, partial dependence, ALE, or SHAP-compatible hooks.

Final-test explanations are audit-only. They cannot select features, models, thresholds, treatment styles, or hyperparameters. The engine rejects a final-test explanation request marked `for_selection=true`.

Coefficient stability is aggregated across folds. Feature importance is predictive evidence, not causal evidence. Correlated features, feature engineering, missingness, and treatment-policy selection can alter attribution.
