from __future__ import annotations
from dataclasses import dataclass
from .models import GateResult, PromotionDecision
from .enums import GateStatus, PromotionStatus
from .hashing import stable_id

@dataclass(frozen=True, slots=True)
class PromotionThresholds:
    minimum_oos_folds: int = 4
    minimum_oos_samples: int = 100
    minimum_positive_fold_share: float = 0.60
    minimum_worst_fold_mean_r: float = -0.10
    minimum_oos_to_is_ratio: float = 0.35
    maximum_pbo: float = 0.45
    minimum_deflated_probability: float = 0.95
    maximum_reality_check_p: float = 0.05
    minimum_surface_support: float = 0.45
    minimum_best_trade_removed_mean_r: float = 0.0
    minimum_stress_floor_mean_r: float = -0.02

@dataclass(frozen=True, slots=True)
class PromotionEvidence:
    oos_fold_count: int
    oos_sample_count: int
    positive_fold_share: float
    worst_fold_mean_r: float
    oos_to_is_ratio: float
    pbo: float
    deflated_probability: float
    reality_check_p: float
    surface_support: float
    best_trade_removed_mean_r: float
    stress_floor_mean_r: float
    fatal_leakage_count: int = 0

def evaluate_promotion(decision_id: str, plan_hash: str, selected_trial_id: str,
                       evidence: PromotionEvidence,
                       thresholds: PromotionThresholds = PromotionThresholds(),
                       evidence_artifact_hashes: tuple[str,...] = ()) -> PromotionDecision:
    checks=[
      ("no_fatal_leakage", evidence.fatal_leakage_count, 0, "<=", evidence.fatal_leakage_count<=0, "LEAKAGE_DETECTED"),
      ("minimum_oos_folds", evidence.oos_fold_count, thresholds.minimum_oos_folds, ">=", evidence.oos_fold_count>=thresholds.minimum_oos_folds, "INSUFFICIENT_OOS_FOLDS"),
      ("minimum_oos_samples", evidence.oos_sample_count, thresholds.minimum_oos_samples, ">=", evidence.oos_sample_count>=thresholds.minimum_oos_samples, "INSUFFICIENT_OOS_SAMPLES"),
      ("positive_fold_share", evidence.positive_fold_share, thresholds.minimum_positive_fold_share, ">=", evidence.positive_fold_share>=thresholds.minimum_positive_fold_share, "FOLD_SIGN_INSTABILITY"),
      ("worst_fold", evidence.worst_fold_mean_r, thresholds.minimum_worst_fold_mean_r, ">=", evidence.worst_fold_mean_r>=thresholds.minimum_worst_fold_mean_r, "WORST_FOLD_FAILURE"),
      ("oos_to_is_ratio", evidence.oos_to_is_ratio, thresholds.minimum_oos_to_is_ratio, ">=", evidence.oos_to_is_ratio>=thresholds.minimum_oos_to_is_ratio, "EXCESSIVE_IS_OOS_DECAY"),
      ("pbo", evidence.pbo, thresholds.maximum_pbo, "<=", evidence.pbo<=thresholds.maximum_pbo, "PBO_TOO_HIGH"),
      ("deflated_probability", evidence.deflated_probability, thresholds.minimum_deflated_probability, ">=", evidence.deflated_probability>=thresholds.minimum_deflated_probability, "DEFLATED_PERFORMANCE_WEAK"),
      ("reality_check", evidence.reality_check_p, thresholds.maximum_reality_check_p, "<=", evidence.reality_check_p<=thresholds.maximum_reality_check_p, "REALITY_CHECK_NOT_SIGNIFICANT"),
      ("surface_support", evidence.surface_support, thresholds.minimum_surface_support, ">=", evidence.surface_support>=thresholds.minimum_surface_support, "PARAMETER_ISLAND"),
      ("best_trade_removal", evidence.best_trade_removed_mean_r, thresholds.minimum_best_trade_removed_mean_r, ">=", evidence.best_trade_removed_mean_r>=thresholds.minimum_best_trade_removed_mean_r, "BEST_TRADE_DEPENDENCY"),
      ("stress_floor", evidence.stress_floor_mean_r, thresholds.minimum_stress_floor_mean_r, ">=", evidence.stress_floor_mean_r>=thresholds.minimum_stress_floor_mean_r, "STRESS_FRAGILITY"),
    ]
    gates=[]; reasons=[]
    for gate_id,observed,threshold,comparison,passed,reason in checks:
        status=GateStatus.PASS if passed else GateStatus.FAIL
        evidence_hash=stable_id("gateev",f"{gate_id}|{observed}|{threshold}|{comparison}")
        gates.append(GateResult(gate_id,status,float(observed),float(threshold),comparison,
                                "PASS" if passed else reason,evidence_hash))
        if not passed: reasons.append(reason)
    status=(PromotionStatus.ELIGIBLE_FOR_DATASET_REVIEW if not reasons
            else PromotionStatus.REJECTED)
    return PromotionDecision(decision_id,plan_hash,selected_trial_id,status,
                             tuple(gates),tuple(reasons),evidence_artifact_hashes).with_hash()
