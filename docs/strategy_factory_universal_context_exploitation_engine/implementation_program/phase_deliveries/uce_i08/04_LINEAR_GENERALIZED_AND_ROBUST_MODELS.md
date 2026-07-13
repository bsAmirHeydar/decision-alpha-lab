# Linear, Generalized, Sparse, and Robust Models

The pack includes linear regression, ridge, lasso, elastic net, Huber regression, logistic regression, ridge classification, and linear margin models. Hyperparameters are bounded in descriptors and seeded where applicable. Features arrive through UCE-I06 train-only transforms; trainers may not fit scalers on calibration, threshold, OOF holdout, or final-test rows.

Linear models are the primary coefficient-stability reference. Fold-level coefficients, signs, regularization strength, convergence evidence, and calibration state are retained. Sparse models are not automatically preferred: unstable feature selection across folds is a warning. Robust regression is included for heavy-tailed utility labels but does not remove tail-sensitive economic evaluation.

Monotonicity claims must be explicit and enforced by the estimator. A prose statement that one feature should help is not equivalent to a constrained model.
