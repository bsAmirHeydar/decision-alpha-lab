import pytest
from saed_v4_constitution.evidence import EvidenceFirewall
from saed_v4_constitution.enums import ClaimClass,DecisionStatus,EvidenceOperation,EvidenceRole,ReasonCode
from saed_v4_constitution.models import EvidenceUseRequest

@pytest.mark.parametrize("role,operation", [
 (EvidenceRole.DEVELOPMENT,EvidenceOperation.TRAIN),(EvidenceRole.DEVELOPMENT,EvidenceOperation.TUNE),
 (EvidenceRole.CALIBRATION,EvidenceOperation.CALIBRATE),(EvidenceRole.SELECTION_VALIDATION,EvidenceOperation.SELECT),
 (EvidenceRole.LOCKED_FINAL,EvidenceOperation.PROMOTE),(EvidenceRole.PROSPECTIVE,EvidenceOperation.PROMOTE),
 (EvidenceRole.SYNTHETIC_STRESS,EvidenceOperation.STRESS),(EvidenceRole.EXTERNAL_ACTUAL,EvidenceOperation.PROMOTE)])
def test_allowed_role_operations(researcher,role,operation):
    req=EvidenceUseRequest("p",researcher,role,operation,ClaimClass.PREDICTIVE,"2026-07-13T00:00:00Z",role==EvidenceRole.SYNTHETIC_STRESS,False)
    assert EvidenceFirewall().evaluate(req).status == DecisionStatus.ALLOW

@pytest.mark.parametrize("role", [EvidenceRole.LOCKED_FINAL,EvidenceRole.PROSPECTIVE,EvidenceRole.SHADOW,EvidenceRole.MICRO_LIVE,EvidenceRole.LIVE,EvidenceRole.EXTERNAL_ACTUAL])
@pytest.mark.parametrize("operation", [EvidenceOperation.TRAIN,EvidenceOperation.TUNE])
def test_protected_evidence_never_trains(researcher,role,operation):
    req=EvidenceUseRequest("p",researcher,role,operation,ClaimClass.PREDICTIVE,"2026-07-13T00:00:00Z")
    result=EvidenceFirewall().evaluate(req)
    assert result.status == DecisionStatus.REJECT
    assert ReasonCode.PROTECTED_EVIDENCE_TRAINING in result.reasons

def test_synthetic_cannot_promote(researcher):
    req=EvidenceUseRequest("p",researcher,EvidenceRole.SYNTHETIC_STRESS,EvidenceOperation.PROMOTE,ClaimClass.STRESS_ONLY,"2026-07-13T00:00:00Z",True,True)
    result=EvidenceFirewall().evaluate(req)
    assert result.status == DecisionStatus.REJECT
    assert ReasonCode.SYNTHETIC_POSITIVE_PROMOTION in result.reasons

def test_static_external_cannot_promote(researcher):
    req=EvidenceUseRequest("p",researcher,EvidenceRole.EXTERNAL_STATIC,EvidenceOperation.PROMOTE,ClaimClass.OPERATIONAL,"2026-07-13T00:00:00Z")
    assert EvidenceFirewall().evaluate(req).status == DecisionStatus.REJECT
