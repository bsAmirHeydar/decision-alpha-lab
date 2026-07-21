import json
from pathlib import Path

from tools.strategy_factory.acl_os.acl_02.service import ACL02ContextIntakeService

ROOT = Path(__file__).resolve().parents[4]
PACKAGE = ROOT / "lab/11_strategy_factory/contexts/CTX_RTHP_CROSS_SYMBOL_CYCLE_DIVERGENCE_V1"


def test_acl02_official_intake_has_no_blockers_or_warnings():
    permit = json.loads((PACKAGE / "governance/authority_permit.json").read_text(encoding="utf-8"))
    result = ACL02ContextIntakeService().evaluate(PACKAGE, authority_permit=permit)
    readiness = result["readiness"]
    assert readiness["blocking_count"] == 0
    assert readiness["warning_count"] == 0
    assert readiness["completeness_score"] == 1.0
    assert readiness["highest_state"] == "INTAKE_COMPLETE"
    assert readiness["stages"]["semantic_review"]["ready"] is True
