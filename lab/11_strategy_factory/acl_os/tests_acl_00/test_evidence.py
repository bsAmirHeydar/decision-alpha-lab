from __future__ import annotations
from dataclasses import replace
from datetime import timedelta
import pytest
from tools.strategy_factory.acl_os.acl_00.evidence import EvidenceEvaluator
from tools.strategy_factory.acl_os.acl_00.types import EvidenceClass


def test_valid_semantic_evidence(valid_bundle):
    r=EvidenceEvaluator().evaluate(valid_bundle.request,list(valid_bundle.evidence),{"required_classes":{"DERIVED":1},"required_claims":["SEMANTIC_COMPLETENESS"],"allowed_environments":["REVIEW"]},valid_bundle.request.requested_at); assert not r

def test_missing_evidence_reference_fails(valid_bundle):
    req=replace(valid_bundle.request,evidence_ids=("EVD_MISSING",)); r=EvidenceEvaluator().evaluate(req,list(valid_bundle.evidence),{"required_classes":{}},req.requested_at); assert any(x.code=="EVIDENCE_REFERENCE_UNRESOLVED" for x in r)

def test_future_known_time_fails(valid_bundle):
    ev=replace(valid_bundle.evidence[0],known_at=valid_bundle.request.requested_at+timedelta(seconds=1)); r=EvidenceEvaluator().evaluate(valid_bundle.request,[ev],{"required_classes":{"DERIVED":1}},valid_bundle.request.requested_at); assert any(x.code=="EVIDENCE_KNOWN_AFTER_REQUEST" for x in r)

def test_mutable_evidence_fails(valid_bundle):
    ev=replace(valid_bundle.evidence[0],immutable=False); r=EvidenceEvaluator().evaluate(valid_bundle.request,[ev],{"required_classes":{"DERIVED":1}},valid_bundle.request.requested_at); assert any(x.code=="EVIDENCE_NOT_IMMUTABLE" for x in r)

def test_synthetic_does_not_satisfy_observed(valid_bundle):
    ev=replace(valid_bundle.evidence[0],evidence_class=EvidenceClass.SYNTHETIC); r=EvidenceEvaluator().evaluate(valid_bundle.request,[ev],{"required_classes":{"OBSERVED":1}},valid_bundle.request.requested_at); assert any(x.code=="EVIDENCE_CLASS_INSUFFICIENT" for x in r)

def test_prospective_can_satisfy_observed(valid_bundle):
    ev=replace(valid_bundle.evidence[0],evidence_class=EvidenceClass.PROSPECTIVE); r=EvidenceEvaluator().evaluate(valid_bundle.request,[ev],{"required_classes":{"OBSERVED":1}},valid_bundle.request.requested_at); assert not r

def test_missing_claim_fails(valid_bundle):
    r=EvidenceEvaluator().evaluate(valid_bundle.request,list(valid_bundle.evidence),{"required_classes":{"DERIVED":1},"required_claims":["OTHER_CLAIM"]},valid_bundle.request.requested_at); assert any(x.code=="EVIDENCE_CLAIM_MISSING" for x in r)
