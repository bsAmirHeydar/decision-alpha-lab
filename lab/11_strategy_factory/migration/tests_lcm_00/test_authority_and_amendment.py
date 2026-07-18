import copy
import pytest

from tools.strategy_factory.lcm.lcm_00.amendment import build_amendment, validate_amendment
from tools.strategy_factory.lcm.lcm_00.authority import build_reference_permit, validate_permit, validate_ownership_registry
from tools.strategy_factory.lcm.lcm_00.errors import AuthorityError, ContractViolation


def test_reference_permit_denies_all_dangerous_capabilities():
    permit = build_reference_permit("sha256:x", "2026-07-18T00:00:00Z")
    validate_permit(permit)
    assert all(value is False for value in permit["capabilities"].values())


def test_permit_escalation_rejected():
    permit = build_reference_permit("sha256:x", "2026-07-18T00:00:00Z")
    permit["capabilities"]["delete_source_files_allowed"] = True
    with pytest.raises(AuthorityError):
        validate_permit(permit)


def test_missing_required_owner_is_blocker():
    report = validate_ownership_registry({"registry_id":"R","assignments":[{"role":"PROGRAM_OWNER","assignee_id":None,"assignment_status":"UNRESOLVED","required_for_lcm01":True}]})
    assert report["lcm01_ownership_ready"] is False
    assert "PROGRAM_OWNER" in report["missing_required_roles"]


def test_role_conflict_detected():
    reg={"registry_id":"R","assignments":[
        {"role":"MIGRATION_ENGINEER","assignee_id":"same","assignment_status":"ASSIGNED","required_for_lcm01":False},
        {"role":"INDEPENDENT_PARITY_REVIEWER","assignee_id":"same","assignment_status":"ASSIGNED","required_for_lcm01":False},
    ]}
    assert validate_ownership_registry(reg)["conflicts"]


def test_semantic_amendment_requires_recharacterization():
    item=build_amendment("B","a.txt","sha256:1","sha256:2","SEMANTIC_BUG_FIX",["CTX_X"],"fix")
    validate_amendment(item)
    assert item["recharacterization_required"] is True


def test_noop_amendment_rejected():
    with pytest.raises(ContractViolation):
        build_amendment("B","a.txt","sha256:1","sha256:1","NON_SEMANTIC",["CTX_X"],"noop")
