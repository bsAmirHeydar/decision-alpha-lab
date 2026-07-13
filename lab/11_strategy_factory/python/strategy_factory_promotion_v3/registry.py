"""Closed registry of I12 evaluation suites and capability flags."""
from __future__ import annotations
from dataclasses import asdict, dataclass
from typing import Mapping
from .canonical import canonical_sha256
from .errors import PromotionError

@dataclass(frozen=True, slots=True)
class SuiteDescriptor:
    key: str
    version: str
    critical: bool
    deterministic: bool
    seed_required: bool
    required_inputs: tuple[str,...]
    outputs: tuple[str,...]

_DESCRIPTORS=(
    SuiteDescriptor("uce.promotion.uncertainty","1.0.0",True,True,True,("returns","dependence_identity"),("uncertainty_report",)),
    SuiteDescriptor("uce.promotion.multiplicity","1.0.0",True,True,False,("selection_universe","family_definition"),("multiplicity_report",)),
    SuiteDescriptor("uce.promotion.winner_overfit","1.0.0",True,True,True,("performance_matrix","trial_universe"),("pbo","deflated_performance","reality_check","spa")),
    SuiteDescriptor("uce.promotion.null_controls","1.0.0",True,True,True,("observed","null_plan"),("null_control_results",)),
    SuiteDescriptor("uce.promotion.stress","1.0.0",True,True,True,("baseline_returns","stress_plan"),("stress_results",)),
    SuiteDescriptor("uce.promotion.calibration","1.0.0",False,True,False,("oof_probabilities","labels","conformal_intervals"),("calibration_report",)),
    SuiteDescriptor("uce.promotion.scorecard","1.0.0",True,True,False,("all_evidence","promotion_policy"),("promotion_decision","signed_bundle")),
)

def registry()->Mapping[str,SuiteDescriptor]: return {d.key:d for d in _DESCRIPTORS}
def registry_snapshot()->Mapping[str,object]:
    payload={k:asdict(v) for k,v in sorted(registry().items())}; return {"version":"1.0.0","suites":payload,"registry_hash":canonical_sha256(payload)}
def require_suite(key:str)->SuiteDescriptor:
    try:return registry()[key]
    except KeyError as exc:raise PromotionError("unknown_promotion_suite","unknown I12 suite",{"key":key}) from exc
