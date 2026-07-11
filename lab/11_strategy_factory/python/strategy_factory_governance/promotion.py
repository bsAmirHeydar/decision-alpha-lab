from __future__ import annotations
from .models import *
from .enums import GateStatus, PromotionVerdict
from .hashing import cfloat

def _gate(gate_id: str, passed: bool, observed: str, required: str,
          evidence_hash: str, fail_reason: str) -> PromotionGateResult:
    return PromotionGateResult(gate_id, GateStatus.PASS if passed else GateStatus.FAIL,
                               observed, required, "PASS" if passed else fail_reason,
                               evidence_hash).with_hash()

def evaluate_promotion(evidence: ModelEvidenceBundle, scope: RegistryScope,
                       policy: PromotionPolicy, measurements: PromotionMeasurements,
                       *, evaluated_at_utc_msc: int, evaluator_id: str) -> PromotionEvaluation:
    evidence.validate(); scope.validate(); policy.validate(); measurements.validate()
    if evidence.feature_schema_hash != scope.feature_schema_hash:
        raise ValueError("feature schema does not match registry scope")
    if evidence.label_contract_hash != scope.label_contract_hash:
        raise ValueError("label contract does not match registry scope")
    ehash=evidence.bundle_hash or evidence.with_hash().bundle_hash
    gates=[]
    gates.append(_gate("phase12_acceptance", (not policy.require_phase12_acceptance) or measurements.phase12_accepted,
                       str(measurements.phase12_accepted).lower(), "true" if policy.require_phase12_acceptance else "optional",
                       ehash, "PHASE12_REJECTED"))
    gates.append(_gate("test_oos_only", (not policy.require_test_oos_only) or measurements.test_oos_only,
                       str(measurements.test_oos_only).lower(), "true" if policy.require_test_oos_only else "optional",
                       evidence.prediction_rowset_hash, "NON_OOS_PREDICTIONS"))
    gates.append(_gate("test_sample_count", measurements.test_sample_count >= policy.min_test_samples,
                       str(measurements.test_sample_count), str(policy.min_test_samples),
                       evidence.prediction_rowset_hash, "INSUFFICIENT_TEST_SAMPLE"))
    gates.append(_gate("validation_score", measurements.validation_score >= policy.min_validation_score,
                       cfloat(measurements.validation_score), cfloat(policy.min_validation_score),
                       evidence.training_report_hash, "VALIDATION_SCORE_BELOW_FLOOR"))
    gates.append(_gate("test_score", measurements.test_score >= policy.min_test_score,
                       cfloat(measurements.test_score), cfloat(policy.min_test_score),
                       evidence.training_report_hash, "TEST_SCORE_BELOW_FLOOR"))
    gap=abs(measurements.validation_score-measurements.test_score)
    gates.append(_gate("generalization_gap", gap <= policy.max_generalization_gap,
                       cfloat(gap), cfloat(policy.max_generalization_gap),
                       evidence.training_report_hash, "GENERALIZATION_GAP_TOO_LARGE"))
    gates.append(_gate("calibration_error", measurements.calibration_error <= policy.max_calibration_error,
                       cfloat(measurements.calibration_error), cfloat(policy.max_calibration_error),
                       evidence.calibration_hash, "CALIBRATION_ERROR_TOO_LARGE"))
    gates.append(_gate("stress_pass_ratio", measurements.stress_pass_ratio >= policy.min_stress_pass_ratio,
                       cfloat(measurements.stress_pass_ratio), cfloat(policy.min_stress_pass_ratio),
                       evidence.anti_overfit_report_hash, "STRESS_COVERAGE_TOO_WEAK"))
    gates.append(_gate("lineage_integrity", (not policy.require_lineage_valid) or measurements.lineage_valid,
                       str(measurements.lineage_valid).lower(), "true" if policy.require_lineage_valid else "optional",
                       ehash, "LINEAGE_INVALID"))
    gates.append(_gate("artifact_inventory", (not policy.require_inventory_valid) or measurements.inventory_valid,
                       str(measurements.inventory_valid).lower(), "true" if policy.require_inventory_valid else "optional",
                       evidence.artifact_inventory_hash, "ARTIFACT_INVENTORY_INVALID"))
    gates.append(_gate("model_card_authority", (not policy.require_model_card_no_capital_authority) or measurements.model_card_no_capital_authority,
                       str(measurements.model_card_no_capital_authority).lower(), "true" if policy.require_model_card_no_capital_authority else "optional",
                       evidence.model_card_hash, "MODEL_CARD_AUTHORITY_VIOLATION"))
    gates.append(_gate("authenticity_attestation", (not policy.require_verified_attestation) or measurements.attestation_verified,
                       str(measurements.attestation_verified).lower(), "true" if policy.require_verified_attestation else "optional",
                       evidence.attestation_hash or evidence.artifact_inventory_hash, "ATTESTATION_NOT_VERIFIED"))
    verdict=PromotionVerdict.ELIGIBLE if all(g.status != GateStatus.FAIL for g in gates) else PromotionVerdict.INELIGIBLE
    evaluation_id=stable_id("peval", "|".join([evidence.model_artifact_hash, scope.scope_id, policy.policy_hash,
                                               str(evaluated_at_utc_msc), evaluator_id]))
    result=PromotionEvaluation(evaluation_id, evidence.model_artifact_hash, scope.scope_id,
        ehash, policy.policy_hash, tuple(gates), verdict, evaluated_at_utc_msc,
        evaluator_id).with_hash()
    result.validate()
    return result
