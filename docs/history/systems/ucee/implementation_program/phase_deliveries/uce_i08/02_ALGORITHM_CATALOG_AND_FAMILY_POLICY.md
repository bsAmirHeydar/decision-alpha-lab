# Algorithm Catalog and Family Policy

The exact-version catalog contains baseline, linear, tree, boosting, kernel, neighborhood, probabilistic, additive, and optional external families. Every descriptor records task support, probability semantics, sample-weight support, missingness behavior, multiclass capability, determinism, portability, export formats, dependency requirements, bounded hyperparameters, tags, and limitations.

Registration is exact-version and immutable after orchestration starts. A behavior-changing default is part of descriptor identity. Silent substitution is forbidden: when CatBoost is unavailable, the system records `skipped_unavailable`; it never executes a random forest under the CatBoost identity.

The mandatory comparison set is a naive base-rate model, frozen manual policy, regularized linear model, and tree model. Random forest is the default nonlinear tabular reference. Optional boosters enrich comparison but cannot replace mandatory families.
