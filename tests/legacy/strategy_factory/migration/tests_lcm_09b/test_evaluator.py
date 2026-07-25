import pytest
from tools.strategy_factory.lcm.lcm_09b.canonical import digest_object
from tools.strategy_factory.lcm.lcm_09b.evaluator import CanonicalSetupEvaluator
from tools.strategy_factory.lcm.lcm_09b.errors import ContractError
from .conftest import j
def snapshot():
 b={"schema_version":"1.0.0","context_identity_id":"UNRESOLVED_CONTEXT","context_version":"0.0.0","occurrence_id":"OCC_TEST_BLOCKED","observed_at":"2026-01-01T00:00:00Z","available_at":"2026-01-01T00:00:00Z","features":{},"states":[],"known_time_complete":True,"source_digest":"sha256:"+"0"*64};return {**b,"snapshot_digest":digest_object(b)}
def test_blocked_package_returns_first_class_no_trade():
 row=j("canonical_setup_registry.json")["packages"][0];p=j(row["package_path"]);d=CanonicalSetupEvaluator().evaluate(p,snapshot());assert d["decision_state"]=="BLOCKED" and d["no_trade"] is True
def test_incomplete_known_time_fails_closed():
 row=j("canonical_setup_registry.json")["packages"][0];p=j(row["package_path"]);s=snapshot();s["known_time_complete"]=False
 with pytest.raises(ContractError):CanonicalSetupEvaluator().evaluate(p,s)
def test_synthetic_ready_rule_order_is_deterministic():
 row=j("canonical_setup_registry.json")["packages"][0];p=j(row["package_path"]);p["package_status"]="REFERENCE_READY";p["executable_reference"]=True;p["blocker_ids"]=[];p["reason_codes"]=[];p["context_binding"]={"state":"BOUND","allowed_context_identity_ids":["UNRESOLVED_CONTEXT"],"independent_context_clock":False,"context_recomputation":False};p["rules"]={"eligibility":{"op":"const","args":[True]},"trigger":{"op":"const","args":[True]},"confirmation":{"op":"const","args":[True]},"invalidation":{"op":"const","args":[False]},"cancellation":{"op":"const","args":[False]},"expiry":{"op":"const","args":[False]},"abstention":{"op":"const","args":[False]},"entitlement":None};p["package_digest"]=digest_object(p,"package_digest")
 d=CanonicalSetupEvaluator().evaluate(p,snapshot());assert d["decision_state"]=="CONFIRMED"
