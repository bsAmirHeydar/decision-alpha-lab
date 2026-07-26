# Support, Overlap, Propensity, and Abstention

Support governance is a first-class safety layer. For each action, the audit records count, effective sample size, minimum and maximum propensity, compatibility, and support state. The global audit records unseen actions, action-mask violations, overlap blockers, and warnings.

Propensities below the floor may be clipped for numerical stability, but the clipped count is preserved and excessive clipping blocks promotion. Effective sample size is reported because a large row count with tiny propensities can contain little usable evidence.

Abstention is a valid output. It is preferred to extrapolation. The runtime must preserve the distinction between selecting the baseline, abstaining from selection, and rejecting the entire decision due to invalid evidence.
