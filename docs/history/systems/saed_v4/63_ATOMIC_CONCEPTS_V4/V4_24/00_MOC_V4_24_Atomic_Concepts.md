---
title: SAED V4-24 Atomic Concepts MOC
status: accepted-reference
version: 1.0.0
phase: SAED_V4_24
evidence_scope: local-deterministic-calibration-selective-control-reference
claim_ceiling: research-only-no-production-authority
tags: [saed-v4, v4-24, atomic-concepts, moc]
---
# SAED V4-24 Atomic Concepts

This map separates the non-negotiable scientific and authority invariants of conformal lower bounds, support-aware OOD, selective action control, retrospective coverage-risk analysis, abstention and drift containment. Each note is atomic so implementation, review and audit can cite one invariant without importing unrelated authority.

## Concepts
- [[001_Conformal_Coverage_Is_Marginal_Not_Universal]]
- [[002_Exchangeability_Is_an_Assumption_Not_a_Fact]]
- [[003_One_Sided_Bounds_Protect_Downside_Decisions]]
- [[004_Finite_Sample_Correction_Is_Mandatory]]
- [[005_Mondrian_Groups_Need_Minimum_Support]]
- [[006_Pooled_Fallback_Is_Safer_Than_Tiny_Groups]]
- [[007_Conformal_Quantiles_Are_Calibration_Artifacts]]
- [[008_Lower_Bounds_Must_Gate_Candidate_Value]]
- [[009_Realized_Outcomes_Cannot_Enter_Decisions]]
- [[010_Outcome_Mutation_Must_Preserve_Decisions]]
- [[011_OOD_Detection_Is_Not_a_Proof_of_Safety]]
- [[012_Robust_MAD_Limits_Scale_Sensitivity]]
- [[013_Nearest_Neighbors_Expose_Local_Novelty]]
- [[014_Support_Deficit_Is_an_OOD_Signal]]
- [[015_Composite_OOD_Scores_Need_Frozen_Weights]]
- [[016_Empirical_OOD_P_Values_Need_Calibration]]
- [[017_Missing_Features_Fail_Closed]]
- [[018_Low_OOD_P_Value_Means_Abstain]]
- [[019_Action_Masks_Precede_Confidence]]
- [[020_Support_Gates_Precede_Selection]]
- [[021_Skip_Is_the_Sovereign_Safe_Action]]
- [[022_Abstention_Is_a_Valid_Decision]]
- [[023_Coverage_Without_Risk_Is_Misleading]]
- [[024_Risk_Without_Coverage_Is_Incomplete]]
- [[025_Risk_Upper_Bounds_Gate_Feasibility]]
- [[026_AURC_Summarizes_a_Tradeoff_Not_Authority]]
- [[027_Threshold_Grids_Must_Be_Frozen]]
- [[028_Monotone_Envelopes_Prevent_Optimistic_Noise]]
- [[029_Target_Risk_Does_Not_Guarantee_Future_Risk]]
- [[030_Baseline_Preservation_Is_Non_Negotiable]]
- [[031_No_Feasible_Threshold_Means_Full_Abstention]]
- [[032_Drift_Can_Invalidate_Calibration]]
- [[033_PSI_Is_a_Diagnostic_Not_Causal_Evidence]]
- [[034_OOD_Rate_Drift_Requires_Containment]]
- [[035_Recalibration_Is_Not_Runtime_Mutation]]
- [[036_Calibration_Aging_Must_Be_Visible]]
- [[037_Cluster_Roles_Must_Stay_Separated]]
- [[038_Feature_Known_Time_Is_Part_of_Every_Record]]
- [[039_Outcome_Observed_Time_Is_Separate]]
- [[040_Future_Suffix_Access_Is_Forbidden]]
- [[041_Protected_Evidence_Exposure_Stays_Zero]]
- [[042_Hidden_Evaluation_Queries_Stay_Zero]]
- [[043_Every_Fit_Consumes_Budget]]
- [[044_Every_Bootstrap_Draw_Is_Ledgered]]
- [[045_Every_Selective_Evaluation_Is_Ledgered]]
- [[046_Budget_Exhaustion_Fails_Closed]]
- [[047_Unknown_Fields_Must_Fail]]
- [[048_Hash_Mismatches_Must_Fail]]
- [[049_Replay_Mismatches_Must_Fail]]
- [[050_Nonfinite_Features_Must_Fail]]
- [[051_Probability_Domain_Violations_Must_Fail]]
- [[052_Authority_Flags_Must_Fail]]
- [[053_Promotion_Belongs_to_UCEE]]
- [[054_Runtime_Compilation_Is_Forbidden]]
- [[055_Risk_Allocation_Is_Forbidden]]
- [[056_Order_Submission_Is_Forbidden]]
- [[057_Online_Learning_Is_Forbidden]]
- [[058_MQL5_Static_Is_Not_MetaEditor_Compile]]
- [[059_MetaEditor_Compile_Is_Not_Runtime_Parity]]
- [[060_Research_Calibration_Is_Not_Prospective_Evidence]]
- [[061_Synthetic_Coverage_Is_Not_Real_Coverage]]
- [[062_Conformal_Certificates_Are_Research_Evidence]]
- [[063_OOD_Certificates_Are_Research_Evidence]]
- [[064_Selective_Decisions_Are_Not_Production_Decisions]]
- [[065_V4_25_Owns_Continual_Meta_and_Transfer]]

## Boundary
All concepts are research-only and fail closed to `skip`. No concept grants promotion, runtime, risk allocation, execution or production authority.
