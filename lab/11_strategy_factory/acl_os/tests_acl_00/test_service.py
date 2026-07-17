from __future__ import annotations
from dataclasses import replace
import json
from pathlib import Path
import pytest
from tools.strategy_factory.acl_os.common import REPO_ROOT
from tools.strategy_factory.acl_os.acl_00.io import load_bundle
from tools.strategy_factory.acl_os.acl_00.service import ACL00ControlPlane,EvaluationBundle
from tools.strategy_factory.acl_os.acl_00.types import Decision,LifecycleState

FIX=REPO_ROOT/"lab"/"11_strategy_factory"/"acl_os"/"fixtures"/"acl_00"

def test_valid_transition_allowed(valid_bundle):
    out=ACL00ControlPlane().evaluate(valid_bundle,valid_bundle.request.requested_at); assert out.decision==Decision.ALLOW; assert not out.capital_activation_allowed; assert not out.live_order_submission_allowed

def test_valid_transition_can_commit(valid_bundle):
    cp=ACL00ControlPlane(); out=cp.evaluate(valid_bundle,valid_bundle.request.requested_at,commit=True); assert out.decision==Decision.ALLOW; assert out.resulting_revision==1

def test_missing_approval_denied():
    b=load_bundle(FIX/"invalid_missing_approval.json"); out=ACL00ControlPlane().evaluate(b,b.request.requested_at); assert out.decision==Decision.DENY; assert any(x.code=="REQUIRED_APPROVAL_MISSING" for x in out.reasons)

def test_security_failure_denied():
    b=load_bundle(FIX/"invalid_security_failure.json"); out=ACL00ControlPlane().evaluate(b,b.request.requested_at); assert out.decision==Decision.DENY; assert any(x.code=="SECURITY_CONTROL_NOT_PASS" for x in out.reasons)

def test_request_digest_mutation_denied(valid_bundle):
    req=replace(valid_bundle.request,rationale=valid_bundle.request.rationale+" changed"); b=EvaluationBundle(req,valid_bundle.evidence,valid_bundle.approvals,valid_bundle.security_results); out=ACL00ControlPlane().evaluate(b,req.requested_at); assert out.decision==Decision.DENY; assert any(x.code=="REQUEST_DIGEST_MISMATCH" for x in out.reasons)

def test_terminal_state_denied(valid_bundle):
    req=replace(valid_bundle.request,from_state=LifecycleState.RETIRED,to_state=LifecycleState.DRAFT_CONTEXT); b=EvaluationBundle(req,(),(),()); out=ACL00ControlPlane().evaluate(b,req.requested_at); assert out.decision==Decision.DENY; assert any(x.code=="TERMINAL_STATE" for x in out.reasons)

def test_unregistered_transition_denied(valid_bundle):
    req=replace(valid_bundle.request,to_state=LifecycleState.CHAMPION); b=EvaluationBundle(req,valid_bundle.evidence,valid_bundle.approvals,valid_bundle.security_results); out=ACL00ControlPlane().evaluate(b,req.requested_at); assert out.decision==Decision.DENY; assert any(x.code=="TRANSITION_NOT_ALLOWED" for x in out.reasons)

def test_audit_event_always_appended(valid_bundle):
    cp=ACL00ControlPlane(); cp.evaluate(valid_bundle,valid_bundle.request.requested_at); assert len(cp.audit.events)==1; assert cp.audit.verify()

def test_policy_digest_exposed(valid_bundle): assert ACL00ControlPlane().evaluate(valid_bundle,valid_bundle.request.requested_at).policy_bundle_digest.startswith("sha256:")
