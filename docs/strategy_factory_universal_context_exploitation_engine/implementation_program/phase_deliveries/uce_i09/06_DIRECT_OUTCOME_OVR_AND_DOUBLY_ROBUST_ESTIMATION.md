# Direct Outcome, One-vs-Rest, and Doubly Robust Estimation

Direct outcome modeling estimates expected net utility conditional on context and action. One-vs-rest models create one utility model per action. Both require fold-local fitting and action-level support disclosure.

Doubly robust estimation combines an outcome model with inverse propensity correction. It is only valid when logged propensities are available, action overlap is sufficient, and propensity clipping is disclosed. The report contains estimated value, standard error, effective sample size, clipped count, and the support-audit identity.

Doubly robust is not a license to extrapolate. If an action is unseen, masked, or below support minimum, the selector must abstain or return the baseline. Propensity models trained from the same data must be out-of-fold and separately versioned.
