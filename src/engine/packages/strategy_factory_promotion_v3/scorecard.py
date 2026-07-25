"""Model-risk scorecard with non-compensatory critical blockers."""
from __future__ import annotations
from typing import Mapping, Sequence
from .canonical import canonical_sha256, stable_id
from .contracts import ModelRiskScorecard, TestEvidence
from .enums import EvidenceStatus, Severity
from .errors import PromotionError
_DEFAULT_WEIGHTS={"uncertainty":.12,"multiplicity":.16,"winner_overfit":.18,"null_controls":.14,"stress":.14,"calibration":.12,"integrity":.14}

def status_score(status:EvidenceStatus)->float:
    return {EvidenceStatus.PASS:1.0,EvidenceStatus.WARN:.65,EvidenceStatus.FAIL:0.0,EvidenceStatus.MISSING:0.0,EvidenceStatus.NOT_APPLICABLE:.5}[status]

def build_scorecard(evidence:Sequence[TestEvidence], *, weights:Mapping[str,float]|None=None, residual_risks:Sequence[str]=())->ModelRiskScorecard:
    if not evidence: raise PromotionError("empty_scorecard_evidence","scorecard requires evidence")
    w=dict(_DEFAULT_WEIGHTS if weights is None else weights)
    if any(v<0 for v in w.values()) or sum(w.values())<=0: raise PromotionError("invalid_scorecard_weights","weights must be non-negative with positive sum")
    grouped={}
    for item in evidence: grouped.setdefault(item.family,[]).append(item)
    component={family:min(status_score(x.status) for x in items) for family,items in grouped.items()}
    # Unknown configured components score zero: missing evidence is not neutral.
    weighted=sum(wv*component.get(family,0.0) for family,wv in w.items())/sum(w.values())
    critical=sorted({b for item in evidence if item.severity is Severity.CRITICAL and item.status in (EvidenceStatus.FAIL,EvidenceStatus.MISSING) for b in (item.blockers or (f"{item.test_id}:{item.status.value}",))})
    high=sorted({b for item in evidence if item.severity is Severity.HIGH and item.status in (EvidenceStatus.FAIL,EvidenceStatus.MISSING,EvidenceStatus.WARN) for b in (item.blockers or item.warnings or (item.test_id,))})
    payload={"component":component,"weighted":weighted,"critical":critical,"high":high,"residual":list(residual_risks)}
    return ModelRiskScorecard(scorecard_id=stable_id("risk",payload),component_scores=component,weighted_score=float(weighted),critical_blockers=tuple(critical),high_risks=tuple(high),residual_risks=tuple(residual_risks),evidence_hash=canonical_sha256(payload))
