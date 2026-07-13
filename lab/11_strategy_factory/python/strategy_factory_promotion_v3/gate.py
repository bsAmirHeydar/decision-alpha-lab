"""Unified non-compensatory UCE-I12 promotion decision."""
from __future__ import annotations
from typing import Sequence
from .canonical import canonical_sha256, stable_id
from .contracts import CalibrationReport, EvidenceBundle, ModelRiskScorecard, MultiplicityReport, NullControlResult, PromotionDecision, PromotionPolicy, ProspectiveChallengeFreeze, SelectionUniverse, StressResult, TestEvidence, UncertaintyReport
from .enums import DecisionRole, EvidenceStatus, GateOutcome, NullKind, TrialDisposition
from .evidence import verify_bundle
from .errors import PromotionError
from .nulls import mandatory_null_coverage

def decide(*, candidate_key:str, role:DecisionRole, universe:SelectionUniverse, policy:PromotionPolicy, scorecard:ModelRiskScorecard, uncertainty:UncertaintyReport, multiplicity:MultiplicityReport, pbo:float, deflated_probability:float, reality_check_p:float, null_results:Sequence[NullControlResult], stress_results:Sequence[StressResult], calibration:CalibrationReport, prospective_freeze:ProspectiveChallengeFreeze, evidence_bundle:EvidenceBundle, signing_secret:bytes, extra_evidence:Sequence[TestEvidence]=())->PromotionDecision:
    blockers=list(scorecard.critical_blockers); challenges=list(scorecard.high_risks)
    if uncertainty.effective_sample_size<policy.minimum_effective_sample_size: blockers.append("effective_sample_size_below_policy")
    if multiplicity.total_choice_count!=len(universe.trials): blockers.append("multiplicity_universe_mismatch")
    if pbo>policy.maximum_pbo: blockers.append("pbo_above_policy")
    if deflated_probability<policy.minimum_deflated_probability: blockers.append("deflated_probability_below_policy")
    if reality_check_p>policy.maximum_reality_check_p: blockers.append("reality_check_not_significant")
    null_coverage=mandatory_null_coverage(null_results,policy.mandatory_nulls)
    if not null_coverage["passed"]: blockers.extend(f"mandatory_null_{x}" for x in null_coverage["missing"]+null_coverage["failed"])
    failed_stress=[r.kind.value for r in stress_results if r.status is EvidenceStatus.FAIL or r.relative_retention<policy.minimum_stress_retention]
    if failed_stress: blockers.extend(f"stress_failed:{x}" for x in failed_stress)
    if calibration.expected_calibration_error>policy.maximum_ece: challenges.append("calibration_ece_above_policy")
    if abs(calibration.conformal_coverage-calibration.target_coverage)>policy.coverage_tolerance: challenges.append("conformal_coverage_outside_tolerance")
    if not prospective_freeze.frozen_before_observation: blockers.append("prospective_challenge_not_frozen")
    overrides=[t.trial_id for t in universe.trials if t.disposition is TrialDisposition.MANUAL_OVERRIDE]
    if overrides and not policy.allow_manual_override_to_promote: blockers.append("manual_override_present")
    signed=verify_bundle(evidence_bundle,signing_secret)
    if not signed: blockers.append("evidence_signature_invalid")
    if evidence_bundle.universe_hash!=universe.universe_hash or evidence_bundle.policy_hash!=policy.policy_hash: blockers.append("evidence_bundle_identity_mismatch")
    if scorecard.weighted_score<policy.minimum_score: challenges.append("model_risk_score_below_promotion_threshold")
    blockers=sorted(set(blockers)); challenges=sorted(set(challenges))
    outcome=GateOutcome.REJECT if blockers else (GateOutcome.CHALLENGE if challenges else GateOutcome.PROMOTE)
    payload={"candidate":candidate_key,"role":role,"outcome":outcome,"policy":policy.policy_hash,"universe":universe.universe_hash,"scorecard":scorecard.evidence_hash,"bundle":evidence_bundle.bundle_hash,"blockers":blockers,"challenges":challenges,"freeze":prospective_freeze.freeze_hash}
    return PromotionDecision(decision_id=stable_id("promotion",payload),candidate_key=candidate_key,role=role,outcome=outcome,policy_hash=policy.policy_hash,universe_hash=universe.universe_hash,scorecard_hash=scorecard.evidence_hash,evidence_bundle_hash=evidence_bundle.bundle_hash,blockers=tuple(blockers),challenges=tuple(challenges),residual_risks=scorecard.residual_risks,prospective_freeze_hash=prospective_freeze.freeze_hash,signed=signed)
