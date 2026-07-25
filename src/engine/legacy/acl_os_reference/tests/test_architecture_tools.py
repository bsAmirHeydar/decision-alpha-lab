from __future__ import annotations
import json
from pathlib import Path
import pytest
from jsonschema import Draft202012Validator
from tools.strategy_factory.acl_os.common import REPO_ROOT, SCHEMA_ROOT, TEMPLATE_ROOT, load_json
from tools.strategy_factory.acl_os.scaffold_context import scaffold
from tools.strategy_factory.acl_os.validate_context_package import validate_context
from tools.strategy_factory.acl_os.generate_context_readiness_report import readiness
from tools.strategy_factory.acl_os.validate_acl_os_architecture import validate

def test_all_public_schemas_are_valid():
    files=list(SCHEMA_ROOT.glob("*.schema.json")); assert len(files)>=10
    for p in files: Draft202012Validator.check_schema(load_json(p))

def test_template_is_structurally_valid_when_placeholders_allowed():
    out=validate_context(TEMPLATE_ROOT,allow_placeholders=True); assert out["passed"],out

def test_template_fails_closed_without_placeholder_allowance():
    out=validate_context(TEMPLATE_ROOT,allow_placeholders=False); assert not out["passed"]
    assert any(c["code"]=="PLACEHOLDER_SCAN" and not c["passed"] for c in out["checks"])

def test_scaffold_rewrites_context_identity(tmp_path: Path):
    root=scaffold("CTX_TEST_ALPHA",tmp_path/"CTX_TEST_ALPHA")
    assert "CTX_TEST_ALPHA" in (root/"context_manifest.yaml").read_text(encoding="utf-8")
    assert validate_context(root,allow_placeholders=True)["passed"]

def test_scaffold_rejects_invalid_identity(tmp_path: Path):
    with pytest.raises(ValueError): scaffold("bad-id",tmp_path/"bad")

def test_readiness_never_claims_live_for_template():
    out=readiness(TEMPLATE_ROOT); assert not out["overall_ready"]
    assert out["stages"]["live_activation"]["ready"] is False

def test_architecture_validator_passes():
    out=validate(REPO_ROOT); assert out["passed"],out

def test_context_manifest_rejects_unknown_fields():
    schema=load_json(SCHEMA_ROOT/"context_manifest.schema.json")
    import yaml
    obj=yaml.safe_load((TEMPLATE_ROOT/"context_manifest.yaml").read_text(encoding="utf-8")); obj["unknown_field"]=1
    assert list(Draft202012Validator(schema).iter_errors(obj))

def test_promotion_requires_evidence():
    schema=load_json(SCHEMA_ROOT/"promotion_decision.schema.json")
    obj={"schema_version":"1.0.0","decision_id":"PROM_TEST_001","candidate_ref":{"artifact_id":"MODEL_TEST","version":"1.0.0","digest":"sha256:"+"a"*64},"current_state":"EVIDENCE_COMPLETE","requested_state":"STATISTICALLY_ELIGIBLE","outcome":"STATISTICALLY_ELIGIBLE","guardrails":[{"gate":"LEAKAGE","passed":True,"reason_code":"PASS"}],"objective_summary":{},"evidence_refs":[],"approvals":[],"decided_at":"2026-07-17T00:00:00Z"}
    assert list(Draft202012Validator(schema).iter_errors(obj))

def test_one_hour_claim_ceiling_is_constant():
    schema=load_json(SCHEMA_ROOT/"one_hour_assessment.schema.json")
    assert schema["properties"]["claim_ceiling"]["const"]=="RESEARCH_TRIAGE"
