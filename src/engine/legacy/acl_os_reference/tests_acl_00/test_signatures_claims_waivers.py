from __future__ import annotations
from dataclasses import replace
from datetime import timedelta
from src.engine.tooling.strategy_factory.acl_os.acl_00.canonical import HMACSignatureAdapter,StructuralSignatureVerifier,digest_object
from src.engine.tooling.strategy_factory.acl_os.acl_00.claims import ClaimCeilingEvaluator
from src.engine.tooling.strategy_factory.acl_os.acl_00.types import Reason,WaiverRecord
from src.engine.tooling.strategy_factory.acl_os.acl_00.waivers import WaiverEvaluator


def test_hmac_signature_roundtrip():
    adapter=HMACSignatureAdapter({"USR_A":b"test-only-key"}); payload={"x":1}; sig=adapter.sign(payload,"USR_A"); assert adapter.verify(payload,sig,"USR_A")


def test_hmac_signature_rejects_mutation():
    adapter=HMACSignatureAdapter({"USR_A":b"test-only-key"}); sig=adapter.sign({"x":1},"USR_A"); assert not adapter.verify({"x":2},sig,"USR_A")


def test_structural_signature_rejects_empty(): assert not StructuralSignatureVerifier().verify({},"","USR_A")


def test_claim_ceiling_exceeded(valid_bundle):
    req=replace(valid_bundle.request,claim_requested="SIGNED_AUTHORIZATION_REQUIRED")
    reasons=ClaimCeilingEvaluator().evaluate(req,{"claim_ceiling":"RESEARCH_TRIAGE"})
    assert any(x.code=="CLAIM_CEILING_EXCEEDED" for x in reasons)


def test_nonwaivable_reason_survives_without_waiver(valid_bundle):
    reason=Reason("SECURITY_CONTROL_MISSING","missing","SECURITY_SEC_AUDIT_AVAILABLE",False)
    evaluator=WaiverEvaluator(StructuralSignatureVerifier(),{"nonwaivable_policy_ids":["SECURITY_SEC_AUDIT_AVAILABLE"],"required_approval_roles":[]})
    remaining,applied=evaluator.apply(valid_bundle.request,[reason],None,valid_bundle.request.requested_at)
    assert remaining==[reason] and not applied


def test_expired_waiver_is_rejected(valid_bundle):
    waiver=WaiverRecord("WVR_TEST_001",valid_bundle.request.transition_id,("SOME_POLICY",),valid_bundle.request.subject_ref,valid_bundle.request.requested_by,valid_bundle.request.requested_at-timedelta(hours=2),valid_bundle.request.requested_at-timedelta(hours=1),("COMPENSATING_MONITOR",),(),"sig:waiver-issuer:000001")
    evaluator=WaiverEvaluator(StructuralSignatureVerifier(),{"nonwaivable_policy_ids":[],"required_approval_roles":[]})
    remaining,_=evaluator.apply(valid_bundle.request,[Reason("X","x","SOME_POLICY",True)],waiver,valid_bundle.request.requested_at)
    assert any(x.code=="WAIVER_EXPIRED" for x in remaining)
