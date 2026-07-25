from tools.strategy_factory.lcm.lcm_16a.service import LCM16AFullSystemAuditService
from tools.strategy_factory.lcm.lcm_16a.verify import verify_package


def test_package_verifies(root, audit_root):
    result = verify_package(root, audit_root)
    assert result.validation_status == "PASS"
    assert result.closure_decision == "BLOCKED"
    assert result.baseline_count == 2168
    assert result.amendment_count == 242
    assert result.unchanged_count == 1926
    assert result.missing_count == 0


def test_service_boundary(root):
    result = LCM16AFullSystemAuditService(root).verify()
    assert result.deterministic_gate_status == "PASS"
    assert result.external_evidence_status == "UNKNOWN_BLOCKING"
